from __future__ import annotations
# ^ In Python 3.7–3.10 this makes type annotations "deferred" (stored as strings),
#   so you can reference types that are defined later in the file or avoid importing
#   heavy typing modules at runtime. In 3.11+ it's the default, but keeping this
#   line doesn't hurt.

from typing import Dict, Any, List, Tuple, Optional
# ^ Static type hints:
#   - Dict[str, Any] means "a dictionary with string keys, values can be anything"
#   - List[T], Tuple[A, B], Optional[T] (could be T or None)

from pathlib import Path
# ^ Path gives clean, cross-platform file paths (better than raw strings like "C:\\x" or "/tmp/x").

import time, json, hashlib, shutil, re
# - time: timestamps, durations
# - json: read/write JSON
# - hashlib: compute hashes (e.g., SHA-256) for integrity
# - shutil: disk usage, file operations
# - re: "regular expressions" for pattern matching in text

try:
    import yaml  # type: ignore
    # ^ Optional: used to load .yaml/.yml manifest files.
    #   "type: ignore" silences linters if the yaml stub types aren't installed.
except Exception:
    yaml = None
    # ^ If PyYAML isn't installed, we set yaml=None and simply won't load YAML files.
    #   JSON manifests will still work.


# ----------------------------
# Tokenization: turn text -> tokens
# ----------------------------

def _tokenize(s: str) -> list[str]:
    """
    Split a string into lowercase tokens (ASCII letters + digits only).
    - If s is None/empty, treat it as "" so we don't crash.
    - Lowercase to make matching case-insensitive ("Shelter" == "shelter").
    - Keep runs of [a-z0-9], drop everything else (spaces, punctuation, emojis, accents).
    """
    # Handle None or empty values safely
    if not s:
        s = ""

    # Normalize case for simpler matching
    s = s.lower()

    # Regex pattern: one or more ASCII letters (a-z) or digits (0-9).
    # The leading r makes this a "raw string" (backslashes aren't special to Python,
    # they are passed directly to the regex engine). Example: r"\n" is the two characters "\" and "n".
    pattern = r"[a-z0-9]+"

    # Find ALL non-overlapping substrings that match the pattern, in order.
    # Example: "N95 mask!" -> ["n95", "mask"]
    tokens = re.findall(pattern, s)

    return tokens


# ----------------------------
# Similarity: Jaccard set overlap
# ----------------------------

def _jaccard(a: List[str], b: List[str]) -> float:
    """
    Compute Jaccard similarity between two token lists.
    Jaccard = |intersection(unique(a), unique(b))| / |union(unique(a), unique(b))|
    Returns 0.0..1.0 (higher means "more overlap").
    """
    # Convert lists to sets to remove duplicates ("oak","oak","st" -> {"oak","st"})
    sa, sb = set(a), set(b)

    # If either side is empty, define similarity as 0.0 (no overlap).
    # (Some definitions use 1.0 for empty vs empty; we choose 0.0 to avoid corner-case surprises.)
    if not sa or not sb:
        return 0.0

    # "&" is set intersection, "|" is set union.
    return len(sa & sb) / len(sa | sb)


# ----------------------------
# Manifest loading: bring policies from files into memory
# ----------------------------

def load_manifests(dir_path: str) -> Dict[str, Dict[str, Any]]:
    """
    Load all manifest files in a directory.
    Supports:
      - YAML (.yaml, .yml) if PyYAML is available
      - JSON (.json)
    Returns: dict keyed by manifest "id" (or filename stem), value = manifest content (dict).
    """
    d = Path(dir_path)
    #Out will be nested dictionary that repersennts empty dir for now
    out: Dict[str, Dict[str, Any]] = {}

    # NOTE: d.glob("*") reads only the top-level of the directory (NOT recursive).
    # If you later want subfolders, change to d.rglob("*") or d.glob("**/*").
    #p stands path...for each path in directory at d
    for p in d.glob("*"):
        if not p.is_file():
            continue

        if p.suffix.lower() in [".yaml", ".yml"] and yaml:
            # Read YAML text and parse into a Python dict
            data = yaml.safe_load(p.read_text(encoding="utf-8"))
        elif p.suffix.lower() == ".json":
            # Read JSON text and parse into a Python dict
            data = json.loads(p.read_text(encoding="utf-8"))
        else:
            # Skip unrecognized extensions (or YAML when PyYAML isn't installed)
            continue

        # Use the "id" from the file if present; else fall back to filename (without extension).
        mid = data.get("id") or p.stem
        out[mid] = data

    return out


