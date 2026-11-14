import json
import os

SCHEMES = [
    {
        "scheme_id": "pm_kisan",
        "scheme_name": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
        "ministry": "Ministry of Agriculture and Farmers Welfare",
        "state_specific": "All India",
        "benefits_summary": "Financial support of ₹6,000 per year in three equal installments of ₹2,000 every 4 months directly into the farmer's bank account.",
        "eligibility_rules": {
            "min_age": 18,
            "max_age": None,
            "allowed_genders": ["male", "female", "other"],
            "allowed_states": ["All"],
            "allowed_occupations": ["farmer", "agriculture"],
            "max_annual_income": None,
            "allowed_categories": ["General", "OBC", "SC", "ST"],
            "requires_land_ownership": True
        },
        "exclusions": [
            "Institutional landholders",
            "Families where a member paid income tax in the last assessment year"
        ],
        "documents_required": [
            "Official Identity Proof",
            "Land ownership papers (Khasra / Khatauni)",
            "Active bank account passbook"
        ],
        "application_steps": [
            "Visit the official PM-KISAN portal or your nearest Common Service Centre (CSC).",
            "Click 'New Farmer Registration' under Farmers Corner.",
            "Enter state, district, and landholding details, then submit."
        ],
        "source_url": "https://www.myscheme.gov.in/schemes/pm-kisan",
        "date_checked": "2026-11-14"
    },
    {
        "scheme_id": "ayushman_bharat",
        "scheme_name": "Ayushman Bharat - Pradhan Mantri Jan Arogya Yojana (AB-PMJAY)",
        "ministry": "Ministry of Health and Family Welfare",
        "state_specific": "All India",
        "benefits_summary": "Health insurance cover of up to ₹5,00,000 per family per year for secondary and tertiary care hospitalization at empaneled public and private hospitals.",
        "eligibility_rules": {
            "min_age": None,
            "max_age": None,
            "allowed_genders": ["male", "female", "other"],
            "allowed_states": ["All"],
            "allowed_occupations": ["All"],
            "max_annual_income": 250000,
            "allowed_categories": ["General", "OBC", "SC", "ST"],
            "requires_land_ownership": None
        },
        "exclusions": [
            "Households paying income tax or owning a four-wheeler vehicle"
        ],
        "documents_required": [
            "Government-issued Identity Card",
            "Ration Card or Family Income Certificate",
            "Active Mobile Number"
        ],
        "application_steps": [
            "Check eligibility on the official PM-JAY portal or at an empaneled hospital.",
            "Visit the nearest Common Service Centre (CSC) or Ayushman Mitra desk with family ID documents.",
            "Complete verification to receive your Ayushman Card."
        ],
        "source_url": "https://www.myscheme.gov.in/schemes/ab-pmjay",
        "date_checked": "2026-11-14"
    },
    {
        "scheme_id": "pm_svanidhi",
        "scheme_name": "PM Street Vendor's AtmaNirbhar Nidhi (PM SVANidhi)",
        "ministry": "Ministry of Housing and Urban Affairs",
        "state_specific": "All India",
        "benefits_summary": "Collateral-free working capital loan up to ₹10,000 for 1 year (expandable to ₹20,000 and ₹50,000 on timely repayment) with a 7% interest subsidy.",
        "eligibility_rules": {
            "min_age": 18,
            "max_age": 65,
            "allowed_genders": ["male", "female", "other"],
            "allowed_states": ["All"],
            "allowed_occupations": ["street_vendor", "hawker", "vendor"],
            "max_annual_income": None,
            "allowed_categories": ["General", "OBC", "SC", "ST"],
            "requires_land_ownership": None
        },
        "exclusions": [
            "Non-vending business owners with permanent commercial shops"
        ],
        "documents_required": [
            "Certificate of Vending or Letter of Recommendation from Urban Local Body (ULB)",
            "Voter ID, Driving License, MNREGA Card, or PAN Card",
            "Bank Account Passbook"
        ],
        "application_steps": [
            "Visit the official PM SVANidhi portal or nearest Common Service Centre (CSC).",
            "Verify your mobile number and check your vendor survey category status.",
            "Fill out the online loan application form, upload your Vending Certificate/ID, and select a preferred lender."
        ],
        "source_url": "https://www.myscheme.gov.in/schemes/pm-svanidhi",
        "date_checked": "2026-11-14"
    }
]

os.makedirs("data_engine/schemes", exist_ok=True)
for s in SCHEMES:
    with open(f"data_engine/schemes/{s['scheme_id']}.json", "w", encoding="utf-8") as f:
        json.dump(s, f, indent=2, ensure_ascii=False)

print("Successfully created 3 starter scheme JSON files in data_engine/schemes/!")
