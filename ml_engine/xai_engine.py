"""
Explainable AI (XAI) Engine for Scam Detection.
Provides token-level feature attribution, behavioral heuristic breakdowns,
and contextual actionable advice.
"""

import re
import numpy as np
from ml_engine.url_features import extract_url_features

# Rule-based threat pattern dictionaries for deep heuristic explanation
THREAT_PATTERNS = {
    "urgency": {
        "title": "Urgency & Fear Coercion",
        "description": "Scammers manufacture artificial urgency to force victims into acting without thinking.",
        "regex": r'\b(immediately|urgent|urgently|within 24 hours|today itself|tonight|blocked today|suspended|freeze|expire|deadline|act now|last chance)\b',
        "severity": "High"
    },
    "credential_harvesting": {
        "title": "Sensitive Information Harvesting",
        "description": "Attempts to solicit confidential financial or identity credentials.",
        "regex": r'\b(otp|password|pin|cvv|aadhaar|pan card|netbanking|login credentials|verify account|update kyc|bank details|credit card details)\b',
        "severity": "Critical"
    },
    "unrealistic_rewards": {
        "title": "Unrealistic Rewards & Lottery Lure",
        "description": "Offers exorbitant monetary returns, prizes, or gifts with little to no effort.",
        "regex": r'\b(won|winner|lottery|lucky draw|free gift|cash bonus|earn \d+ daily|double your money|100% profit|guaranteed returns)\b',
        "severity": "High"
    },
    "utility_threat": {
        "title": "Essential Service Disconnection Threat",
        "description": "Threatens immediate cut-off of electricity, gas, water, or mobile service.",
        "regex": r'\b(electricity power will be disconnected|power cut|disconnected tonight|gas supply|bill not updated|power house|officer at)\b',
        "severity": "High"
    },
    "authority_impersonation": {
        "title": "Brand / Authority Impersonation",
        "description": "Pretends to represent trusted entities like banks, government, or courier services.",
        "regex": r'\b(rbi|sbi|hdfc|income tax|cyber crime|police|fedex|dhl|india post|microsoft support|apple support|netflix)\b',
        "severity": "Medium"
    },
    "fee_advance": {
        "title": "Advance Fee / Delivery Surcharge Request",
        "description": "Asks for a minor upfront processing fee to release a parcel or unlock earnings.",
        "regex": r'\b(delivery fee|customs fee|registration deposit|processing charge|unpaid duty|pay rs \d+)\b',
        "severity": "High"
    }
}

URL_REGEX = r'(https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9.-]+\.(?:com|org|in|net|xyz|top|club|info|buzz|tk|ml|cf|gq|work|rest|link)/[^\s]*)'

def analyze_heuristic_signals(text: str) -> list:
    """Analyze text for cognitive and cyber-attack deception signals."""
    text_lower = text.lower()
    signals = []

    for key, spec in THREAT_PATTERNS.items():
        matches = list(set(re.findall(spec["regex"], text_lower, re.IGNORECASE)))
        if matches:
            signals.append({
                "category": key,
                "title": spec["title"],
                "description": spec["description"],
                "severity": spec["severity"],
                "matched_terms": matches[:5]
            })

    return signals

def extract_and_analyze_embedded_urls(text: str) -> list:
    """Extract any URLs present inside a message and run structural inspection."""
    found_urls = re.findall(URL_REGEX, text)
    url_reports = []
    for raw_url in found_urls:
        clean_url = raw_url.rstrip('.,;!?')
        url_report = extract_url_features(clean_url)
        url_reports.append(url_report)
    return url_reports

