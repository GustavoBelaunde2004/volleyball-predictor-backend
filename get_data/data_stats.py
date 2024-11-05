# generate_team_stats.py
import pandas as pd

# Load match data
data = pd.read_csv('C:/GUSTAVO/Projects/volley/volley-backend/superlega_matches_large.csv')

# Calculate additional team stats
def recent_avg_points(scores):
    # Calculate recent average for the last 5 matches
    return scores[-5:].mean() if len(scores) >= 5 else scores.mean()

def variance_scores(scores):
    # Calculate variance for set scores
    return scores.var()

# Home and Away Stats
home_stats = data.groupby('Home Team').agg(
    avg_points_home=('Home Score', 'mean'),
    recent_home_avg=('Home Score', lambda x: recent_avg_points(x)),
    home_set_variance=('Home Score', lambda x: variance_scores(x)),
    home_last_5_games_avg=('Home Score', lambda x: recent_avg_points(x)),
    win_rate_home=('Home Score', lambda x: sum(x > 0) / len(x))
).reset_index()
home_stats.rename(columns={'Home Team': 'Team'}, inplace=True)

away_stats = data.groupby('Away Team').agg(
    avg_points_away=('Away Score', 'mean'),
    recent_away_avg=('Away Score', lambda x: recent_avg_points(x)),
    away_set_variance=('Away Score', lambda x: variance_scores(x)),
    away_last_5_games_avg=('Away Score', lambda x: recent_avg_points(x)),
    win_rate_away=('Away Score', lambda x: sum(x > 0) / len(x))
).reset_index()
away_stats.rename(columns={'Away Team': 'Team'}, inplace=True)

# Merge and calculate overall stats
team_stats = pd.merge(home_stats, away_stats, on='Team', how='outer')
team_stats['avg_points'] = team_stats[['avg_points_home', 'avg_points_away']].mean(axis=1)
team_stats['win_rate'] = team_stats[['win_rate_home', 'win_rate_away']].mean(axis=1)

# Keep only the necessary columns
team_stats = team_stats[['Team', 'avg_points', 'win_rate', 'recent_home_avg', 'recent_away_avg', 'home_set_variance', 'away_set_variance', 'home_last_5_games_avg', 'away_last_5_games_avg']]

# Save updated team stats
team_stats.to_csv('C:/GUSTAVO/Projects/volley/volley-backend/team_stats.csv', index=False)
print("Team stats saved to team_stats.csv with additional features.")
