from fastapi import APIRouter, HTTPException
from app.schemas.prediction import MatchPredictionRequest, MatchDetailsResponse
import pandas as pd
from app.models.model_loader import (
    load_home_set_score_model,
    load_away_set_score_model
)
import random

router = APIRouter()

# Load the models and team stats
home_set_score_model = load_home_set_score_model()
away_set_score_model = load_away_set_score_model()
team_stats = pd.read_csv("team_stats.csv")

def adjust_scores(home_score, away_score):
    # Clamp the scores within a realistic range
    home_score = max(15, min(home_score, 30))
    away_score = max(15, min(away_score, 30))

    # Apply volleyball scoring logic
    if home_score >= 25 and away_score < 25:
        return home_score, away_score
    elif away_score >= 25 and home_score < 25:
        return home_score, away_score
    elif home_score < 25 and away_score < 25:
        # Adjust to make one team reach 25 if close
        if home_score > away_score:
            home_score = max(25, home_score)
        else:
            away_score = max(25, away_score)
        return home_score, away_score
    else:
        # If both teams scored >= 25, ensure one wins by 2 points
        if abs(home_score - away_score) < 2:
            if home_score > away_score:
                home_score += 2
            else:
                away_score += 2
        return home_score, away_score

@router.post("/match-details", response_model=MatchDetailsResponse)
async def predict_match_details(request: MatchPredictionRequest):
    # Get team stats
    home_stats = team_stats[team_stats['Team'] == request.home_team]
    away_stats = team_stats[team_stats['Team'] == request.away_team]

    if home_stats.empty or away_stats.empty:
        raise HTTPException(status_code=404, detail="One or both teams not found")

    # Initialize set counts for predicting sets won during the match
    home_sets_won = 0
    away_sets_won = 0
    home_set_scores = []
    away_set_scores = []

    # Predict each set's score up to 5 sets (best-of-5 format)
    for set_number in range(1, 6):
        # Add dynamic match state (home_sets_won and away_sets_won)
        score_features = [[
            home_stats['avg_points'].iloc[0],
            home_stats['win_rate'].iloc[0],
            away_stats['avg_points'].iloc[0],
            away_stats['win_rate'].iloc[0],
            set_number,
            home_sets_won,
            away_sets_won,
            1 if home_sets_won > away_sets_won else 0  # match_winner to reflect current state
        ]]

        # Predict and adjust scores
        home_set_score = home_set_score_model.predict(score_features)[0]
        away_set_score = away_set_score_model.predict(score_features)[0]
        home_set_score, away_set_score = adjust_scores(int(home_set_score), int(away_set_score))

        # Append scores and update set wins
        home_set_scores.append(home_set_score)
        away_set_scores.append(away_set_score)

        if home_set_score > away_set_score:
            home_sets_won += 1
        else:
            away_sets_won += 1

        # Stop prediction if one team has already won 3 sets
        if home_sets_won == 3 or away_sets_won == 3:
            break

    # Determine the match winner based on sets won
    predicted_winner = request.home_team if home_sets_won > away_sets_won else request.away_team

    return {
        "winner": predicted_winner,
        "home_sets_won": home_sets_won,
        "away_sets_won": away_sets_won,
        "sets": {
            request.home_team: home_set_scores,
            request.away_team: away_set_scores
        }
    }
