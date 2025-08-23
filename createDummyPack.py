#!/usr/bin/env python3
"""
Create the first_aid_pack folder tree with empty files.
Exact structure only (Option A).
"""

from pathlib import Path

BASE = Path("first_aid_pack")

FLAT_FILES = [
    # root
    "manifest.yaml",

    # core / bleed-control
    "core/bleed-control/hi_en/bleeding_control_overview.md",
    "core/bleed-control/hi_en/bleeding_tourniquet_steps.pdf",
    "core/bleed-control/hi_en/bleeding_control_quickref.docx",
    "core/bleed-control/local/bleeding_control_local_practices.txt",

    # core / fracture-splint
    "core/fracture-splint/hi_en/fracture_overview.md",
    "core/fracture-splint/hi_en/splint_with_local_materials.pdf",
    "core/fracture-splint/hi_en/fracture_when_to_refer.md",
    "core/fracture-splint/local/fracture_referral_paths_bihar.md",

    # core / burns
    "core/burns/hi_en/burns_first_steps.md",
    "core/burns/hi_en/burns_dos_and_donts.md",
    "core/burns/hi_en/burns_referral_criteria.pdf",
    "core/burns/local/burns_local_facilities.txt",

    # core / heat-illness
    "core/heat-illness/hi_en/heat_illness_overview.md",
    "core/heat-illness/hi_en/heat_active_cooling.pdf",
    "core/heat-illness/hi_en/heat_quick_ref.docx",
    "core/heat-illness/local/heat_illness_local_signs.md",

    # core / snakebite
    "core/snakebite/hi_en/snakebite_first_aid.md",
    "core/snakebite/hi_en/snakebite_dos_and_donts.md",
    "core/snakebite/hi_en/snakebite_transport.pdf",
    "core/snakebite/local/snakebite_hotspots_clinics_bihar.md",

    # core / flood-wounds
    "core/flood-wounds/hi_en/flood_cuts_cleaning.docx",
    "core/flood-wounds/hi_en/flood_infection_signs.md",
    "core/flood-wounds/hi_en/flood_tetanus_precautions.md",
    "core/flood-wounds/local/flood_wound_care_supply_list.txt",

    # core / diarrhea-ors
    "core/diarrhea-ors/hi_en/ors_homemade_recipe.md",
    "core/diarrhea-ors/hi_en/ors_usage_in_children.pdf",
    "core/diarrhea-ors/hi_en/zinc_supplementation.md",
    "core/diarrhea-ors/local/safe_water_sources_bihar.md",

    # core / choking
    "core/choking/hi_en/choking_adult.md",
    "core/choking/hi_en/choking_child.md",
    "core/choking/hi_en/choking_infant.pdf",

    # core / cpr
    "core/cpr/hi_en/cpr_steps.md",
    "core/cpr/hi_en/cpr_quick_checklist.docx",

    # core / maternal
    "core/maternal/hi_en/maternal_danger_signs.md",
    "core/maternal/hi_en/maternal_referral_steps.pdf",

    # core / poisoning
    "core/poisoning/hi_en/poisoning_overview.md",
    "core/poisoning/hi_en/poisoning_first_aid.md",

    # assets (images)
    "assets/bleeding/tourniquet_step_diagram.png",
    "assets/bleeding/direct_pressure.png",
    "assets/fracture/basic_splint_bamboo.png",
    "assets/diarrhea/ors_mixing.png",
    "assets/heat/evap_cooling_cloth.png",
    "assets/rabies/wound_wash.png",
    "assets/snakebite/no-cut-no-suck.png",

    # vector_db / text
    "vector_db/text/embeddings.jsonl",
    "vector_db/text/index.bin",
    "vector_db/text/meta.json",

    # vector_db / images
    "vector_db/images/captions.jsonl",
    "vector_db/images/embeddings.jsonl",
    "vector_db/images/index.bin",
    "vector_db/images/meta.json",

    # citations
    "citations/sources.md",
]

def build_tree(base: Path, files: list[str]) -> None:
    for rel in files:
        p = base / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if not p.exists():
            p.touch()

def main():
    BASE.mkdir(parents=True, exist_ok=True)
    build_tree(BASE, FLAT_FILES)
    print(f"Created tree under: {BASE.resolve()}")

if __name__ == "__main__":
    main()
