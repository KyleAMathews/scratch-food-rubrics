#!/usr/bin/env python3
"""Validate and deterministically generate a Scratch Food interactive explorer."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

GENERATOR_VERSION = "1.0"
SCHEMA_VERSION = "1.0"
PAYLOAD_MARKER = "__INTERACTIVE_RESULTS_PAYLOAD__"
CRITERION_MAXIMA = {
    "restaurant": {"base_prep": 25, "production": 40, "coherence": 20, "operator_format": 15},
    "bakery": {"core_craft": 30, "input_sourcing": 20, "breadth_capacity": 20, "bake_cadence": 20, "operator_format": 10},
}


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def canonical_json_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def sha256_uri(value):
    return "sha256:" + hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def sha256_file(path):
    return "sha256:" + hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _finite_errors(value, path="$"):
    errors=[]
    if isinstance(value, float) and not math.isfinite(value):
        errors.append(f"{path}: number must be finite")
    elif isinstance(value, dict):
        for key, child in value.items(): errors += _finite_errors(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value): errors += _finite_errors(child, f"{path}[{index}]")
    return errors


def _safe_relative(path):
    if not isinstance(path, str) or not path: return False
    p=Path(path)
    return not p.is_absolute() and ".." not in p.parts


def _valid_coordinates(coords):
    return coords is None or (isinstance(coords,dict) and set(coords)=={"lat","lng"} and
        all(isinstance(coords[k],(int,float)) and not isinstance(coords[k],bool) and math.isfinite(coords[k]) for k in ("lat","lng")) and
        -90 <= coords["lat"] <= 90 and -180 <= coords["lng"] <= 180)


def validate_decisions(value, run_dir=None):
    errors=_finite_errors(value)
    if not isinstance(value,dict): return errors+["decision ledger must be an object"]
    for key in ("schema_version","category","run_id","generated_at","source_artifacts","records"):
        if key not in value: errors.append(f"missing decision field: {key}")
    if value.get("schema_version") != SCHEMA_VERSION: errors.append("unsupported decision schema_version")
    if value.get("category") not in ("bakery","restaurant"): errors.append("decision category must be bakery or restaurant")
    records=value.get("records")
    if not isinstance(records,list) or not records: errors.append("decision records must be a nonempty array"); return errors
    ids=[]
    required=("id","name","aliases","branch","address","coordinates","disposition","reason","score","rating","tier","ranking_eligible","occasions","rare_finds","access","merge_target","rationale","sources")
    for i,row in enumerate(records):
        if not isinstance(row,dict): errors.append(f"record {i} must be object"); continue
        for key in required:
            if key not in row: errors.append(f"record {i} missing {key}")
        rid=row.get("id")
        if not isinstance(rid,str) or not rid: errors.append(f"record {i} has invalid id")
        else: ids.append(rid)
        if not isinstance(row.get("name"),str) or not row.get("name"): errors.append(f"record {rid} has invalid name")
        if not _valid_coordinates(row.get("coordinates")): errors.append(f"record {rid} has invalid coordinate")
        score=row.get("score")
        if score is not None:
            if not isinstance(score,dict): errors.append(f"record {rid} score must be object or null")
            else:
                state=score.get("state","complete")
                if state not in ("complete","partial"): errors.append(f"record {rid} score state must be complete or partial")
                if score.get("provenance") not in ("documented","estimated","mixed","user-ground-truth","calibrated","provisional-secondary"):
                    errors.append(f"record {rid} score provenance is invalid")
                if state=="partial":
                    if any(score.get(key) is not None for key in ("s","i","g")):
                        errors.append(f"record {rid} partial score s/i/g must be null")
                    for key in ("s_earned","s_observed_possible","s_coverage"):
                        n=score.get(key)
                        if not isinstance(n,(int,float)) or isinstance(n,bool) or not math.isfinite(n):
                            errors.append(f"record {rid} partial score {key} must be finite")
                    possible=score.get("s_observed_possible")
                    coverage=score.get("s_coverage")
                    earned=score.get("s_earned")
                    if isinstance(earned,(int,float)) and not isinstance(earned,bool) and not 0 < earned <= 100:
                        errors.append(f"record {rid} partial earned score out of range")
                    if isinstance(possible,(int,float)) and not isinstance(possible,bool) and not 0 < possible <= 100:
                        errors.append(f"record {rid} partial observed possible out of range")
                    if isinstance(coverage,(int,float)) and not isinstance(coverage,bool) and not 0 < coverage <= 1:
                        errors.append(f"record {rid} partial coverage out of range")
                    if isinstance(possible,(int,float)) and isinstance(coverage,(int,float)) and abs(coverage-possible/100)>0.0001:
                        errors.append(f"record {rid} partial coverage does not match observed possible")
                    if score.get("confidence") not in ("high","medium","low"):
                        errors.append(f"record {rid} partial confidence is invalid")
                    criteria=score.get("criteria")
                    maxima=CRITERION_MAXIMA.get(value.get("category"),{})
                    if not isinstance(criteria,dict) or set(criteria)!=set(maxima):
                        errors.append(f"record {rid} partial criteria do not match {value.get('category')} rubric")
                    else:
                        observed_possible=0
                        observed_earned=0
                        for key,maximum in maxima.items():
                            n=criteria[key]
                            if n is None: continue
                            if not isinstance(n,(int,float)) or isinstance(n,bool) or not math.isfinite(n) or not 0 <= n <= maximum:
                                errors.append(f"record {rid} partial criterion {key} out of range")
                                continue
                            observed_possible+=maximum
                            observed_earned+=n
                        if possible != observed_possible: errors.append(f"record {rid} partial observed possible does not match criteria")
                        if earned != observed_earned: errors.append(f"record {rid} partial earned score does not match criteria")
                    if row.get("ranking_eligible"): errors.append(f"record {rid} partial score cannot be ranking eligible")
                else:
                    for key in ("s","i","g"):
                        n=score.get(key)
                        if not isinstance(n,(int,float)) or isinstance(n,bool) or not math.isfinite(n) or not 0 <= n <= 100: errors.append(f"record {rid} score {key} out of range")
        if row.get("ranking_eligible") and score is None: errors.append(f"record {rid} ranking eligible without score")
        rating=row.get("rating")
        if rating is not None:
            rv=rating.get("value") if isinstance(rating,dict) else None
            if rv is not None and (not isinstance(rv,(int,float)) or isinstance(rv,bool) or not 0 <= rv <= 5): errors.append(f"record {rid} rating out of range")
        sources=row.get("sources",[])
        if not isinstance(sources,list): errors.append(f"record {rid} sources must be array")
        else:
            for source in sources:
                artifact=source.get("artifact") if isinstance(source,dict) else None
                if not _safe_relative(artifact): errors.append(f"record {rid} source artifact must be safe relative path")
                elif run_dir is not None and not (Path(run_dir)/artifact).exists(): errors.append(f"record {rid} source artifact missing: {artifact}")
    seen=set()
    for rid in ids:
        if rid in seen: errors.append(f"duplicate decision id: {rid}")
        seen.add(rid)
    known=set(ids)
    for row in records:
        target=row.get("merge_target") if isinstance(row,dict) else None
        if target is not None and target not in known: errors.append(f"record {row.get('id')} merge target does not resolve: {target}")
        if row.get("disposition")=="canonical-duplicate" and not target: errors.append(f"record {row.get('id')} canonical duplicate requires merge target")
    arts=value.get("source_artifacts")
    if not isinstance(arts,dict): errors.append("source_artifacts must be object")
    else:
        for key in ("manifest","evidence"):
            if not _safe_relative(arts.get(key)): errors.append(f"source_artifacts.{key} must be safe relative path")
    return errors


def validate_projection(value, decisions):
    errors=_finite_errors(value)
    if not isinstance(value,dict): return errors+["projection must be an object"]
    for key in ("schema_version","source","snapshots","title","scope","facets","theme","counts","practical","audit","omitted"):
        if key not in value: errors.append(f"missing projection field: {key}")
    if value.get("schema_version") != SCHEMA_VERSION: errors.append("unsupported projection schema_version")
    source=value.get("source",{})
    if source.get("run_id") != decisions.get("run_id"): errors.append("projection run_id does not match decisions")
    if source.get("category") != decisions.get("category"): errors.append("projection category does not match decisions")
    if source.get("decision_hash") != sha256_uri(decisions): errors.append("projection decision_hash does not match decisions")
    decision_by_id={r.get("id"):r for r in decisions.get("records",[]) if isinstance(r,dict)}
    facets=value.get("facets",[])
    declared={}
    if not isinstance(facets,list): errors.append("facets must be array"); facets=[]
    for facet in facets:
        key=facet.get("key") if isinstance(facet,dict) else None
        if not key: errors.append("facet missing key"); continue
        if key in declared: errors.append(f"duplicate facet key: {key}")
        declared[key]={v.get("value") for v in facet.get("values",[]) if isinstance(v,dict)}
    practical=value.get("practical",[]); audit=value.get("audit",[]); omitted=value.get("omitted",[])
    if not all(isinstance(x,list) for x in (practical,audit,omitted)): errors.append("projection populations must be arrays"); return errors
    pids=[r.get("id") for r in practical if isinstance(r,dict)]; aids=[r.get("id") for r in audit if isinstance(r,dict)]; oids=[r.get("id") for r in omitted if isinstance(r,dict)]
    overlap=(set(pids)&set(aids)) | (set(pids)&set(oids)) | (set(aids)&set(oids))
    if overlap: errors.append("projection populations overlap: "+", ".join(sorted(overlap)))
    all_ids=pids+aids+oids
    if len(all_ids)!=len(set(all_ids)): errors.append("duplicate projected id")
    missing=set(decision_by_id)-set(all_ids); extra=set(all_ids)-set(decision_by_id)
    if missing: errors.append("canonical IDs silently omitted: "+", ".join(sorted(missing)))
    if extra: errors.append("projection references unknown decision IDs: "+", ".join(sorted(extra)))
    for mode,rows in (("practical",practical),("audit",audit)):
        for row in rows:
            rid=row.get("id"); canonical=decision_by_id.get(rid)
            if canonical is None: continue
            for key in ("name","address","coordinates"):
                if row.get(key) != canonical.get(key): errors.append(f"{mode} {rid} {key} differs from canonical decision")
            if not _valid_coordinates(row.get("coordinates")): errors.append(f"{mode} {rid} has invalid coordinate")
            if mode=="practical" and canonical.get("access") is None: errors.append(f"practical {rid} requires explicit current access")
            fv=row.get("facet_values",{})
            if not isinstance(fv,dict): errors.append(f"{mode} {rid} facet_values must be object"); continue
            for key,vals in fv.items():
                if key not in declared: errors.append(f"{mode} {rid} uses undeclared facet: {key}"); continue
                for item in vals:
                    if item not in declared[key]: errors.append(f"{mode} {rid} undeclared facet value: {key}={item}")
    actual={"practical":len(practical),"audit":len(audit),"omitted":len(omitted),"mapped":sum(1 for r in practical if r.get("coordinates") is not None)}
    counts=value.get("counts",{})
    for key,n in actual.items():
        if counts.get(key)!=n: errors.append(f"{key} count mismatch: declared {counts.get(key)}, actual {n}")
    return errors


def _maps_url(name,address,scope):
    location = address or scope
    if not location: return None
    return "https://www.google.com/maps/search/?"+urlencode({"api":"1","query":f"{name}, {location}"})


def build_payload(decisions,projection):
    by_id={r["id"]:r for r in decisions["records"]}
    def join(row,mode):
        d=by_id[row["id"]]
        return {"id":d["id"],"name":d["name"],"address":d["address"],"coordinates":d["coordinates"],"location_label":row["location_label"],"summary":row["summary"],"facet_values":row["facet_values"],"disposition":d["disposition"],"reason":d["reason"],"score":d["score"],"rating":d["rating"],"tier":d["tier"],"ranking_eligible":d["ranking_eligible"],"occasions":d["occasions"],"rare_finds":d["rare_finds"],"access":d["access"],"map_url":_maps_url(d["name"],d["address"],projection["scope"]),"map_action":("Directions" if d["address"] and mode=="practical" else "Find on Google Maps")}
    return {"meta":{"run_id":decisions["run_id"],"title":projection["title"],"scope":projection["scope"],"category":decisions["category"],"snapshots":projection["snapshots"],"counts":projection["counts"]},"facets":projection["facets"],"theme":projection["theme"],"practical":[join(r,"practical") for r in projection["practical"]],"audit":[join(r,"audit") for r in projection["audit"]]}


def _safe_payload_json(payload):
    raw=canonical_json_bytes(payload).decode("utf-8")
    return raw.replace("&","\\u0026").replace("<","\\u003c").replace(">","\\u003e").replace("\u2028","\\u2028").replace("\u2029","\\u2029")


def render(template,payload):
    if template.count(PAYLOAD_MARKER)!=1: raise ValueError(f"template must contain {PAYLOAD_MARKER} exactly once")
    return template.replace(PAYLOAD_MARKER,_safe_payload_json(payload))


def _atomic_write(path,data):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    temp=None
    try:
        with tempfile.NamedTemporaryFile("wb",delete=False,dir=path.parent,prefix=f".{path.name}.") as f:
            temp=Path(f.name); f.write(data); f.flush(); os.fsync(f.fileno())
        os.replace(temp,path); temp=None
    finally:
        if temp and temp.exists(): temp.unlink()


def generate(decisions_path,projection_path,template_path,output_path,validation_output,generated_at):
    decisions=load_json(decisions_path); projection=load_json(projection_path)
    errors=validate_decisions(decisions,Path(decisions_path).parent)+validate_projection(projection,decisions)
    if errors: raise ValueError("validation failed:\n- "+"\n- ".join(errors))
    template=Path(template_path).read_text(encoding="utf-8")
    payload=build_payload(decisions,projection)
    output=render(template,payload).encode("utf-8")
    report={"schema_version":"1.0","generator_version":GENERATOR_VERSION,"generated_at":generated_at,"status":"static-pass","hashes":{"decisions":sha256_uri(decisions),"projection":sha256_uri(projection),"template":sha256_file(template_path),"output":"sha256:"+hashlib.sha256(output).hexdigest()},"expected_counts":projection["counts"],"static_checks":{"decision_validation":True,"projection_validation":True,"safe_embedding":True,"atomic_write":True},"browser":None}
    _atomic_write(output_path,output)
    _atomic_write(validation_output,canonical_json_bytes(report)+b"\n")
    return report


def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument("--decisions",required=True); parser.add_argument("--projection",required=True)
    parser.add_argument("--template",required=True); parser.add_argument("--output",required=True)
    parser.add_argument("--validation-output",required=True); parser.add_argument("--generated-at",required=True)
    args=parser.parse_args(argv)
    try: generate(args.decisions,args.projection,args.template,args.output,args.validation_output,args.generated_at)
    except Exception as exc:
        parser.exit(1,f"error: {exc}\n")

if __name__=="__main__": main()
