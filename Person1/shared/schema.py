from pydantic import BaseModel
from typing import Optional, List, Literal

class UserProfile(BaseModel):
    age: Optional[int] = None
    gender: Optional[Literal["male", "female", "other"]] = None
    state: Optional[str] = None
    occupation: Optional[str] = None
    income: Optional[int] = None
    category: Optional[str] = None
    owns_land: Optional[bool] = None

class SchemeMatch(BaseModel):
    scheme_id: str
    scheme_name: str
    status: Literal["eligible", "possibly_eligible", "not_eligible"]
    reasons: List[str]
    missing_fields: List[str]
    benefits_summary: str
    documents_required: List[str]
    application_steps: List[str]
    source_url: str
    date_checked: str
