# generate_team_stats.py
import pandas as pd

# Load match data
data = pd.read_csv('C:\GUSTAVO\Projects\\volley\\volley-backend\superlega_matches_large.csv')  # Update path as needed

# Calculate average points and win rate for each team
# Aggregate stats as both Home Team and Away Team separately
home_stats = data.groupby('Home Team').agg(
    avg_points_home=('Home Score', 'mean'),
    win_rate_home=('Home Score', lambda x: sum(x > 0) / len(x))  # Example: Win if Home Score > 0
).reset_index()
home_stats.rename(columns={'Home Team': 'Team'}, inplace=True)

away_stats = data.groupby('Away Team').agg(
    avg_points_away=('Away Score', 'mean'),
    win_rate_away=('Away Score', lambda x: sum(x > 0) / len(x))
).reset_index()
away_stats.rename(columns={'Away Team': 'Team'}, inplace=True)

# Merge home and away stats on team name
team_stats = pd.merge(home_stats, away_stats, on='Team', how='outer')

# Calculate overall stats
team_stats['avg_points'] = team_stats[['avg_points_home', 'avg_points_away']].mean(axis=1)
team_stats['win_rate'] = team_stats[['win_rate_home', 'win_rate_away']].mean(axis=1)

# Drop intermediate columns to keep it clean
team_stats = team_stats[['Team', 'avg_points', 'win_rate']]

# Save the team stats to a CSV file
team_stats.to_csv('C:\GUSTAVO\Projects\\volley\\volley-backend\\team_stats.csv', index=False)  # Update path as needed
print("Team stats saved to team_stats.csv")
