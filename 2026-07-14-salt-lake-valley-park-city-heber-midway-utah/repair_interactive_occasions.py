#!/usr/bin/env python3
"""Expand bakery occasion facets without changing the canonical top-three picks."""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


RUN_DIR = Path(__file__).resolve().parent
DECISIONS_PATH = RUN_DIR / "06-decisions.json"
PROJECTION_PATH = RUN_DIR / "interactive-results-projection.json"
AUDIT_PATH = RUN_DIR / "interactive-occasion-assignment-audit.json"

OCCASION_ORDER = (
    "best-bread",
    "pastry-coffee",
    "gift",
    "cross-town",
    "rare-find",
)
PASTRY_STOP_SPECIALTIES = {
    "pastry-patisserie",
    "doughnuts",
    "cakes-cheesecake",
    "gluten-free-vegan",
}
GIFT_SPECIALTIES = {
    "pies",
    "cookies-sweets",
    "cakes-cheesecake",
    "regional-specialty",
}
RARE_ITEM_PATTERN = re.compile(
    r"\b(stroopwafel|baklava|kouign(?:-amann)?|kekepua|lamington|factura|"
    r"flatbread|empanada|pasty|pasties|hand-pie|wafer|ensaymada|pandesal|phyllo)\b",
    re.IGNORECASE,
)


def main() -> None:
    decisions = json.loads(DECISIONS_PATH.read_text())
    projection = json.loads(PROJECTION_PATH.read_text())
    by_id = {record["id"]: record for record in decisions["records"]}

    for row in projection["practical"]:
        record = by_id[row["id"]]
        specialty = set(row["facet_values"].get("specialty", []))
        access = set(row["facet_values"].get("access", []))
        occasions = set(row["facet_values"].get("occasion", []))
        scratch = record["score"].get("s")
        combined = record["score"].get("g")
        accepted_text = " ".join(
            [
                record["name"],
                row["summary"],
                *record.get("rationale", []),
                *record.get("rare_finds", []),
            ]
        )

        def add(value: str) -> None:
            occasions.add(value)

        if scratch is not None and scratch >= 70 and "bread" in specialty:
            add("best-bread")
        if (
            scratch is not None
            and "walk-in" in access
            and specialty.intersection(PASTRY_STOP_SPECIALTIES)
        ):
            add("pastry-coffee")
        if (
            combined is not None
            and combined >= 55
            and specialty.intersection(GIFT_SPECIALTIES)
        ):
            add("gift")
        if combined is not None and combined >= 70:
            add("cross-town")
        if scratch is not None and (
            record.get("rare_finds") or RARE_ITEM_PATTERN.search(accepted_text)
        ):
            add("rare-find")

        row["facet_values"]["occasion"] = [
            value for value in OCCASION_ORDER if value in occasions
        ]

    after = Counter(
        value
        for row in projection["practical"]
        for value in row["facet_values"].get("occasion", [])
    )
    after_assigned = sum(
        bool(row["facet_values"].get("occasion"))
        for row in projection["practical"]
    )
    PROJECTION_PATH.write_text(
        json.dumps(projection, indent=2, ensure_ascii=False) + "\n"
    )

    audit = {
        "schema_version": "1.0",
        "artifact": "interactive occasion assignment audit",
        "run_id": decisions["run_id"],
        "scope": "practical projection rows only",
        "constraints": {
            "occasion_values": list(OCCASION_ORDER),
            "markdown_top_three_changed": False,
            "decisions_changed": False,
            "decision_hash_changed": False,
            "external_research": False,
        },
        "rules": [
            {
                "occasion": "all",
                "rule": "Preserve explicit occasion values already represented in the projection.",
            },
            {
                "occasion": "best-bread",
                "rule": "Assign to the bread specialty when completed scratch score S >= 70.",
            },
            {
                "occasion": "pastry-coffee",
                "rule": "Assign to walk-in pastry, doughnut, cake, or gluten-free/vegan bakery records with a completed scratch score.",
            },
            {
                "occasion": "gift",
                "rule": "Assign to pie, cookie/sweet, cake, or regional-specialty records when completed combined score G >= 55.",
            },
            {
                "occasion": "cross-town",
                "rule": "Assign when completed combined score G >= 70, the strongest practical score band in this snapshot.",
            },
            {
                "occasion": "rare-find",
                "rule": "Retain explicit rare finds and add only named scarce regional items documented in accepted decision text.",
            },
            {
                "occasion": "unassigned",
                "rule": "Leave empty when none of the evidence-backed suitability rules apply.",
            },
        ],
        "counts": {
            "practical_rows": len(projection["practical"]),
            "markdown_top_three_by_occasion": {
                value: 3 for value in OCCASION_ORDER
            },
            "interactive_by_occasion": {
                value: after[value] for value in OCCASION_ORDER
            },
            "interactive_assigned_rows": after_assigned,
            "interactive_unassigned_rows": len(projection["practical"]) - after_assigned,
        },
    }
    AUDIT_PATH.write_text(json.dumps(audit, indent=2) + "\n")
    print(json.dumps(audit, indent=2))


if __name__ == "__main__":
    main()
