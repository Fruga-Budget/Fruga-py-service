import os
import pytest
import vcr
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
vcr = vcr.VCR(
    cassette_library_dir='tests/cassettes',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
    record_mode='once',  # or 'new_episodes', 'none', 'all' depending on your use case
    match_on=['method', 'scheme', 'host', 'port', 'path', 'query', 'body'],
    filter_headers=['Authorization']
)

@vcr.use_cassette('generate_advice.yaml')
def test_generate_advice():
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        pytest.fail("OpenAI API key is missing!")

    headers = {"Authorization": f"Bearer {openai_api_key}"}
    response = client.post("/v1/generate_advice", json={
        "total_income": 5000,
        "needs": [
            {"name": "Rent", "cost": 1500, "description": "On a lease, this can't be changed!", "isNegotiable": False},
            {"name": "Utilities", "cost": 500, "description": "", "isNegotiable": True},
            {"name": "Misc.", "cost": 500, "description": "Food Budget, Gas", "isNegotiable": False}
        ],
        "wants": [
            {"name": "Dining Out", "cost": 500, "description": "Yummy!"},
            {"name": "Entertainment", "cost": 500, "description": "Going to the movies is important to me"},
            {"name": "Starbucks Coffee", "cost": 200, "description": "I don't know how to make coffee"},
            {"name": "Shoes", "cost": 500, "description": "Every time I drive by DSW I buy shoes"}
        ],
        "savings": [
            {"name": "401k", "cost": 200, "description": "Deposited from paycheck at work."},
            {"name": "Savings Account", "cost": 800, "description": "0.5% apr"}
        ]
    }, headers=headers)

    print("Request headers:", response.request.headers)
    print("Request body:", response.request.content.decode('utf-8'))
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())

    assert response.status_code == 200
    data = response.json()
    assert "advice" in data
