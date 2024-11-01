from fastapi import APIRouter, HTTPException
from app.schemas.prediction import MatchPredictionRequest, MatchDetailsResponse
import pandas as pd
from app.models.model_loader import load_match_winner_model, load_home_sets_won_model, load_away_sets_won_model, load_home_set_score_model, load_away_set_score_model


router = APIRouter()

# Load the models and team stats
match_winner_model = load_match_winner_model()
home_sets_model = load_home_sets_won_model()
away_sets_model = load_away_sets_won_model()
home_set_score_model = load_home_set_score_model()
away_set_score_model = load_away_set_score_model()
team_stats = pd.read_csv("team_stats.csv")


@router.post("/match-details", response_model=MatchDetailsResponse)
async def predict_match_details(request: MatchPredictionRequest):
    # Get team stats
    home_stats = team_stats[team_stats['Team'] == request.home_team]
    away_stats = team_stats[team_stats['Team'] == request.away_team]

    if home_stats.empty or away_stats.empty:
        raise HTTPException(status_code=404, detail="One or both teams not found")

    # Predict Match Winner
    features = [[home_stats['avg_points'].iloc[0], home_stats['win_rate'].iloc[0],
                 away_stats['avg_points'].iloc[0], away_stats['win_rate'].iloc[0]]]
    winner_prediction = match_winner_model.predict(features)
    predicted_winner = request.home_team if winner_prediction[0] == 1 else request.away_team

    # Predict Sets Won
    home_sets_won = home_sets_model.predict(features)[0]
    away_sets_won = away_sets_model.predict(features)[0]

    # Predict Set Scores for Each Set
    home_set_scores = []
    away_set_scores = []

    for set_number in range(1, 6):  # Assuming best-of-5 sets
        score_features = [[set_number, home_stats['avg_points'].iloc[0], away_stats['avg_points'].iloc[0]]]
        home_set_score = home_set_score_model.predict(score_features)[0]
        away_set_score = away_set_score_model.predict(score_features)[0]

        home_set_scores.append(int(home_set_score))
        away_set_scores.append(int(away_set_score))

    # Format total score
    total_score = f"{sum(home_set_scores)} - {sum(away_set_scores)}"

    return {
        "winner": predicted_winner,
        "total_score": total_score,
        "sets": {
            request.home_team: home_set_scores,
            request.away_team: away_set_scores
        }
    }
