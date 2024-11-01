import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load the match data
data = pd.read_csv('C:/GUSTAVO/Projects/volley/volley-backend/superlega_matches_large.csv')

# Calculate the number of sets won by each team
data['home_sets_won'] = data['Home Set Scores'].apply(lambda x: sum(1 for score in x.split() if int(score) > 20))
data['away_sets_won'] = data['Away Set Scores'].apply(lambda x: sum(1 for score in x.split() if int(score) > 20))

# Select features and target variables
# Here we could use match-level statistics, such as total scores and perhaps other features in the future
X = data[['Home Score', 'Away Score']]
y_home = data['home_sets_won']
y_away = data['away_sets_won']

# Train separate models for predicting the number of sets won by the home and away teams
model_home_sets = RandomForestRegressor(random_state=42)
model_away_sets = RandomForestRegressor(random_state=42)

# Train the models
model_home_sets.fit(X, y_home)
model_away_sets.fit(X, y_away)

# Save the models
joblib.dump(model_home_sets, 'app/models/home_sets_won_model.pkl')
joblib.dump(model_away_sets, 'app/models/away_sets_won_model.pkl')

print("Set win prediction models trained and saved successfully.")
