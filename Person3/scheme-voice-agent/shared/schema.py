# shared/contracts.py
CONTRACT_VERSION = "0.1"

from enum import Enum
from typing import Optional, Literal
from pydantic import BaseModel, Field

# ---------- Languages ----------
LANGS = ["hi", "ta", "pun", "kan","en"]

# ---------- Allowed values (Person 1 finalises these) ----------
class Gender(str, Enum):
    male = "male"; female = "female"; other = "other"

class Category(str, Enum):
    general = "general"; sc = "sc"; st = "st"; obc = "obc"

class Occupation(str, Enum):
    farmer = "farmer"; artisan = "artisan"; student = "student"
    street_vendor = "street_vendor"; daily_wage = "daily_wage"
    unemployed = "unemployed"; other = "other"

# ---------- The user profile ----------
# None = unknown. Never use 0 or "" for unknown.
class UserProfile(BaseModel):
    age: Optional[int] = Field(None, ge=0, le=120)
    gender: Optional[Gender] = None
    state: Optional[str] = None            # canonical name from STATES list
    is_rural: Optional[bool] = None
    occupation: Optional[Occupation] = None
    annual_income_inr: Optional[int] = Field(None, ge=0)
    category: Optional[Category] = None
    land_hectares: Optional[float] = Field(None, ge=0)
    # Add only fields that real scheme rules need.
    # Deliberately absent: aadhaar, phone, bank account, OTP.

# ---------- Eligibility output ----------
class RuleOutcome(BaseModel):
    field: str                              # which profile field this rule checked
    outcome: Literal["pass", "fail", "unknown"]
    explanation_en: str                     # plain-English sentence

class SchemeResult(BaseModel):
    scheme_id: str
    name: str
    status: Literal["eligible", "possibly_eligible", "not_eligible"]
    rule_outcomes: list[RuleOutcome]
    missing_fields: list[str]               # fields that would settle "unknown"
    benefits: str
    documents: list[str]
    steps: list[str]
    source_url: str
    date_checked: str                       # "YYYY-MM-DD"

class Chunk(BaseModel):
    scheme_id: str
    text: str
    source_url: str

class Transcript(BaseModel):
    text: str
    lang: str
    confidence: float                       # 0.0 to 1.0

# ---------- Function signatures (implemented by the owners) ----------
# Person 1  (knowledge/)
def check_eligibility(profile: UserProfile) -> list[SchemeResult]: ...
def required_fields(profile: UserProfile) -> list[str]: ...   # ranked, most useful first
def retrieve(query: str, scheme_id: Optional[str] = None, k: int = 4) -> list[Chunk]: ...

# Person 2  (voice/)
def transcribe(audio: bytes, lang_hint: Optional[str] = None) -> Transcript: ...
def translate(text: str, src: str, tgt: str) -> str: ...
def speak(text: str, lang: str) -> bytes: ...

# Person 3  (dialogue/)
def handle_turn(state: dict, user_text_en: str, lang: str) -> tuple[dict, str, list[SchemeResult]]: ...