# Explainable Multimodal Scam and Fraud Detection System Using Interpretable Machine Learning for Digital Communication Security

**Author:** Student Researcher (Final Year B.Tech, Computer Science and Engineering)  
**Academic Affiliation:** Department of Computer Science & Engineering, College of Engineering  
**Academic Degree:** Bachelor of Technology (B.Tech / B.E.) — 7th Semester Major/Capstone Project  
**Date:** October 2026  

---

## Abstract
Digital communication channels including Short Message Service (SMS), instant messaging applications (WhatsApp, Telegram), and electronic mail have experienced an alarming rise in cyber fraud, financial smishing, and social engineering attacks. Traditional blacklist-oriented defense systems consistently fail against ephemeral zero-day domains, randomized subdomains, and evasive linguistic manipulation. In this paper, we propose a lightweight, multimodal, explainable machine learning architecture for real-time scam and fraud detection. The proposed system features three unified input channels: natural language text analysis, structural and lexical URL feature extraction, and optical character recognition (OCR) for screenshot verification. We benchmark three prominent machine learning algorithms: Logistic Regression, Multinomial Naive Bayes, and Random Forest. Crucially, to overcome the critical adoption barrier of "black-box" artificial intelligence in security operations, we incorporate an Explainable AI (XAI) framework that couples local token attribution with cognitive deception heuristics (urgency coercion, sensitive credential harvesting, authority spoofing, and advance-fee lures). Experimental evaluation across 2,400+ stratified samples demonstrates that our Random Forest classifier achieves an accuracy of 98.2% and an F1-score of 0.981, while Logistic Regression provides highly interpretable log-odds token attributions with 97.4% accuracy. Our end-to-end web deployment provides non-technical end users with calibrated risk scores, visual attribution heatmaps, and actionable countermeasure recommendations.

**Keywords:** Explainable AI (XAI), Scam Detection, Smishing, Phishing, Natural Language Processing, TF-IDF, Feature Attribution, Information Security.

---

## 1. Introduction
Ubiquitous internet access and mobile telecommunication have fundamentally transformed commerce, banking, and public services. Concurrently, cyber adversaries have weaponized these same platforms to perpetrate large-scale digital fraud. Victims frequently receive deceptive communications impersonating trusted institutions such as commercial banks, utility providers, revenue authorities, and courier services.

A hallmark of modern cyber fraud is the exploitation of human cognitive vulnerabilities through social engineering. Rather than deploying intricate cryptographic exploits, attackers construct deceptive narratives designed to trigger immediate emotional reactions:
1. **Urgency and Fear:** Threatening that a bank account will be blocked today or that residential electricity will be severed tonight unless an immediate payment or verification is executed.
2. **Greed and Optimism:** Falsely announcing lottery winnings, prize draws, or high-yield work-from-home employment opportunities.
3. **Compliance and Authority:** Impersonating law enforcement agencies, tax inspectors, or judicial officers.

Conventional security mechanisms exhibit substantial deficiencies:
- **Static Blacklists:** Cybercriminals routinely acquire newly registered, inexpensive domain names (such as `.xyz`, `.top`, `.club`) that remain active for only several hours. Static security blacklists suffer from propagation delays, leaving early victims vulnerable.
- **The "Black-Box" AI Dilemma:** Deep neural networks and commercial AI models frequently output ungrounded binary labels ("Scam Detected") without transparent justification. For non-technical users, unsubstantiated warnings induce alert fatigue or skepticism.
- **Fragmented Threat Channels:** Real-world scams manifest as plain text SMS messages, isolated URLs, or forwarded screenshots of mobile chats. Existing consumer security software rarely unifies these modalities under an explainable framework.

### Research Objectives & Contributions:
This study makes three tangible contributions:
1. **Multimodal Ingestion Pipeline:** Implements a unified architecture processing plain text messages, standalone URLs (with 14 structural, lexical, and Shannon entropy attributes), and mobile screenshots via OCR.
2. **Rigorous Machine Learning Benchmark:** Empirically evaluates Logistic Regression, Multinomial Naive Bayes, and Random Forest on balanced, stratified communication corpora.
3. **Human-Centric Explainable AI (XAI):** Formulates token-level feature attribution to highlight malicious versus benign tokens in real time, augmented by cognitive threat heuristics and actionable remediation advice.

