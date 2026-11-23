
import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:4b"

REVIEW_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {
            "type": "string"
        },
        "bugs": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "severity": {
                        "type": "string",
                        "enum": ["high", "medium", "low"]
                    },
                    "line": {
                        "type": ["integer", "null"]
                    },
                    "description": {
                        "type": "string"
                    },
                    "suggestion": {
                        "type": "string"
                    }
                },
                "required": [
                    "severity",
                    "line",
                    "description",
                    "suggestion"
                ],
                "additionalProperties": False
            }
        },
        "improvements": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "corrected_code": {
            "type": "string"
        },
        "test_cases": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "input": {
                        "type": "string"
                    },
                    "expected_output": {
                        "type": "string"
                    },
                    "description": {
                        "type": "string"
                    }
                },
                "required": [
                    "input",
                    "expected_output",
                    "description"
                ],
                "additionalProperties": False
            }
        }
    },
    "required": [
        "summary",
        "bugs",
        "improvements",
        "corrected_code",
        "test_cases"
    ],
    "additionalProperties": False
}


def review_code(code: str, language: str) -> dict:

    prompt = f"""
You are a senior software engineer performing a detailed code review.

Review the following {language} source code.

Analyze:
1. Actual bugs and logical errors.
2. Runtime errors and edge cases.
3. Code quality and performance.
4. Corrected source code.
5. Useful unit test cases.

Rules:
- Do not invent bugs.
- If there are no bugs, return an empty bugs array.
- If there are no improvements, return an empty improvements array.
- If the code is correct, clearly state that in the summary.
- Do not claim that code was executed.
- Preserve the original programming language.
- Return all required fields in the requested JSON structure.

Source code:

{code}
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": REVIEW_SCHEMA,
        "options": {
            "temperature": 0.1,
            "num_ctx": 4096,
            "num_predict": 1500
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=180
        )

        response.raise_for_status()

        result = response.json()
        ai_text = result.get("response", "").strip()

        if not ai_text:
            raise RuntimeError(
                "Ollama returned an empty response."
            )

        review = json.loads(ai_text)

        if not isinstance(review, dict):
            raise RuntimeError(
                "AI response must be a JSON object."
            )

        required_fields = {
            "summary",
            "bugs",
            "improvements",
            "corrected_code",
            "test_cases"
        }

        missing_fields = required_fields - review.keys()

        if missing_fields:
            raise RuntimeError(
                f"Missing fields: {missing_fields}. "
                f"Actual response: {ai_text}"
            )

        if not isinstance(review["summary"], str):
            raise RuntimeError("Invalid summary format.")

        if not isinstance(review["bugs"], list):
            raise RuntimeError("Invalid bugs format.")

        if not isinstance(review["improvements"], list):
            raise RuntimeError("Invalid improvements format.")

        if not isinstance(review["corrected_code"], str):
            raise RuntimeError("Invalid corrected_code format.")

        if not isinstance(review["test_cases"], list):
            raise RuntimeError("Invalid test_cases format.")

        return review

    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(
            "Cannot connect to Ollama. Check whether Ollama is running."
        ) from exc

    except requests.exceptions.Timeout as exc:
        raise RuntimeError(
            "AI review timed out. Try shorter source code."
        ) from exc

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(
            f"Ollama API error: {exc}"
        ) from exc

    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "Ollama returned invalid JSON."
        ) from exc
