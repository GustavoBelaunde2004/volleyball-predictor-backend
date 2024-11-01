from fastapi import APIRouter, HTTPException
from app.schemas.prediction import SetOutcomePredictionRequest, SetOutcomePredictionResponse
import pandas as pd
from app.models.model_loader import load_home_sets_won_model, load_away_sets_won_model

router = APIRouter()

# Load the models and team stats
home_sets_model = load_home_sets_won_model()
away_sets_model = load_away_sets_won_model()
team_stats = pd.read_csv("C:\GUSTAVO\Projects\\volley\\volley-backend\\team_stats.csv")

@router.post("/set-outcome", response_model=SetOutcomePredictionResponse)
async def predict_set_outcome(request: SetOutcomePredictionRequest):
    # Get home and away team stats
    home_stats = team_stats[team_stats['Team'] == request.home_team]
    away_stats = team_stats[team_stats['Team'] == request.away_team]

    if home_stats.empty or away_stats.empty:
        raise HTTPException(status_code=404, detail="One or both teams not found")

    # Extract total scores (you might want to calculate these based on historical data)
    # For this example, using the average points to simulate Home and Away scores
    home_score = home_stats['avg_points'].iloc[0]
    away_score = away_stats['avg_points'].iloc[0]
    
    # Prepare features for prediction
    features = [[home_score, away_score]]
    
    # Predict sets won by each team
    home_sets_won = home_sets_model.predict(features)[0]
    away_sets_won = away_sets_model.predict(features)[0]
    
    return {
        "home_sets_won": int(home_sets_won),
        "away_sets_won": int(away_sets_won)
    }