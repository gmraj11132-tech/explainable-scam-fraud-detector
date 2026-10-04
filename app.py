"""
Flask Backend Application for Explainable Multimodal Scam & Fraud Detection System.
Provides RESTful API endpoints for Text, URL, and Screenshot analysis,
Model Benchmarking, Forensics History, and Document Downloads.
"""

import os
import json
import joblib
from flask import Flask, request, jsonify, render_template, send_file
from werkzeug.utils import secure_filename

from ml_engine.url_features import extract_url_features
from ml_engine.xai_engine import explain_prediction
from ml_engine.image_analyzer import analyze_image_screenshot, DEMO_PRESETS
from ml_engine.ai_engine import inspect_live_url, analyze_with_gpt, analyze_image_with_gpt_vision
from database.db import log_scan, get_recent_scans, get_scan_by_id, submit_feedback, get_statistics

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
if os.environ.get("VERCEL"):
    UPLOAD_DIR = "/tmp/uploads"
else:
    UPLOAD_DIR = os.path.join(BASE_DIR, "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB

# Load models and artifacts safely
vectorizer = None
text_models = {}
url_model = None
benchmark_data = {}

try:
    vectorizer = joblib.load(os.path.join(MODELS_DIR, "vectorizer.pkl"))
    text_models = joblib.load(os.path.join(MODELS_DIR, "text_models.pkl"))
    url_model = joblib.load(os.path.join(MODELS_DIR, "url_model.pkl"))
    with open(os.path.join(MODELS_DIR, "benchmark_results.json"), "r") as f:
        benchmark_data = json.load(f)
    print("All ML models and artifacts successfully loaded!")
except Exception as e:
    print(f"Warning: ML model loading error: {e}. Retrain if needed.")

@app.route("/")
@app.route("/api/index")
@app.route("/api/index/")
def index():
    return render_template("index.html")

@app.route("/api/presets", methods=["GET"])
def get_presets():
    """Returns curated demo presets for fast classroom demonstration."""
    presets = [
        {
            "id": "bank_kyc",
            "title": "Bank KYC Suspension Threat (SMS)",
            "type": "text",
            "text": "Dear SBI customer, your savings account will be blocked within 24 hours due to pending KYC. Update your PAN immediately at http://sbi-netbanking-kyc-verify.xyz to avoid permanent suspension."
        },
        {
            "id": "electricity_cut",
            "title": "Electricity Power Cut Alert (SMS)",
            "type": "text",
            "text": "Dear consumer, your electricity power will be disconnected tonight at 9:30 PM because your previous month bill was not updated. Contact electricity officer at +91 9876543210 immediately."
        },
        {
            "id": "kbc_lottery",
            "title": "KBC Lucky Draw Award Lure (WhatsApp)",
            "type": "text",
            "text": "Congratulations! Your mobile number has won Rs 25 Lakh in KBC All India Lucky Draw 2026. Send your bank details to claim on WhatsApp: +91 9123456789."
        },
        {
            "id": "job_offer",
            "title": "Work From Home Like Video Job (Telegram)",
            "type": "text",
            "text": "Part-time job offer! Earn Rs 3,000 - 8,000 daily working from home on your phone. Just like and subscribe YouTube videos. Contact HR on WhatsApp: +91 9988776655."
        },
        {
            "id": "legit_bank",
            "title": "Legitimate Bank Debit Alert (SMS)",
            "type": "text",
            "text": "Dear customer, INR 1,500.00 debited from account ending in **4582 on 04-Oct-2026 at Amazon India. Available balance is INR 45,200.00. If not done by you, SMS BLOCK to 567676."
        },
        {
            "id": "legit_college",
            "title": "Legitimate College Project Notice",
            "type": "text",
            "text": "Reminder: The submission deadline for 4th Year B.Tech Mini Project synopsis and research paper draft is Friday at 5:00 PM in Seminar Hall 2."
        },
        {
            "id": "url_phish",
            "title": "Suspicious Bank Spoofing Link",
            "type": "url",
            "url": "http://sbi-netbanking-kyc-verify.xyz/login.php"
        },
        {
            "id": "url_ip",
            "title": "Raw IP Address Phishing Host",
            "type": "url",
            "url": "http://192.168.1.155/banking/secure-auth.php"
        },
        {
            "id": "url_legit",
            "title": "Legitimate State Bank Portal",
            "type": "url",
            "url": "https://www.onlinesbi.sbi"
        }
    ]
    return jsonify(presets)

@app.route("/api/analyze/text", methods=["POST"])
def analyze_text():
    data = request.get_json() or {}
    text = data.get("text", "").strip()
    model_name = data.get("model", "Logistic Regression")
    api_key = data.get("api_key") or request.headers.get("X-API-Key") or os.environ.get("OPENAI_API_KEY")

    if not text:
        return jsonify({"error": "Please provide message text to analyze."}), 400

    # 1. Try real-time GPT analysis if API key is provided
    if api_key:
        gpt_result = analyze_with_gpt(text, api_key=api_key)
        if gpt_result:
            scan_id = log_scan(
                input_type="text",
                preview=text,
                risk_score=gpt_result["risk_score"],
                verdict=gpt_result["verdict"],
                verdict_badge=gpt_result["verdict_badge"],
                model_name=gpt_result.get("engine", "OpenAI GPT-4o-mini"),
                signals=gpt_result.get("signals", []),
                recs=gpt_result.get("recommendations", []),
                tokens=gpt_result.get("token_weights", [])
            )
            gpt_result["scan_id"] = scan_id
            gpt_result["model_used"] = gpt_result.get("engine", "OpenAI GPT-4o-mini")
            return jsonify(gpt_result)

    # 2. Local Machine Learning & XAI fallback
    if model_name not in text_models:
        model_name = "Logistic Regression"

    model = text_models.get(model_name)
    if not model or not vectorizer:
        return jsonify({"error": "ML model is not loaded."}), 500

    X_vec = vectorizer.transform([text])
    ml_prob = float(model.predict_proba(X_vec)[0][1])

    xai_result = explain_prediction(text, ml_prob, vectorizer, model)

    scan_id = log_scan(
        input_type="text",
        preview=text,
        risk_score=xai_result["risk_score"],
        verdict=xai_result["verdict"],
        verdict_badge=xai_result["verdict_badge"],
        model_name=model_name,
        signals=xai_result["signals"],
        recs=xai_result["recommendations"],
        tokens=xai_result["token_weights"]
    )

    xai_result["scan_id"] = scan_id
    xai_result["model_used"] = model_name
    return jsonify(xai_result)

@app.route("/api/analyze/url", methods=["POST"])
def analyze_url():
    data = request.get_json() or {}
    url = data.get("url", "").strip()
    api_key = data.get("api_key") or request.headers.get("X-API-Key") or os.environ.get("OPENAI_API_KEY")

    if not url:
        return jsonify({"error": "Please provide a valid website URL."}), 400

    # 1. Real-time Live Web Inspection (Performs live HTTP query, inspects forms & redirects)
    live_web_report = inspect_live_url(url)
    url_report = extract_url_features(url)

    # Combine warning signals
    combined_signals = list(url_report["warning_signals"])
    if live_web_report.get("risk_signals"):
        combined_signals.extend(live_web_report["risk_signals"])

    # 2. If API Key provided, use GPT-4o with live web telemetry
    if api_key:
        gpt_prompt = f"Target URL: {url}\nPage Title: {live_web_report.get('page_title')}\nReachable: {live_web_report.get('is_reachable')}\nRedirected: {live_web_report.get('is_redirected')}\nPassword Field in HTML: {live_web_report.get('has_password_field')}\nFinancial Identity Input: {live_web_report.get('has_financial_form')}"
        gpt_result = analyze_with_gpt(gpt_prompt, api_key=api_key, live_context=live_web_report)
        if gpt_result:
            scan_id = log_scan(
                input_type="url",
                preview=url,
                risk_score=gpt_result["risk_score"],
                verdict=gpt_result["verdict"],
                verdict_badge=gpt_result["verdict_badge"],
                model_name="OpenAI GPT-4o-mini + Live Web Telemetry",
                signals=gpt_result.get("signals", []),
                recs=gpt_result.get("recommendations", []),
                tokens=gpt_result.get("token_weights", [])
            )
            gpt_result["scan_id"] = scan_id
            gpt_result["model_used"] = "OpenAI GPT-4o-mini + Live Web Telemetry"
            gpt_result["live_web"] = live_web_report
            gpt_result["domain"] = url_report["domain"]
            gpt_result["entropy"] = url_report["entropy"]
            return jsonify(gpt_result)

    # 3. Machine Learning + Live Heuristic calculation
    ml_url_prob = 0.5
    if url_model:
        feat_vector = [url_report["features"]]
        ml_url_prob = float(url_model.predict_proba(feat_vector)[0][1])

    # Factor in live web findings
    live_penalty = 0
    if live_web_report.get("has_password_field") and not url_report["is_trusted_domain"]:
        live_penalty += 35
    if live_web_report.get("has_financial_form") and not url_report["is_trusted_domain"]:
        live_penalty += 30
    if live_web_report.get("is_redirected"):
        live_penalty += 15

    composite_url_score = int(min(100, max(0, (ml_url_prob * 100 * 0.4) + (url_report["risk_score"] * 0.3) + live_penalty)))

    if composite_url_score >= 65:
        verdict = "Phishing / Malicious Website"
        badge = "danger"
    elif composite_url_score >= 35:
        verdict = "Suspicious / Unverified Website"
        badge = "warning"
    else:
        verdict = "Legitimate / Safe Website"
        badge = "success"

    recs = []
    if composite_url_score >= 65:
        recs.append("Do NOT enter passwords, phone numbers, or credit card details on this website.")
        recs.append("The domain exhibits indicators of brand spoofing and deceptive credential harvesting.")
    elif composite_url_score >= 35:
        recs.append("Proceed with caution. Verify the domain spelling and SSL certificate.")
    else:
        recs.append("Low risk indicators detected for this domain structure.")

    signals_formatted = [{"title": "Live Web / Structural Indicator", "description": s, "severity": "High"} for s in combined_signals]

    scan_id = log_scan(
        input_type="url",
        preview=url,
        risk_score=composite_url_score,
        verdict=verdict,
        verdict_badge=badge,
        model_name="Random Forest + Live Web Inspector",
        signals=signals_formatted,
        recs=recs,
        tokens=[]
    )

    return jsonify({
        "scan_id": scan_id,
        "url": url,
        "domain": url_report["domain"],
        "risk_score": composite_url_score,
        "verdict": verdict,
        "verdict_badge": badge,
        "entropy": url_report["entropy"],
        "is_trusted": url_report["is_trusted_domain"],
        "warning_signals": combined_signals,
        "live_web": live_web_report,
        "recommendations": recs,
        "model_used": "Random Forest + Live Web Inspector",
        "features": {name: val for name, val in zip(url_report["feature_names"], url_report["features"])}
    })

@app.route("/api/analyze/image", methods=["POST"])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided in request."}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected image file."}), 400

    image_bytes = file.read()
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(filepath, "wb") as f:
        f.write(image_bytes)

    model_name = request.form.get("model", "Logistic Regression")
    api_key = request.form.get("api_key") or request.headers.get("X-API-Key") or os.environ.get("OPENAI_API_KEY")

    # 1. Multimodal GPT-4o Vision if API key provided (True pixel-level OCR & Visual Fraud Inspection)
    if api_key:
        ext = filename.split('.')[-1].lower() if '.' in filename else 'png'
        vision_result = analyze_image_with_gpt_vision(image_bytes, image_format=ext, api_key=api_key)
        if vision_result:
            extracted_text = vision_result.get("extracted_text", "[Image Analyzed by GPT-4o Vision]")
            scan_id = log_scan(
                input_type="image",
                preview=f"[Screenshot Vision] {extracted_text[:120]}",
                risk_score=vision_result["risk_score"],
                verdict=vision_result["verdict"],
                verdict_badge=vision_result["verdict_badge"],
                model_name="OpenAI GPT-4o Vision",
                signals=vision_result.get("signals", []),
                recs=vision_result.get("recommendations", []),
                tokens=vision_result.get("token_weights", [])
            )
            vision_result["scan_id"] = scan_id
            vision_result["extracted_text"] = extracted_text
            vision_result["model_used"] = "OpenAI GPT-4o Vision"
            return jsonify(vision_result)

    # 2. Local fallback inspection
    ocr_result = analyze_image_screenshot(filepath)
    extracted_text = ocr_result.get("extracted_text", "").strip()

    model = text_models.get(model_name, text_models.get("Logistic Regression"))
    X_vec = vectorizer.transform([extracted_text])
    ml_prob = float(model.predict_proba(X_vec)[0][1])

    xai_result = explain_prediction(extracted_text, ml_prob, vectorizer, model)

    scan_id = log_scan(
        input_type="image",
        preview=f"[Screenshot OCR] {extracted_text[:120]}",
        risk_score=xai_result["risk_score"],
        verdict=xai_result["verdict"],
        verdict_badge=xai_result["verdict_badge"],
        model_name=f"{model_name} (Local OCR)",
        signals=xai_result["signals"],
        recs=xai_result["recommendations"],
        tokens=xai_result["token_weights"]
    )

    xai_result["scan_id"] = scan_id
    xai_result["extracted_text"] = extracted_text
    xai_result["image_meta"] = ocr_result
    xai_result["model_used"] = f"{model_name} (Local OCR)"
    xai_result["tip"] = "Tip: Configure an OpenAI API key in the top AI Settings to activate full multimodal GPT-4o vision on any custom screenshot."

    return jsonify(xai_result)

