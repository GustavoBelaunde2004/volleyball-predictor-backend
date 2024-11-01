import pandas as pd

# Load the match data
data = pd.read_csv('C:/GUSTAVO/Projects/volley/volley-backend/superlega_matches_large.csv')

set_data = []

# Process each match and expand set scores
for _, row in data.iterrows():
    home_set_scores = [int(score) for score in row['Home Set Scores'].split()]
    away_set_scores = [int(score) for score in row['Away Set Scores'].split()]

    # Generate set-level data for each set in the match
    for i in range(min(len(home_set_scores), len(away_set_scores))):
        set_data.append({
            'date_time': row['Date & Time'],
            'home_team': row['Home Team'],
            'away_team': row['Away Team'],
            'set_number': i + 1,
            'home_set_score': home_set_scores[i],
            'away_set_score': away_set_scores[i],
            'home_score': row['Home Score'],
            'away_score': row['Away Score']
        })

# Create DataFrame and save as CSV
set_df = pd.DataFrame(set_data)
set_df.to_csv('C:/GUSTAVO/Projects/volley/volley-backend/superlega_set_data.csv', index=False)
print("Set-level data saved to superlega_set_data.csv")
