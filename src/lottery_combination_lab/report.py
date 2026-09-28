import json
from pathlib import Path

def write_audit(audit:dict,out:Path):
    out.mkdir(parents=True,exist_ok=True);jp=out/"FINAL_TICKET_AUDIT.json";mp=out/"FINAL_TICKET_AUDIT.md"
    jp.write_text(json.dumps(audit,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    lines=["# FINAL TICKET AUDIT","",f"- Game: `{audit['game']}`",f"- Rule version: `{audit['rule_version']}`",f"- Candidate: `{audit['candidate']}`",f"- Generation method: `{audit['candidate-generation-method']}`",f"- Independent reproduction: `{audit['independent-reproduction-status']['reproduced']}`","","## Selection rationale",audit["selection-rationale"],"","## Execution checklist","```json",json.dumps(audit["execution-checklist"],indent=2),"```"]
    mp.write_text("\n".join(lines)+"\n",encoding="utf-8");return jp,mp
