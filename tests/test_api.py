
from fastapi.testclient import TestClient
from unittest.mock import patch

from backend.main import app

client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == (
        "AI Code Review Assistant API is running"
    )


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@patch("backend.main.review_code")
def test_review_endpoint(mock_review_code):

    mock_review_code.return_value = {
        "summary": "The code may fail for an empty list.",
        "bugs": [
            {
                "severity": "medium",
                "line": 2,
                "description": "Division by zero for an empty list.",
                "suggestion": "Check whether the list is empty."
            }
        ],
        "improvements": [
            "Add input validation."
        ],
        "corrected_code": (
            "def calculate_average(numbers):\n"
            "    if not numbers:\n"
            "        return 0\n"
            "    return sum(numbers) / len(numbers)"
        ),
        "test_cases": [
            {
                "input": "[]",
                "expected_output": "0",
                "description": "Tests an empty list."
            }
        ]
    }

    request_data = {
        "language": "python",
        "code": (
            "def calculate_average(numbers):\n"
            "    return sum(numbers) / len(numbers)"
        )
    }

    response = client.post("/review", json=request_data)

    assert response.status_code == 200

    result = response.json()

    assert result["language"] == "python"
    assert result["status"] == "completed"
    assert result["ai_review"]["summary"] == (
        "The code may fail for an empty list."
    )
    assert len(result["ai_review"]["bugs"]) == 1

    mock_review_code.assert_called_once()


def test_review_endpoint_invalid_language():

    request_data = {
        "language": "javascript",
        "code": "console.log('Hello');"
    }

    response = client.post("/review", json=request_data)

    assert response.status_code == 422


@patch("backend.main.review_code")
def test_review_endpoint_ai_unavailable(mock_review_code):

    mock_review_code.side_effect = RuntimeError(
        "Cannot connect to Ollama."
    )

    request_data = {
        "language": "python",
        "code": "def add(a, b):\n    return a + b"
    }

    response = client.post("/review", json=request_data)

    assert response.status_code == 200

    result = response.json()

    assert result["ai_review"] is None
    assert result["status"].startswith("static_only:")
