#!/usr/bin/env python3
from pathlib import Path
import os
import sys
#where files get made
BASE = Path("/Users/ktejwani/Personal CS Projects/Summer 2025/Offline AI Kiosk/Offline-AI-Kiosk/first_aid_knowledge_pack_v3")

FLAT_FILES = [
    "manifest.yaml",
    # core topics (TEMP.md inside hi_en/)
    "core/bleeding/hi_en/TEMP.md",
    "core/choking-cpr/hi_en/TEMP.md",
    "core/snakebite/hi_en/TEMP.md",
    "core/heat/hi_en/TEMP.md",
    "core/burns/hi_en/TEMP.md",
    "core/diarrhea/hi_en/TEMP.md",
    "core/maternal/hi_en/TEMP.md",
    "core/child-illness/hi_en/TEMP.md",
    "core/joint-pain/hi_en/TEMP.md",
    "core/fractures/hi_en/TEMP.md",
    "core/rash/hi_en/TEMP.md",
    "core/safe-water/hi_en/TEMP.md",
    "core/water-storage/hi_en/TEMP.md",
    "core/rainwater/hi_en/TEMP.md",
    "core/flood-wounds/hi_en/TEMP.md",
    "core/pesticides/hi_en/TEMP.md",
    "core/wild-animals/hi_en/TEMP.md",
    "core/transport/hi_en/TEMP.md",
    "core/contacts/hi_en/TEMP.md",
    "core/education/hi_en/TEMP.md",

    # assets (images) — empty placeholders
    "assets/bleeding/tourniquet.png",
    "assets/bleeding/pressure.png",
    "assets/choking-cpr/heimlich.png",
    "assets/choking-cpr/hands_only_cpr.png",
    "assets/snakebite/no_cut.png",
    "assets/snakebite/immobilize.png",
    "assets/heat/cooling.png",
    "assets/heat/shade.png",
    "assets/burns/cool_water.png",
    "assets/burns/cover.png",
    "assets/diarrhea/ors.png",
    "assets/maternal/warning.png",
    "assets/child-illness/fever.png",
    "assets/joint-pain/rest.png",
    "assets/fractures/splint.png",
    "assets/rash/plant_contact.png",
    "assets/safe-water/boil.png",
    "assets/water-storage/containers.png",
    "assets/rainwater/collection.png",
    "assets/flood-wounds/wound.png",
    "assets/pesticides/safety.png",
    "assets/wild-animals/fence.png",
    "assets/transport/bus.png",
    "assets/contacts/office.png",
    "assets/education/school.png",

    # vector_db / text
    "vector_db/text/embeddings.jsonl",
    "vector_db/text/meta.json",
    "vector_db/text/faiss_index",                       # directory
    "vector_db/text/faiss_index/index.faiss",
    "vector_db/text/faiss_index/index.pkl",

    # vector_db / images
    "vector_db/images/captions.jsonl",
    "vector_db/images/embeddings.jsonl",
    "vector_db/images/index.bin",
    "vector_db/images/meta.json",
    "vector_db/images/faiss_index",                    # directory
    "vector_db/images/faiss_index/index.faiss",
    "vector_db/images/faiss_index/index.pkl",
]

def is_dir_marker(rel: str) -> bool:
    return '.' not in Path(rel).name

def main():
    base = BASE.resolve()
    print(f"BASE: {base}")
    base.mkdir(parents=True, exist_ok=True)

    if not os.access(base, os.W_OK):
        print(f"ERROR: BASE is not writable: {base}")
        sys.exit(2)

    made_dirs = made_files = skipped_dirs = skipped_files = 0

    for rel in FLAT_FILES:
        target = base / rel
        if is_dir_marker(rel):
            if target.exists():
                print(f"[dir exists] {target}")
                skipped_dirs += 1
            else:
                target.mkdir(parents=True, exist_ok=True)
                print(f"[dir created] {target}")
                made_dirs += 1
        else:
            if not target.parent.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                print(f"[dir created] {target.parent}")
                made_dirs += 1
            if target.exists():
                print(f"[file exists] {target}")
                skipped_files += 1
            else:
                target.touch()
                print(f"[file created] {target}")
                made_files += 1

    print("\nSummary:")
    print(f"  Dirs created:  {made_dirs}")
    print(f"  Files created: {made_files}")
    print(f"  Dirs existed:  {skipped_dirs}")
    print(f"  Files existed: {skipped_files}")

if __name__ == "__main__":
    main()