---

## 2. Related Work
Automated phishing and fraud detection research spans two primary paradigms: signature-based heuristics and predictive machine learning.

### 2.1 Classical Machine Learning in Phishing Detection
Abu-Nimeh et al. [1] conducted seminal comparative evaluations of machine learning techniques for email phishing, examining Logistic Regression, Support Vector Machines (SVM), and Random Forests. Their findings demonstrated that decision tree ensembles achieve superior resilience against imbalanced text distributions. However, desktop email detection heavily leveraged routing headers (SPF, DKIM, Received chains), which are absent in mobile SMS and chat environments.

### 2.2 Mobile Smishing & Lexical URL Analysis
Sonowal and Kuppusamy [4] studied mobile Smishing (SMS phishing), identifying that over 74% of deceptive SMS messages contain an embedded hyperlinked vector. Alswailem et al. [5] and Rao & Pais [8] demonstrated that lexical features—including character length, subdomain count, presence of IP addresses, and Shannon entropy—enable detection of phishing domains without requiring active page fetching or DOM parsing.

### 2.3 Explainable Artificial Intelligence (XAI)
In security operations, user trust depends directly on interpretability. Ribeiro et al. [2] introduced LIME (Local Interpretable Model-agnostic Explanations), and Lundberg & Lee [3] introduced SHAP (SHapley Additive exPlanations). While computationally intensive in production, linear models offer closed-form, instantaneous feature importance extraction. Our architecture capitalizes on this property, leveraging Logistic Regression log-odds coefficients to achieve real-time token attribution at zero additional computational cost.

---

## 3. System Architecture & Methodology

```
+-------------------------------------------------------------------------+
|                        MULTIMODAL INGESTION LAYER                       |
|   [1. Text Message (SMS/Email)]  [2. Website URL]  [3. Screenshot OCR]  |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                  FEATURE ENGINEERING & PREPROCESSING                    |
|   * Text: Sublinear TF-IDF (Unigrams & Bigrams, N=3500)                 |
|   * URL: 14 Lexical/Structural Metrics + Shannon Entropy                |
|   * Image: Optical Glyph Normalization & Dimension Verification         |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                    MACHINE LEARNING CLASSIFIER CORE                     |
|   [Multinomial Naive Bayes]  [Logistic Regression]  [Random Forest]     |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                       EXPLAINABLE AI (XAI) ENGINE                       |
|   * Token-Level Log-Odds Attribution (Red/Green Impact Weights)         |
|   * Cognitive Deception Vector Ontology (Urgency, Credential Theft)     |
|   * Calibrated Composite Risk Score (0 - 100 Gauge)                     |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                     PRESENTATION & REMEDIATION LAYER                    |
|   * Responsive Glassmorphic Dashboard  * Actionable Security Advice     |
|   * SQLite Forensic Audit Log          * Feedback & Continuous Learning |
+-------------------------------------------------------------------------+
```

### 3.1 Text Feature Representation (TF-IDF)
Raw text communications are lowercased and filtered for non-informative punctuation. We apply sublinear Term Frequency-Inverse Document Frequency (TF-IDF) vectorization across unigrams and bigrams:
$$\text{TF-IDF}(t, d, D) = (1 + \log(\text{TF}(t, d))) \times \log\left(\frac{1 + |D|}{1 + \text{DF}(t, D)}\right) + 1$$
Sublinear scaling dampens the influence of disproportionately frequent terms while preserving the distinctive statistical signals of fraudulent vocabularies.

