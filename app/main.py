from fastapi import FastAPI
from app.api.endpoints import predict_set_score, predict_match_details 

app = FastAPI(title="Volleyball Match Predictor API")

# Include the endpoints
app.include_router(predict_set_score.router, prefix="/predict")
app.include_router(predict_match_details.router)