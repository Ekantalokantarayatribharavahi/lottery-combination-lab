from lottery_combination_lab.games import resolve_game
from lottery_combination_lab.candidates import generate_candidates,validate_candidate
from lottery_combination_lab.features import feature_vector
from lottery_combination_lab.pipeline import filter_candidates,rank_candidates,independent_recheck

def test_generation_and_validity():
 m=resolve_game("lotto");c=generate_candidates(m,50,2);assert len(c)==50;assert all(not validate_candidate(x,m) for x in c)
def test_deterministic_features():
 m=resolve_game("lotto");c=generate_candidates(m,1,5)[0];assert feature_vector(c)==feature_vector(c)
def test_recheck():
 m=resolve_game("lotto");c=generate_candidates(m,20,4);s,_=filter_candidates(c,m);r=rank_candidates(s);assert independent_recheck(r)["reproduced"]
