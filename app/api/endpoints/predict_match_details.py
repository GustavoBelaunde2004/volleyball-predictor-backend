from fastapi import APIRouter, HTTPException
from app.schemas.prediction import MatchPredictionRequest, MatchDetailsResponse
import pandas as pd
from app.models.model_loader import load_home_set_score_model, load_away_set_score_model
import random

router = APIRouter()

# Load the models and team stats
home_set_score_model = load_home_set_score_model()
away_set_score_model = load_away_set_score_model()
team_stats = pd.read_csv("team_stats.csv")

def get_team_stats(team_name, role):
    # Filter the team stats
    stats = team_stats[team_stats['Team'] == team_name]
    if stats.empty:
        raise HTTPException(status_code=404, detail=f"Stats for team {team_name} not found in {role}")
    return stats.iloc[0]

def adjust_set_score(home_score, away_score):
    if home_score >= 25 and away_score < 25:
        return home_score, away_score
    elif away_score >= 25 and home_score < 25:
        return home_score, away_score
    # If neither team reaches 25, set the winning team's score to at least 25
    elif home_score < 25 and away_score < 25:
        if home_score > away_score:
            return 25, away_score
        elif away_score > home_score:
            return home_score, 25
    return home_score, away_score

@router.post("/match-details", response_model=MatchDetailsResponse)
async def predict_match_details(request: MatchPredictionRequest):
    # Get home and away stats
    try:
        home_stats = get_team_stats(request.home_team, "home")
        away_stats = get_team_stats(request.away_team, "away")
    except HTTPException as e:
        raise e

    # Predict Set Scores for Each Set
    home_set_scores = []
    away_set_scores = []

    for set_number in range(1, 6):  # Assuming best-of-5 sets
        # Features aligned to trained model input format
        score_features = [[
            home_stats['avg_points'], home_stats['win_rate'],
            away_stats['avg_points'], away_stats['win_rate'],
            1 if home_stats['Team'] == 'match_winner' else 0,
            set_number
        ]]
        home_set_score = home_set_score_model.predict(score_features)[0]
        away_set_score = away_set_score_model.predict(score_features)[0]

        # Adjust scores to ensure realistic volleyball rules
        home_set_score, away_set_score = adjust_set_score(int(home_set_score), int(away_set_score))

        home_set_scores.append(home_set_score)
        away_set_scores.append(away_set_score)

    # Calculate sets won based on predicted set scores
    actual_home_sets_won = sum(1 for hs, as_ in zip(home_set_scores, away_set_scores) if hs > as_)
    actual_away_sets_won = sum(1 for hs, as_ in zip(home_set_scores, away_set_scores) if as_ > hs)

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
