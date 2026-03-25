from pydantic import BaseModel
from typing import List



# ─────────────────────────────────────────
# INPUT — what user sends to API
# ─────────────────────────────────────────
class GrammarRequest(BaseModel):
    text: str



# ─────────────────────────────────────────
# Each mistake found
# ─────────────────────────────────────────
class MistakeDetail(BaseModel):
    mistake: str        # wrong text
    correction: str     # correct text
    explanation: str    # why it's wrong



# ─────────────────────────────────────────
# OUTPUT — what API returns to user
# ─────────────────────────────────────────
class GrammarResponse(BaseModel):
    original: str               # user's original text
    corrected: str              # fully corrected text
    mistakes: List[MistakeDetail]  # list of mistakes
    score: str                  # e.g. "75/100"
    summary: str                # overall feedback


