"""
URL Feature Extractor and Analyzer for Scam/Phishing Detection.
Extracts lexical, structural, statistical, and security heuristics from URLs.
"""

import math
import re
from urllib.parse import urlparse

SUSPICIOUS_TLDS = {
    'xyz', 'top', 'club', 'work', 'tk', 'ml', 'cf', 'gq', 'buzz',
    'info', 'click', 'rest', 'ru', 'country', 'stream', 'download',
    'racing', 'review', 'party', 'trade', 'accountant', 'date', 'faith',
    'bid', 'kim', 'cricket', 'science', 'party', 'gdn', 'mom', 'vip'
}

SUSPICIOUS_KEYWORDS = [
    'login', 'verify', 'account', 'update', 'secure', 'banking', 'signin',
    'confirm', 'password', 'credential', 'support', 'free', 'bonus',
    'reward', 'claim', 'wallet', 'kyc', 'aadhar', 'pan', 'otp', 'bill',
    'refund', 'gift', 'lottery', 'winner', 'unblock', 'suspend'
]

TRUSTED_DOMAINS = {
    'google.com', 'microsoft.com', 'apple.com', 'amazon.com', 'amazon.in',
    'github.com', 'wikipedia.org', 'gov.in', 'nic.in', 'sbi.co.in',
    'hdfcbank.com', 'icicibank.com', 'netflix.com', 'youtube.com',
    'facebook.com', 'instagram.com', 'twitter.com', 'linkedin.com'
}

def calculate_shannon_entropy(text: str) -> float:
    """Calculate Shannon entropy to detect randomly generated strings/DGA."""
    if not text:
        return 0.0
    entropy = 0.0
    text_len = len(text)
    counts = {}
    for char in text:
        counts[char] = counts.get(char, 0) + 1
    for count in counts.values():
        p = count / text_len
        entropy -= p * math.log2(p)
    return round(entropy, 3)

def extract_url_features(url: str) -> dict:
    """
    Extract comprehensive lexical and structural features from a URL.
    Returns numeric feature vector and descriptive flags.
    """
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url_with_scheme = 'http://' + url
    else:
        url_with_scheme = url

    try:
        parsed = urlparse(url_with_scheme)
    except Exception:
        parsed = urlparse('http://' + url)

    domain = parsed.netloc.lower()
    path = parsed.path
    query = parsed.query

    # Remove port if present for domain analysis
    domain_host = domain.split(':')[0]

    # Feature 1: URL Length
    url_length = len(url)

    # Feature 2: Domain Length
    domain_length = len(domain_host)

    # Feature 3: Number of dots in domain
    dots_in_domain = domain_host.count('.')

    # Feature 4: Has IP address in hostname
    ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    has_ip = 1 if re.match(ip_pattern, domain_host) else 0

    # Feature 5: Has '@' symbol (often used to obscure target destination)
    has_at_symbol = 1 if '@' in url else 0

    # Feature 6: Has hyphen in domain
    has_hyphen_in_domain = 1 if '-' in domain_host else 0

    # Feature 7: Has double slash in path (redirect trick)
    has_double_slash_path = 1 if '//' in path else 0

    # Feature 8: Subdomain count
    domain_parts = domain_host.split('.')
    subdomain_count = max(0, len(domain_parts) - 2) if len(domain_parts) > 1 else 0

    # Feature 9: Suspicious TLD
    tld = domain_parts[-1] if domain_parts else ''
    is_suspicious_tld = 1 if tld in SUSPICIOUS_TLDS else 0

    # Feature 10: Shannon entropy
    entropy = calculate_shannon_entropy(url)

    # Feature 11: Digit count in domain
    digits_in_domain = sum(c.isdigit() for c in domain_host)

    # Feature 12: Suspicious keywords present
    keywords_found = [kw for kw in SUSPICIOUS_KEYWORDS if kw in url.lower()]
    suspicious_keyword_count = len(keywords_found)

    # Feature 13: HTTPS check
    is_https = 1 if parsed.scheme == 'https' else 0

    # Feature 14: Has non-standard port
    has_non_standard_port = 0
    if ':' in domain:
        port_str = domain.split(':')[-1]
        if port_str.isdigit() and int(port_str) not in (80, 443):
            has_non_standard_port = 1

    # Feature 15: Trusted domain whitelist check
    is_trusted_domain = any(domain_host == td or domain_host.endswith('.' + td) for td in TRUSTED_DOMAINS)

    # Feature vector for ML
    numeric_vector = [
        url_length,
        domain_length,
        dots_in_domain,
        has_ip,
        has_at_symbol,
        has_hyphen_in_domain,
        has_double_slash_path,
        subdomain_count,
        is_suspicious_tld,
        entropy,
        digits_in_domain,
        suspicious_keyword_count,
        is_https,
        has_non_standard_port
    ]

    # Generate heuristic risk score for URL
    risk_points = 0
    warning_signals = []

    if has_ip:
        risk_points += 35
        warning_signals.append("URL uses a raw IP address instead of a recognized domain name.")

    if is_suspicious_tld:
        risk_points += 25
        warning_signals.append(f"Domain uses high-abuse top-level domain (.{tld}).")

    if has_at_symbol:
        risk_points += 20
        warning_signals.append("URL contains '@' symbol used in URL obfuscation.")

    if has_hyphen_in_domain:
        risk_points += 15
        warning_signals.append("Domain contains hyphens often used in typosquatting/brand spoofing.")

    if subdomain_count >= 3:
        risk_points += 20
        warning_signals.append(f"Excessive subdomains detected ({subdomain_count} subdomains).")

    if suspicious_keyword_count > 0:
        risk_points += min(30, suspicious_keyword_count * 12)
        warning_signals.append(f"Contains high-risk trigger keywords: {', '.join(keywords_found)}.")

    if not is_https:
        risk_points += 15
        warning_signals.append("Unencrypted connection (HTTP instead of secure HTTPS).")

    if digits_in_domain >= 3:
        risk_points += 15
        warning_signals.append(f"Domain contains unusual numbers ({digits_in_domain} digits).")

    if entropy > 4.5:
        risk_points += 15
        warning_signals.append(f"High character entropy ({entropy}), suggesting randomized/algorithmically generated link.")

    if is_trusted_domain and not has_ip and not has_at_symbol and suspicious_keyword_count == 0:
        risk_points = max(0, risk_points - 60)

    url_risk_score = min(100, max(0, risk_points))

    return {
        "url": url,
        "domain": domain_host,
        "scheme": parsed.scheme or 'http',
        "features": numeric_vector,
        "feature_names": [
            "url_length", "domain_length", "dots_in_domain", "has_ip",
            "has_at_symbol", "has_hyphen_in_domain", "has_double_slash_path",
            "subdomain_count", "is_suspicious_tld", "entropy",
            "digits_in_domain", "suspicious_keyword_count", "is_https",
            "has_non_standard_port"
        ],
        "risk_score": url_risk_score,
        "warning_signals": warning_signals,
        "keywords_found": keywords_found,
        "is_trusted_domain": is_trusted_domain,
        "entropy": entropy
    }
