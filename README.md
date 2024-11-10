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
