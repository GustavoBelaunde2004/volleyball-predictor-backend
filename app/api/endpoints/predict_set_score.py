from fastapi import APIRouter, HTTPException
from schemas.prediction import SetScorePredictionRequest, SetScorePredictionResponse
import pandas as pd
from app.models.model_loader import load_home_set_score_model, load_away_set_score_model

router = APIRouter()

# Load the models and team stats
home_set_score_model = load_home_set_score_model()
away_set_score_model = load_away_set_score_model()
team_stats = pd.read_csv("team_stats.csv")

@router.post("/set-score", response_model=SetScorePredictionResponse)
async def predict_set_score(request: SetScorePredictionRequest):
    # Get home and away team stats
    home_stats = team_stats[team_stats['Team'] == request.home_team]
    away_stats = team_stats[team_stats['Team'] == request.away_team]

    if home_stats.empty or away_stats.empty:
        raise HTTPException(status_code=404, detail="One or both teams not found")

    features = [[request.set_number, home_stats['avg_points'].iloc[0], 
                 away_stats['avg_points'].iloc[0]]]
    
    # Predict scores for the specified set number
    home_set_score = home_set_score_model.predict(features)[0]
    away_set_score = away_set_score_model.predict(features)[0]
    
    return {"home_set_score": int(home_set_score), "away_set_score": int(away_set_score)}
