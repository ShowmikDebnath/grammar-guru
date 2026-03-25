from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.schemas import GrammarRequest, GrammarResponse
from app.checker import check_grammar



# ─────────────────────────────────────────
# App Setup
# ─────────────────────────────────────────
app = FastAPI(
    title="Grammar Guru API",
    description="AI powered grammar checker that teaches you from your mistakes!",
    version="1.0.0"
)



# ─────────────────────────────────────────
# Root
# ─────────────────────────────────────────
@app.get("/")
def root():
    return {
        "name": "Grammar Guru API 📝",
        "version": "1.0.0",
        "description": "Send your text and learn from your grammar mistakes!",
        "endpoints": {
            "check grammar": "POST /check-grammar",
            "health check": "GET /health"
        }
    }




# ─────────────────────────────────────────
# Health Check
# ─────────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok"}




# ─────────────────────────────────────────
# Main Endpoint — Grammar Check
# ─────────────────────────────────────────
@app.post("/check-grammar")
def grammar_check(request: GrammarRequest):

    # Call checker function
    result = check_grammar(request.text)

    # If error returned
    if isinstance(result, dict) and "error" in result:
        return JSONResponse(
            status_code=400,
            content=result
        )

    # Return successful response
    return result










