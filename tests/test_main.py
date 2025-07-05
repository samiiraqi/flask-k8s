import pytest
import json
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_index_page(client):
    """Test the index page loads correctly"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Flask K8s Application' in response.data

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert data['service'] == 'flask-k8s'

def test_api_data_get(client):
    """Test GET request to /api/data"""
    response = client.get('/api/data')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'platform' in data
    assert 'python_version' in data

def test_api_data_post_valid(client):
    """Test POST request with valid data"""
    test_data = {'name': 'test', 'message': 'hello'}
    response = client.post('/api/data', 
                          data=json.dumps(test_data),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'

def test_api_data_post_invalid(client):
    """Test POST request with invalid data"""
    test_data = {'invalid': 'data'}
    response = client.post('/api/data', 
                          data=json.dumps(test_data),
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
