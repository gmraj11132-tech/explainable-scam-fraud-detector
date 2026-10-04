"""
Automated System Verification Tests.
Validates ML models, XAI explainability engine, SQLite database, and Flask REST endpoints.
"""

import os
import unittest
import json
from app import app
from ml_engine.url_features import extract_url_features
from database.db import log_scan, get_recent_scans, get_statistics

class SystemTestSuite(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_01_index_page(self):
        """Test home page loads with 200 OK."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ScamGuard XAI", response.data)

    def test_02_url_features(self):
        """Test lexical & structural URL feature extraction."""
        phish_url = "http://sbi-kyc-verify-portal.xyz/login.php"
        report = extract_url_features(phish_url)
        self.assertGreater(report["risk_score"], 20)
        self.assertEqual(report["domain"], "sbi-kyc-verify-portal.xyz")
        self.assertIn("url_length", report["feature_names"])

    def test_03_text_analysis_scam(self):
        """Test text scam detection with Explainable AI attribution."""
        scam_text = "Dear customer, your bank account will be blocked today due to pending KYC. Update PAN immediately at http://sbi-kyc.xyz"
        response = self.client.post('/api/analyze/text', 
            data=json.dumps({"text": scam_text, "model": "Logistic Regression"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("risk_score", data)
        self.assertGreaterEqual(data["risk_score"], 60)
        self.assertIn("token_weights", data)
        self.assertGreater(len(data["token_weights"]), 0)
        self.assertIn("recommendations", data)

    def test_04_text_analysis_legitimate(self):
        """Test legitimate message receives low risk score."""
        legit_text = "Dear customer, INR 1,500.00 debited from account **4582 on 04-Oct-2026 at Amazon India. Available balance is INR 45,200.00."
        response = self.client.post('/api/analyze/text',
            data=json.dumps({"text": legit_text, "model": "Random Forest"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertLess(data["risk_score"], 35)

    def test_05_url_endpoint(self):
        """Test URL inspection endpoint."""
        response = self.client.post('/api/analyze/url',
            data=json.dumps({"url": "http://192.168.1.105/bank/verify"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("risk_score", data)
        self.assertIn("entropy", data)

    def test_06_database_logging(self):
        """Test SQLite database logging and analytics."""
        scan_id = log_scan(
            input_type="text",
            preview="Test scam sample",
            risk_score=85,
            verdict="Scam",
            verdict_badge="danger",
            model_name="Test Model",
            signals=[],
            recs=[],
            tokens=[]
        )
        self.assertIsNotNone(scan_id)
        scans = get_recent_scans(5)
        self.assertGreater(len(scans), 0)
        stats = get_statistics()
        self.assertGreaterEqual(stats["total_scans"], 1)

    def test_07_downloads_available(self):
        """Test that generated PDF and PPTX files exist and can be downloaded."""
        res_paper = self.client.get('/download/paper')
        self.assertEqual(res_paper.status_code, 200)
        self.assertEqual(res_paper.content_type, 'application/pdf')

        res_ppt = self.client.get('/download/presentation')
        self.assertEqual(res_ppt.status_code, 200)
        self.assertIn('presentation', res_ppt.content_type)

if __name__ == '__main__':
    unittest.main()