# ----------------------------
# Domain routing: choose which manifest fits a message
# ----------------------------

def score_domain(message: str, manifest: Dict[str, Any]) -> float:
    """
    Score how well 'message' matches a given domain manifest.
    Two signals (simple, fast, offline):
      1) pattern_hits: count of manifest intent patterns found in the message tokens
      2) seed_sim: Jaccard similarity between message tokens and each 'embedding_seeds' text; take the max
    We then combine them with weights (0.6 and 0.8). The absolute scale isn't important—only ranking.
    """
    toks = _tokenize(message)

    # Manifest may include "intents": {"patterns": ["evacuate","shelter",...]}
    # Lowercase all patterns to compare with our already-lowercased tokens.
    patterns = [s.lower() for s in manifest.get("intents", {}).get("patterns", [])]

    # Count how many patterns appear as substrings in the *joined* token string.
    # NOTE: This is a simple substring check ("oak st" → "oak" hits).
    #       It's cheap but not perfect; it's fine for a first pass.
    pattern_hits = sum(1 for pat in patterns if pat in " ".join(toks))

    # "embedding_seeds" are short sentences that describe the domain.
    # We Jaccard-compare tokens(message) against tokens(seed) and take the maximum similarity across all seeds.
    # 1) Get the seed sentences for this domain (or empty list)
    seeds: List[str] = manifest.get("embedding_seeds", [])
    if not isinstance(seeds, list):
        seeds = []  # be safe if manifest is malformed

    # 2) For each seed, compute Jaccard similarity with the message tokens
    similarities: List[float] = []
    for seed in seeds:
        seed_tokens = _tokenize(seed)          # turn seed sentence into tokens
        sim = _jaccard(toks, seed_tokens)      # 0.0 .. 1.0
        similarities.append(sim)
        
    # 3) Take the best (highest) similarity; default 0.0 if no seeds
    seed_sim = max(similarities) if similarities else 0.0

    # 4) Combine signals into a single score
    #    - pattern_hits: integer count of keyword matches
    #    - seed_sim: 0..1 overlap with the best-matching seed
    #    - weights (0.6, 0.8): tune these on your data so the top domain is usually correct
    score = (pattern_hits * 0.6) + (seed_sim * 0.8)
    return score


def pick_domain(message: str, manifests: Dict[str, Dict[str, Any]]) -> Tuple[str, Dict[str, Any], float]:
    """
    Score every manifest and pick the top one.
    Returns: (manifest_id, manifest_dict, score). If no manifests, returns ("", {}, 0.0).
    """
    # Build list of (manifest_id, score) for each manifest
    scores = [(mid, score_domain(message, m)) for mid, m in manifests.items()]

    # Highest score first
    scores.sort(key=lambda x: x[1], reverse=True)

    if not scores:
        return "", {}, 0.0

    # Top choice: id, the manifest object, and the numeric score
    return scores[0][0], manifests[scores[0][0]], scores[0][1]


def pick_task(message: str, manifest: Dict[str, Any]) -> str:
    """
    Inside a chosen domain, decide which 'task' label best fits the message.
    Uses a simple pattern-count method over manifest["task_patterns"].
    Falls back to the first entry in manifest["tasks"] or "general".
    """
    m = message.lower()

    # task_patterns looks like: {"evac_shelter": ["evacuate","shelter",...], "cleanup":[...], ...}
    task_patterns: Dict[str, List[str]] = manifest.get("task_patterns", {})

    best_task, best_score = None, -1

    for task, pats in task_patterns.items():
        # Count how many patterns are present in the lowercased message (substring check)
        sc = sum(p in m for p in pats)
        if sc > best_score:
            best_task, best_score = task, sc

    # Fallback logic if no patterns matched
    return best_task or (manifest.get("tasks", ["general"])[0])


# ----------------------------
# Retrieval policy: decide context attachment and which packs to query
# ----------------------------

def requires_sources(task: str, manifest: Dict[str, Any]) -> bool:
    """
    Check if this task is marked as 'must attach sources' per the manifest.
    Example: "utilities_safety" in disaster domain -> True.
    """
    return task in set(manifest.get("requires_sources", []))


def packs_for_task(task: str, area_code: str, manifest: Dict[str, Any]) -> List[str]:
    """
    Map a task to knowledge packs (data collections) using the manifest.
    Replaces the placeholder <AREA> with the actual area_code (e.g., "WARD-5").
    Example: packs_by_task["evac_shelter"] -> ["evac_routes::<AREA>", "shelters::<AREA>"]
             becomes ["evac_routes::WARD-5", "shelters::WARD-5"].
    """
    packs = manifest.get("packs_by_task", {}).get(task, [])
    return [p.replace("<AREA>", area_code) for p in packs]


