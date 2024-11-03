from fastapi import FastAPI
from app.api.endpoints import predict_set_score, predict_match_details 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Volleyball Match Predictor API")

# Allow CORS requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify your frontend URL, e.g., ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include the endpoints
app.include_router(predict_set_score.router, prefix="/predict")
app.include_router(predict_match_details.router)