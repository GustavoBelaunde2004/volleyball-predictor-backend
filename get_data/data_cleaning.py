import re
import csv

# Read data from a text file
with open('volleyball_data.txt', 'r', encoding='utf-8') as file:
    lines = [line.strip() for line in file if line.strip()]  # Strips whitespace and filters out empty lines

# Initialize a list to store each match’s parsed data
matches = []

# Iterate through the lines
i = 0
while i < len(lines):
    # Look for lines with the date & time format as the start of a match
    if re.match(r'\d{2}\.\d{2}\.\s\d{2}:\d{2}', lines[i]):
        date_time = lines[i]
        home_team = lines[i + 1]
        away_team = lines[i + 2]
        home_score = lines[i + 3]
        away_score = lines[i + 4]

        # Collect the set scores (assuming they follow directly after scores)
        set_scores = []
        j = i + 5  # Start after the main scores
        while j < len(lines) and re.match(r'^\d+$', lines[j]):
            set_scores.append(int(lines[j]))
            j += 1

        # Split the set scores into home and away by alternating indices
        home_set_scores = set_scores[0::2]
        away_set_scores = set_scores[1::2]

        # Add parsed match details to matches list
        matches.append([
            date_time, home_team, away_team, home_score, away_score,
            " ".join(map(str, home_set_scores)), " ".join(map(str, away_set_scores))
        ])

        # Move index to the end of this match block
        i = j
    else:
        i += 1  # Move to the next line if no match is found

# Write matches to CSV
with open('superlega_matches_large.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Date & Time", "Home Team", "Away Team", "Home Score", "Away Score", "Home Set Scores", "Away Set Scores"])
    csvwriter.writerows(matches)

print("Data successfully cleaned and saved to superlega_matches_large.csv")
