# 🛡️ Product Review Guardian (PRG)

**Product Review Guardian (PRG)** is an AI-powered backend service built using **FastAPI**, designed to analyze user product reviews for:

- **Sentiment Score**
- **Spam Detection**
- **Toxicity Detection**
- **AI-Generated Summaries**

It also includes a full **authentication system**, **JWT support**, **database models**, and **complete CRUD operations**.

---

# 🚀 Features

### 🔐 Authentication & Users
- User Registration  
- Login with JWT  
- Protected Routes  
- Supports role-based access (user/admin)

### 📝 Product Reviews
- Create reviews  
- Update / Patch reviews  
- Delete reviews  
- List + fetch individual reviews  
- Reviews automatically analyzed using AI

### 🤖 AI Capabilities
- Sentiment analysis  
- Spam detection  
- Toxicity analysis  
- Auto-summary generation  

*(Located in `app/ai/ai_service.py` — easily replaceable with real models.)*

### 🧱 Clean Architecture
- Async SQLAlchemy ORM  
- Pydantic v2 schemas  
- Dependency injection  
- Modular routing  
- Fully structured folders

### 🐳 Production Friendly
- Dockerfile included  
- Environment variables support  
- Tests included  
- Perfect for GitHub PR workflow  

---

# 📁 Project Structure

```
product-review-guardian/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── deps.py
│   ├── auth.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py
│   │   └── review_routes.py
│   └── ai/
│       ├── __init__.py
│       └── ai_service.py
│
├── tests/
│   └── test_basic.py
│
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
└── README.md
```

---

# 🛠️ Setup Instructions

## 1️⃣ Clone Repository
```
git clone https://github.com/<your-username>/product-review-guardian.git
cd product-review-guardian
```

---

## 2️⃣ Create a Virtual Environment

### Windows:
```
python -m venv .venv
.venv\Scripts\activate
```

### macOS/Linux:
```
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3️⃣ Install Dependencies
```
pip install -r requirements.txt
```

---

## 4️⃣ Configure Environment Variables

Create `.env` file:

```
cp .env.example .env
```

Edit with your values:

```
DATABASE_URL=sqlite+aiosqlite:///./prg.db
SECRET_KEY=replace_with_secure_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## 5️⃣ Run the Server

```
uvicorn app.main:app --reload
```

Your API is now running 🎉

- API Root → http://127.0.0.1:8000  
- Interactive Docs → http://127.0.0.1:8000/docs  

---

# 🔐 Authentication Flow

### Register User  
`POST /auth/register`

### Login  
`POST /auth/token`

Copy your `access_token` → click **Authorize** in Swagger → paste token.

---

# 🧪 Running Tests

```
pytest -q
```

---

# 🤖 AI Integration (Customizable)

The AI logic exists in:

```
app/ai/ai_service.py
```

You can plug in:

- HuggingFace Transformers  
- OpenAI / Cohere APIs  
- Local BERT model  
- Any ML pipeline  

---

# 🐳 Run Using Docker

```
docker build -t prg .
docker run -p 8000:80 prg
```

---

# 🤝 Git Workflow (Recommended)

1. Create branch  
2. Write code  
3. `git add . && git commit`  
4. `git push`  
5. Open Pull Request  
6. Teammate reviews  
7. Merge into main  

---

# 📌 Future Enhancements
- Product CRUD API  
- Review clustering (Embeddings)  
- Fraud detection  
- Admin dashboard  
- Background tasks  
- Celery + Redis  
- Real AI models  

---

# 📄 License
MIT License.
