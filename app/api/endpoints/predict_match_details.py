from fastapi import APIRouter, HTTPException
from app.schemas.prediction import MatchPredictionRequest, MatchDetailsResponse
import pandas as pd
from app.models.model_loader import (
    load_match_winner_model,
    load_home_sets_won_model,
    load_away_sets_won_model,
    load_home_set_score_model,
    load_away_set_score_model
)
import random


router = APIRouter()

# Load the models and team stats
match_winner_model = load_match_winner_model()
home_sets_model = load_home_sets_won_model()
away_sets_model = load_away_sets_won_model()
home_set_score_model = load_home_set_score_model()
away_set_score_model = load_away_set_score_model()
team_stats = pd.read_csv("team_stats.csv")

def adjust_scores(home_score, away_score):
    if home_score >= 25 and away_score < 25:
        return home_score, away_score
    elif away_score >= 25 and home_score < 25:
        return home_score, away_score
    elif home_score < 25 and away_score < 25:
        if home_score > away_score:
            return random.randint(25, 30), away_score
        else:
            return home_score, random.randint(25, 30)
    else:
        return home_score, away_score

@router.post("/match-details", response_model=MatchDetailsResponse)
async def predict_match_details(request: MatchPredictionRequest):
    # Get team stats
    home_stats = team_stats[team_stats['Team'] == request.home_team]
    away_stats = team_stats[team_stats['Team'] == request.away_team]

    if home_stats.empty or away_stats.empty:
        raise HTTPException(status_code=404, detail="One or both teams not found")

    # Predict Set Scores for Each Set
    home_set_scores = []
    away_set_scores = []

    for set_number in range(1, 6):  # Assuming best-of-5 sets
        score_features = [[home_stats['avg_points'].iloc[0], away_stats['avg_points'].iloc[0], set_number]]
        home_set_score = home_set_score_model.predict(score_features)[0]
        away_set_score = away_set_score_model.predict(score_features)[0]

        home_set_score, away_set_score = adjust_scores(home_set_score, away_set_score)

        home_set_scores.append(int(home_set_score))
        away_set_scores.append(int(away_set_score))

    # Calculate sets won based on predicted set scores
    actual_home_sets_won = sum(1 for home_score, away_score in zip(home_set_scores, away_set_scores) if home_score > away_score)
    actual_away_sets_won = sum(1 for home_score, away_score in zip(home_set_scores, away_set_scores) if away_score > home_score)

    # Determine the match winner based on sets won
    predicted_winner = request.home_team if actual_home_sets_won > actual_away_sets_won else request.away_team

    return {
        "winner": predicted_winner,
        "home_sets_won": actual_home_sets_won,
        "away_sets_won": actual_away_sets_won,
        "sets": {
            request.home_team: home_set_scores,
            request.away_team: away_set_scores
        }
    }
