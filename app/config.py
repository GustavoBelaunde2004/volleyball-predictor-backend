import os

class Settings:
    MODEL_PATH = os.getenv("MODEL_PATH", "./app/models/")
    # Add other config settings here as needed

settings = Settings()
