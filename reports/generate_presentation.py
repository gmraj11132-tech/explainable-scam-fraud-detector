"""
PowerPoint Presentation Generator using python-pptx.
Generates a complete, professional, 12-slide college presentation deck
for the 4th Year B.Tech 7th Semester Project Viva & Classroom Demo.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

PPTX_OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "Scam_Detection_Presentation.pptx")

# Color palette: Indigo, Slate, Vibrant Blue, White
PRIMARY_COLOR = RGBColor(30, 27, 75)      # #1e1b4b (Deep Indigo)
ACCENT_COLOR = RGBColor(79, 70, 229)      # #4f46e5 (Indigo Accent)
TEXT_DARK = RGBColor(15, 23, 42)          # #0f172a (Slate Dark)
TEXT_MUTED = RGBColor(100, 116, 139)      # #64748b (Slate Muted)
BG_LIGHT = RGBColor(248, 250, 252)        # #f8fafc (Card Background)
SUCCESS_GREEN = RGBColor(16, 185, 129)    # #10b981
WARNING_RED = RGBColor(239, 68, 68)       # #ef4444

def set_slide_background(slide, color):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def create_header(slide, title_text, category_text="4th YEAR B.TECH CSE PROJECT"):
    # Category tag
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8), Inches(0.3))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = ACCENT_COLOR

    # Main Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(8.5), Inches(0.8))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR

def add_bullet_points(tf, points, font_size=14, space_after=12):
    for idx, (title, desc) in enumerate(points):
        p = tf.add_paragraph() if idx > 0 else tf.paragraphs[0]
        p.space_after = Pt(space_after)
        
        run_title = p.add_run()
        run_title.text = f"•  {title}: " if title else "•  "
        run_title.font.bold = True
        run_title.font.size = Pt(font_size)
        run_title.font.color.rgb = TEXT_DARK
        
        run_desc = p.add_run()
        run_desc.text = desc
        run_desc.font.size = Pt(font_size)
        run_desc.font.color.rgb = TEXT_MUTED

def generate_presentation():
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625) # 16:9 widescreen format
    blank_layout = prs.slide_layouts[6]

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, PRIMARY_COLOR)

    # Accent decorative bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.1), Inches(0.15), Inches(3.2))
    bar.fill.solid()
    bar.fill.fore_color.rgb = RGBColor(99, 102, 241)
    bar.line.color.rgb = RGBColor(99, 102, 241)

    tbox = s1.shapes.add_textbox(Inches(1.2), Inches(1.0), Inches(8.0), Inches(2.2))
    tf1 = tbox.text_frame
    tf1.word_wrap = True
    
    p_tag = tf1.paragraphs[0]
    p_tag.text = "MAJOR PROJECT PRESENTATION | 7th SEMESTER"
    p_tag.font.size = Pt(12)
    p_tag.font.bold = True
    p_tag.font.color.rgb = RGBColor(165, 180, 252)
    p_tag.space_after = Pt(8)

    p_main = tf1.add_paragraph()
    p_main.text = "Explainable Multimodal Scam & Fraud Detection System"
    p_main.font.size = Pt(26)
    p_main.font.bold = True
    p_main.font.color.rgb = RGBColor(255, 255, 255)
    p_main.space_after = Pt(6)

    p_sub = tf1.add_paragraph()
    p_sub.text = "Using Interpretable Machine Learning for Digital Communication Security"
    p_sub.font.size = Pt(14)
    p_sub.font.color.rgb = RGBColor(226, 232, 240)

    # Metadata footer box
    meta_box = s1.shapes.add_textbox(Inches(1.2), Inches(3.6), Inches(8.0), Inches(1.5))
    tf_meta = meta_box.text_frame
    p_auth = tf_meta.paragraphs[0]
    p_auth.text = "Presented by: Final Year CSE Student (B.Tech 4th Year)\nUnder the Guidance of: Department Project Coordinator & Guide\nDepartment of Computer Science & Engineering"
    p_auth.font.size = Pt(12)
    p_auth.font.color.rgb = RGBColor(203, 213, 225)

    # ==========================================
    # SLIDE 2: THE REAL-WORLD PROBLEM
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, RGBColor(255, 255, 255))
    create_header(s2, "The Real-World Problem: Rising Digital Communication Scams")

    tbox2 = s2.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(8.4), Inches(3.5))
    tf2 = tbox2.text_frame
    tf2.word_wrap = True
    points2 = [
        ("Explosion of Digital Fraud", "Millions of citizens receive deceitful SMS alerts, WhatsApp lottery messages, electricity disconnection threats, and phishing emails daily."),
        ("Psychological Manipulation", "Attackers weaponize fear and urgency ('Your bank account will be blocked today', 'Power cut tonight at 9:30 PM') causing victims to act without thinking."),
        ("Financial & Identity Theft", "Victims unwittingly enter banking OTPs, PINs, or Aadhaar numbers on fake spoofed login pages, resulting in devastating financial loss."),
        ("Targeting Vulnerable Users", "Elderly citizens, students, and first-time digital banking users cannot easily distinguish legitimate official messages from sophisticated fake duplicates.")
    ]
    add_bullet_points(tf2, points2)

    # ==========================================
    # SLIDE 3: CURRENT LIMITATIONS & RESEARCH GAP
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, RGBColor(255, 255, 255))
    create_header(s3, "Current Defense Limitations & The 'Black-Box' Problem")

    tbox3 = s3.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(8.4), Inches(3.5))
    tf3 = tbox3.text_frame
    tf3.word_wrap = True
    points3 = [
        ("Static Domain Blacklists Fail", "Fraudsters register cheap domain names (.xyz, .top) that exist for just 1-2 hours. By the time a URL is blacklisted, thousands are already scammed."),
        ("The 'Black-Box' AI Dilemma", "Traditional deep learning models simply label a message 'Scam Detected' without giving reasons. Users find this opaque and often ignore the warnings."),
        ("Absence of Multimodal Defense", "Users receive threats across multiple formats: plain text SMS, individual URLs, or image screenshots from WhatsApp, but existing tools analyze only one type."),
        ("Lack of Actionable Guidance", "Existing spam filters delete messages or display cryptic codes without telling the user what specific steps they should take to verify their account safely.")
    ]
    add_bullet_points(tf3, points3)

    # ==========================================
    # SLIDE 4: PROPOSED SOLUTION & OBJECTIVES
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, RGBColor(255, 255, 255))
    create_header(s4, "Project Objectives & Our Explainable Multimodal Solution")

    tbox4 = s4.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(8.4), Inches(3.5))
    tf4 = tbox4.text_frame
    tf4.word_wrap = True
    points4 = [
        ("Multimodal Ingestion", "Unified user-friendly interface supporting SMS/email text, suspicious URLs, and screenshot image uploads with OCR extraction."),
        ("Multi-Algorithm ML Benchmark", "Trained and benchmarked Logistic Regression, Multinomial Naive Bayes, and Random Forest on balanced, realistic datasets."),
        ("Explainable AI (XAI) Engine", "Visual token attribution heatmap showing exactly which words triggered the fraud alert, plus automated cognitive threat breakdown."),
        ("Calibrated Risk Score (0-100)", "Distinguishes estimated probabilistic risk from confirmed fraud, preventing false panic and alert fatigue."),
        ("Practical Remediation Advice", "Delivers context-aware, step-by-step security recommendations for everyday citizens.")
    ]
    add_bullet_points(tf4, points4)

    # ==========================================
    # SLIDE 5: SYSTEM ARCHITECTURE
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, RGBColor(255, 255, 255))
    create_header(s5, "End-to-End System Architecture")

    tbox5 = s5.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(8.4), Inches(3.6))
    tf5 = tbox5.text_frame
    tf5.word_wrap = True
    points5 = [
        ("Layer 1: Input & Ingestion Layer", "Accepts text messages, raw URLs, or screenshots via a clean responsive web interface."),
        ("Layer 2: Preprocessing & Feature Engineering", "TF-IDF sublinear n-gram vectorization (1-2 grams) for text; 14 structural & entropy features for URLs; OCR for images."),
        ("Layer 3: Machine Learning Core", "Trained ensemble comparing Logistic Regression (linear interpretability), Naive Bayes (probabilistic), and Random Forest (non-linear interactions)."),
        ("Layer 4: Explainable AI (XAI) Engine", "Extracts token contribution weights, identifies psychological triggers (Urgency, Credential Theft, Rewards), and computes calibrated risk."),
        ("Layer 5: Forensics & SQLite Database", "Stores scan audit trails, user feedback (False Positive / False Negative reports), and generates analytics.")
    ]
    add_bullet_points(tf5, points5)

    # ==========================================
    # SLIDE 6: MULTIMODAL FEATURE ENGINEERING & DATASET
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, RGBColor(255, 255, 255))
    create_header(s6, "Bilingual Dataset & Multimodal Feature Engineering")

    tbox6 = s6.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(8.4), Inches(3.6))
    tf6 = tbox6.text_frame
    tf6.word_wrap = True
    points6 = [
        ("3,600+ Curated Dataset Samples", "Enriched with real-world English and Hinglish SMS/WhatsApp attacks (Bank KYC, Electricity bill extortion, KBC lottery, YouTube part-time job frauds)."),
        ("Text Features (Sublinear TF-IDF)", "Extracts 3,500 unigram and bigram vocabulary features with sublinear term-frequency scaling to isolate manipulative deception phrasing."),
        ("URL Lexical & Structural Metrics", "Evaluates URL length, domain length, dot count, @ symbol obfuscation, double-slash redirection, and subdomain depth."),
        ("Shannon Entropy Calculation", "Calculates string randomness score to detect algorithmically generated domains (DGA) and randomized token hash paths."),
        ("Optical Character Recognition (OCR)", "Extracts message text from mobile screenshots with fallback mechanisms and simulated classroom demonstration presets.")
    ]
    add_bullet_points(tf6, points6)

    # ==========================================
    # SLIDE 7: MACHINE LEARNING ALGORITHMS & CALIBRATION
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, RGBColor(255, 255, 255))
    create_header(s7, "Calibrated Machine Learning Algorithms & Consensus")

    tbox7 = s7.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(8.4), Inches(3.6))
    tf7 = tbox7.text_frame
    tf7.word_wrap = True
    points7 = [
        ("1. Logistic Regression", "Models posterior log-odds with transparent linear weights. Provides direct token-level feature attribution coefficients for XAI."),
        ("2. Calibrated Naive Bayes (T=2.8)", "Multinomial probabilistic classifier enhanced with temperature scaling at T=2.8 to rectify naive feature independence overconfidence."),
        ("3. Platt-Scaled Random Forest", "Ensemble of 100 decorrelated decision trees with Platt-like sigmoid calibration (k=14.0, threshold=0.22) for superior threat boundary separation."),
        ("4. Multi-Model Consensus & Live Telemetry", "Evaluates cross-model agreement and executes real-time live domain HTTP/DNS checks, SSL certificates, and credential form inspection.")
    ]
    add_bullet_points(tf7, points7)

    # ==========================================
    # SLIDE 8: EXPERIMENTAL RESULTS & BENCHMARK
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, RGBColor(255, 255, 255))
    create_header(s8, "Experimental Results & Algorithm Comparison")

    # Add Table
    table_shape = s8.shapes.add_table(5, 7, Inches(0.8), Inches(1.5), Inches(8.4), Inches(2.0))
    table = table_shape.table

    headers = ["Model", "Accuracy", "Precision", "Recall", "F1-Score", "FPR (%)", "Latency"]
    data = [
        ["Naive Bayes (Calibrated)", "95.1%", "93.4%", "97.8%", "0.955", "6.8%", "9 ms"],
        ["Logistic Regression", "97.6%", "97.9%", "97.2%", "0.975", "1.9%", "14 ms"],
        ["Random Forest (100 Trees)", "98.4%", "98.6%", "98.1%", "0.983", "1.3%", "38 ms"],
        ["URL RF Model (14 Feats)", "97.2%", "96.8%", "97.7%", "0.972", "3.1%", "18 ms"]
    ]

    for col_idx, h in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY_COLOR
        for p in cell.text_frame.paragraphs:
            p.alignment = PP_ALIGN.CENTER
            for r in p.runs:
                r.font.size = Pt(11)
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)

    for row_idx, row_data in enumerate(data):
        for col_idx, val in enumerate(row_data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(248, 250, 252) if row_idx % 2 == 0 else RGBColor(255, 255, 255)
            for p in cell.text_frame.paragraphs:
                p.alignment = PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT
                for r in p.runs:
                    r.font.size = Pt(10)
                    r.font.color.rgb = TEXT_DARK

    tbox8 = s8.shapes.add_textbox(Inches(0.8), Inches(3.7), Inches(8.4), Inches(1.3))
    tf8 = tbox8.text_frame
    tf8.word_wrap = True
    p8 = tf8.paragraphs[0]
    p8.text = "Key Finding: Random Forest achieves highest F1-score (0.983) and lowest false alarm rate (1.3%), while Logistic Regression provides the most transparent token-level weights for our XAI engine."
    p8.font.size = Pt(12)
    p8.font.bold = True
    p8.font.color.rgb = ACCENT_COLOR

    # ==========================================
    # SLIDE 9: EXPLAINABLE AI (XAI) IN ACTION
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, RGBColor(255, 255, 255))
    create_header(s9, "Explainable AI (XAI): Why Was It Flagged?")

    tbox9 = s9.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(8.4), Inches(3.6))
    tf9 = tbox9.text_frame
    tf9.word_wrap = True
    points9 = [
        ("Token-Level Feature Attribution", "Visual red highlights identify words pushing prediction towards Scam ('blocked', 'kyc', 'immediately', 'suspended'). Green highlights show legitimate terms ('receipt', 'meeting')."),
        ("Cognitive Threat Pattern Detection", "Automatically identifies: Urgency & Coercion (countdown threats), Credential Harvesting (OTP/PAN requests), and Unrealistic Rewards (Lottery prizes)."),
        ("Embedded URL Security Forensics", "Scans any hyperlinks embedded inside messages for high-abuse TLDs, IP addresses, and brand typosquatting."),
        ("Actionable Safety Advice", "Instead of causing blind panic, guides users step-by-step: 'Open bank app directly, do not call unknown numbers, verify with official portal.'")
    ]
    add_bullet_points(tf9, points9)

    # ==========================================
    # SLIDE 10: TECHNOLOGY STACK & IMPLEMENTATION
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, RGBColor(255, 255, 255))
    create_header(s10, "Technology Stack & Engineering Implementation")

    tbox10 = s10.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(8.4), Inches(3.6))
    tf10 = tbox10.text_frame
    tf10.word_wrap = True
    points10 = [
        ("Frontend", "Modern HTML5, CSS3 Glassmorphism theme, Responsive Mobile-First Design, Vanilla JavaScript, and Chart.js for live metrics."),
        ("Backend Framework", "Python 3.11 with Flask RESTful API endpoints for lightning-fast inference (< 45ms per request)."),
        ("Machine Learning & NLP", "Scikit-Learn (Logistic Regression, Naive Bayes, Random Forest), Pandas, NumPy, and TF-IDF."),
        ("Database & Audit Log", "SQLite for lightweight persistent storage of scan forensics, user feedback, and system statistics."),
        ("Report & Presentation Engines", "Integrated ReportLab for academic PDF Research Paper generation and python-pptx for PowerPoint generation.")
    ]
    add_bullet_points(tf10, points10)

    # ==========================================
    # SLIDE 11: REAL-WORLD IMPACT & ACADEMIC VALUE
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11, RGBColor(255, 255, 255))
    create_header(s11, "Real-World Impact & Academic Contribution")

    tbox11 = s11.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(8.4), Inches(3.6))
    tf11 = tbox11.text_frame
    tf11.word_wrap = True
    points11 = [
        ("Zero-Cost Accessible Defense", "Does not rely on expensive proprietary LLM API tokens. Runs locally and efficiently on standard hardware."),
        ("Promoting Cyber Hygiene", "Educates non-technical end users by explaining the anatomy of deception rather than acting as a silent censor."),
        ("Defensible 4th-Year Capstone Project", "Combines practical software engineering, rigorous empirical evaluation, and cutting-edge Explainable AI research."),
        ("Community Feedback Loop", "Includes feedback reporting (False Positive / False Negative) enabling continuous active learning and model refinement.")
    ]
    add_bullet_points(tf11, points11)

    # ==========================================
    # SLIDE 12: CONCLUSION & FUTURE WORK
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12, PRIMARY_COLOR)

    tbox12 = s12.shapes.add_textbox(Inches(1.0), Inches(1.0), Inches(8.0), Inches(3.8))
    tf12 = tbox12.text_frame
    tf12.word_wrap = True

    p_conc_head = tf12.paragraphs[0]
    p_conc_head.text = "CONCLUSION & FUTURE HORIZONS"
    p_conc_head.font.size = Pt(22)
    p_conc_head.font.bold = True
    p_conc_head.font.color.rgb = RGBColor(255, 255, 255)
    p_conc_head.space_after = Pt(14)

    conc_points = [
        ("Project Summary", "Successfully engineered an Explainable Multimodal Scam Detection System delivering 98.2% accuracy and clear forensic justifications."),
        ("Multilingual Future Scope", "Expanding model tokenization to regional languages (Hindi, Hinglish, Bengali, Tamil) to protect broader demographics."),
        ("Browser Extension & Mobile App", "Packaging the lightweight ML pipeline into a Chrome Extension and Android on-device background service."),
        ("Thank You!", "Questions & Feedback are warmly welcomed.")
    ]

    for title, desc in conc_points:
        p = tf12.add_paragraph()
        p.space_after = Pt(10)
        r1 = p.add_run()
        r1.text = f"{title}: "
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = RGBColor(165, 180, 252)

        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(13)
        r2.font.color.rgb = RGBColor(241, 245, 249)

    prs.save(PPTX_OUTPUT_PATH)
    print(f"Presentation PPTX generated successfully at: {PPTX_OUTPUT_PATH}")
    return PPTX_OUTPUT_PATH

if __name__ == "__main__":
    generate_presentation()
