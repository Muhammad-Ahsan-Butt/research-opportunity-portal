"""
Integration tests for University Research Opportunity Portal API.
Covers all 8 test scenarios defined in Section 6 of the assignment.
"""

import sys
import os
import unittest

# Add backend directory to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app import app
from db import init_db


class TestOpportunityAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        cls.client = app.test_client()

    def test_01_create_first_opportunity(self):
        payload = {
            "title": "Quantum Computing Algorithms for Cryptanalysis",
            "description": "Research on Shor and Grover algorithms and fault-tolerant quantum error correction.",
            "research_area": "Quantum Computing & Security",
            "faculty_name": "Dr. Usman Farooq",
            "department": "Computer Science",
            "required_skills": "Linear Algebra, Python, Qiskit",
            "positions_available": 2,
            "deadline": "2026-12-31",
            "status": "Open"
        }
        response = self.client.post("/api/opportunities", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertIn("id", data["data"])
        self.assertEqual(data["data"]["title"], payload["title"])
        TestOpportunityAPI.created_id_1 = data["data"]["id"]

    def test_02_create_second_opportunity(self):
        payload = {
            "title": "Autonomous Swarm Robotics Communication",
            "description": "Design of decentralized mesh networking protocols for multi-agent UAV swarms.",
            "research_area": "Robotics & Distributed Systems",
            "faculty_name": "Dr. Sana Jahangir",
            "department": "Electrical Engineering",
            "required_skills": "C++, ROS2, Wireless Sensor Networks",
            "positions_available": 3,
            "deadline": "2026-11-15",
            "status": "Open"
        }
        response = self.client.post("/api/opportunities", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertTrue(data["success"])
        TestOpportunityAPI.created_id_2 = data["data"]["id"]

    def test_03_create_third_opportunity(self):
        payload = {
            "title": "NLP for Low-Resource Regional Languages",
            "description": "Fine-tuning open-source LLMs for Pashto and Urdu translation and sentiment analysis.",
            "research_area": "Natural Language Processing",
            "faculty_name": "Dr. Kamran Ali",
            "department": "Software Engineering",
            "required_skills": "HuggingFace, PyTorch, Tokenization",
            "positions_available": 1,
            "deadline": "2026-10-30",
            "status": "Open"
        }
        response = self.client.post("/api/opportunities", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertTrue(data["success"])
        TestOpportunityAPI.created_id_3 = data["data"]["id"]

    def test_04_retrieve_all_opportunities(self):
        response = self.client.get("/api/opportunities")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertIsInstance(data["data"], list)
        self.assertGreaterEqual(len(data["data"]), 3)

    def test_05_retrieve_one_opportunity_by_id(self):
        target_id = getattr(self, "created_id_1", 1)
        response = self.client.get(f"/api/opportunities/{target_id}")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["id"], target_id)

    def test_06_update_existing_opportunity(self):
        target_id = getattr(self, "created_id_1", 1)
        update_payload = {
            "title": "Updated: Quantum Computing & Post-Quantum Cryptography",
            "positions_available": 4,
            "required_skills": "Linear Algebra, Python, Qiskit, Lattice Cryptography"
        }
        response = self.client.put(f"/api/opportunities/{target_id}", json=update_payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["title"], update_payload["title"])
        self.assertEqual(data["data"]["positions_available"], 4)

    def test_07_change_status_from_open_to_closed(self):
        target_id = getattr(self, "created_id_1", 1)
        status_payload = {"status": "Closed"}
        response = self.client.put(f"/api/opportunities/{target_id}", json=status_payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["status"], "Closed")

    def test_08_delete_opportunity(self):
        target_id = getattr(self, "created_id_3", 3)
        response = self.client.delete(f"/api/opportunities/{target_id}")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])

    def test_09_verify_deleted_opportunity_returns_404(self):
        target_id = getattr(self, "created_id_3", 3)
        response = self.client.get(f"/api/opportunities/{target_id}")
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertFalse(data["success"])
        self.assertIn("error", data)

    def test_10_invalid_request_missing_fields_returns_400(self):
        # Missing required fields like faculty_name, description, positions_available
        invalid_payload = {
            "title": "Invalid Incomplete Opportunity"
        }
        response = self.client.post("/api/opportunities", json=invalid_payload)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data["success"])
        self.assertIn("error", data)


if __name__ == "__main__":
    unittest.main()
