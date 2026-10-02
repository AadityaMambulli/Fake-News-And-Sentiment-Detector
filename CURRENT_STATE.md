# CURRENT_STATE.md

# Fake News & Sentiment Detection App

> Single source of truth for the current project state.
> Read this file at the beginning of a new chat/session before making project decisions.
> Do not silently change established architecture or decisions. If a change is needed, discuss it first and update this file after the decision.

---

## 1. Project Overview

**Project name:** Fake News & Sentiment Detection App

**Primary goal:** Build a full-stack web application that accepts news/text input and performs:
1. Fake-news classification
2. Sentiment detection

**Current project deadline:** October 3, 2026

The priority before the deadline is to get a functional, understandable, deployable application. Deep ML/DL implementation from scratch is a separate follow-up project.

---

## 2. Current Tech Stack

### Frontend
- React
- Vite
- JavaScript

### Backend
- Python
- Flask
- Flask-CORS

### NLP / ML
- Hugging Face Transformers
- BERT-based model(s)
- Hugging Face tokenizer
- PyTorch

### Database
- PostgreSQL

### Deployment
- Render

### Development
- Git / GitHub
- Python virtual environment: `.venv`

---

## 3. Architecture

Current intended architecture:

```text
                    USER
                      |
                      v
              +---------------+
              | React + Vite  |
              |   Frontend    |
              +-------+-------+
                      |
                 HTTP / REST
                      |
                      v
              +---------------+
              | Flask Backend |
              +-------+-------+
                      |
              +-------+--------+
              |                |
              v                v
      +---------------+  +-------------+
      | Hugging Face  |  | PostgreSQL  |
      | BERT + Tokenizer| |  Database   |
      +-------+-------+  +-------------+
              |
              v
       Predictions
       - Fake / Real
       - Sentiment
              |
              v
          React UI

Deployment:
Render hosts the application components/services as appropriate.
```

---

## 4. Important ML Decision

For THIS project, do NOT implement BERT, tokenization, embeddings, attention, or the neural-network internals from scratch.

Use Hugging Face's pretrained/fine-tuned models and tokenizer.

Example conceptual flow:

```text
Raw text
   |
   v
Hugging Face Tokenizer
   |
   v
Token IDs + Attention Mask
   |
   v
BERT-based model
   |
   v
Logits / probabilities
   |
   +----> Fake / Real
   |
   +----> Sentiment
```

The internals should still be understood conceptually, but they do not need to be manually implemented for this application.

---

## 5. Separate Learning Project

After the October 3 deadline, build a separate project to understand ML/DL internals from scratch.

Goal: understand concepts rather than simply using `.fit()` from libraries.

Planned progression:

```text
Python + NumPy
      |
      v
Data preprocessing
      |
      v
Feature engineering
      |
      v
Feature selection
      |
      v
Linear Regression
      |
      v
Logistic Regression
      |
      v
Gradient Descent
      |
      v
Neural Networks
      |
      v
Forward Propagation
      |
      v
Backpropagation
      |
      v
Optimizers
      |
      v
Embeddings
      |
      v
Tokenization
      |
      v
Attention
      |
      v
Transformer
      |
      v
Mini-GPT
```

The goal of this second project is to implement core algorithms/functions ourselves rather than relying on things like:

```python
sklearn_model.fit(...)
```

This second project is NOT part of the current October 3 deadline.

---

## 6. Current Repository Structure

Planned structure:

```text
fake-news-sentiment-app/
│
├── backend/
│   ├── .venv/                    # Local only; never commit
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   │
│   │   ├── ml/
│   │   │   ├── __init__.py
│   │   │   ├── classifier.py
│   │   │   ├── sentiment.py
│   │   │   └── preprocessing.py
│   │   │
│   │   └── database/
│   │       ├── __init__.py
│   │       └── db.py
│   │
│   ├── tests/
│   │   └── __init__.py
│   │
│   ├── .env                     # Local secrets; never commit
│   ├── .env.example             # Safe template; commit this
│   ├── requirements.txt
│   └── run.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── data/
│   └── .gitkeep
│
├── models/
│   └── .gitkeep
│
├── docs/
│   └── .gitkeep
│
├── .gitignore
├── README.md
└── LICENSE
```

Note: This is the intended structure. Some files/directories may not exist yet if setup has not been executed.

---

## 7. Python Environment

Use a project-local Python virtual environment:

```bash
cd backend
python -m venv .venv
```

Windows PowerShell activation:

```powershell
.\.venv\Scripts\Activate.ps1
```

`.venv` must NOT be committed to Git.

---

## 8. Environment Variables

Actual secrets belong in:

```text
backend/.env
```

A safe template belongs in:

```text
backend/.env.example
```

Current intended `.env.example`:

```env
# Flask
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=replace_with_a_random_secret

# PostgreSQL
DATABASE_URL=postgresql://username:password@localhost:5432/fake_news_db

# ML
FAKE_NEWS_MODEL=your-huggingface-model
SENTIMENT_MODEL=your-huggingface-model

# Frontend
FRONTEND_URL=http://localhost:5173
```

Generate a Flask secret key locally with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

The generated secret must not be committed.

For Render, use Render environment variables and a separate production secret.

---

## 9. PostgreSQL

PostgreSQL is intended to be used locally during development.

Expected local database:

```text
Database: fake_news_db
Host: localhost
Port: 5432
```

Example connection string:

```text
postgresql://username:password@localhost:5432/fake_news_db
```

