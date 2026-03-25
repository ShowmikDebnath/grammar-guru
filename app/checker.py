from groq import Groq
from dotenv import load_dotenv
from app.schemas import GrammarResponse, MistakeDetail
import os
import json


load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))



# ─────────────────────────────────────────
# Limits
# ─────────────────────────────────────────
MIN_CHARACTERS = 10
MAX_CHARACTERS = 1000




# ─────────────────────────────────────────
# Validate input text
# ─────────────────────────────────────────
def validate_text(text: str):
    # Check if empty
    if not text.strip():
        return "Text cannot be empty!"

    # Check minimum length
    if len(text.strip()) < MIN_CHARACTERS:
        return f"Text too short! Please write at least {MIN_CHARACTERS} characters."

    # Check maximum length
    if len(text) > MAX_CHARACTERS:
        return f"Text too long! Maximum {MAX_CHARACTERS} characters allowed. Your text has {len(text)} characters."

    return None  # None means no error




# ─────────────────────────────────────────
# Main grammar checking function
# ─────────────────────────────────────────
def check_grammar(text: str):

    # Step 1 — Validate first
    error = validate_text(text)
    if error:
        return {"error": error}

    # Step 2 — Build the prompt
    prompt = f"""You are an expert English grammar teacher.
Analyze the following text for grammar mistakes.

Return ONLY a valid JSON object with exactly this structure, nothing else:
{{
    "corrected": "the fully corrected version of the text",
    "mistakes": [
        {{
            "mistake": "the wrong phrase from original text",
            "correction": "the correct version",
            "explanation": "simple explanation why it is wrong and how to remember the correct form"
        }}
    ],
    "score": "X/100",
    "summary": "brief overall feedback about the writing"
}}

Rules:
- If there are no mistakes, return empty list for mistakes and score 100/100
- Keep explanations simple and educational
- Focus on grammar, punctuation and sentence structure
- Do not add any text outside the JSON

Text to analyze:
\"\"\"{text}\"\"\"
"""


    # Step 3 — Send to Groq AI
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a grammar checking assistant. Always respond with valid JSON only. Never add explanation outside JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1  # low temperature = more consistent responses
        )

#temperature=0.0  →  very consistent, same answer every time
#temperature=0.1  →  mostly consistent ✅ (we use this)
#temperature=1.0  →  very creative, random answers

        # Step 4 — Get AI response text
        ai_response = response.choices[0].message.content.strip()


        # Step 5 — Clean response (remove markdown if AI adds it)
        if ai_response.startswith("```"):
            ai_response = ai_response.split("```")[1]
            if ai_response.startswith("json"):
                ai_response = ai_response[4:]

        # Step 6 — Parse JSON
        result = json.loads(ai_response)

        # Step 7 — Build mistakes list
        mistakes = []
        for m in result.get("mistakes", []):
            mistakes.append(MistakeDetail(
                mistake=m["mistake"],
                correction=m["correction"],
                explanation=m["explanation"]
            ))

        # Step 8 — Return final response
        return GrammarResponse(
            original=text,
            corrected=result["corrected"],
            mistakes=mistakes,
            score=result["score"],
            summary=result["summary"]
        )

    # Step 9 — Handle errors
    except json.JSONDecodeError:
        return {"error": "AI returned invalid response. Please try again."}
    except Exception as e:
        if "429" in str(e):
            return {"error": "Too many requests! Please wait a minute and try again."}
        return {"error": f"Something went wrong: {str(e)}"}
    

