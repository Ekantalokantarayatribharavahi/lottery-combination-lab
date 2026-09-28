from __future__ import annotations
from dataclasses import dataclass
import hashlib,json,random
from .games import GameModel

@dataclass(frozen=True)
class Candidate:
    numbers:tuple[int,...]
    powerball:int|None=None
    generation_method:str="unknown"
    def to_dict(self):
        return {"numbers":list(self.numbers),"powerball":self.powerball,"generation_method":self.generation_method}

def validate_candidate(c:Candidate,m:GameModel)->list[str]:
    e=[]
    if len(c.numbers)!=m.main_count:e.append("wrong number count")
    if len(set(c.numbers))!=len(c.numbers):e.append("duplicate main number")
    if any(n<m.main_min or n>m.main_max for n in c.numbers):e.append("main number out of range")
    if m.powerball_min is None and c.powerball is not None:e.append("unexpected powerball")
    if m.powerball_min is not None:
        if c.powerball is None:e.append("missing powerball")
        elif not m.powerball_min<=c.powerball<=m.powerball_max:e.append("powerball out of range")
    return e

def generate_candidates(m:GameModel,count:int,seed:int)->list[Candidate]:
    if count<1:raise ValueError("count must be positive")
    r=random.Random(seed);seen=set();out=[]
    while len(out)<count:
        nums=tuple(sorted(r.sample(range(m.main_min,m.main_max+1),m.main_count)))
        pb=r.randint(m.powerball_min,m.powerball_max) if m.powerball_min is not None else None
        key=(nums,pb)
        if key not in seen:seen.add(key);out.append(Candidate(nums,pb,"seeded-random"))
    return out

def candidate_set_hash(cs):
    return hashlib.sha256(json.dumps([c.to_dict() for c in cs],sort_keys=True,separators=(",",":" )).encode()).hexdigest()

def overlap(a:Candidate,b:Candidate)->int:return len(set(a.numbers)&set(b.numbers))
