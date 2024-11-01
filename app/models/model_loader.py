import joblib

def load_match_winner_model():
    """Load the match winner prediction model."""
    return joblib.load("app/models/match_winner_model.pkl")

# Load separate models for predicting the number of sets won
def load_home_sets_won_model():
    """Load the model to predict sets won by the home team."""
    return joblib.load("app/models/home_sets_won_model.pkl")

def load_away_sets_won_model():
    """Load the model to predict sets won by the away team."""
    return joblib.load("app/models/away_sets_won_model.pkl")

# Load separate models for predicting the score of individual sets
def load_home_set_score_model():
    """Load the model to predict the set score for the home team."""
    return joblib.load("app/models/home_set_score_model.pkl")

def load_away_set_score_model():
    """Load the model to predict the set score for the away team."""
    return joblib.load("app/models/away_set_score_model.pkl")
