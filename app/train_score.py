import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import numpy as np

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

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_expanded_df)

# Split data into training and testing sets
X_train, X_test, y_train_home, y_test_home = train_test_split(X_scaled, y_home_flat, test_size=0.2, random_state=42)
_, _, y_train_away, y_test_away = train_test_split(X_scaled, y_away_flat, test_size=0.2, random_state=42)

# Define a parameter grid for tuning
param_grid = {
    'n_estimators': [50, 100, 150],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5, 10]
}

# Use GridSearchCV to find the best model for home set scores
home_grid_search = GridSearchCV(RandomForestRegressor(random_state=42), param_grid, cv=3, scoring='neg_mean_absolute_error', n_jobs=-1)
home_grid_search.fit(X_train, y_train_home)
best_home_model = home_grid_search.best_estimator_

# Use GridSearchCV to find the best model for away set scores
away_grid_search = GridSearchCV(RandomForestRegressor(random_state=42), param_grid, cv=3, scoring='neg_mean_absolute_error', n_jobs=-1)
away_grid_search.fit(X_train, y_train_away)
best_away_model = away_grid_search.best_estimator_

# Predictions on the test set
y_pred_home = best_home_model.predict(X_test)
y_pred_away = best_away_model.predict(X_test)

# Evaluate performance metrics
def print_metrics(y_true, y_pred, team_type):
    print(f"\n{team_type} Set Score Prediction Metrics:")
    print(f"Mean Absolute Error: {mean_absolute_error(y_true, y_pred)}")
    print(f"Mean Squared Error: {mean_squared_error(y_true, y_pred)}")
    print(f"Root Mean Squared Error: {np.sqrt(mean_squared_error(y_true, y_pred))}")
    print(f"R^2 Score: {r2_score(y_true, y_pred)}")

print_metrics(y_test_home, y_pred_home, "Home")
print_metrics(y_test_away, y_pred_away, "Away")

# Save the models
joblib.dump(best_home_model, 'app/models/home_set_score_model.pkl')
joblib.dump(best_away_model, 'app/models/away_set_score_model.pkl')

print("Set score prediction models trained, optimized, and saved successfully.")
print("Best parameters for home set model:", home_grid_search.best_params_)
print("Best parameters for away set model:", away_grid_search.best_params_)
