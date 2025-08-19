#!/usr/bin/env python3
import os
import sys
import glob
import readline  # nice arrow-key history on mac/linux
from dataclasses import dataclass, field
from typing import List, Tuple

from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ChatMessageHistory
from langchain.callbacks.base import BaseCallbackHandler

# ---------- Config ----------
INDEX_DIR = "./index"
DOCS_DIR = "./docs"
EMBED_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3.1"
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 180
DEFAULT_TOP_K = 4


# ---------- Streaming callback ----------
class StdoutStreamingHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs):
        # print tokens as they arrive (no color/styles to keep it simple)
        sys.stdout.write(token)
        sys.stdout.flush()


# ---------- Utilities ----------
def load_docs_from_folder(folder: str):
    paths = []
    paths.extend(glob.glob(os.path.join(folder, "**", "*.pdf"), recursive=True))
    paths.extend(glob.glob(os.path.join(folder, "**", "*.txt"), recursive=True))
    paths.extend(glob.glob(os.path.join(folder, "**", "*.md"), recursive=True))

    docs = []
    for p in paths:
        try:
            if p.lower().endswith(".pdf"):
                loader = PyPDFLoader(p)
                docs.extend(loader.load())
            else:
                loader = TextLoader(p, encoding="utf-8")
                docs.extend(loader.load())
        except Exception as e:
            print(f"[warn] Skipped {p}: {e}")

    if not docs:
        print(f"[info] No docs found in {folder}. You can add later with /add.")
    return docs


def build_or_load_index(index_dir: str = INDEX_DIR, docs_dir: str = DOCS_DIR):
    embeddings = OllamaEmbeddings(model=EMBED_MODEL)
    if os.path.isdir(index_dir) and os.listdir(index_dir):
        # load existing
        vector = FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)
        return vector, embeddings, False

    # build new
    raw_docs = load_docs_from_folder(docs_dir)
    if raw_docs:
        splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        chunks = splitter.split_documents(raw_docs)
        vector = FAISS.from_documents(chunks, embeddings)
        os.makedirs(index_dir, exist_ok=True)
        vector.save_local(index_dir)
        return vector, embeddings, True
    else:
        # empty store (still create so retriever works)
        vector = FAISS.from_texts([""], embeddings)
        os.makedirs(index_dir, exist_ok=True)
        vector.save_local(index_dir)
        return vector, embeddings, True


def add_files(paths: List[str], index_dir: str = INDEX_DIR):
    embeddings = OllamaEmbeddings(model=EMBED_MODEL)
    vector = FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)

    new_docs = []
    for p in paths:
        try:
            if p.lower().endswith(".pdf"):
                loader = PyPDFLoader(p)
                new_docs.extend(loader.load())
            else:
                loader = TextLoader(p, encoding="utf-8")
                new_docs.extend(loader.load())
        except Exception as e:
            print(f"[warn] Skipped {p}: {e}")

    if not new_docs:
        print("[info] No new documents added.")
        return

    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = splitter.split_documents(new_docs)
    vector.add_documents(chunks)
    vector.save_local(index_dir)
    print(f"[ok] Added {len(new_docs)} doc(s) and updated index.")


@dataclass
class ChatState:
    show_sources: bool = True
    top_k: int = DEFAULT_TOP_K
    history: ChatMessageHistory = field(default_factory=ChatMessageHistory)
    chain: ConversationalRetrievalChain = None  # set later

    def make_chain(self, vector: FAISS, llm: ChatOllama):
        retriever = vector.as_retriever(search_type="similarity", search_kwargs={"k": self.top_k})
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            return_source_documents=True,
            verbose=False,
        )

    def rebuild_chain(self, vector: FAISS, llm: ChatOllama):
        # keep history, swap retriever settings (e.g., new top_k)
        self.make_chain(vector, llm)


def print_sources(docs):
    seen = set()
    lines = []
    for d in docs:
        src = d.metadata.get("source") or d.metadata.get("file_path") or "unknown"
        if src not in seen:
            seen.add(src)
            lines.append(f" - {src}")
    if lines:
        print("\n\n[sources]")
        for s in lines[:10]:
            print(s)


def main():
    os.makedirs(DOCS_DIR, exist_ok=True)
    os.makedirs(INDEX_DIR, exist_ok=True)

    print("[init] Loading index and starting model…")
    vector, embeddings, created = build_or_load_index(INDEX_DIR, DOCS_DIR)

    llm = ChatOllama(
        model=LLM_MODEL,
        temperature=0.2,
        streaming=True,
        callbacks=[StdoutStreamingHandler()],
    )

    state = ChatState()
    state.make_chain(vector, llm)
    if created:
        print("[ok] Index ready.")
    print("""
RAG Chat CLI
Type your question and press Enter.

Commands:
  /add <path ...>      Add files into the index (PDF/TXT/MD)
  /rebuild             Re-scan ./docs and rebuild the whole index
  /reset               Clear chat history (keeps index)
  /topk <n>            Set number of retrieved chunks (default {DEFAULT_TOP_K})
  /sources on|off      Toggle showing source file list
  /quit                Exit
""".strip())

    while True:
        try:
            user = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break

        if not user:
            continue

        # ---- commands ----
        if user.lower() in ("/quit", "/exit"):
            print("Bye.")
            break

        if user.startswith("/add"):
            parts = user.split()[1:]
            if not parts:
                print("Usage: /add path1 [path2 ...]")
                continue
            add_files(parts, INDEX_DIR)
            # reload vector so in-memory retriever sees new chunks
            vector = FAISS.load_local(INDEX_DIR, embeddings, allow_dangerous_deserialization=True)
            state.rebuild_chain(vector, llm)
            continue

        if user.startswith("/topk"):
            parts = user.split()
            if len(parts) != 2 or not parts[1].isdigit():
                print("Usage: /topk <int>")
                continue
            state.top_k = int(parts[1])
            state.rebuild_chain(vector, llm)
            print(f"[ok] top_k set to {state.top_k}")
            continue

        if user.startswith("/sources"):
            parts = user.split()
            if len(parts) != 2 or parts[1] not in ("on", "off"):
                print("Usage: /sources on|off")
                continue
            state.show_sources = (parts[1] == "on")
            print(f"[ok] sources {'enabled' if state.show_sources else 'disabled'}")
            continue

        if user == "/rebuild":
            print("[build] Rebuilding full index from ./docs …")
            # wipe and rebuild
            for f in glob.glob(os.path.join(INDEX_DIR, "*")):
                try:
                    os.remove(f)
                except IsADirectoryError:
                    pass
            vector, embeddings, _ = build_or_load_index(INDEX_DIR, DOCS_DIR)
            state.rebuild_chain(vector, llm)
            print("[ok] Rebuilt.")
            continue

        if user == "/reset":
            state.history = ChatMessageHistory()
            print("[ok] Chat history cleared.")
            continue

        # ---- normal chat ----
        # run the chain and stream tokens
        try:
            result = state.chain.invoke(
                {
                    "question": user,
                    "chat_history": state.history.messages,  # list of AI/User messages
                }
            )
            # ensure newline after streaming
            print()
        except Exception as e:
            print(f"\n[error] {e}")
            continue

        # update history manually (crc also tracks, but we keep explicit)
        # Note: ChatMessageHistory expects messages or strings; use add_user_message/add_ai_message
        state.history.add_user_message(user)
        state.history.add_ai_message(result["answer"])

        # optionally show sources
        if state.show_sources and "source_documents" in result:
            print_sources(result["source_documents"])


if __name__ == "__main__":
    main()
