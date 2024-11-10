# Volleyball Match Predictor Backend

This repository contains the backend for the **Volleyball Match Predictor** app, designed to predict match outcomes based on team statistics from the Italian Superlega.

## Features

- Predicts:
  - Match winner
  - Number of sets won by each team
  - Individual set scores
- FastAPI-powered RESTful API.
- Handles input data and provides real-time predictions.

## Repository Structure

```plaintext
volleyball-predictor-backend/
│
├── app/                     # Core backend logic
│   ├── main.py              # Entry point for the FastAPI app
│   └── ...                  # Other backend modules
├── get_data/                # Data processing logic
│   └── ...                  # Scripts for gathering and preprocessing data
├── superlega_matches_large.csv  # Dataset with match details
├── team_stats.csv           # Dataset with team statistics
├── requirements.txt         # List of Python dependencies
├── .gitignore               # Ignored files and folders
└── README.md                # Project documentation
```
## Tech Stack
- Language: Python
- Framework: FastAPI
- Dependencies:
  - uvicorn: ASGI server to run the FastAPI app.
  - pandas: For data manipulation.
  - scikit-learn: For model-based predictions.

## Installation
Clone the Repository:

```plaintext
git clone https://github.com/yourusername/volleyball-predictor-backend.git
cd volleyball-predictor-backend
```

Set Up a Virtual Environment:
```plaintext
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```

Install Dependencies:

```plaintext
pip install -r requirements.txt
```

## Usage
Start the Server: Run the FastAPI server using Uvicorn:

```
uvicorn app.main:app --reload
```

Access the API: The API will be available at:
```plaintext
http://127.0.0.1:8000
```

Endpoints:

```plaintext
POST /match-details:
{
  "home_team": "Perugia",
  "away_team": "Trentino"
}

Response:
{
  "winner": "Perugia",
  "sets_won": {"home": 3, "away": 1},
  "set_scores": [25, 20, 25, 15]
}
```

## Future Enhancements
- Machine Learning Integration:
  	- Add ML models for more accurate match predictions.
- Support for More Leagues:
  - Expand beyond the Italian Superlega.
- Database Integration:
  - Store historical match data for analytics.

## Contributing
We welcome contributions! Please follow these steps:

1) Fork the repository
2) Create a feature branch:
```plaintext
git checkout -b feature/your-feature-name
```
3) Commit your changes:
```plaintext
git commit -m "Add your message here"
```
4) Push to the branch:
```plaintext
git push origin feature/your-feature-name
```
5) Open a pull request on GitHub!
