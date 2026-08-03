import unittest
import io
import json
import os
import sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.pipeline import pipeline

class TestSmartRetailPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pipeline.initialize()

    def test_01_pipeline_initialized(self):
        self.assertTrue(pipeline.is_initialized)

    def test_02_positive_sentiment(self):
        res = pipeline.analyze_sentiment("The quality of this leather jacket is exceptional. Super comfortable and stylish!")
        self.assertEqual(res["sentiment"], "positive")
        self.assertGreater(res["confidence"], 0.35)

    def test_03_negative_sentiment(self):
        res = pipeline.analyze_sentiment("Battery life is terrible, died in less than 4 hours. Waste of money.")
        self.assertEqual(res["sentiment"], "negative")
        self.assertGreater(res["confidence"], 0.35)

    def test_04_chatbot_rule_matching(self):
        res = pipeline.process_chat("Where is my order?")
        self.assertEqual(res["intent"], "order_status")
        self.assertIn("Rule-Based", res["strategy_used"])

    def test_05_chatbot_return_policy(self):
        res = pipeline.process_chat("What is your return policy?")
        self.assertEqual(res["intent"], "return_policy")

    def test_06_product_classifier(self):
        img = Image.new('RGB', (224, 224), color=(120, 80, 200))
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        img_bytes = buf.getvalue()
        
        res = pipeline.classify_product(img_bytes)
        self.assertIn("predicted_category", res)
        self.assertIn(res["predicted_category"], ["clothing", "shoes", "electronics", "bags", "groceries"])

    def test_07_face_recognition(self):
        img = Image.new('RGB', (300, 300), color=(73, 109, 137))
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        img_bytes = buf.getvalue()
        
        res = pipeline.recognize_face(img_bytes)
        self.assertIn(res["status"], ["recognized", "unrecognized"])
        self.assertGreaterEqual(res["total_visits"], 1)

    def test_08_aggregate_stats(self):
        stats = pipeline.get_aggregate_stats()
        self.assertIn("total_customer_visits", stats)
        self.assertIn("sentiment_summary", stats)
        self.assertEqual(stats["system_status"], "HEALTHY")

if __name__ == "__main__":
    unittest.main()
