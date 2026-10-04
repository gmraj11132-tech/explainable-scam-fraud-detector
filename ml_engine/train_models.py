"""
Machine Learning Training Pipeline & Model Comparison Engine.
Trains Logistic Regression, Multinomial Naive Bayes, and Random Forest on text and URL datasets.
Computes evaluation metrics, confusion matrices, and exports model artifacts and comparison graphs.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_auc_score, roc_curve
)

from ml_engine.dataset_generator import generate_dataset
from ml_engine.url_features import extract_url_features

MODELS_DIR = "models"
IMAGES_DIR = "static/images"

def train_and_evaluate_all():
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)

    print("Generating comprehensive dataset...")
    df_text, df_urls = generate_dataset()

    # 1. Text Classification Pipeline
    print("Fitting TF-IDF Vectorizer...")
    vectorizer = TfidfVectorizer(
        max_features=3500,
        ngram_range=(1, 2),
        stop_words='english',
        sublinear_tf=True
    )

    X_text = vectorizer.fit_transform(df_text['text'])
    y_text = df_text['label'].values

    X_train, X_test, y_train, y_test = train_test_split(
        X_text, y_text, test_size=0.25, random_state=42, stratify=y_text
    )

    algorithms = {
        "Logistic Regression": LogisticRegression(max_iter=1000, C=1.0, random_state=42),
        "Naive Bayes": MultinomialNB(alpha=0.5),
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42)
    }

    trained_models = {}
    benchmark_results = {}

    print("\n--- Model Benchmark & Evaluation ---")
    for name, clf in algorithms.items():
        print(f"Training {name}...")
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        y_prob = clf.predict_proba(X_test)[:, 1] if hasattr(clf, "predict_proba") else y_pred

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_prob)
        cm = confusion_matrix(y_test, y_pred)
        tn, fp, fn, tp = cm.ravel()

        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
        fnr = fn / (fn + tp) if (fn + tp) > 0 else 0

        benchmark_results[name] = {
            "accuracy": round(float(acc), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "f1_score": round(float(f1), 4),
            "roc_auc": round(float(auc), 4),
            "confusion_matrix": {
                "TN": int(tn),
                "FP": int(fp),
                "FN": int(fn),
                "TP": int(tp)
            },
            "false_positive_rate": round(float(fpr), 4),
            "false_negative_rate": round(float(fnr), 4),
            "test_sample_size": len(y_test)
        }
        trained_models[name] = clf

        print(f"{name} -> Accuracy: {acc:.4f}, Precision: {prec:.4f}, Recall: {rec:.4f}, F1: {f1:.4f}, AUC: {auc:.4f}")

    # 2. URL Classification Pipeline
    print("\nTraining URL Classifier...")
    url_feature_rows = []
    for u in df_urls['url']:
        feat = extract_url_features(u)['features']
        url_feature_rows.append(feat)

    X_url = np.array(url_feature_rows)
    y_url = df_urls['label'].values

    X_u_train, X_u_test, y_u_train, y_u_test = train_test_split(
        X_url, y_url, test_size=0.25, random_state=42, stratify=y_url
    )

    url_clf = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42)
    url_clf.fit(X_u_train, y_u_train)
    y_u_pred = url_clf.predict(X_u_test)

    url_acc = accuracy_score(y_u_test, y_u_pred)
    url_f1 = f1_score(y_u_test, y_u_pred)
    print(f"URL Classifier -> Accuracy: {url_acc:.4f}, F1: {url_f1:.4f}")

    benchmark_results["URL Classifier (Random Forest)"] = {
        "accuracy": round(float(url_acc), 4),
        "f1_score": round(float(url_f1), 4),
        "test_sample_size": len(y_u_test)
    }

    # 3. Generate Comparative Charts
    print("\nGenerating Academic Evaluation Plots...")
    # Plot 1: Model Comparison Metrics Bar Chart
    plt.figure(figsize=(9, 5))
    metrics_to_plot = ["accuracy", "precision", "recall", "f1_score"]
    model_names = ["Logistic Regression", "Naive Bayes", "Random Forest"]
    
    x = np.arange(len(metrics_to_plot))
    width = 0.25

    colors = ["#4f46e5", "#06b6d4", "#10b981"]
    for i, m_name in enumerate(model_names):
        vals = [benchmark_results[m_name][m] for m in metrics_to_plot]
        plt.bar(x + (i * width), vals, width, label=m_name, color=colors[i], alpha=0.9)

    plt.xlabel("Evaluation Metric", fontsize=11, fontweight='bold')
    plt.ylabel("Score (0.0 to 1.0)", fontsize=11, fontweight='bold')
    plt.title("Comparative Performance Analysis Across ML Algorithms", fontsize=13, fontweight='bold', pad=15)
    plt.xticks(x + width, ["Accuracy", "Precision", "Recall", "F1-Score"], fontsize=10)
    plt.ylim(0.7, 1.02)
    plt.legend(loc='lower right', frameon=True)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, "model_comparison_chart.png"), dpi=200)
    plt.close()

    # Plot 2: Confusion Matrices
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    for i, m_name in enumerate(model_names):
        cm_data = benchmark_results[m_name]["confusion_matrix"]
        cm_matrix = np.array([[cm_data["TN"], cm_data["FP"]], [cm_data["FN"], cm_data["TP"]]])
        sns.heatmap(
            cm_matrix, annot=True, fmt='d', cmap="Blues", cbar=False, ax=axes[i],
            xticklabels=["Legitimate", "Scam"], yticklabels=["Legitimate", "Scam"]
        )
        axes[i].set_title(f"{m_name}\nAcc: {benchmark_results[m_name]['accuracy'] * 100:.1f}%", fontweight='bold')
        axes[i].set_xlabel("Predicted Label")
        axes[i].set_ylabel("True Label")

    plt.suptitle("Confusion Matrix Comparison (Test Split N = 600)", fontsize=13, fontweight='bold', y=1.03)
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, "confusion_matrices.png"), dpi=200)
    plt.close()

    # Save artifacts
    print("Saving serialized model artifacts...")
    joblib.dump(vectorizer, os.path.join(MODELS_DIR, "vectorizer.pkl"))
    joblib.dump(trained_models, os.path.join(MODELS_DIR, "text_models.pkl"))
    joblib.dump(url_clf, os.path.join(MODELS_DIR, "url_model.pkl"))

    with open(os.path.join(MODELS_DIR, "benchmark_results.json"), "w") as f:
        json.dump(benchmark_results, f, indent=4)

    print("Model training pipeline executed successfully!")
    return benchmark_results

if __name__ == "__main__":
    train_and_evaluate_all()