def compute_token_attributions(text: str, vectorizer, model) -> list:
    """
    Calculate feature attribution (importance score) for individual words in the input.
    Provides local explainability (XAI) similar to linear LIME / SHAP.
    """
    if not hasattr(model, 'coef_'):
        # If model doesn't have linear coefficients (e.g., Random Forest),
        # return frequency-weighted heuristic word importances
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        results = []
        for w in set(words):
            if any(w in p["regex"] for p in THREAT_PATTERNS.values()):
                results.append({"word": w, "weight": 0.45, "impact": "scam"})
        return sorted(results, key=lambda x: abs(x["weight"]), reverse=True)[:10]

    feature_names = vectorizer.get_feature_names_out()
    feature_to_idx = {feat: idx for idx, feat in enumerate(feature_names)}
    coefficients = model.coef_[0]

    words = re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())
    attributions = []
    seen = set()

    for word in words:
        if word in seen:
            continue
        seen.add(word)
        if word in feature_to_idx:
            idx = feature_to_idx[word]
            weight = float(coefficients[idx])
            attributions.append({
                "word": word,
                "weight": round(weight, 4),
                "impact": "scam" if weight > 0 else "legitimate"
            })

    # Sort by absolute magnitude of importance
    attributions.sort(key=lambda item: abs(item["weight"]), reverse=True)
    return attributions[:15]

def generate_recommendations(signals: list, embedded_urls: list, risk_score: int) -> list:
    """Generate structured, context-aware cybersecurity advice for the user."""
    recommendations = []

    if risk_score >= 65:
        recommendations.append("Do NOT click any hyperlinks, dial provided phone numbers, or reply to this communication.")
        recommendations.append("If this claims to be from your bank, open the bank's official application directly or call the verified toll-free number printed on your card.")
    elif risk_score >= 30:
        recommendations.append("Exercise caution: This communication displays characteristics of unsolicited or persuasive social engineering.")
        recommendations.append("Verify the sender's identity through independent official channels before taking action.")
    else:
        recommendations.append("Low risk indicators detected. The communication conforms to standard transactional or conversational patterns.")
        recommendations.append("Security best practice: Never share One-Time Passwords (OTPs) or PINs with anyone.")

    for s in signals:
        if s["category"] == "credential_harvesting":
            recommendations.append("Legitimate financial institutions and government portals will never solicit passwords, PINs, or OTPs via SMS or messaging apps.")
        elif s["category"] == "utility_threat":
            recommendations.append("Official utility providers do not send disconnection threats from personal mobile numbers requesting immediate offline transfer.")
        elif s["category"] == "unrealistic_rewards":
            recommendations.append("Unprompted lottery winnings and prize claims without prior entry represent standard financial advance-fee lures.")

    for u in embedded_urls:
        if u.get("risk_score", 0) > 40:
            recommendations.append(f"Suspicious external destination detected ({u['domain']}). Avoid entering any personal credentials.")

    # Deduplicate while preserving order
    deduped = []
    for r in recommendations:
        if r not in deduped:
            deduped.append(r)
    return deduped

def explain_prediction(text: str, ml_probability: float, vectorizer, model) -> dict:
    """
    Main XAI evaluation function combining ML probabilities,
    token-level attribution, and cognitive threat heuristics.
    """
    signals = analyze_heuristic_signals(text)
    embedded_urls = extract_and_analyze_embedded_urls(text)
    token_weights = compute_token_attributions(text, vectorizer, model)

    # Heuristic adjustment score
    heuristic_penalty = sum(20 if s["severity"] == "Critical" else 14 if s["severity"] == "High" else 8 for s in signals)
    url_penalty = max([u["risk_score"] for u in embedded_urls], default=0) * 0.35

    # Composite calibrated risk calculation (ML probability 60%, Heuristics 25%, URL factors 15%)
    raw_score = (ml_probability * 100 * 0.60) + (min(100, heuristic_penalty) * 0.25) + (url_penalty)
    calibrated_risk = int(min(100, max(0, round(raw_score))))

    if calibrated_risk >= 65:
        verdict = "Scam / High Risk Fraud"
        verdict_badge = "danger"
    elif calibrated_risk >= 30:
        verdict = "Suspicious / Caution Advised"
        verdict_badge = "warning"
    else:
        verdict = "Legitimate / Safe Communication"
        verdict_badge = "success"

    recommendations = generate_recommendations(signals, embedded_urls, calibrated_risk)

    return {
        "verdict": verdict,
        "verdict_badge": verdict_badge,
        "risk_score": calibrated_risk,
        "ml_probability": round(ml_probability * 100, 2),
        "signals": signals,
        "embedded_urls": embedded_urls,
        "token_weights": token_weights,
        "recommendations": recommendations,
        "disclaimer": "This system provides automated probabilistic threat estimation and heuristic explanation. A high score signifies significant indicators of deception, not absolute judicial proof."
    }
