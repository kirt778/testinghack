import json
import glob
from typing import List, Dict, Any
from shared.schema import UserProfile, SchemeMatch

def load_all_schemes(schemes_dir: str = "data_engine/schemes/*.json") -> List[Dict[str, Any]]:
    schemes = []
    for filepath in glob.glob(schemes_dir):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Handle both single JSON objects {...} and lists of objects [...]
                if isinstance(data, dict) and "eligibility_rules" in data:
                    schemes.append(data)
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and "eligibility_rules" in item:
                            schemes.append(item)
                else:
                    print(f"[SKIPPED] {filepath} does not match the scheme format.")
        except Exception as e:
            print(f"[ERROR] Could not read {filepath}: {e}")
    return schemes

def evaluate_single_scheme(profile: UserProfile, scheme: Dict[str, Any]) -> SchemeMatch:
    rules = scheme["eligibility_rules"]
    reasons = []
    missing_fields = []
    is_disqualified = False

    if rules.get("min_age") is not None or rules.get("max_age") is not None:
        if profile.age is None:
            missing_fields.append("age")
        else:
            if rules.get("min_age") is not None and profile.age < rules["min_age"]:
                is_disqualified = True
                reasons.append(f"Minimum age required is {rules['min_age']} (user is {profile.age}).")
            elif rules.get("max_age") is not None and profile.age > rules["max_age"]:
                is_disqualified = True
                reasons.append(f"Maximum age allowed is {rules['max_age']} (user is {profile.age}).")
            else:
                reasons.append(f"Age ({profile.age}) meets the scheme criteria.")

    allowed_genders = [g.lower() for g in rules.get("allowed_genders", [])]
    if allowed_genders and len(allowed_genders) < 3:
        if profile.gender is None:
            missing_fields.append("gender")
        elif profile.gender.lower() not in allowed_genders:
            is_disqualified = True
            reasons.append(f"Scheme is restricted to {', '.join(allowed_genders)} applicants.")
        else:
            reasons.append(f"Gender ({profile.gender}) matches eligibility.")

    allowed_states = [s.lower() for s in rules.get("allowed_states", ["All"])]
    if "all" not in allowed_states:
        if profile.state is None:
            missing_fields.append("state")
        elif profile.state.lower() not in allowed_states:
            is_disqualified = True
            reasons.append(f"Only available in {', '.join(rules['allowed_states'])} (user is in {profile.state}).")
        else:
            reasons.append(f"Resident of eligible state ({profile.state}).")

    allowed_occ = [o.lower() for o in rules.get("allowed_occupations", [])]
    if allowed_occ and "all" not in allowed_occ:
        if profile.occupation is None:
            missing_fields.append("occupation")
        elif profile.occupation.lower() not in allowed_occ:
            is_disqualified = True
            reasons.append(f"Requires occupation in {rules['allowed_occupations']} (user is {profile.occupation}).")
        else:
            reasons.append(f"Occupation ({profile.occupation}) qualifies.")

    if rules.get("max_annual_income") is not None:
        if profile.income is None:
            missing_fields.append("income")
        elif profile.income > rules["max_annual_income"]:
            is_disqualified = True
            reasons.append(f"Annual income (₹{profile.income}) exceeds limit of ₹{rules['max_annual_income']}.")
        else:
            reasons.append(f"Annual income (₹{profile.income}) is within the ₹{rules['max_annual_income']} cap.")

    allowed_cats = [c.lower() for c in rules.get("allowed_categories", [])]
    if allowed_cats and len(allowed_cats) < 4:
        if profile.category is None:
            missing_fields.append("category")
        elif profile.category.lower() not in allowed_cats:
            is_disqualified = True
            reasons.append(f"Restricted to {', '.join(rules['allowed_categories'])} categories.")
        else:
            reasons.append(f"Category ({profile.category}) is eligible.")

    if rules.get("requires_land_ownership") is not None:
        if profile.owns_land is None:
            missing_fields.append("owns_land")
        elif profile.owns_land != rules["requires_land_ownership"]:
            is_disqualified = True
            req_str = "must own cultivable land" if rules["requires_land_ownership"] else "must be landless"
            reasons.append(f"Applicant {req_str}.")
        else:
            reasons.append("Land ownership status meets requirement.")

    if is_disqualified:
        status = "not_eligible"
    elif len(missing_fields) > 0:
        status = "possibly_eligible"
        reasons.append(f"Missing details to confirm eligibility: {', '.join(missing_fields)}.")
    else:
        status = "eligible"

    return SchemeMatch(
        scheme_id=scheme["scheme_id"],
        scheme_name=scheme["scheme_name"],
        status=status,
        reasons=reasons,
        missing_fields=missing_fields,
        benefits_summary=scheme["benefits_summary"],
        documents_required=scheme["documents_required"],
        application_steps=scheme["application_steps"],
        source_url=scheme["source_url"],
        date_checked=scheme["date_checked"]
    )

def evaluate_schemes(profile: UserProfile) -> List[SchemeMatch]:
    schemes = load_all_schemes()
    return [evaluate_single_scheme(profile, s) for s in schemes]

STATE_CSC_PORTALS = {
    "karnataka": "Karnataka One / Bangalore One / Bapuji Seva Kendra (sevasindhu.karnataka.gov.in)",
    "tamil nadu": "TNeGA e-Sevai Centre (tnesevai.tn.gov.in)",
    "west bengal": "Duare Sarkar Camp / Bangla Sahayata Kendra (bsk.wb.gov.in)",
    "maharashtra": "Aaple Sarkar Seva Kendra / Maha e-Seva (aaplesarkar.mahaonline.gov.in)",
    "madhya pradesh": "MP Online Kiosk / Lok Seva Kendra (mponline.gov.in)",
    "uttar pradesh": "UP Jan Seva Kendra / e-District CSC (edistrict.up.gov.in)",
    "telangana": "MeeSeva Centre (tg.meeseva.gov.in)",
    "odisha": "Mo Seba Kendra / Odisha One (odishaone.gov.in)",
    "rajasthan": "e-Mitra Kiosk (emitra.rajasthan.gov.in)"
}

def get_nearest_csc_guidance(state: str = None) -> dict:
    """Provides guidance to the nearest Common Service Centre (CSC) for application help."""
    state_key = (state or "").strip().lower()
    state_center = STATE_CSC_PORTALS.get(state_key, "Digital Seva Common Service Centre (CSC)")
    return {
        "center_name": state_center,
        "locator_url": "https://locator.csccloud.in/",
        "helpline": "14599 (CSC Toll-Free Helpline)",
        "instructions": (
            f"Visit your nearest {state_center} with original documents from the checklist above. "
            "Operators can scan your documents and submit the online form on your behalf."
        )
    }