def probe_score(query: str, packs: List[str], manifest: Dict[str, Any]) -> float:
    """
    Cheap, heuristic "does this query look related to these packs?" score in [0.0..1.0].
    Implementation here is intentionally simple:
      - Lowercase the query
      - Extract keywords from pack names (alphanumeric runs)
      - Filter out some common throwaway words
      - Count how many of those keywords appear in the query
      - Convert count to a small score: 0.2 + 0.15*hits, capped at 1.0
    TUNE THIS based on real data; it's a placeholder until you plug in BM25/embeddings.
    """
    q = query.lower()

    if not packs:
        return 0.0

    # Pull crude "keywords" out of pack names
    kw: List[str] = []
    for p in packs:
        kw += re.findall(r"[a-z0-9]+", p.lower())

    # Remove generic terms that don't help decide relevance
    kw = [k for k in kw if k not in {"area", "routes", "rules", "basic", "first", "aid", "lines"}]

    # Unique keyword hits that also appear in the query
    hits = sum(1 for k in set(kw) if k in q)

    # Convert to a score (small base so that one hit isn't zero)
    return min(1.0, 0.2 + 0.15 * hits)


def should_attach_context(query: str, task: str, packs: List[str], manifest: Dict[str, Any]) -> bool:
    """
    Decide whether to attach external context (RAG) to the prompt.
    Attach if:
      - The task is marked as "requires_sources" in the manifest, OR
      - The quick probe score meets a per-domain threshold (manifest.thresholds.probe_score_min)
    """
    threshold = float(manifest.get("thresholds", {}).get("probe_score_min", 0.33))
    return requires_sources(task, manifest) or probe_score(query, packs, manifest) >= threshold


# ----------------------------
# Safety screen: use per-domain phrases to raise flags
# ----------------------------

