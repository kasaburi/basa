# -------------------------
# CATEGORIES (AI labels)
# -------------------------
CATEGORIES = [
    "road damage",
    "garbage",
    "lighting issue",
    "water leak",
    "other"
]

# -------------------------
# MAP (LABEL → DB ID)
# -------------------------
CATEGORY_MAP = {
    "road damage": 1,
    "garbage": 2,
    "lighting issue": 3,
    "water leak": 4,
    "other": 5
}

# -------------------------
# KEYWORDS (SCALABLE RULES)
# -------------------------
KEYWORDS = {
    "road damage": ["გზა", "ორმო", "ასფალტი", "დაზიანებული გზა"],
    "garbage": ["ნაგავი", "დასუფთავება", "ბინძური"],
    "lighting issue": ["სინათლე", "ლამპა", "ბოძი", "განათება"],
    "water leak": ["წყალი", "გაჟონვა", "მილი"]
}

# -------------------------
# 1. RULE-BASED (FAST)
# -------------------------
import re

def normalize(text: str) -> str:
    """Clean and normalize input text"""
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def rule_based(text: str):
    text = normalize(text)

    for category, keywords in KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return category

    return "other"


# -------------------------
# 2. AI MODEL (FALLBACK - OPTIONAL)
# -------------------------
def ai_model_predict(text: str):
    """
    Placeholder for future ML / NLP model.
    Example: HuggingFace model or OpenAI API
    """
    return "other"


# -------------------------
# 3. MAIN FUNCTION
# -------------------------
def suggest_category(text: str) -> int:
    """
    Returns category DB ID
    """

    # 1. FAST RULE-BASED
    label = rule_based(text)

    # 2. FALLBACK TO AI (if needed)
    if label == "other":
        label = ai_model_predict(text)

    # 3. RETURN DB ID
    return CATEGORY_MAP.get(label, CATEGORY_MAP["other"])