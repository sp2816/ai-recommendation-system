# AI Recommendation System Architecture

```text
                    USER / FRONTEND
                           │
                           ▼
                React Frontend (Vite)
                           │
                           ▼
                    FastAPI Backend
                  (/recommend/{user_id})
                           │
          ┌────────────────┴──────────────┐
          ▼                               ▼
      Redis Feature Store          Recommendation Engine
   (User Profiles + Item Vectors)   (ANN Similarity Search)
          │                               │
          └──────────────┬────────────────┘
                         ▼
               Recommendation Response
              (Top K Recommended Products)
                         │
                         ▼
                    Frontend UI


────────────────────────────────────────

Offline ML Pipeline

Transaction Dataset
        │
        ▼
Feature Engineering (PySpark)
        │
        ▼
Two-Tower Model Training (TFRS)
        │
        ▼
Item Embeddings Generation
        │
        ▼
Redis Storage Update
        │
        ▼
FastAPI Serving
```