def safety_screen_with_manifest(
    input_text: str,
    output_text: Optional[str],
    manifest: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Very basic safety pass:
      - manifest["safety_rules"] is a dict like {"hazard": ["smell gas", "downed line"], ...}
      - If ANY phrase appears in the input or (if provided) the output, we add that label to flags.
    Returns: {"ok": bool, "flags": [labels], "message": "..."}
    """
    flags: List[str] = []

    # Normalize case to make checks case-insensitive
    lower_in = (input_text or "").lower()
    lower_out = (output_text or "").lower() if output_text is not None else ""

    rules: Dict[str, List[str]] = manifest.get("safety_rules", {})

    for label, phrases in rules.items():
        # If any phrase is present in either text, raise that flag
        if any(p.lower() in lower_in for p in phrases) or any(p.lower() in lower_out for p in phrases):
            flags.append(label)

    ok = len(flags) == 0
    return {"ok": ok, "flags": flags, "message": "ok" if ok else "; ".join(flags)}


# ----------------------------
# Prompt building: turn message + context into the final LLM input
# ----------------------------

def build_prompt_with_template(
    message: str,
    context_chunks: List[Dict[str, Any]],
    manifest: Dict[str, Any],
    area_code: str
) -> str:
    """
    Build the actual text prompt sent to the model:
      - Start with the domain's prompt template (from manifest), and fill <AREA>
      - Add the "User Question"
      - If we have context chunks, list them as "References" with tiny citations
      - Otherwise, say "No external references attached"

    NOTE: This function currently joins lines with "\\n" (a literal backslash + n).
          If you want actual newlines in the returned string, use "\n" instead.
    """
    # Get the header template; default to a generic sentence if missing
    template = manifest.get("prompt_template", "You are a helper for <AREA>.")

    # Replace placeholder with the real area code
    header = template.replace("<AREA>", area_code)

    # Start assembling the lines of the prompt
    lines = [header, "", "## User Question", message.strip(), ""]

    if context_chunks:
        lines.append("## References")
        # Include up to 6 context snippets; the model can cite [1], [2], ...
        for i, ch in enumerate(context_chunks[:6], 1):
            src = ch.get("source", "unknown")
            span = ch.get("span", (0, 0))  # character range in the source (optional)
            text = (ch.get("text", "") or "").strip()
            lines.append(f"[{i}] {text}  (source: {src} chars {span[0]}-{span[1]})")

        lines += [
            "",
            "Use the references when relevant and cite [1], [2], ... inline."
        ]
    else:
        lines.append("## No external references attached")

    # IMPORTANT: This returns a string with *literal* backslash-n if "\\n" is used.
    # If you want real newlines in the final string, replace "\\n" with "\n".
    return "\\n".join(lines)


# ----------------------------
# Retrieval & ranking placeholders (to be wired to your index)
# ----------------------------

def search_chunks(query: str, packs: List[str], top_k: int = 6) -> List[Dict[str, Any]]:
    """
    STUB: Query your local index (BM25 / embeddings) using 'query' over 'packs'.
    Return a list of chunk dicts:
      {"doc_id": str, "text": str, "score": float, "source": str, "span": (start, end), "meta": {...}}
    """
    return []


def rank_confidence(chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Sort chunks so the most relevant/trusted appear first.
    Default: sort by score (desc), then by doc_id to keep it deterministic.
    """
    return sorted(
        chunks,
        key=lambda c: (-float(c.get("score", 0.0)), str(c.get("doc_id", "")))
    )


def enough_context(
    chunks: List[Dict[str, Any]],
    min_score: float = 0.7,
    min_coverage: float = 0.6
) -> bool:
    """
    Decide if the attached context is "good enough" to trust.
    - "strong" chunks: score >= min_score
    - "coverage": fraction of chunks that are strong
    Require at least one strong chunk AND sufficient coverage.
    Tune thresholds on your eval set.
    """
    if not chunks:
        return False

    strong = [c for c in chunks if float(c.get("score", 0.0)) >= min_score]
    coverage = len(strong) / max(1, len(chunks))

    return bool(strong) and coverage >= min_coverage


# ----------------------------
# Model call placeholder
# ----------------------------

def call_llm(prompt: str) -> str:
    """
    STUB: Connect this to Ollama (HTTP or subprocess).
    Raise for now so it's obvious at runtime that this isn't wired yet.
    """
    raise NotImplementedError("call_llm not wired.")


# ----------------------------
# Orchestration helpers: put the decisions together
# ----------------------------

def decide_and_prepare(
    message: str,
    area_code: str,
    manifests: Dict[str, Dict[str, Any]]
) -> Dict[str, Any]:
    """
    High-level helper that:
      1) picks the best domain (manifest),
      2) picks a task within that domain,
      3) maps the task to knowledge packs,
      4) decides if we should attach context,
      5) (if yes) retrieves and ranks chunks.

    Returns a dict with everything downstream code needs:
      {
        "domain": str,
        "task": str,
        "attach_context": bool,
        "packs": [str],
        "chunks": [dict],         # could be empty if not attaching or search returned nothing
        "manifest": dict
      }
    """
    # Domain (which manifest), using the scoring function above
    dom_id, manifest, score = pick_domain(message, manifests)

    # Task within that manifest
    task = pick_task(message, manifest)

    # Which packs to search (with <AREA> replaced)
    packs = packs_for_task(task, area_code, manifest)

    # Should we attach external context for this (task, packs)?
    attach = should_attach_context(message, task, packs, manifest)

    # Pull context if needed (search_chunks is a stub; wire to your index)
    chunks: List[Dict[str, Any]] = []
    if attach:
        chunks = rank_confidence(search_chunks(message, packs, top_k=6))

    return {
        "domain": dom_id,
        "task": task,
        "attach_context": attach,
        "packs": packs,
        "chunks": chunks,
        "manifest": manifest
    }


def dry_run_with_manifests(
    message: str,
    area_code: str,
    manifests: Dict[str, Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Non-destructive "what would happen?" helper for demos and debugging.
    It runs routing + policy, builds a prompt preview, and runs a safety pass on the input.
    It does NOT call the model or read any real knowledge packs in this stub.
    """
    decision = decide_and_prepare(message, area_code, manifests)

    # Build a prompt preview (shortened below to keep the output readable)
    prompt_preview = build_prompt_with_template(
        message,
        decision["chunks"],
        decision["manifest"],
        area_code
    )

    # Safety check against the input (only). You can also pass the model's output later.
    safety = safety_screen_with_manifest(message, None, decision["manifest"])

    # Return a compact summary for inspection
    return {
        "domain": decision["domain"],
        "task": decision["task"],
        "attach_context": decision["attach_context"],
        "packs": decision["packs"],
        "chunks": [c.get("doc_id", "") for c in decision["chunks"]],
        "flags": safety["flags"],
        # Show only the first 800 characters so logs don't explode
        "prompt_preview": (prompt_preview[:800] + ("..." if len(prompt_preview) > 800 else ""))
    }
