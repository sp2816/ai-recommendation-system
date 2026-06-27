                    USER / FRONTEND
                           │
                           ▼
                React Frontend (Vite)
                           │
                           ▼
                    FastAPI Backend
                           │
      ┌────────────────────┼────────────────────┐
      ▼                    ▼                    ▼
 Product APIs      User Activity APIs      Recommendation API
 (/products)      (search/view history)   (/recommend/{user_id})
      │                    │                    │
      └──────────────┬─────┴─────┬─────────────┘
                     ▼           ▼
               PostgreSQL      Redis
              Application DB  Feature Store
                     │           │
                     └─────┬─────┘
                           ▼
                 Recommendation Engine
              (ANN Search + Re-ranking)
                           │
                           ▼
              Personalized Recommendations
                           │
                           ▼
                    Frontend Dashboard


────────────────────────────────────────

Offline ML Pipeline

H&M Dataset
(articles.csv + transactions.csv + customers.csv)
        │
        ▼
Data Preprocessing & Feature Engineering
        │
        ▼
Two-Tower Recommendation Model (TensorFlow Recommenders)
        │
        ▼
User Embeddings
Item Embeddings
        │
        ▼
ANN Candidate Retrieval
        │
        ▼
Embedding Storage
(Redis Feature Store)
        │
        ▼
FastAPI Recommendation Serving


────────────────────────────────────────

User Activity Flow

Search Product
      │
      ▼
search_history table

View Product
      │
      ▼
view_history table

Recommendation Generated
      │
      ▼
user_interactions table

Wishlist Added
      │
      ▼
wishlist table

These signals influence future recommendations.