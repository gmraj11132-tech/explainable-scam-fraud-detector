"""
Explainable AI (XAI) Engine for Scam Detection.
Provides token-level feature attribution, behavioral heuristic breakdowns,
and contextual actionable advice.
"""

import re
import numpy as np
from ml_engine.url_features import extract_url_features

# Rule-based threat pattern dictionaries for deep heuristic explanation (English & Hinglish)
THREAT_PATTERNS = {
    "urgency": {
        "title": "Urgency & Fear Coercion",
        "description": "Scammers manufacture artificial urgency to force victims into acting without thinking.",
        "regex": r'\b(immediately|urgent|urgently|within 24 hours|today itself|tonight|blocked today|suspended|freeze|expire|deadline|act now|last chance|turant|jaldi|aaj hi|aaj raat|kal tak|band ho|kat di|khatam|seize|arrest)\b',
        "severity": "High"
    },
    "credential_harvesting": {
        "title": "Sensitive Information Harvesting",
        "description": "Attempts to solicit confidential financial or identity credentials.",
        "regex": r'\b(otp|password|pin|cvv|aadhaar|pan card|pan|netbanking|login credentials|verify account|update kyc|kyc update|bank details|credit card details|debit card|atm card|card number|16 digit|khata|bank account|upi pin|mpin)\b',
        "severity": "Critical"
    },
    "unrealistic_rewards": {
        "title": "Unrealistic Rewards & Lottery Lure",
        "description": "Offers exorbitant monetary returns, prizes, or gifts with little to no effort.",
        "regex": r'\b(won|winner|lottery|lucky draw|free gift|cash bonus|earn \d+ daily|double your money|100% profit|guaranteed returns|jita|jite|inaam|badhai|free recharge|kamaye|daily payout|usdt|crypto profit)\b',
        "severity": "High"
    },
    "utility_threat": {
        "title": "Essential Service Disconnection Threat",
        "description": "Threatens immediate cut-off of electricity, gas, water, or mobile service.",
        "regex": r'\b(electricity|bijli|power cut|power house|bill not updated|bill unpaid|disconnected|disconnection|power disconnected|kat di jayegi|kat jayegi|gas supply|pipeline service|sim block|sim service)\b',
        "severity": "High"
    },
    "authority_impersonation": {
        "title": "Brand / Authority Impersonation",
        "description": "Pretends to represent trusted entities like banks, government, or courier services.",
        "regex": r'\b(rbi|sbi|hdfc|icici|axis bank|income tax|cyber crime|police|cbi|narcotics|fedex|dhl|india post|bluedart|traffic police|e-challan|challan|microsoft|apple|netflix|amazon hr)\b',
        "severity": "Medium"
    },
    "fee_advance": {
        "title": "Advance Fee / Delivery Surcharge Request",
        "description": "Asks for a minor upfront processing fee to release a parcel or unlock earnings.",
        "regex": r'\b(delivery fee|customs fee|registration deposit|processing charge|unpaid duty|pay rs \d+|file charge|advance fee|deposit fee)\b',
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
    Calculate mathematical feature attribution (importance score) for individual words in the input.
    - Logistic Regression: Uses linear log-odds coefficients (coef_[0])
    - Naive Bayes: Uses log-likelihood ratio (feature_log_prob_[1] - feature_log_prob_[0])
    - Random Forest: Uses ensemble feature importance weighted by TF-IDF presence
    """
    if vectorizer is None or model is None:
        return []

    feature_names = vectorizer.get_feature_names_out()
    feature_to_idx = {feat: idx for idx, feat in enumerate(feature_names)}
    words = re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())
    attributions = []
    seen = set()

    # 1. Logistic Regression: Linear Coefficients
    if hasattr(model, 'coef_') and len(model.coef_) > 0:
        coefficients = model.coef_[0]
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

    # 2. Multinomial Naive Bayes: Log-Likelihood Ratio
    elif hasattr(model, 'feature_log_prob_') and len(model.feature_log_prob_) > 1:
        log_prob_scam = model.feature_log_prob_[1]
        log_prob_legit = model.feature_log_prob_[0]
        for word in words:
            if word in seen:
                continue
            seen.add(word)
            if word in feature_to_idx:
                idx = feature_to_idx[word]
                # Log-odds ratio: positive means more likely scam, negative means legitimate
                weight = float(log_prob_scam[idx] - log_prob_legit[idx])
                attributions.append({
                    "word": word,
                    "weight": round(weight, 4),
                    "impact": "scam" if weight > 0 else "legitimate"
                })

    # 3. Random Forest: Feature Importances
    elif hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        # Transform document to get TF-IDF weights
        doc_vec = vectorizer.transform([text]).toarray()[0]
        for word in words:
            if word in seen:
                continue
            seen.add(word)
            if word in feature_to_idx:
                idx = feature_to_idx[word]
                importance = float(importances[idx] * doc_vec[idx] * 50.0)
                # Determine impact based on word frequency in threat indicators
                is_scam_pattern = any(word in p["regex"] for p in THREAT_PATTERNS.values())
                attributions.append({
                    "word": word,
                    "weight": round(importance if is_scam_pattern else -importance, 4),
                    "impact": "scam" if is_scam_pattern or importance > 0.05 else "legitimate"
                })

    # Fallback for out-of-vocabulary heuristic words
    if len(attributions) < 3:
        for w in set(words):
            if w not in seen:
                for key, p in THREAT_PATTERNS.items():
                    if re.search(r'\b' + re.escape(w) + r'\b', p["regex"], re.IGNORECASE):
                        attributions.append({
                            "word": w,
                            "weight": 0.65 if p["severity"] == "Critical" else 0.40,
                            "impact": "scam"
                        })
                        seen.add(w)

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
        recommendations.append("Low risk indicators detected. The communication conforms to standard conversational or transactional patterns.")
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

    deduped = []
    for r in recommendations:
        if r not in deduped:
            deduped.append(r)
    return deduped

def calculate_calibrated_probability(model_name: str, model, X_vec) -> float:
    """
    Computes mathematically calibrated class probability for text.
    - Logistic Regression: Direct logistic sigmoid probability
    - Naive Bayes: Temperature-scaled log-likelihood to prevent extreme 0%/100% saturation
    - Random Forest: Platt-style threshold calibration for sparse decision tree voting
    """
    try:
        raw_p = float(model.predict_proba(X_vec)[0][1])
    except Exception:
        raw_p = 0.5

    if model_name == "Random Forest":
        # Platt / threshold calibration for sparse short-text tree ensemble
        scaled = 1.0 / (1.0 + np.exp(-14.0 * (raw_p - 0.22)))
        return float(scaled)
    elif model_name == "Naive Bayes":
        # Temperature smoothing on joint log-likelihood
        try:
            log_prob = model.predict_log_proba(X_vec)[0]
            temp = 2.8
            exp_scaled = np.exp(log_prob / temp)
            smoothed_p = exp_scaled[1] / np.sum(exp_scaled)
            return float(smoothed_p)
        except Exception:
            return raw_p
    else:
        return raw_p

def explain_prediction(text: str, ml_probability: float, vectorizer, model, all_models=None) -> dict:
    """
    Main XAI evaluation function combining ML probabilities,
    token-level attribution, cognitive heuristics, and multi-model consensus.
    """
    signals = analyze_heuristic_signals(text)
    embedded_urls = extract_and_analyze_embedded_urls(text)
    token_weights = compute_token_attributions(text, vectorizer, model)

    # Multi-model consensus comparison (Calculated with dynamic calibration)
    model_comparisons = {}
    if all_models and vectorizer:
        try:
            X_vec = vectorizer.transform([text])
            for m_name, m_obj in all_models.items():
                p = calculate_calibrated_probability(m_name, m_obj, X_vec)
                model_comparisons[m_name] = round(p * 100, 1)
        except Exception:
            pass

    # Dynamic composite risk calculation
    heuristic_penalty = sum(25 if s["severity"] == "Critical" else 18 if s["severity"] == "High" else 10 for s in signals)
    url_penalty = max([u["risk_score"] for u in embedded_urls], default=0) * 0.40

    # If ML probability is decisive (> 0.70 or < 0.25), give it primary authority (70%)
    if ml_probability > 0.70 or ml_probability < 0.25:
        raw_score = (ml_probability * 100 * 0.75) + (min(60, heuristic_penalty) * 0.15) + (url_penalty * 0.10)
    else:
        raw_score = (ml_probability * 100 * 0.55) + (min(100, heuristic_penalty) * 0.30) + (url_penalty * 0.15)

    # Ensure clean conversational messages have low scores
    if len(signals) == 0 and len(embedded_urls) == 0 and ml_probability < 0.40:
        raw_score = min(raw_score, ml_probability * 60)

    calibrated_risk = int(min(100, max(1, round(raw_score))))

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
        "model_comparisons": model_comparisons,
        "signals": signals,
        "embedded_urls": embedded_urls,
        "token_weights": token_weights,
        "recommendations": recommendations,
        "disclaimer": "This system provides automated probabilistic threat estimation and heuristic explanation. A high score signifies significant indicators of deception, not absolute judicial proof."
    }
