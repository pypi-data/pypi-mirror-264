from datetime import datetime

from typing import Dict

from pydantic import BaseModel, Field, Extra, root_validator

from chaiverse.config import ELO_BASE_SUBMISSION_ID, ELO_BASE_RATING
from chaiverse.lib.elo import get_elo_ratings, get_mle_elo_scores
from chaiverse.lib.now import utcnow


class PreferenceSummary(BaseModel):
    '''
    wins_dict[player_a,player_b] is a sparse matrix of win count for player a vs player b
    elo_scores[player] must include all players, and the value is last known best elo score
    '''
    wins_dict: Dict[str, Dict[str, int]] = Field(default={})
    elo_scores: Dict[str, float] = Field(default={})

    @root_validator
    def validate_elo_scores(cls, value):
        wins_dict = value.get('wins_dict')
        initial_elo_scores = value.get('elo_scores')
        value['elo_scores'] = get_mle_elo_scores(initial_elo_scores, wins_dict)
        return value

    def wins(self, a_id: str, b_id: str):
        wins = self.wins_dict.get(a_id, {}).get(b_id, 0)
        return wins
    
    def rounds(self, a_id: str, b_id: str):
        return self.wins(a_id, b_id) + self.wins(b_id, a_id)

    def win_rate(self, a_id: str, b_id: str):
        return self.wins(a_id, b_id) / self.rounds(a_id, b_id)
    
    def calculate_elo_ratings(self, elo_base_id:str=ELO_BASE_SUBMISSION_ID, elo_base_rating:float=ELO_BASE_RATING):
        elo_base_score = self.elo_scores[elo_base_id]
        elo_ratings = get_elo_ratings(self.elo_scores, elo_base_score, elo_base_rating)
        return elo_ratings


class PreferenceSummaries(BaseModel, extra=Extra.allow):
    summaries: Dict[str, PreferenceSummary] = Field(default={})
    created_at: datetime = Field(default_factory=utcnow)  
