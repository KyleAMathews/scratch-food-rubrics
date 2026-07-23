#!/usr/bin/env python3
"""Apply the two user-adjudicated v8.14 bakery partial scores."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


RUN_DIR = Path(__file__).resolve().parent
DECISIONS_PATH = RUN_DIR / "06-decisions.json"
PROJECTION_PATH = RUN_DIR / "interactive-results-projection.json"


def canonical_hash(value: object) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def source(artifact: str, ref: str) -> dict[str, str]:
    return {"artifact": artifact, "ref": ref}


def main() -> None:
    decisions = json.loads(DECISIONS_PATH.read_text())
    by_id = {record["id"]: record for record in decisions["records"]}

    baby = by_id["A-012"]
    baby.update(
        {
            "address": "204 East 500 South, Salt Lake City, UT 84111",
            "coordinates": {"lat": 40.7582678, "lng": -111.885046},
            "disposition": "scratch-eligible-partial",
            "reason": "user ground truth establishes scratch bagels; other bakery criteria and aggregate rating remain unknown",
            "score": {
                "s": None,
                "i": None,
                "g": None,
                "provenance": "mixed",
                "state": "partial",
                "s_earned": 18,
                "s_observed_possible": 30,
                "s_coverage": 0.3,
                "confidence": "medium",
                "criteria": {
                    "core_craft": 18,
                    "input_sourcing": None,
                    "breadth_capacity": None,
                    "bake_cadence": None,
                    "operator_format": None,
                },
            },
            "rating": None,
            "tier": "scratch-verified partial evidence; rating exhausted",
            "ranking_eligible": False,
            "occasions": [],
            "rare_finds": [],
            "access": {
                "format": "storefront",
                "state": "walk-in active",
                "evidence_date": "2026-07-14",
            },
            "rationale": [
                "The user's direct ground truth establishes that the bagels are scratch-made; the core-craft band is competent but shallow because no fermentation or shaping detail was documented.",
                "Accepted run evidence separately attributes in-house cured lox and house sauces to Baby's. Those components do not add proof for dough, sourcing, cadence, capacity, or operator format.",
                "The literal aggregate rating remained exhausted-unavailable after the run's direct-platform sequence, so this partial score stays unranked in the rating-unconfirmed tier.",
            ],
            "sources": [
                source("04-worker-returns/batch-B08-evidence_batch_01.md", "Baby’s Bagels"),
                source("04-worker-returns/repair-R08-evidence_batch_01.md", "A-012"),
                source("06-user-ground-truth.md", "A-012 — Baby's Bagels"),
            ],
        }
    )

    bagel_den = by_id["A-013"]
    bagel_den.update(
        {
            "address": "570 North Main Street, Heber City, UT 84032",
            "coordinates": {"lat": 40.515541, "lng": -111.4123809},
            "disposition": "scratch-eligible-partial",
            "reason": "official evidence establishes scratch-made schmears while bagel dough is sourced from New York; other criteria and aggregate rating remain unknown",
            "score": {
                "s": None,
                "i": None,
                "g": None,
                "provenance": "documented",
                "state": "partial",
                "s_earned": 8,
                "s_observed_possible": 30,
                "s_coverage": 0.3,
                "confidence": "high",
                "criteria": {
                    "core_craft": 8,
                    "input_sourcing": None,
                    "breadth_capacity": None,
                    "bake_cadence": None,
                    "operator_format": None,
                },
            },
            "rating": None,
            "tier": "scratch-verified partial evidence; rating exhausted; schmears only",
            "ranking_eligible": False,
            "occasions": [],
            "rare_finds": [],
            "access": {
                "format": "storefront",
                "state": "walk-in active",
                "evidence_date": "2026-07-14",
            },
            "rationale": [
                "The official site says the schmears are made from scratch daily and in house, which supports a narrow component-level core-craft score.",
                "The same official source says bagel dough comes fresh from Long Island each week. The partial score does not claim scratch bagel dough or on-site bagel production.",
                "The aggregate rating remained exhausted-unavailable, so the record stays unranked in the rating-unconfirmed tier.",
            ],
            "sources": [
                source("04-worker-returns/batch-B08-evidence_batch_01.md", "Bagel Den"),
                source("04-worker-returns/repair-R08-evidence_batch_01.md", "A-013"),
            ],
        }
    )

    valsof = by_id["A-231"]
    valsof.update(
        {
            "address": "9486 South Union Square, Sandy, UT 84070",
            "coordinates": {"lat": 40.5790037, "lng": -111.874049},
            "disposition": "scratch-eligible-partial",
            "reason": "low-confidence user evidence supports house fillings only; dough, bread, puff pastry, and lamination remain unknown",
            "score": {
                "s": None,
                "i": None,
                "g": None,
                "provenance": "user-ground-truth",
                "state": "partial",
                "s_earned": 8,
                "s_observed_possible": 30,
                "s_coverage": 0.3,
                "confidence": "low",
                "criteria": {
                    "core_craft": 8,
                    "input_sourcing": None,
                    "breadth_capacity": None,
                    "bake_cadence": None,
                    "operator_format": None,
                },
            },
            "rating": {
                "value": 4.4,
                "count": 141,
                "count_state": "literal",
                "platform": "Restaurantji",
                "provenance": "direct",
                "accessed_at": "2026-07-14",
            },
            "tier": "rating-confirmed partial evidence; fillings only",
            "ranking_eligible": False,
            "occasions": [],
            "rare_finds": [],
            "access": {
                "format": "storefront",
                "state": "walk-in active",
                "evidence_date": "2026-07-14",
            },
            "rationale": [
                "The user's cautious assessment supports only house fillings. The low core-craft partial reflects a meaningful component, not scratch dough or a scratch bakery-wide claim.",
                "The run found no explicit hand-mixing, proofing, baking-location, or lamination statement. Menu breadth and soft/flaky review text cannot fill those gaps.",
                "Restaurantji directly reported 4.4/5 from 141 ratings. The partial clears the bakery rating gate but remains unranked because the other scratch criteria are unknown.",
            ],
            "sources": [
                source("04-worker-returns/batch-B24-evidence_batch_01.md", "A-231 — ValSof Bakery"),
                source("04-worker-returns/repair-R24-evidence_batch_01.md", "A-231"),
                source("06-user-ground-truth.md", "A-231 — ValSof Bakery"),
            ],
        }
    )

    decisions["generated_at"] = "2026-07-23T00:00:00-06:00"
    decisions["source_artifacts"]["user_ground_truth"] = "06-user-ground-truth.md"
    DECISIONS_PATH.write_text(json.dumps(decisions, indent=2, ensure_ascii=False) + "\n")

    projection = json.loads(PROJECTION_PATH.read_text())
    projection["theme"]["rating_floor"] = 4.3
    for population in ("practical", "audit", "omitted"):
        for row in projection[population]:
            row["summary"] = (
                row["summary"]
                .replace("pÃ¢tisserie", "pâtisserie")
                .replace("Ã©clair", "éclair")
                .replace("cafÃ©", "café")
            )
    rows = {}
    for population in ("practical", "audit", "omitted"):
        for row in projection[population]:
            rows[row["id"]] = (population, row)

    status_facet = next(facet for facet in projection["facets"] if facet["key"] == "status")
    if not any(value["value"] == "partial" for value in status_facet["values"]):
        status_facet["values"].insert(
            1, {"value": "partial", "label": "Scratch evidence (partial)"}
        )

    updates = {
        "A-012": {
            "location_label": "Salt Lake City",
            "summary": "Scratch bagels are confirmed by user ground truth; the run also found in-house cured lox and sauces. Rating and most rubric criteria remain unknown.",
            "facet_values": {
                "region": ["salt-lake-city"],
                "access": ["walk-in"],
                "occasion": [],
                "status": ["partial"],
                "specialty": ["bagels-savory"],
            },
        },
        "A-013": {
            "location_label": "Heber City",
            "summary": "The official site confirms scratch-made schmears but says the bagel dough arrives from New York. The partial score covers schmears only; the aggregate rating remains unavailable.",
            "facet_values": {
                "region": ["heber-midway"],
                "access": ["walk-in"],
                "occasion": [],
                "status": ["partial"],
                "specialty": ["bagels-savory"],
            },
        },
        "A-231": {
            "location_label": "Sandy",
            "summary": "Low-confidence evidence supports house fillings only. Dough, bread, puff pastry, and lamination remain unknown; Restaurantji reported 4.4/5 from 141 ratings.",
            "facet_values": {
                "region": ["salt-lake-valley"],
                "access": ["walk-in"],
                "occasion": [],
                "status": ["partial"],
                "specialty": ["regional-specialty"],
            },
        },
    }
    for record_id, changes in updates.items():
        old_population, row = rows[record_id]
        projection[old_population] = [
            candidate for candidate in projection[old_population] if candidate["id"] != record_id
        ]
        canonical = by_id[record_id]
        row.update(
            {
                "name": canonical["name"],
                "address": canonical["address"],
                "coordinates": canonical["coordinates"],
                **changes,
            }
        )
        projection["practical"].append(row)

    projection["source"]["decision_hash"] = canonical_hash(decisions)
    projection["counts"] = {
        "practical": len(projection["practical"]),
        "audit": len(projection["audit"]),
        "omitted": len(projection["omitted"]),
        "mapped": sum(
            row["coordinates"] is not None for row in projection["practical"]
        ),
    }
    PROJECTION_PATH.write_text(
        json.dumps(projection, indent=2, ensure_ascii=False) + "\n"
    )

    print(
        json.dumps(
            {
                "updated": ["A-012", "A-013", "A-231"],
                "counts": projection["counts"],
                "decision_hash": projection["source"]["decision_hash"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
