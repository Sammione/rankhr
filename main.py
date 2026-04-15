import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Union
from ranking_logic import rank_cvs

app = FastAPI(title="Seamless HR - AI Ranking Engine")

# ==== Data Models ==== #
class Applicant(BaseModel):
    id: Union[str, int]
    name: Optional[str] = "Unknown"
    text: str

class RankRequest(BaseModel):
    job_description: str
    cvs: List[Applicant]
    top_n: Optional[int] = None

# ==== Endpoints ==== #
@app.get("/")
def home():
    return {
        "message": "AI Ranking Engine is running", 
        "endpoints": [
            "GET /",
            "POST /rank (Send Job Description and CVs directly in the request body)"
        ]
    }

@app.post("/rank")
def process_ranking(payload: RankRequest):
    """
    Accepts the Job Description and a list of CVs directly from the backend.
    The backend service sends the actual TEXT data in the payload.
    """
    try:
        # 1. Convert Pydantic objects to a list of dictionaries for the ranking logic
        cv_list = [{"id": cv.id, "name": cv.name, "text": cv.text} for cv in payload.cvs]
        
        # 2. Run the AI Ranking logic
        ranked_list = rank_cvs(payload.job_description, cv_list)
        
        # 3. Filter top N if requested
        if payload.top_n is not None and payload.top_n > 0:
            ranked_list = ranked_list[:payload.top_n]
        
        # 4. Return the result back to the backend
        return {
            "total_applicants": len(ranked_list),
            "rankings": ranked_list
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Render and other platforms provide a PORT environment variable
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
