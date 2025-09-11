<a name="top"></a>
#  Beacon Offline Agent

**Beacon Offline Agent is an offline AI assistant that uses curated Knowledge Packs to deliver trusted, local information.**  
Built for resilience, it runs fully on modest laptops with no internet dependency, ensuring that critical guidance remains available in disaster and low resource scenarios.

[![gpt-oss](https://img.shields.io/badge/gpt--oss-20B-lightgrey.svg?style=flat-square&logo=openai)](https://ollama.ai/library/gpt-oss)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg?style=flat-square&logo=open-source-initiative)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat-square&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116-green.svg?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg?style=flat-square&logo=jupyter)](https://jupyter.org/)
[![Gradio](https://img.shields.io/badge/Gradio-5.44-lightblue.svg?style=flat-square&logo=gradio)](https://gradio.app/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3-purple.svg?style=flat-square&logo=chainlink)](https://www.langchain.com/)
[![Ollama](https://img.shields.io/badge/Ollama-0.5.3-black.svg?style=flat-square&logo=llama)](https://ollama.ai/)
[![Whisper](https://img.shields.io/badge/OpenAI-Whisper-red.svg?style=flat-square&logo=openai)](https://github.com/openai/whisper)
[![Piper](https://img.shields.io/badge/TTS-Piper-yellow.svg?style=flat-square&logo=speaker-deck)](https://github.com/rhasspy/piper)

![Beacon demo](Beacon%20Media%20Assets/bihar%20demo%20v4%20edited.gif)
---

## Table of Contents
- [📖 Introduction](#introduction)
- [🖥 Hardware Requirements](#hardware-requirements)
- [🚀 Installation & Configuration](#installation--config)
- [⚡ Quick Start](#quick-start)
- [🌳 File Tree](#file-tree)
- [🧠 Knowledge Packs](#knowledge-packs)
- [🤝 Contributing](#contributing)
- [✍️ Acknowledgments](#acknowledgments)
- [👾 Proof of Concept for Hackathon](#proof-of-concept-for-hackathon)
- [📄 License](#license)

---

<a id="introduction"></a>

## 📖 Introduction

When internet or electricity goes down, people lose access to the information they need most. Beacon Offline Agent was built to solve this. After Hurricanes Milton and Helene in 2024, parts of Florida had no internet for weeks. In Bihar, India, 53 percent of people still lack reliable internet access. GPT OSS 20B is exceptionally powerful and has tool calling capabilties, but without local context it risks hallucinating. It cannot know which shelters are open in Pinellas County, FL or what first aid steps are safe in rural Bihar, India.

Beacon closes that gap with curated Knowledge Packs. These are community made bundles of documents, images, and citations that ground the model in trusted local sources. Packs can include first aid guides, disaster steps, or shelter maps, and the system runs entirely offline on a modest laptop, remaining useful even in low resource or emergency settings.

This project is especially relevant for:
- Communities affected by disasters
- Rural regions with limited connectivity
- Humanitarian and relief organizations
- Educators or local leaders sharing essential guidance
- Travelers in remote or offline environments

---
<a id="hardware-requirements"></a>

## 🖥 Hardware Requirements

Beacon Offline Agent depends on running **GPT-OSS 20B** locally with Ollama.  
This means it will **only work on laptops or desktops that can run GPT-OSS**.  

At a minimum, your system should have:
- **16 GB RAM** (required for GPT-OSS 20B with quantization)  
- A modern **CPU** (runs slower without GPU support)  
- (Recommended) A **GPU with ≥16 GB VRAM** for faster inference  

---
<a id="installation--config"></a>

## 🚀 Installation & Configuration

Follow these steps to set up the project.

### 1. Clone the repository
Download the project code from GitHub:
```bash
git clone https://github.com/KaartikDev/beacon-offline-agent.git
cd beacon-offline-agent
```



### 2. Create and activate a virtual environment
It is recommended to use a virtual environment to isolate dependencies.

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**
```bash
python -m venv venv
venv\Scripts\activate
```

When activated, your terminal prompt should show `(venv)` at the beginning.


### 3. Install Python dependencies
Update pip and install all required packages from `requirements.txt`:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```


### 4. Install Ollama
Download and install Ollama for your operating system:  
👉 [Ollama Installation Guide](https://ollama.ai/download)

Verify the installation:
```bash
ollama --version
```

### 5. Pull required Ollama models
This project requires:
- **GPT-OSS 20B** (main language model)  
- **Nomic-Embed-Text v1.5** (embedding model)  

Download them with:
```bash
ollama pull gpt-oss:20b
ollama pull nomic-embed-text:v1.5
```

This may take several minutes depending on your internet speed.

---
<a id="quick-start"></a>

## ⚡ Quick Start

Follow these steps to launch the **Beacon Offline Agent** demo UI from the Jupyter notebook `FinalBeaconAgent.ipynb`, using your virtual environment kernel and a preloaded Knowledge Pack.



### 1) Open the Jupyter notebook
- Open the **beacon-offline-agent** folder in your IDE (VS Code, PyCharm, JupyterLab, etc.).
- Open **FinalBeaconAgent.ipynb**.
- If prompted for an interpreter, pick your project’s **venv**.



### 2) Set the notebook kernel to your venv
In the notebook menu bar:
- Go to **Kernel → Change kernel → Python (beacon-venv)** (or select the venv name you created).
- If you didn’t register the kernel, choose the venv’s Python via **Kernel → Change kernel** and select the appropriate interpreter.

> Tip: If you see import errors, you’re likely not using the venv. Switch the kernel and try again.


### 3) Run all cells
In the notebook menu bar:
- Click **Kernel → Restart & Run All** (or **Run → Run All Cells**).  
- Wait for all cells to finish executing (you’ll see a `*` next to a cell while it’s running).



### 4) Choose a Knowledge Pack
When prompted in the notebook, type exactly one of the following options into the input cell / prompt:
- `FLORIDA` → **Pinellas County, Florida — Hurricane Response** kpack  
- `INDIA` → **Bihar, India — Support** kpack

The notebook will initialize the selected pack (load FAISS indices, metadata, etc.).



### 5) Open the local UI
At the end of the notebook logs you’ll see lines similar to:

```
* Running on local URL:  http://XXX.X.X.X:XXXX
* To create a public link, set `share=True` in `launch()`.
```

Open the **local URL** in your browser to use the app. If a different port is shown, use that one.



### Notes & Troubleshooting
- If the page doesn’t load, verify the notebook finished running and that the URL/port match the printed output.
- If the port `7860` is busy, the app may select another port automatically; use the URL printed by the notebook.
- If you change packs, **Restart & Run All** again to reload with the new selection.
- Make sure Ollama is running and the models are downloaded:
  ```bash
  ollama list
  ```
---
<a id="file-tree"></a>

## 🌳 File Tree
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
---
<a id="knowledge-packs"></a>

## 🧠 Knowledge Packs

**Knowledge Packs** are curated, domain-specific bundles of trusted, local information.  
Instead of letting the LLM “make things up,” Beacon answers by running **RAG over these packs** only.

**What’s inside a pack**
- Structured metadata (`manifest.yaml`: name, version, locales, asset paths)
- Curated sources (core docs, maps, infographics, local contacts)
- Citations & provenance (sources, licenses, hashes)
- Precomputed vector indices (FAISS + embeddings) for fast offline search

**Agent flow (per query)**
1. Select the appropriate pack for the user’s question
2. Retrieve relevant chunks via **RAG** from that pack only
3. Compose an answer grounded in those chunks  
4. If insufficient evidence exists, respond **“I don’t know.”**


### Current Packs

**1) Pinellas County, Florida — Hurricane Response (Kpack)**  
- **Scope:** Evacuation/shelters, post-hurricane safety, potable water, insurance steps, local contacts  
- **Includes:** Shelter maps, county guidance, Ready.gov/FEMA references, local numbers  
- **Try it:** In the notebook prompt, type `FLORIDA`

**2) Bihar, India — Support (Kpack)**  
- **Scope:** First aid basics, water safety, clinic/administration contacts, rural safety tips  
- **Includes:** Core first-aid docs, local overlays (clinics/administration), Hindi/English materials  
- **Try it:** In the notebook prompt, type `INDIA`

> The notebook (`FinalBeaconAgent.ipynb`) will initialize the selected pack and load its FAISS indices.


### ⬇️ Pack Installation (planned)

Preview our proof-of-concept site: **[Pack Hub (mock)](https://chatgpt.com/canvas/shared/68bf664edce08191898c65c23b63542d)**

**Buttons & behavior (planned):**
- **Preview** — opens a details modal (Region, Domain, Locales, Size, Updated, Downloads, tags).
- **Quick Download** — one-click download of the pack `.zip`.
- **Download** (in modal) — same as Quick Download.
- **Add to Device** (in modal) — sends the pack to `./knowledge_packs/<pack-name>/` on your machine (once local linking is enabled).
- **Download Selected** — batch downloads multiple checked packs.
- **Clear Selection** — clears current selections.
- **Browse Packs / Create Pack** — browse catalog or start the pack creation flow.
- **Search bar** — search by name, region, domain, or tag.
- **Filters** — filter by Region and Locales; includes grid/list view toggle.

> **Current status:** This is a UI proof-of-concept — installs from the website are not enabled yet.  

---
<a id="contributing"></a>

## 🤝 Contributing

We’re excited to collaborate—especially on creating high-quality **Knowledge Packs** that help real communities.

### Ways You Can Help (Knowledge Packs)
- **Pick a scope:** Choose one *place × domain × scenario* (e.g., “Pinellas, FL — Post-Hurricane Response”).
- **Curate trusted sources:** FEMA/Ready.gov/WHO/Red Cross + **local overlays** (shelters, clinics, maps, contacts).
- **Verify licensing & cite everything:** Add source, license, and (if possible) hash in the pack manifest.
- **Structure the pack folder:**
  - `manifest.yaml` (name, version, date, locales, assets, citations, indices)
  - `assets/` (pngs of images, maps, infographics)
  - `core/` (PDF or Markdown files of human-readable guidance by topic/locale: `en/`, `hi/`, etc.)
  - `vector_db/` (precomputed FAISS + embeddings)
- **Build indices:** Use `textVectorDBCreation.ipynb` (and optional `imageCaptionVectorDB.ipynb`) to generate embeddings + FAISS.
- **Follow conventions:** lowercase/kebab-case folders (e.g., `choking-cpr/`), accurate paths, clear topics, version bumps.
- **Test locally:** Change the path and load the pack in `FinalBeaconAgent.ipynb`, run all cells, ask in-scope questions, and confirm “I don’t know” for out-of-scope.
- **Package & share:** Zip the folder; users will place it under `./knowledge_packs/<pack-name>/`. Include a short README and changelog.

### Questions, Ideas, or Deployments
If you’re interested in helping out **or** want to **deploy Beacon** in your community/organization, please contact:  
**[ktejwani81@ucla.edu](mailto:ktejwani81@ucla.edu)**\
**[mukundsk@uw.edu](mailto:mukundsk@uw.edu)**

---
<a id="acknowledgments"></a>

## ✍️ Acknowledgments

**Core team** — Kaartik Tejwani & Mukund Senthil Kumar.

Community & sources — We’re grateful for publicly available guidance, maps, and data from FEMA/Ready.gov, WHO, Red Cross/IFRC, and local agencies (e.g., Pinellas County Emergency Management & Fire District, Bihar state/district administration).

Open-source stack — This project stands on the shoulders of: GPT-OSS 20B (via Ollama), Whisper, Piper TTS, FastAPI, Gradio, LangChain, FAISS, Nomic-Embed, Python, and Jupyter.

Friends & family — Thank you for testing, feedback, and the moral support that kept us shipping.

OpenAI Hackathon — For the spark (and deadline!) that pushed us to build this idea.

---
<a id="proof-of-concept-for-hackathon"></a>

## 👾 Proof of Concept for Hackathon
- Identify one **target community** (rural or disaster-affected).
- Build **two scoped Knowledge Packs** (e.g., Bihar First Aid, Tampa Hurricane).
- Run fully offline on local hardware.
- Deliver a **simple live demo + static website hub mock** for packs.

Sample Conversations can be found under media assets. 

### Demo (3 min)
[![Watch the demo](https://img.youtube.com/vi/fFMrIK-SFQ8/hqdefault.jpg)](https://youtu.be/fFMrIK-SFQ8)
---
<a id="license"></a>

## 📄 License
Apache License 2.0 — see [LICENSE](./LICENSE).

[Back to top](#top)