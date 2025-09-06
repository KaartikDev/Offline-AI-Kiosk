#!/usr/bin/env python3
from pathlib import Path
import os
import sys

# >>> CHANGE THIS IF YOU WANT A DIFFERENT TARGET <<<
BASE = Path("/Users/ktejwani/Personal CS Projects/Summer 2025/Offline AI Kiosk/Offline-AI-Kiosk/first_aid_knowledge_pack_v3")

FLAT_FILES = [
    "manifest.yaml",
    "core/bleeding/TEMP.md",
    "core/choking-cpr/TEMP.md",
    "core/snakebite/TEMP.md",
    "core/heat/TEMP.md",
    "core/burns/TEMP.md",
    "core/diarrhea/TEMP.md",
    "core/maternal/TEMP.md",
    "core/child-illness/TEMP.md",
    "core/joint-pain/TEMP.md",
    "core/fractures/TEMP.md",
    "core/rash/TEMP.md",
    "core/safe-water/TEMP.md",
    "core/water-storage/TEMP.md",
    "core/rainwater/TEMP.md",
    "core/flood-wounds/TEMP.md",
    "core/pesticides/TEMP.md",
    "core/wild-animals/TEMP.md",
    "core/transport/TEMP.md",
    "core/contacts/TEMP.md",
    "core/education/TEMP.md",
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
    "vector_db/text/embeddings.jsonl",
    "vector_db/text/meta.json",
    "vector_db/text/faiss_index",                       # directory
    "vector_db/text/faiss_index/index.faiss",
    "vector_db/text/faiss_index/index.pkl",
    "vector_db/images/captions.jsonl",
    "vector_db/images/embeddings.jsonl",
    "vector_db/images/index.bin",
    "vector_db/images/meta.json",
    "vector_db/images/faiss_index",                    # directory
    "vector_db/images/faiss_index/index.faiss",
    "vector_db/images/faiss_index/index.pkl",
]

def is_dir_marker(rel: str) -> bool:
    # Treat entries with no extension as directories
    return '.' not in Path(rel).name

def main():
    base = BASE.resolve()
    print(f"BASE: {base}")
    # Ensure base exists
    base.mkdir(parents=True, exist_ok=True)

    # Check writability
    if not os.access(base, os.W_OK):
        print(f"ERROR: BASE is not writable: {base}")
        sys.exit(2)

    made_dirs = 0
    made_files = 0
    skipped_dirs = 0
    skipped_files = 0

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
