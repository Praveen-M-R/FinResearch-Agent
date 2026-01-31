"""
Tests for health check endpoints
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_health_check():
    """Test root endpoint returns healthy status"""
    response = client.get("/api/v1/")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert "app" in data
    assert "version" in data
    assert "environment" in data


def test_detailed_health_check():
    """Test detailed health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert "app" in data
    assert "version" in data
    assert "environment" in data
    assert "debug" in data


def test_health_response_schema():
    """Test health response follows expected schema"""
    response = client.get("/api/v1/")
    data = response.json()

    # Check required fields
    required_fields = ["status", "app", "version", "environment"]
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"
