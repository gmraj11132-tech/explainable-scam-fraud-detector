# 🛡️ ScamGuard XAI: Explainable Multimodal Scam & Fraud Detection System
> **4th Year B.Tech Computer Science & Engineering (7th Semester Major/Mini Project)**  
> **Topic:** Explainable Multimodal Scam Detection System Using Machine Learning for Digital Communication Security

---

## 🌟 Project Overview
**ScamGuard XAI** is a proactive cybersecurity platform designed to protect everyday citizens, students, and banking customers from digital communication fraud (SMS smishing, phishing emails, fake WhatsApp messages, and deceptive URLs).

Unlike black-box spam filters that only show a generic "Scam Detected" badge, this system uses **Explainable Artificial Intelligence (XAI)** to show users **exactly why** a message was flagged (word-level token attribution, urgency analysis, credential harvesting alerts) and provides **clear, step-by-step safety advice**.

---

## 🚀 Key Features

### 1. 🌐 Multimodal Input Ingestion
- **Text Messages:** SMS alerts, WhatsApp forwards, phishing emails.
- **Website URLs:** Lexical, structural, and Shannon Entropy analysis of suspicious links (detects IP addresses, excessive subdomains, and malicious TLDs like `.xyz`, `.top`).
- **Screenshot Images (OCR):** Upload message screenshots to automatically extract text for forensic analysis.

### 2. 🧠 Explainable AI (XAI) Engine
- **Token Attribution Heatmap:** Mathematical feature attribution highlights scam-contributing words in <span style="color:red">red</span> (e.g., `blocked`, `kyc`, `immediately`, `suspended`) and legitimate contextual words in <span style="color:green">green</span>.
- **Cognitive Threat Detection:** Detects urgency tactics, sensitive credential harvesting (OTP/PIN/Aadhaar/PAN), and unrealistic prize lures.
- **Calibrated Risk Meter (0–100):** Distinguishes estimated probabilistic risk from confirmed fraud.

### 3. 📊 Academic ML Model Benchmark & Comparison
Compares three distinct machine learning algorithms trained on 2,400+ balanced samples:
- **Random Forest (100 Trees):** Highest accuracy (**98.2%**, F1-score: **0.981**, FPR: **1.5%**).
- **Logistic Regression:** Linear transparency (**97.4%** accuracy, provides exact log-odds weights for XAI).
- **Multinomial Naive Bayes:** High-speed probabilistic baseline (**94.6%** accuracy).

### 4. 📜 SQLite Forensics Audit & Feedback Loop
- Automatically logs all scans, risk scores, verdicts, and forensic details in a local SQLite database (`database/scam_detector.db`).
- Interactive feedback buttons ("Accurate", "False Alarm", "Missed Scam") for active learning.

### 5. 🎓 Complete College Deliverables Included
- **Academic Research Paper (PDF):** `reports/Research_Paper_Explainable_Scam_Detection.pdf` (IEEE/Springer two-column style).
- **PowerPoint Presentation (PPTX):** `reports/Scam_Detection_Presentation.pptx` (12 professional slides with animations and tables).
- **Classroom Presentation & Viva Guide:** `reports/PRESENTATION_NOTES.md` (Slide-by-slide script + Top 7 viva defense questions with answers in Hinglish & English).

---

## 🛠️ Technology Stack
| Layer | Technologies |
| :--- | :--- |
| **Frontend** | HTML5, CSS3 (Modern Glassmorphic Theme), Vanilla JavaScript, Mobile-First Responsive Design |
| **Backend API** | Python 3.11 + Flask RESTful Endpoints |
| **Machine Learning** | Scikit-Learn, Pandas, NumPy |
| **NLP & Text Analysis** | Sublinear TF-IDF (Unigrams & Bigrams, N=3500) |
| **Database** | SQLite (`database/scam_detector.db`) |
| **Document Engines** | ReportLab (for Research Paper PDF) & `python-pptx` (for PowerPoint Slides) |

---

## ⚡ How to Run the Project

### Method 1: One-Click Windows Launch (Easiest)
Simply double-click the **`run.bat`** file in this folder!

### Method 2: Via Terminal / PowerShell
```powershell
# 1. Open PowerShell in this project folder
cd "c:\Users\Administrator\Downloads\clg mini project"

# 2. Run the application
.\.venv\Scripts\python.exe app.py
```

Now open your browser and navigate to:
👉 **`http://127.0.0.1:5000`**

---

## 📁 Directory Structure
```
clg mini project/
├── app.py                     # Main Flask web application & REST API
├── run.bat                    # 1-Click Windows server launcher
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
│
├── ml_engine/
│   ├── dataset_generator.py   # Curated scam & legitimate training dataset generator
│   ├── train_models.py        # Model training, validation & comparison plot generator
│   ├── xai_engine.py          # Explainable AI token attribution & heuristic engine
│   ├── url_features.py        # 14-parameter lexical, structural & entropy URL analyzer
│   └── image_analyzer.py      # Screenshot OCR processor & realistic demonstration presets
│
├── models/
│   ├── text_models.pkl        # Serialized Logistic Regression, Naive Bayes, Random Forest
│   ├── url_model.pkl          # Trained URL classifier
│   ├── vectorizer.pkl         # Fitted TF-IDF Vectorizer
│   └── benchmark_results.json # Academic evaluation metrics (Accuracy, F1, FPR, FNR)
│
├── database/
│   ├── db.py                  # SQLite database manager for history, forensics & feedback
│   └── scam_detector.db       # SQLite database file
│
├── reports/
│   ├── Research_Paper_Explainable_Scam_Detection.pdf   # Publication-ready Research Paper
│   ├── Scam_Detection_Presentation.pptx                # 12-Slide College PPT Presentation
│   ├── RESEARCH_PAPER.md                               # Full markdown version of the paper
│   ├── PRESENTATION_NOTES.md                           # Slide-by-slide viva & presentation guide
│   ├── generate_research_paper.py                      # ReportLab PDF generation script
│   └── generate_presentation.py                        # python-pptx generation script
│
├── static/
│   ├── css/style.css          # Clean, modern, responsive CSS design
│   ├── js/app.js              # Interactive frontend logic & XAI visualizer
│   └── images/                # Generated benchmark & confusion matrix charts
│
├── templates/
│   └── index.html             # Single-page modern dashboard UI
│
└── tests/
    └── test_system.py         # Automated verification tests
```

---

## 🎯 Classroom Live Demonstration Tips
When presenting in front of your teacher:
1. Open **`http://127.0.0.1:5000`** in your browser.
2. Click any of the **1-Click Classroom Demo** buttons (e.g., *Bank KYC Suspension* or *Electricity Power Cut*).
3. Click **"Run Explainable AI Scan"**.
4. Show the teachers the **Token Feature Attribution**: point out how the red highlighted words (`blocked`, `immediately`, `kyc`) contributed to the score!
5. Switch to the **📊 Model Benchmark** tab to show the comparative metrics table and confusion matrices.
6. Switch to the **📥 Paper & PPT Hub** tab to show the downloadable PDF research paper and PowerPoint presentation.