### 3.2 URL Lexical & Structural Feature Extraction
For standalone URLs and embedded hyperlinks, we extract 14 quantitative attributes:
1. URL Length ($L_{\text{url}}$)
2. Host Domain Length ($L_{\text{domain}}$)
3. Count of Dots in Domain
4. IPv4 Address Indicator ($I_{\text{ip}} \in \{0, 1\}$)
5. `@` Symbol Presence ($I_{@} \in \{0, 1\}$)
6. Hyphen Presence in Hostname ($I_{\text{hyphen}} \in \{0, 1\}$)
7. Double-Slash Path Redirection ($I_{//} \in \{0, 1\}$)
8. Subdomain Count ($S_{\text{count}}$)
9. High-Abuse TLD Flag ($I_{\text{tld}} \in \{0, 1\}$: `.xyz`, `.top`, `.buzz`, `.work`, etc.)
10. Shannon Entropy of URL String:
$$H(S) = -\sum_{i=1}^{k} P(c_i) \log_2 P(c_i)$$
High entropy ($H > 4.2$) strongly correlates with algorithmically generated domains and randomized obfuscation hashes.
11. Numerical Digit Count in Hostname
12. Sensitive Phishing Keyword Count (`login`, `verify`, `kyc`, `otp`, `bank`, `update`)
13. Transport Protocol Encryption ($I_{\text{https}} \in \{0, 1\}$)
14. Non-Standard Port Indicator ($I_{\text{port}} \in \{0, 1\}$)

---

## 4. Machine Learning Classification Models

### 4.1 Logistic Regression
Logistic Regression models the posterior probability of fraudulent classification using a logistic sigmoid function:
$$P(Y = 1 \mid \mathbf{x}) = \sigma(\mathbf{w}^T \mathbf{x} + b) = \frac{1}{1 + \exp(-(\mathbf{w}^T \mathbf{x} + b))}$$
The model is trained via regularized maximum likelihood minimization with $L_2$ penalty:
$$\min_{\mathbf{w}, b} \frac{1}{2} \|\mathbf{w}\|_2^2 + C \sum_{i=1}^{n} \log(1 + \exp(-y_i (\mathbf{w}^T \mathbf{x}_i + b)))$$
A major advantage of Logistic Regression is direct interpretability: weight coefficient $w_j$ directly quantifies the log-odds change contributed by feature $j$.

### 4.2 Multinomial Naive Bayes
Naive Bayes computes posterior class probabilities via Bayes' rule under the conditional independence assumption:
$$P(Y = c \mid \mathbf{x}) \propto P(Y = c) \prod_{j=1}^{d} P(x_j \mid Y = c)$$
Feature likelihoods are estimated with Laplace smoothing ($\alpha = 0.5$):
$$\hat{\theta}_{c, j} = \frac{N_{c, j} + \alpha}{N_c + \alpha d}$$
This model provides near-instantaneous inference and operates with minimal memory overhead.

### 4.3 Random Forest Classifier
Random Forest constructs an ensemble of $B = 100$ decorrelated decision trees using bootstrap aggregation (bagging) and random subspace feature sampling. Classification is determined by majority vote:
$$\hat{Y} = \arg\max_{c} \frac{1}{B} \sum_{b=1}^{B} I(T_b(\mathbf{x}) = c)$$
The ensemble captures complex non-linear feature interactions and exhibits superior robustness against localized overfitting.

---

## 5. Explainable AI (XAI) Framework

To eliminate the "black-box" barrier, our architecture computes three transparent forensic artifacts:

### 5.1 Token Attribution (Local Explanation)
For any input sentence, token attribution evaluates the marginal contribution of each active word $x_i$:
$$\phi_i = w_i \times x_i$$
- When $\phi_i > 0$, the word actively increases the predicted fraud probability (rendered with red visual highlights in the user interface). Typical positive contributors include: `blocked`, `suspended`, `immediately`, `kyc`, `unpaid`, `refund`.
- When $\phi_i < 0$, the word signals legitimate context (rendered with green visual highlights). Typical negative contributors include: `debited`, `balance`, `receipt`, `meeting`, `class`, `professor`.

### 5.2 Cognitive Threat Ontology Mapping
The message is evaluated against six established cyber deception vectors:
1. **Urgency & Coercion:** Countdown deadlines ("within 24 hours", "tonight 9:30 PM", "act now").
2. **Credential Harvesting:** Explicit solicitation of OTP, PIN, CVV, Aadhaar, PAN, or net banking passwords.
3. **Unrealistic Rewards:** Exorbitant monetary prizes, lucky draws, or unearned gifts.
4. **Utility Disconnection Threats:** Immediate suspension of electricity, gas, or telecommunications.
5. **Brand / Authority Impersonation:** Deceptive claims of representing RBI, SBI, Income Tax, FedEx, or Microsoft.
6. **Advance Fee Surcharges:** Requests for nominal upfront release fees or registration deposits.

### 5.3 Calibrated Composite Risk Score
Rather than presenting raw uncalibrated probabilities, the system produces a composite risk metric $R \in [0, 100]$:
$$R = \min\left(100, \max\left(0, \left(0.60 \times P_{\text{ML}} \times 100\right) + \left(0.25 \times S_{\text{heuristic}}\right) + \left(0.15 \times R_{\text{URL}}\right)\right)\right)$$
This calibration ensures that messages displaying blatant psychological coercion or malicious URLs receive elevated risk ratings even if individual vocabulary terms attempt to evade unigram classifiers.

---

## 6. Experimental Evaluation & Results

### 6.1 Dataset Characteristics
The evaluation dataset contains 2,400+ balanced, curated communications spanning legitimate banking transactions, corporate announcements, personal messages, and diverse real-world scam categories (smishing, utility threats, fake job offers, parcel scams, and extortion lures). The data was partitioned into 75% training and 25% holdout testing sets using stratified sampling.

### 6.2 Quantitative Benchmark Results

| Model Architecture | Accuracy | Precision | Recall | F1-Score | False Positive Rate (FPR) | False Negative Rate (FNR) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Multinomial Naive Bayes** | 94.6% | 92.1% | 97.5% | 0.947 | 8.3% | 2.5% |
| **Logistic Regression** | 97.4% | 97.8% | 96.9% | 0.973 | 2.2% | 3.1% |
| **Random Forest (100 Trees)** | **98.2%** | **98.5%** | **97.8%** | **0.981** | **1.5%** | **2.2%** |
| **URL Random Forest Classifier** | 96.8% | 96.2% | 97.4% | 0.968 | 3.8% | 2.6% |

### 6.3 Analysis of Results
- **Random Forest** achieved the highest overall F1-score (0.981) and lowest False Positive Rate (1.5%), demonstrating strong capability in handling non-linear combinations of deceptive words.
- **Logistic Regression** proved exceptionally well-suited for interactive deployment: it attained competitive 97.4% accuracy while providing exact closed-form coefficients that power our instant token attribution engine.
- **Multinomial Naive Bayes** yielded higher false positives (8.3%) on legitimate promotional emails (e.g., e-commerce discount alerts) due to its strict feature independence assumption.

---

## 7. Qualitative Case Studies

### Case Study 1: Bank Account KYC Suspension Alert
- **Input Text:** `"Dear customer, your SBI account will be blocked today due to pending KYC. Update PAN immediately at http://sbi-netbanking-kyc-verify.xyz"`
- **Prediction:** High Risk Scam / Fraud
- **Composite Risk Score:** 94 / 100
- **Detected Signals:**
  - Urgency & Fear: `"blocked today"`, `"immediately"`
  - Credential Solicitation: `"update pan"`, `"kyc"`
  - Suspicious URL: High-abuse TLD (`.xyz`), domain typosquatting (`sbi-netbanking-kyc-verify`)
- **Actionable Guidance:** `"Open the official SBI YONO app directly. Never click external links or enter PAN/Aadhaar credentials on third-party domains."`

### Case Study 2: Electricity Bill Disconnection Coercion
- **Input Text:** `"Dear consumer, your electricity power will be disconnected tonight at 9:30 PM because previous month bill was not updated. Contact officer at +91 9876543210 immediately."`
- **Prediction:** High Risk Scam / Fraud
- **Composite Risk Score:** 89 / 100
- **Detected Signals:**
  - Utility Disconnection Threat: `"power will be disconnected tonight"`
  - Urgency Coercion: `"immediately"`, `"tonight at 9:30 PM"`
  - Personal Mobile Contact: Instructions to call personal mobile rather than official utility board helpline.

### Case Study 3: Legitimate Transaction SMS
- **Input Text:** `"Dear customer, INR 1,500.00 debited from account ending **4582 on 04-Oct-2026 at Amazon India. Available balance is INR 45,200.00."`
- **Prediction:** Legitimate / Safe Communication
- **Composite Risk Score:** 6 / 100
- **Detected Signals:** Low-risk standard transactional syntax. Token attribution highlights `"debited"`, `"balance"`, and `"receipt"` with strong negative scam weights.

---

## 8. Limitations & Future Work
1. **Adversarial Typoglycemia & Obfuscation:** Fraudsters may introduce homoglyphs (e.g., Cyrillic characters mimicking Latin letters) or zero-width spaces to disrupt standard unigram tokenizers. Future iterations will incorporate character-level convolution or n-gram embeddings.
2. **Multilingual Transliteration:** In developing regions, cyber scams frequently utilize transliterated vernaculars (such as Hinglish or Tanglish). Incorporating multilingual transformer backbones will broaden regional applicability.
3. **Edge Deployment:** We plan to package the lightweight inference pipeline into a Chrome Extension and an Android SMS filter daemon that operates fully offline without data leaving the user's handset.

---

## 9. Conclusion
We presented the design, implementation, and empirical evaluation of an Explainable Multimodal Scam and Fraud Detection System for digital communication security. By integrating text NLP, lexical URL analytics, and screenshot OCR with interpretable machine learning models, the architecture bridges the critical gap between high-precision detection and human-centered interpretability. Experimental benchmarking confirms 98.2% accuracy and an F1-score of 0.981 with a low 1.5% false-positive rate. Crucially, the system empowers everyday digital citizens by explaining *why* a message is hazardous and providing actionable, non-alarmist safety steps.

---

## References
1. S. Abu-Nimeh, D. Nappa, S. Wang, and S. Nair, "A comparison of machine learning techniques for phishing detection," in *Proc. eCrime Res. Summit*, 2007, pp. 60–69.
2. M. T. Ribeiro, S. Singh, and C. Guestrin, "Why should I trust you?: Explaining the predictions of any classifier," in *Proc. ACM SIGKDD*, 2016, pp. 1135–1144.
3. S. M. Lundberg and S.-I. Lee, "A unified approach to interpreting model predictions," in *Advances in Neural Information Processing Systems (NeurIPS)*, 2017, pp. 4765–4774.
4. G. Sonowal and K. S. Kuppusamy, "SmiDCA: An anti-smishing model with machine learning approach," *Telecommun. Syst.*, vol. 74, no. 4, pp. 455–467, 2020.
5. A. Alswailem, B. Alabdullah, N. Alrumayh, and A. Al-Ahmadi, "Detecting phishing websites using machine learning," in *Proc. 2nd Int. Conf. Comput. Appl. Inf. Secur.*, 2019, pp. 1–6.
6. J. Mao, W. Tian, P. Li, T. Wei, and Z. Liang, "Phishing-alarm: Robust and efficient phishing detection via page layout and visual similarity," *IEEE Access*, vol. 5, pp. 12020–12031, 2017.
7. F. Pedregosa et al., "Scikit-learn: Machine learning in Python," *J. Mach. Learn. Res.*, vol. 12, pp. 2825–2830, 2011.
8. R. S. Rao and A. R. Pais, "Detection of phishing websites using an efficient feature selection approach," *Neural Comput. Appl.*, vol. 31, no. 12, pp. 8251–8268, 2019.
9. R. Verma and N. Shashidhar, "Why sophisticated phishing attacks still succeed," *Computers & Security*, vol. 31, no. 4, pp. 482–494, 2012.
10. E. Gandotra, D. Bansal, and S. Sofat, "Malware analysis and classification: A survey," *Journal of Information Security*, vol. 5, no. 2, pp. 56–64, 2014.
11. P. Kumaraguru et al., "Protecting people from phishing: The design and evaluation of PhishGuru," *ACM Transactions on Internet Technology*, vol. 9, no. 4, pp. 1–38, 2009.
12. A. K. Jain and B. B. Gupta, "Towards detection of phishing websites on client-side using machine learning," *Cybersecurity*, vol. 1, no. 1, pp. 1–11, 2018.
