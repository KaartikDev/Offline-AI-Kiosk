# Offline-AI-Kiosk

# Introduction

This project aims to create a **community-driven system** where people can upload, download, and share curated **Knowledge Packs**—collections of trusted, localized information designed for specific communities and situations. These packs are paired with an **offline AI agent** that can run on modest hardware and provide answers even when internet and power are unavailable.

Native language support, cultural grounding, and strict safety guardrails are key. The project is being entered into OpenAI's Hackathon.


## Core Concepts

### Knowledge Packs (“Dropbox for Local Knowledge”)
- Each pack = curated, verified data for one *place × domain × scenario*.
- Contents:
  - **Core docs** (authoritative guidance, e.g., WHO, Red Cross).
  - **Local overlays** (clinics, shelters, NGOs, transportation, contacts).
  - **Canonical Q/A** (pre-vetted critical phrases to prevent translation drift).
  - **Citations & provenance** (sources, licenses, hashes).
- Packs are versioned, signed, and community-maintained.
- **Examples**:
  - *Rural Indian Village — Basic First Aid* (nearest clinic, snakebite response).
  - *Tampa, FL — Post-Hurricane Response* (shelters, water safety, insurance steps).

The AI Agent will use GPT-OSS:20B and entered into OpenAI's hackathon.


### Potential Avenues:
 - "Internet without internet"
  - LLMs trained on extremely large corpus of text
  - General knowledge of many domains wihtout needing external databse
  - More responsive, adaptable, and customziable than a search engine
 - "Wise Elder"
  - Fine tune model to local dialects, culture, etc
  - People can ask questions and get information to solve problems

Strongest use case is rural village in developing country, for example India.

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
- Must understand and respond in **native languages**.
- Must ground answers in **verified Knowledge Packs**, never guess.
- Must **refuse gracefully** when outside scope.
- Must be **simple, durable, and useful** under stress (voice-first, minimal interface).
- Must work **offline and long-term** with swappable pack storage.

### Immediate Problems:
- GPT-OSS:20b is a large model, signficant hardware reqs
- Native dialiects may be poorly documented/avialable
- Long term maintence care

### Proof of Concept for Hackathon
- Identify and contact one **target community** (rural or disaster-affected).
- Build **two scoped Knowledge Packs** (e.g., Bihar First Aid, Tampa Hurricane).
- Demo **voice in, voice out** (non-English query → safe, cited answer).
- Show **response safety**:
  - Refusal when outside scope.
  - “I don't know” when unsure.
  - Citations on sensitive issues.
- Run fully offline on local hardware.
- Deliver a **simple live demo + static website hub mock** for packs.

**Optional Stretch Goals:**
- Fine-tuned local dialect support.
- Pack version history + swappable downloads.
- Community contribution model (upload/review).
