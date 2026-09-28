from dataclasses import dataclass

@dataclass(frozen=True)
class GameModel:
    game:str
    rule_version:str
    main_count:int
    main_min:int
    main_max:int
    powerball_min:int|None=None
    powerball_max:int|None=None

GAMES={
 "lotto":GameModel("lotto","lotto-current",6,1,52),
 "powerball":GameModel("powerball","powerball-current",5,1,50,1,20),
 "daily_lotto":GameModel("daily_lotto","daily_lotto-current",5,1,36),
}

def resolve_game(game:str)->GameModel:
    try:return GAMES[game]
    except KeyError as e:raise ValueError(f"unknown game: {game}") from e
