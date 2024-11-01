import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load the set-level data
data = pd.read_csv('C:/GUSTAVO/Projects/volley/volley-backend/superlega_set_data.csv')

# Select features and targets
# Using features like set number, total match score, and team names as potential predictors for set score
X = data[['set_number', 'home_score', 'away_score']]
y_home = data['home_set_score']
y_away = data['away_set_score']

# Train separate models for predicting the set scores of the home and away teams
model_home = RandomForestRegressor(random_state=42)
model_away = RandomForestRegressor(random_state=42)

# Train the models
model_home.fit(X, y_home)
model_away.fit(X, y_away)

# Save the models
joblib.dump(model_home, 'app/models/home_set_score_model.pkl')
joblib.dump(model_away, 'app/models/away_set_score_model.pkl')

print("Set score models trained and saved successfully.")