@app.route("/api/benchmarks", methods=["GET"])
def get_benchmarks():
    return jsonify(benchmark_data)

@app.route("/api/history", methods=["GET"])
def get_history():
    scans = get_recent_scans(limit=25)
    return jsonify(scans)

@app.route("/api/stats", methods=["GET"])
def get_stats():
    return jsonify(get_statistics())

@app.route("/api/feedback", methods=["POST"])
def post_feedback():
    data = request.get_json() or {}
    scan_id = data.get("scan_id")
    feedback_type = data.get("feedback_type", "accurate")
    comment = data.get("comment", "")

    if not scan_id:
        return jsonify({"error": "Missing scan_id."}), 400

    submit_feedback(scan_id, feedback_type, comment)
    return jsonify({"success": True, "message": "Feedback submitted successfully. Thank you!"})

@app.route("/download/paper")
def download_paper():
    paper_path = os.path.join(REPORTS_DIR, "Research_Paper_Explainable_Scam_Detection.pdf")
    if os.path.exists(paper_path):
        return send_file(
            paper_path,
            as_attachment=True,
            download_name="Research_Paper_Explainable_Scam_Detection.pdf",
            mimetype="application/pdf"
        )
    return jsonify({"error": "Research paper PDF not found."}), 404

@app.route("/download/presentation")
def download_presentation():
    ppt_path = os.path.join(REPORTS_DIR, "Scam_Detection_Presentation.pptx")
    if os.path.exists(ppt_path):
        return send_file(
            ppt_path,
            as_attachment=True,
            download_name="Scam_Detection_Presentation.pptx",
            mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
    return jsonify({"error": "Presentation file not found."}), 404

if __name__ == "__main__":
    print("Starting Explainable Scam Detection Server on http://127.0.0.1:5000 ...")
    app.run(host="127.0.0.1", port=5000, debug=True)
