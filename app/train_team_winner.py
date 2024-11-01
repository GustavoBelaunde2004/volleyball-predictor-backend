# train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib

# Load match data
data = pd.read_csv('C:\GUSTAVO\Projects\\volley\\volley-backend\superlega_matches_large.csv')

# Convert 'Date & Time' to datetime
data['Date & Time'] = pd.to_datetime(data['Date & Time'], format="%d.%m. %H:%M")

# Calculate team statistics (e.g., win rate, average points)
# Group by each team and calculate desired metrics
team_stats = data.groupby('Home Team').agg(
    avg_points=('Home Score', 'mean'),
    win_rate=('Home Score', lambda x: sum(x > 0) / len(x))  # Example win rate calculation
).reset_index()
team_stats.rename(columns={'Home Team': 'Team'}, inplace=True)

# Join team stats to each match
data = data.merge(team_stats, left_on='Home Team', right_on='Team', suffixes=('', '_home'))
data = data.merge(team_stats, left_on='Away Team', right_on='Team', suffixes=('_home', '_away'))

# Create target variable: 1 if Home Team wins, 0 if Away Team wins
data['winner'] = (data['Home Score'] > data['Away Score']).astype(int)

# Select features and target
X = data[['avg_points_home', 'win_rate_home', 'avg_points_away', 'win_rate_away']]
y = data['winner']

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LogisticRegression()
model.fit(X_train, y_train)

# Save the trained model
joblib.dump(model, 'app/models/match_winner_model.pkl')
print("Model training complete and saved to app/models/match_winner_model.pkl")
