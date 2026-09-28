from collections import Counter
from .candidates import Candidate

FEATURE_NAMES=("date_density","repeat_digit_score","consecutive_score","sequence_score","visual_pattern_score","low_range_density","symmetry_score","human_salience_score")

def feature_vector(c:Candidate)->dict[str,float]:
    n=sorted(c.numbers);k=len(n);dd=sum(x<=31 for x in n)/k
    rep=sum(max(v-1,0) for v in Counter(str(x) for x in n).values())/max(1,k-1)
    con=sum(b==a+1 for a,b in zip(n,n[1:]))/max(1,k-1);d=[b-a for a,b in zip(n,n[1:])]
    ar=float(len(d)>=2 and len(set(d))==1)
    sym=float(all(n[i]+n[-i-1]==n[0]+n[-1] for i in range(k//2)))
    salient=sum(x in {7,8,11,13,18,21,23,24,27,28,31} for x in n)/k
    visual=float(ar or (len(set(d))<=2 and max(d,default=0)<=10))
    return {"date_density":dd,"repeat_digit_score":min(1,rep),"consecutive_score":con,"sequence_score":ar,"visual_pattern_score":visual,"low_range_density":dd,"symmetry_score":sym,"human_salience_score":min(1,.6*dd+.4*salient),"sum":sum(n),"odd_count":sum(x%2 for x in n),"low_count":sum(x<=31 for x in n),"high_count":sum(x>=32 for x in n),"consecutive_pairs":sum(b==a+1 for a,b in zip(n,n[1:]))}

def crowding_score(f:dict[str,float],weights:dict[str,float]|None=None)->float:
    w=weights or {k:1.0 for k in FEATURE_NAMES}; den=sum(abs(x) for x in w.values())
    return 0 if den==0 else sum(f[k]*w[k] for k in w)/den
