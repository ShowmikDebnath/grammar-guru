# 📝 Grammar Guru API

An AI powered grammar checker that doesn't just correct your 
mistakes — it teaches you WHY they are wrong, so you can learn 
and improve your English writing skills.

> Built with FastAPI + Groq + LLaMA 3.3

---

## 💡 Why Grammar Guru?

| Tool | Corrects | Explains | Teaches |
|------|----------|----------|---------|
| Grammarly | ✅ | ❌ | ❌ |
| ChatGPT | ✅ | Sometimes | ❌ |
| Grammar Guru | ✅ | ✅ | ✅ |

Grammar Guru is built for **students and learners** who want 
to understand their mistakes, not just get a corrected version.

---

## 🛠️ Tech Stack

- **Python 3.11**
- **FastAPI** — web framework
- **Groq API** — fast LLM inference
- **LLaMA 3.3 70B** — Meta's open source AI model
- **Pydantic** — data validation
- **python-dotenv** — environment variables

---

## 📁 Project Structure
```
grammar-guru/
├── app/
│   ├── __init__.py
│   ├── main.py       # API routes
│   ├── schemas.py    # Input/output structure
│   └── checker.py    # AI grammar checking logic
├── .env              # API keys (never pushed!)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

**1. Clone the repo**
```bash
git clone https://github.com/ShowmikDebnath/grammar-guru.git
cd grammar-guru
```

**2. Create virtual environment**
```bash
python3.11 -m venv myenv
source myenv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create `.env` file**
```
GROQ_API_KEY=your-groq-api-key-here
```
Get your free API key at: console.groq.com

**5. Run the server**
```bash
uvicorn app.main:app --reload
```

**6. Open Swagger UI**
```
http://127.0.0.1:8000/docs
```

---

## 📌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome + available endpoints |
| GET | `/health` | Server health check |
| POST | `/check-grammar` | Check grammar and learn from mistakes |

---

## 📥 Example Request
```json
POST /check-grammar

{
  "text": "I are going to school yesterday and I buyed a book."
}
```

## 📤 Example Response
```json
{
  "original": "I are going to school yesterday and I buyed a book.",
  "corrected": "I was going to school yesterday and I bought a book.",
  "mistakes": [
    {
      "mistake": "I are",
      "correction": "I was",
      "explanation": "Use 'was' for singular subjects in past tense."
    },
    {
      "mistake": "buyed",
      "correction": "bought",
      "explanation": "Irregular verb — past tense of 'buy' is 'bought'."
    }
  ],
  "score": "60/100",
  "summary": "2 mistakes found. Focus on past tense verb forms."
}
```

---

## ⚠️ Current Limitations

- Maximum 1000 characters per request
- No user accounts or history yet
- API only — no frontend yet
- Free tier API limits apply

---

## 🗺️ Roadmap

- [ ] User authentication
- [ ] Save mistake history
- [ ] Track improvement over time
- [ ] Frontend web interface
- [ ] Mobile app support
- [ ] Deploy to cloud

---

## 👨‍💻 Author

**Showmik Debnath**
- GitHub: [@ShowmikDebnath](https://github.com/ShowmikDebnath)
- LinkedIn: [showmikdebnath](https://linkedin.com/in/showmikdebnath)
