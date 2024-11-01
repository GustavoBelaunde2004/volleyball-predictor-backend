# app/schemas/prediction.py
from pydantic import BaseModel

class MatchPredictionRequest(BaseModel):
    home_team: str
    away_team: str

class MatchPredictionResponse(BaseModel):
    prediction: str  # Predicted winning team

class SetOutcomePredictionRequest(BaseModel):
    home_team: str
    away_team: str

class SetOutcomePredictionResponse(BaseModel):
    home_sets_won: int
    away_sets_won: int

class SetScorePredictionRequest(BaseModel):
    home_team: str
    away_team: str
    set_number: int

class SetScorePredictionResponse(BaseModel):
    home_set_score: int
    away_set_score: int

class MatchDetailsResponse(BaseModel):
    winner: str
    home_sets_won: int
    away_sets_won: int
    sets: dict  # Adjust as necessary for your specific structure