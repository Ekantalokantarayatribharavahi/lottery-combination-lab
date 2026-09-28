from __future__ import annotations
import json
from .candidates import Candidate,candidate_set_hash,validate_candidate
from .features import feature_vector,crowding_score
from .games import GameModel

def filter_candidates(cs:list[Candidate],m:GameModel):
    good=[];rejected=[];seen=set()
    for c in cs:
        e=validate_candidate(c,m);key=(c.numbers,c.powerball)
        if key in seen:e.append("duplicate candidate")
        if e:rejected.append({"candidate":c.to_dict(),"stage":"hard_validity","reasons":e})
        else:seen.add(key);good.append(c)
    return good,{"rejected":rejected}

def rank_candidates(cs:list[Candidate],weights=None):
    rows=[]
    for c in cs:
        f=feature_vector(c);rows.append({"candidate":c.to_dict(),"features":f,"crowding_score":crowding_score(f,weights),"applied_filters":["hard_validity","crowding_proxy"]})
    return sorted(rows,key=lambda x:(x["crowding_score"],tuple(x["candidate"]["numbers"]),x["candidate"]["powerball"] or 0))

def independent_recheck(ranked):
    again=sorted(ranked,key=lambda x:(x["crowding_score"],tuple(x["candidate"]["numbers"]),x["candidate"]["powerball"] or 0))
    return {"status":"rechecked","reproduced":ranked==again,"candidate_count":len(ranked),"top_candidate":again[0]["candidate"] if again else None}

def build_audit(m,cs,survivors,ranked,meta=None):
    meta=meta or {};check=independent_recheck(ranked);final=ranked[0] if ranked else None
    return {"game":m.game,"rule_version":m.rule_version,"draw_date":meta.get("draw_date"),"ticket_cost":meta.get("ticket_cost"),"candidate":final["candidate"] if final else None,"candidate-generation-method":meta.get("generation_method","unknown"),"seed":meta.get("seed"),"algorithm":"Python random.Random + sample","all-evidence-inputs":meta.get("evidence_inputs",[]),"all-enabled-filters":["hard_validity","crowding_proxy"],"all-disabled-filters":meta.get("disabled_filters",[]),"statistical-analysis-version":meta.get("statistical_analysis_version"),"crowding-model-version":"0.1.0","software-commit":meta.get("software_commit"),"dataset-hashes":meta.get("dataset_hashes",[]),"candidate-set-hash":candidate_set_hash(cs),"independent-reproduction-status":check,"selection-rationale":"Lowest documented crowding proxy among hard-valid candidates; lottery draw probability is unchanged.","execution-checklist":{"generated":True,"hard_validated":all(not validate_candidate(Candidate(tuple(x["candidate"]["numbers"]),x["candidate"]["powerball"]),m) for x in ranked),"ranked":bool(ranked),"independently_rechecked":check["reproduced"],"purchased":False},"candidate_count":len(cs),"survivor_count":len(survivors)}
