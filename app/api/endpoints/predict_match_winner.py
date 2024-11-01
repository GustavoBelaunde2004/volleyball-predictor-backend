# app/api/endpoints/predict_match_winner.py
from fastapi import APIRouter, HTTPException
from app.schemas.prediction import MatchPredictionRequest, MatchPredictionResponse
from app.models.model_loader import load_match_winner_model
import pandas as pd

# Initialize the router
router = APIRouter()

# Load the model and team stats
model = load_match_winner_model()
team_stats = pd.read_csv('C:\GUSTAVO\Projects\\volley\\volley-backend\\team_stats.csv')  # Precomputed team stats

@router.post("/match-winner", response_model=MatchPredictionResponse)
async def predict_match_winner(request: MatchPredictionRequest):
    # Get home and away team stats
    home_stats = team_stats[team_stats['Team'] == request.home_team].iloc[0]
    away_stats = team_stats[team_stats['Team'] == request.away_team].iloc[0]

    if home_stats.empty or away_stats.empty:
        raise HTTPException(status_code=404, detail="One or both teams not found")

    # Extract features
    features = [[
        home_stats['avg_points'], home_stats['win_rate'],
        away_stats['avg_points'], away_stats['win_rate']
    ]]
    
    # Make a prediction
    prediction = model.predict(features)
    predicted_winner = request.home_team if prediction[0] == 1 else request.away_team
    
    return {"prediction": predicted_winner}
