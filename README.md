# Fake News & Sentiment Detection AI Application

An end-to-end full-stack web application for analyzing text authenticity (Fake vs. Real) and emotional sentiment (Positive, Negative, Neutral) using Hugging Face Transformer models.

![App Stack](https://img.shields.io/badge/Stack-React%20%7C%20Flask%20%7C%20Hugging%20Face%20%7C%20PostgreSQL-blue)

---

## 📌 Problem Statement & Overview

In today's fast-paced digital ecosystem, misinformation spreads rapidly alongside shifting public sentiments. This application provides a real-time NLP classification engine that allows users to evaluate news articles or text snippets for:
1. **Fake News Prediction**: Predicts if an input text exhibits patterns of fake/manipulative news or standard news (`FAKE` / `REAL`).
2. **Sentiment Analysis**: Evaluates the emotional tone (`POSITIVE`, `NEGATIVE`, `NEUTRAL`).

*Note: The fake-news model functions as a statistical prediction and pattern-classification system, not as an absolute fact-checking authority.*

---

## 🛠️ Tech Stack

- **Frontend**: React 18, Vite, JavaScript, Custom Glassmorphic Dark UI (Vanilla CSS)
- **Backend**: Python 3.14+, Flask 3.x, Flask-CORS, SQLAlchemy
- **NLP / Machine Learning**: Hugging Face `transformers`, PyTorch, Hugging Face Pipelines
- **Database**: PostgreSQL (with graceful degradation for offline local runs)
- **Environment**: Python `.venv`, `dotenv`

---

## 🏗️ Architecture & Data Flow

```text
User Input (React UI)
        │
        ▼ (POST /api/analyze)
Flask REST Controller
        │
   ┌────┴────────────────────────┐
   ▼                             ▼
Text Preprocessing      Database Persistence
(Tokenization Ready)    (PostgreSQL / SQLAlchemy)
   │
   ├──────► Fake News Model (Hugging Face BERT) ────► Prediction & Confidence
   │
   └──────► Sentiment Model (DistilBERT SST-2)   ────► Prediction & Confidence
        │
        ▼
JSON Response ──► React UI Dashboard
```

---

## 🚀 Getting Started (Local Development)

### 1. Prerequisites
- Python 3.10+
- Node.js 18+

### 2. Backend Setup

```bash
# Navigate to project root
cd "Fake News and sentiment detector app"

# Create virtual environment (if not already created)
python -m venv backend/.venv

# Activate virtual environment
# Windows PowerShell:
.\backend\.venv\Scripts\Activate.ps1

# Install backend dependencies
pip install -r backend/requirements.txt

# Start Flask Backend Server (Port 5000)
python backend/run.py
```

### 3. Frontend Setup

Open a separate terminal:

```bash
# Navigate to frontend folder
cd frontend

# Install node dependencies
npm install

# Start Vite Development Server (Port 5173)
npm run dev
```

Open browser at `http://localhost:5173`.

---

## 🔑 Environment Variables

Copy `backend/.env.example` to `backend/.env`:

```env
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your_secret_key_here
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/fake_news_db
FAKE_NEWS_MODEL=mrm8488/bert-tiny-finetuned-fake-news-detection
SENTIMENT_MODEL=distilbert/distilbert-base-uncased-finetuned-sst-2-english
FRONTEND_URL=http://localhost:5173
```

---

## 🧪 API Endpoints

### `GET /api/health`
**Response:**
```json
{
  "status": "ok"
}
```

### `POST /api/analyze`
**Request:**
```json
{
  "text": "Tech giant introduces breakthrough energy-efficient quantum chip."
}
```
**Response:**
```json
{
  "success": true,
  "fake_news": {
    "label": "REAL",
    "confidence": 0.895
  },
  "sentiment": {
    "label": "POSITIVE",
    "confidence": 0.942
  },
  "record_id": 1
}
```

---

## 🤖 Pretrained ML Models Used

1. **Fake News Classifier**: `mrm8488/bert-tiny-finetuned-fake-news-detection`
   - Compact fine-tuned BERT model optimized for fast text classification.
2. **Sentiment Model**: `distilbert/distilbert-base-uncased-finetuned-sst-2-english`
   - DistilBERT fine-tuned on SST-2 for sentiment classification.

---

## 🧪 Testing

Run automated tests:

```bash
backend\.venv\Scripts\pytest.exe backend/tests
```

---

## 📄 License
MIT License
