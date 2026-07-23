#!/usr/bin/env python3
"""Repair canonical identity fields and the interactive projection after v8.14 rescore."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


RUN_DIR = Path(__file__).resolve().parent
DECISIONS_PATH = RUN_DIR / "06-decisions.json"
PROJECTION_PATH = RUN_DIR / "interactive-results-projection.json"
CANDIDATES_PATH = RUN_DIR / "02-source-data/canonical-candidates.json"
REPORT_PATH = RUN_DIR / "06-interactive-repair-validation.json"


def canonical_hash(value: object) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def main() -> None:
    decisions = json.loads(DECISIONS_PATH.read_text())
    candidates_doc = json.loads(CANDIDATES_PATH.read_text())
    candidates = {
        row["candidate_id"]: row for row in candidates_doc["candidates"]
    }

    missing_candidates = []
    matched_candidates = 0
    for record in decisions["records"]:
        candidate = candidates.get(record["id"])
        if candidate is None:
            missing_candidates.append(record["id"])
        else:
            matched_candidates += 1
            point = candidate.get("point")
            address = candidate.get("address") or None
            coordinates = (
                {"lat": point["lat"], "lng": point["lon"]} if point else None
            )
            aliases = list(
                dict.fromkeys(record.get("aliases", []) + candidate.get("aliases", []))
            )
            record["address"] = address
            record["coordinates"] = coordinates
            record["aliases"] = aliases

        for source in record["sources"]:
            if source["artifact"] == "06-decisions.md":
                source["artifact"] = "06-decisions.legacy-v8.10.md"

    decisions["generated_at"] = "2026-07-21T00:00:00-06:00"
    decisions["source_artifacts"]["legacy_decisions"] = (
        "06-decisions.legacy-v8.10.json"
    )
    DECISIONS_PATH.write_text(
        json.dumps(decisions, indent=2, ensure_ascii=False) + "\n"
    )

    projection = json.loads(PROJECTION_PATH.read_text())
    projection["theme"]["rating_floor"] = 4.0
    by_id = {record["id"]: record for record in decisions["records"]}
    projected_ids = []
    for population in ("practical", "audit", "omitted"):
        for row in projection[population]:
            canonical = by_id[row["id"]]
            row["name"] = canonical["name"]
            row["address"] = canonical["address"]
            row["coordinates"] = canonical["coordinates"]
            projected_ids.append(row["id"])

    projection["source"]["run_id"] = decisions["run_id"]
    projection["source"]["category"] = decisions["category"]
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

    decision_ids = {record["id"] for record in decisions["records"]}
    normalized_legacy_sources = sum(
        source["artifact"] == "06-decisions.legacy-v8.10.md"
        for record in decisions["records"]
        for source in record["sources"]
    )
    report = {
        "schema_contract": "restaurant v8.14 identity and projection repair",
        "decision_population": len(decisions["records"]),
        "identities_resolved_from_candidate_source": matched_candidates,
        "normalized_legacy_source_references": normalized_legacy_sources,
        "candidate_ids_missing_from_identity_source": sorted(missing_candidates),
        "projection_population": len(projected_ids),
        "projection_ids_match_decisions": set(projected_ids) == decision_ids,
        "projection_counts": projection["counts"],
        "decision_hash": projection["source"]["decision_hash"],
        "passed": len(projected_ids) == len(set(projected_ids)) == len(decision_ids)
        and set(projected_ids) == decision_ids,
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