The production database will use the appropriate Render PostgreSQL connection string through `DATABASE_URL`.

Do not hard-code database credentials in Python source code.

---

## 10. Initial Python Dependencies

Initial planned `requirements.txt`:

```text
Flask==3.1.2
flask-cors==6.0.1
python-dotenv==1.1.1

transformers==4.56.2
torch==2.8.0
tokenizers==0.22.1

psycopg[binary]==3.2.10
SQLAlchemy==2.0.43

requests==2.32.5

pytest==8.4.2
```

These versions are an initial plan. Once the actual environment and model choices are established, verify compatibility and regenerate/update `requirements.txt` from the working environment when appropriate.

---

## 11. Git Rules

Initialize the repository from the project root:

```bash
git init
git add .
git status
git commit -m "Initial project structure"
```

Never commit:

```text
backend/.venv/
backend/.env
node_modules/
large datasets
model weights/checkpoints
local database files
secrets/API keys/passwords
```

Commit:

```text
backend/.env.example
backend/requirements.txt
.gitignore
source code
documentation
package.json
package-lock.json
```

---

## 12. Current `.gitignore`

```gitignore
# =========================
# Python
# =========================
__pycache__/
*.py[cod]
*.pyo
*.pyd

# Virtual environments
.venv/
venv/
env/
ENV/

# =========================
# Environment / Secrets
# =========================
.env
.env.*
!.env.example

# =========================
# Testing / Coverage
# =========================
.pytest_cache/
.coverage
htmlcov/

# =========================
# IDE / Editors
# =========================
.vscode/
.idea/
*.swp
*.swo

# =========================
# OS
# =========================
.DS_Store
Thumbs.db

# =========================
# Node / React
# =========================
node_modules/
dist/
build/
.npm/
*.log

# =========================
# ML / Datasets
# =========================
data/*
!data/.gitkeep

models/*
!models/.gitkeep

# Hugging Face cache
.cache/
huggingface_cache/

# =========================
# Logs
# =========================
logs/

# =========================
# Database
# =========================
*.sqlite
*.sqlite3
*.db
```

---

## 13. Frontend Decision

Use:

```text
React + Vite
```

React is the UI library/framework being used for the frontend.

Vite is the development/build tool used to create and run the React application.

Initial creation command:

```bash
npm create vite@latest frontend
```

Choose:

```text
Framework: React
Variant: JavaScript
```

---

## 14. Development Philosophy

This project has two goals:

### Primary goal
Build a working real-world application before October 3, 2026.

### Secondary goal
Understand what the components are doing instead of blindly copying code.

For example, while using Hugging Face, understand:

- Tokenization
- Token IDs
- Attention masks
- Embeddings
- BERT/Transformer architecture at a conceptual level
- Logits
- Softmax/probabilities
- Classification
- Fine-tuning vs inference
- Model evaluation

But do not implement BERT from scratch for this deadline.

---

## 15. AI/CLI Agent Usage

The preferred workflow is:

```text
Understand concept
      |
      v
Discuss/design implementation
      |
      v
Implement
      |
      v
Run/test
      |
      v
Debug
      |
      v
Understand why it works
```

Use ChatGPT primarily for:
- Concepts
- Architecture
- Mathematical explanations
- Design decisions
- Code review
- Debugging explanations
- Learning guidance

Use a CLI coding agent primarily for:
- File creation
- Boilerplate
- Refactoring
- Running tests
- Repetitive code changes
- Repository inspection
- Implementation assistance

Do not let an agent generate large sections of unexplained code just to make the project appear finished.

---

## 16. Current Status

### Decisions already made
- Project name established.
- React + Vite chosen for frontend.
- Flask chosen for backend.
- Hugging Face BERT-based models chosen for NLP.
- PostgreSQL chosen for database.
- Render chosen for deployment.
- Python `.venv` will be used.
- `.env` will hold secrets/configuration locally.
- `.env.example` will be committed.
- Git repository will be used.
- From-scratch BERT/GPT implementation is explicitly postponed until after the current project deadline.

### Not yet completed / next setup tasks
1. Create the project directory.
2. Create the repository structure.
3. Initialize Git.
4. Create Python `.venv`.
5. Install/verify Python dependencies.
6. Install PostgreSQL locally.
7. Create `fake_news_db`.
8. Generate/configure the Flask secret key.
9. Create the Flask application skeleton.
10. Create the React + Vite frontend.
11. Decide/select the exact Hugging Face fake-news model.
12. Decide/select the exact Hugging Face sentiment model.
13. Implement model inference.
14. Build Flask API endpoints.
15. Connect PostgreSQL.
16. Build React UI.
17. Connect React to Flask.
18. Add tests.
19. Test locally end-to-end.
20. Deploy to Render.
21. Document the project.

---

## 17. Rules for Future Sessions

When continuing this project in a new chat:

1. Read `CURRENT_STATE.md` first.
2. Treat established decisions as the current source of truth.
3. Do not replace the stack without discussing the change.
4. Do not introduce unnecessary technologies just because they are popular.
5. Keep the October 3, 2026 deadline in mind.
6. Prefer simple, maintainable implementations over unnecessary complexity.
7. Explain important ML concepts while implementing them.
8. Do not implement BERT from scratch for this project.
9. Keep the from-scratch ML/GPT learning project separate.
10. Update this file whenever a major architecture, dependency, workflow, or project-state decision changes.

---

## 18. Immediate Next Step

The next practical task is to create the actual repository structure and initialize Git.

After that, proceed in small verified steps rather than generating the entire application at once.
