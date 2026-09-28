from __future__ import annotations
import argparse,json
from pathlib import Path
from .games import resolve_game
from .candidates import Candidate,generate_candidates
from .pipeline import filter_candidates,rank_candidates,build_audit
from .report import write_audit

def load(path):
    x=json.loads(path.read_text(encoding="utf-8"));return [Candidate(tuple(i["numbers"]),i.get("powerball"),i.get("generation_method","unknown")) for i in x.get("candidates",x)]
def save(path,cs):path.write_text(json.dumps({"candidates":[c.to_dict() for c in cs]},indent=2)+"\n",encoding="utf-8")
def main():
    p=argparse.ArgumentParser(prog="combination-lab");s=p.add_subparsers(dest="cmd",required=True)
    g=s.add_parser("generate");g.add_argument("--game",required=True,choices=["lotto","powerball","daily_lotto"]);g.add_argument("--count",type=int,required=True);g.add_argument("--seed",type=int,default=42);g.add_argument("--output",type=Path,default=Path("candidates.json"))
    for n in ("filter","audit","export-final"):
        q=s.add_parser(n);q.add_argument("--input",type=Path,required=True);q.add_argument("--game",required=True,choices=["lotto","powerball","daily_lotto"])
        if n!="export-final":q.add_argument("--output",type=Path,default=Path("reports"))
    a=p.parse_args()
    if a.cmd=="generate":save(a.output,generate_candidates(resolve_game(a.game),a.count,a.seed));print(a.output);return 0
    cs=load(a.input);m=resolve_game(a.game);sv,_=filter_candidates(cs,m)
    if a.cmd=="filter":save(a.output,sv);print(a.output);return 0
    ranked=rank_candidates(sv);audit=build_audit(m,cs,sv,ranked,{"generation_method":cs[0].generation_method if cs else "unknown","seed":42})
    if a.cmd=="audit":print(*write_audit(audit,a.output),sep="\n")
    else:print(json.dumps(audit["candidate"],sort_keys=True) if audit["candidate"] else "no final candidate")
    return 0
if __name__=="__main__":raise SystemExit(main())
