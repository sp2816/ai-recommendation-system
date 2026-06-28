# 🛍️ Context-Aware Neural Recommendation Engine (Deep Learning)

A **Deep Learning-based Fashion Recommendation System** that generates personalized clothing recommendations using a **Two-Tower Neural Network**. The system combines user interaction history, product metadata, and neural embeddings to recommend relevant fashion products in real time.

---

## 📌 Overview

This project implements a **Context-Aware Neural Recommendation Engine** for fashion e-commerce. Instead of relying on traditional collaborative filtering, it uses **TensorFlow Recommenders (TFRS)** to learn user and item embeddings independently and retrieve the most relevant products using **Approximate Nearest Neighbor (ANN)** search.

The application includes:

* Deep Learning recommendation model
* FastAPI backend
* React frontend
* PostgreSQL database
* Dockerized development environment

---

## ✨ Features

* 👤 Personalized recommendations based on user preferences
* 🧠 Two-Tower Neural Network using TensorFlow Recommenders
* ⚡ Approximate Nearest Neighbor (ANN) search
* 🔍 Product search functionality
* ❤️ Wishlist management
* 🛒 Product details page
* 🔐 User Authentication
* 📊 User interaction tracking
* 📱 Responsive React frontend

---

# 🏗️ System Architecture

```
React Frontend
        │
        ▼
FastAPI Backend
        │
        ├──────────────┐
        ▼              ▼
 Recommendation      PostgreSQL
 Engine              Database
        │
        ▼
TensorFlow Recommenders
(Two-Tower Model)
        │
        ▼
ANN Search
        │
        ▼
Top-K Recommendations
```

---

# 🧠 Two-Tower Recommendation Model

### Query Tower (User)

* User ID
* Age
* Interaction History
* Favorite Product Type
* User Features

↓

User Embedding

---

### Candidate Tower (Product)

* Article ID
* Product Type
* Product Group
* Colour
* Product Metadata

↓

Item Embedding

---

Similarity between both embeddings is calculated to retrieve the most relevant products.

---

## 🛠️ Tech Stack

### Frontend

* React
* React Router
* Axios
* CSS

### Backend

* FastAPI
* SQLAlchemy
* JWT Authentication

### Machine Learning

* TensorFlow
* TensorFlow Recommenders (TFRS)
* NumPy
* Pandas

### Database

* PostgreSQL

### DevOps

* Docker
* Git

---


## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/sp2816/ai-recommendation-system.git

cd ai-recommendation-system
```

---

### Backend

```bash
cd backend

pip install -r requirements.txt

uvicorn backend.main:app --reload
```

---

### Frontend

```bash
cd frontend

npm install

npm run dev
```

---

### Docker

```bash
docker compose up --build
```

---

## 🔌 API Endpoints

| Method | Endpoint             | Description                  |
| ------ | -------------------- | ---------------------------- |
| POST   | /api/register        | Register User                |
| POST   | /api/login           | Login                        |
| GET    | /api/products        | Get Products                 |
| GET    | /api/products/search | Search Products              |
| GET    | /recommend/{user_id} | Personalized Recommendations |
| GET    | /api/product/{id}    | Product Details              |
| GET    | /api/wishlist        | Wishlist                     |

---

## 📊 Dataset

**H&M Personalized Fashion Recommendations**

Source:
https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations
