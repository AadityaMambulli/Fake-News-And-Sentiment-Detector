import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data == {"status": "ok"}

def test_analyze_empty_payload(client):
    response = client.post('/api/analyze', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False

def test_analyze_empty_text(client):
    response = client.post('/api/analyze', json={"text": "   "})
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False

def test_analyze_valid_text(client):
    response = client.post('/api/analyze', json={"text": "Government announces new economic policy to boost tech startups."})
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert "fake_news" in data
    assert "sentiment" in data
    assert "label" in data["fake_news"]
    assert "confidence" in data["fake_news"]
    assert "label" in data["sentiment"]
    assert "confidence" in data["sentiment"]
