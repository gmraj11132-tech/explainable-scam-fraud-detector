"""
Real-time AI Reasoning Engine & Live Web Inspection.
Integrates OpenAI (GPT-4o / GPT-4o-mini) and Gemini Multimodal Vision,
along with real-time HTTP website inspection and form credential scanning.
"""

import os
import re
import json
import base64
import requests
from urllib.parse import urlparse

# Default system prompt for scam detection
XAI_SYSTEM_PROMPT = """You are ScamGuard XAI, an expert cybersecurity threat analyst and digital fraud investigator.
Analyze the provided communication (SMS, WhatsApp message, email, or live website context) for indicators of fraud, smishing, and social engineering.

You must respond ONLY with a valid JSON object with the following exact keys:
{
  "verdict": "Scam / High Risk Fraud" OR "Suspicious / Caution Advised" OR "Legitimate / Safe Communication",
  "verdict_badge": "danger" OR "warning" OR "success",
  "risk_score": <integer from 0 to 100>,
  "reasoning_summary": "<clear 2-sentence explanation of why this was flagged>",
  "signals": [
    {
      "category": "urgency|credential_harvesting|unrealistic_rewards|utility_threat|authority_impersonation|live_phishing_form",
      "title": "<Signal title>",
      "description": "<Detailed explanation of the psychological or technical deception>",
      "severity": "Critical|High|Medium"
    }
  ],
  "token_weights": [
    {"word": "<specific word>", "weight": <float between -1.0 and +1.0>, "impact": "scam|legitimate"}
  ],
  "recommendations": [
    "<actionable instruction for the user>",
    "<actionable instruction for the user>"
  ]
}
Make sure your risk score and token weights are precise. Tokens that indicate scams (e.g. 'blocked', 'kyc', 'immediately', 'lottery', 'power cut') must have positive weight and impact 'scam'. Legitimate contextual tokens must have negative weight and impact 'legitimate'."""

def inspect_live_url(url: str) -> dict:
    """
    Performs real-time HTTP fetch to inspect live domain status,
    detect deceptive redirects, and scan page DOM for phishing login forms.
    """
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    report = {
        "url": url,
        "is_reachable": False,
        "status_code": None,
        "final_url": url,
        "is_redirected": False,
        "page_title": "",
        "has_password_field": False,
        "has_financial_form": False,
        "server_header": "",
        "risk_signals": []
    }

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=6, allow_redirects=True, verify=False)
        report["is_reachable"] = True
        report["status_code"] = resp.status_code
        report["final_url"] = resp.url
        report["server_header"] = resp.headers.get("Server", "Unknown")

        if resp.history:
            report["is_redirected"] = True
            report["risk_signals"].append(f"Redirected through {len(resp.history)} hops to: {resp.url}")

        content_lower = resp.text.lower()

        # Extract <title>
        title_match = re.search(r'<title>(.*?)</title>', resp.text, re.IGNORECASE | re.DOTALL)
        if title_match:
            report["page_title"] = title_match.group(1).strip()[:100]

        # Scan for sensitive form inputs (classic credential phishing)
        if 'type="password"' in content_lower or "type='password'" in content_lower:
            report["has_password_field"] = True
            report["risk_signals"].append("Live webpage contains a password credential input field.")

        if any(term in content_lower for term in ['otp', 'cvv', 'card number', 'aadhaar', 'pan card', 'bank login']):
            report["has_financial_form"] = True
            report["risk_signals"].append("Live webpage contains sensitive financial identity fields (OTP/CVV/Aadhaar).")

    except requests.exceptions.RequestException as e:
        report["is_reachable"] = False
        report["risk_signals"].append(f"Connection failed or domain unreachable: {type(e).__name__}")

    return report

def analyze_with_gpt(text: str, api_key: str = None, live_context: dict = None) -> dict:
    """
    Analyzes communication text using OpenAI GPT-4o-mini or GPT-4o with real-time web intelligence.
    """
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        return None

    user_prompt = f"Analyze this digital communication:\n\"\"\"{text}\"\"\""
    if live_context and live_context.get("is_reachable"):
        user_prompt += f"\n\nReal-Time Live Web Inspection Telemetry:\n- Final URL: {live_context.get('final_url')}\n- Page Title: {live_context.get('page_title')}\n- Has Password Input: {live_context.get('has_password_field')}\n- Sensitive Inputs Found: {live_context.get('has_financial_form')}\n- Warnings: {', '.join(live_context.get('risk_signals', []))}"

    try:
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": XAI_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.2
        }

        resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            result = json.loads(content)
            result["engine"] = "OpenAI GPT-4o-mini (Real-time Reasoning)"
            return result
        else:
            print(f"OpenAI API Error ({resp.status_code}): {resp.text}")
            return None
    except Exception as e:
        print(f"GPT analysis exception: {e}")
        return None

def analyze_image_with_gpt_vision(image_bytes: bytes, image_format: str = "png", api_key: str = None) -> dict:
    """
    Sends screenshot directly to GPT-4o Vision for real-world OCR, layout analysis,
    brand logo spoofing verification, and text fraud detection.
    """
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        return None

    b64_image = base64.b64encode(image_bytes).decode("utf-8")
    mime_type = f"image/{image_format.lower()}" if image_format.lower() in ['png', 'jpeg', 'jpg', 'webp'] else "image/png"

    try:
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": XAI_SYSTEM_PROMPT + "\nAdditionally, extract all readable text from the screenshot and include it in an 'extracted_text' key in your JSON response."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Inspect this screenshot of a message/chat/website for scam and fraud indicators:"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{b64_image}"
                            }
                        }
                    ]
                }
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.2
        }

        resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=20)
        if resp.status_code == 200:
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            result = json.loads(content)
            result["engine"] = "OpenAI GPT-4o Vision (Multimodal OCR & Forensic Analysis)"
            return result
        else:
            print(f"OpenAI Vision Error ({resp.status_code}): {resp.text}")
            return None
    except Exception as e:
        print(f"GPT Vision exception: {e}")
        return None
