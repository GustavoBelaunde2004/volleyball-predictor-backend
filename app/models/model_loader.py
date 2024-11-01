import joblib

# Load separate models for predicting the score of individual sets
def load_home_set_score_model():
    """Load the model to predict the set score for the home team."""
    return joblib.load("app/models/home_set_score_model.pkl")

def load_away_set_score_model():
    """Load the model to predict the set score for the away team."""
    return joblib.load("app/models/away_set_score_model.pkl")
