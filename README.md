# Seamless HR - AI Ranking Engine

This is the AI-powered ranking service for the Seamless HR platform. It uses **Sentence-Transformers** (SBERT) to calculate the semantic similarity between Job Descriptions and CVs using **Cosine Similarity**.

## 🛠 Setup

1. **Install Python 3.9+**
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 How to Run

Start the API server:
```bash
python main.py
```

The server will be available at `http://localhost:8000`.

## 📍 API Endpoints

- **POST `/rank/{job_id}`**: 
  - This is the main endpoint.
  - It fetches the JD and CVs from your company's APIs.
  - It returns a JSON list of applicants ranked from highest to lowest score.

## 📝 Integration Notes for the AI Engineer

- **Updating URLs**: Change the `CV_API_URL` and `JD_API_URL` in `main.py` once your company provides the final endpoints.
- **LLM Extension**: To add OpenAI/Gemini logic, you can modify `ranking_logic.py` to include a second stage for the top-ranked candidates.
