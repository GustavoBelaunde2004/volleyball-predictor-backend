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

# Create rolling averages and recent performance stats
def calculate_recent_performance(df, team_column, score_column):
    df[f'{team_column}_recent_avg_points'] = df.groupby(team_column)[score_column].transform(lambda x: x.rolling(3, min_periods=1).mean())
    df[f'{team_column}_win_rate_last_3'] = df.groupby(team_column)['match_winner'].transform(lambda x: x.rolling(3, min_periods=1).mean())
    return df

data = calculate_recent_performance(data, 'Home Team', 'Home Score')
data = calculate_recent_performance(data, 'Away Team', 'Away Score')

# Calculate set-by-set performance stats
data['home_score_variance'] = data['Home Set Scores'].apply(lambda x: np.var([int(score) for score in x.split()]))
data['away_score_variance'] = data['Away Set Scores'].apply(lambda x: np.var([int(score) for score in x.split()]))

# Prepare expanded training data with match state and new features
X_expanded = []
y_home_flat = []
y_away_flat = []

for _, row in data.iterrows():
    home_set_scores = list(map(int, row['Home Set Scores'].split()))
    away_set_scores = list(map(int, row['Away Set Scores'].split()))
    
    home_sets_won, away_sets_won = 0, 0
    for set_number, (home_score, away_score) in enumerate(zip(home_set_scores, away_set_scores), start=1):
        # Stop recording sets after one team reaches 3 wins
        if home_sets_won == 3 or away_sets_won == 3:
            break
        
        # Append the match state and new features
        X_expanded.append([
            row['home_avg_points'], row['home_win_rate'],
            row['away_avg_points'], row['away_win_rate'],
            row['match_winner'], set_number,
            home_sets_won, away_sets_won,
            row['Home Team_recent_avg_points'], row['Away Team_recent_avg_points'],
            row['home_score_variance'], row['away_score_variance'],
            row['Home Team_win_rate_last_3'], row['Away Team_win_rate_last_3']
        ])
        y_home_flat.append(home_score)
        y_away_flat.append(away_score)
        
        # Update set win counts
        if home_score > away_score:
            home_sets_won += 1
        else:
            away_sets_won += 1

X_expanded_df = pd.DataFrame(X_expanded, columns=[
    'home_avg_points', 'home_win_rate', 'away_avg_points', 'away_win_rate', 'match_winner', 'set_number',
    'home_sets_won', 'away_sets_won',
    'home_recent_avg_points', 'away_recent_avg_points',
    'home_score_variance', 'away_score_variance',
    'home_win_rate_last_3', 'away_win_rate_last_3'
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
