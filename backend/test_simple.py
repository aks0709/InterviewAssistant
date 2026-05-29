#!/usr/bin/env python3
"""Test script for Agent 1 API endpoint."""

import requests
import json

API_URL = "http://localhost:8001/agent1/evaluate"

# Test data
test_data = {
    "jd_text": "We are looking for a Python developer with experience in FastAPI, machine learning, and vector databases. Must have knowledge of REST APIs and cloud deployment.",
    "resume_text": "Experienced Python developer with 3 years in FastAPI development. Worked with machine learning models and vector databases like FAISS. Strong background in REST API development and AWS cloud services."
}

def test_api():
    """Test the Agent 1 evaluate endpoint."""
    try:
        print("Testing Agent 1 API endpoint...")
        print(f"URL: {API_URL}")
        print(f"Request data: JD length={len(test_data['jd_text'])}, Resume length={len(test_data['resume_text'])}")
        
        response = requests.post(
            API_URL,
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("SUCCESS!")
            print(f"Similarity Score: {result.get('similarity_score', 'N/A')}")
            print(f"Match Percentage: {result.get('match_percentage', 'N/A')}%")
            print(f"Key Matches: {len(result.get('key_matches', []))}")
            print(f"Missing Skills: {len(result.get('missing_skills', []))}")
            print(f"Recommendations: {result.get('recommendations', 'N/A')}")
        else:
            print("FAILED!")
            print(f"Error response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("CONNECTION ERROR: Backend server is not running on port 8001")
    except requests.exceptions.Timeout:
        print("TIMEOUT ERROR: Request took too long")
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    test_api()