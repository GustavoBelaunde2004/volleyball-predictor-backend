import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

# Load match data
data = pd.read_csv('C:/GUSTAVO/Projects/volley/volley-backend/superlega_matches_large.csv')
data['match_winner'] = data.apply(lambda row: 1 if row['Home Score'] > row['Away Score'] else 0, axis=1)

# Load team stats and merge
team_stats = pd.read_csv('team_stats.csv')
data = data.merge(team_stats, left_on='Home Team', right_on='Team').rename(columns={'avg_points': 'home_avg_points', 'win_rate': 'home_win_rate'})
data = data.merge(team_stats, left_on='Away Team', right_on='Team').rename(columns={'avg_points': 'away_avg_points', 'win_rate': 'away_win_rate'})
data = data.drop(columns=['Team_x', 'Team_y'])

# Prepare expanded training data
X_expanded = []
y_home_flat = []
y_away_flat = []

for _, row in data.iterrows():
    home_set_scores = list(map(int, row['Home Set Scores'].split()))
    away_set_scores = list(map(int, row['Away Set Scores'].split()))
    
    for set_number, (home_score, away_score) in enumerate(zip(home_set_scores, away_set_scores), start=1):
        X_expanded.append([
            row['home_avg_points'], row['home_win_rate'],
            row['away_avg_points'], row['away_win_rate'],
            row['match_winner'], set_number
        ])
        y_home_flat.append(home_score)
        y_away_flat.append(away_score)

X_expanded_df = pd.DataFrame(X_expanded, columns=[
    'home_avg_points', 'home_win_rate', 'away_avg_points', 'away_win_rate', 'match_winner', 'set_number'
])

# Split data into training and testing sets
X_train, X_test, y_train_home, y_test_home = train_test_split(X_expanded_df, y_home_flat, test_size=0.2, random_state=42)
_, _, y_train_away, y_test_away = train_test_split(X_expanded_df, y_away_flat, test_size=0.2, random_state=42)

# Train models
model_home_set_scores = RandomForestRegressor(random_state=42)
model_away_set_scores = RandomForestRegressor(random_state=42)

model_home_set_scores.fit(X_train, y_train_home)
model_away_set_scores.fit(X_train, y_train_away)

# Make predictions on the test set
y_pred_home = model_home_set_scores.predict(X_test)
y_pred_away = model_away_set_scores.predict(X_test)

# Calculate evaluation metrics
print("Home Set Score Prediction Metrics:")
print("Mean Absolute Error:", mean_absolute_error(y_test_home, y_pred_home))
print("Mean Squared Error:", mean_squared_error(y_test_home, y_pred_home))
print("R^2 Score:", r2_score(y_test_home, y_pred_home))

print("\nAway Set Score Prediction Metrics:")
print("Mean Absolute Error:", mean_absolute_error(y_test_away, y_pred_away))
print("Mean Squared Error:", mean_squared_error(y_test_away, y_pred_away))
print("R^2 Score:", r2_score(y_test_away, y_pred_away))

# Save the models
joblib.dump(model_home_set_scores, 'app/models/home_set_score_model.pkl')
joblib.dump(model_away_set_scores, 'app/models/away_set_score_model.pkl')

print("Set score prediction models trained, tested, and saved successfully.")
