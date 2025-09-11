# Offline-AI-Kiosk

# Introduction

This project aims to create a **community-driven system** where people can upload, download, and share curated **Knowledge Packs**—collections of trusted, localized information designed for specific communities and situations. These packs are paired with an **offline AI agent** that can run on modest laptops and provide answers even when internet and the electric grid is unavailable.

## Core Concepts

### Knowledge Packs (“Dropbox for Local Knowledge”)
- Each pack = curated, verified data for one *place × domain × scenario*.
- Contents:
  - **Core docs** (authoritative guidance, e.g., WHO, Red Cross).
  - **Local overlays** (clinics, shelters, NGOs, transportation, contacts).
  - **Citations & provenance** (sources, licenses, hashes).
- Packs are versioned, signed, and community-maintained.
- **Examples**:
  - *Rural Indian Village — Basic First Aid* (nearest clinic, snakebite response).
  - *Pinellas, FL — Post-Hurricane Response* (shelters, water safety, insurance steps).

The AI Agent will use GPT-OSS:20B and entered into OpenAI's hackathon.

### File Tree
Simplfied knowledge pack file tree
```
first_aid_knowledge_pack_v3/
└── first_aid_knowledge_pack_v3/
    ├── manifest.yaml
    ├── assets/
    │   ├── bleeding/
    │   │   ├── pressure.png
    │   │   └── tourniquet.png
    │   ├── burns/
    │   │   ├── cool_water.png
    │   │   └── cover.png
    │   ├── child-illness/fever.png
    │   ├── choking-cpr/
    │   │   ├── hands_only_cpr.png
    │   │   └── heimlich.png
    │   ├── contacts/office.png
    ├── core/
    │   ├── bleeding/hi_en/TEMP.md
    │   ├── burns/hi_en/TEMP.md
    │   ├── child-illness/hi_en/TEMP.md
    │   ├── choking-cpr/hi_en/TEMP.md
    │   └── wild-animals/hi_en/TEMP.md
    ├── vector_db/
    │   ├── text/
    │   │   ├── embeddings.jsonl
    │   │   ├── meta.json
    │   │   └── faiss_index/
    │   │       ├── index.faiss
    │   │       └── index.pkl
    │   └── images/
    │       ├── captions.jsonl
    │       ├── embeddings.jsonl
    │       ├── index.bin
    │       ├── meta.json
    │       └── faiss_index/
    │           ├── index.faiss
    │           └── index.pkl
```


### Device Overview:
- Any laptop with a strong enough CPU and 16GB RAM

### Knowledge Packs:
Instead of relying on LLM agent to generate information, create a curated database of verified sources agent can pull from. Each database is called a "Knowledge Pack" and is domain specifc. Knowledge Pack will be a combination of structred JSON data + local vector store of pre-embbedded information.

Agent will be fine tuned to each knowledge pack. A culture knowledge pack will also be provided.

Agent should do the following:
1. Understand which knowledge base can help answer query
2. Run a RAG to get relevant chunks
3. Build an answer using information
 - Say I don't know if its unsure


### Usage Requirements
- Must ground answers in **verified Knowledge Packs**, never guess.
- Must **refuse gracefully** when outside scope.
- Must be **simple, durable, and useful** under stress (voice-first, minimal interface).
- Must work **offline and long-term** with swappable pack storage.


### Proof of Concept for Hackathon
- Identify one **target community** (rural or disaster-affected).
- Build **two scoped Knowledge Packs** (e.g., Bihar First Aid, Tampa Hurricane).
- Run fully offline on local hardware.
- Deliver a **simple live demo + static website hub mock** for packs.



### Dependancies
Please use **requirments.txt** for full package list. Sample of the most important libraries.
```
gradio==5.44.1
langchain==0.3.27
langchain-community==0.3.27
langchain-core==0.3.74
langchain-ollama==0.3.6
langgraph==0.6.6
faiss-cpu==1.12.0
pypdf==6.0.0
PyYAML==6.0.2
ollama==0.5.3
requests==2.32.5
numpy==2.2.6
```