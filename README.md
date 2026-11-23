
# AI Code Review & Debugging Assistant

An AI-powered code review application that combines Python static analysis with a locally hosted Large Language Model (Gemma 3) to identify potential bugs, explain code issues, suggest improvements, and generate test cases.

## Features

- **AI-powered code review:** Uses Ollama and Gemma 3 4B to analyse submitted source code.
- **Static analysis:** Detects selected Python issues using Python's AST module.
- **Bug detection:** Identifies potential logical errors and runtime issues.
- **Code improvements:** Generates suggestions and corrected source code.
- **Test case generation:** Recommends test cases with expected outputs.
- **REST API:** FastAPI backend with interactive Swagger documentation.
- **Web interface:** Streamlit frontend.
- **Downloadable reports:** Export review results as JSON or corrected source code.
- **Automated testing:** Pytest tests for static analysis and API endpoints.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Backend | FastAPI |
| Frontend | Streamlit |
| AI Model | Gemma 3 4B |
| LLM Runtime | Ollama |
| Static Analysis | Python AST |
| API Testing | FastAPI TestClient |
| Testing Framework | Pytest |
| HTTP Client | Requests |
| Data Validation | Pydantic |
| Version Control | Git |

## Architecture

```text
              User
                |
                v
         Streamlit Frontend
                |
                v
          FastAPI Backend
                |
         Code Validation
                |
          +-----+-----+
          |           |
          v           v
     Static         Ollama
    Analyzer       Gemma 3
          |           |
          +-----+-----+
                |
                v
        Structured JSON
                |
                v
         Review Results
                |
                v
             User
```

## Project Structure

```text
ai-code-review-assistant/
|
|-- backend/
|   |-- __init__.py
|   |-- main.py
|   |-- schemas.py
|   |
|   |-- services/
|       |-- __init__.py
|       |-- ai_reviewer.py
|       |-- static_analyzer.py
|
|-- frontend/
|   |-- app.py
|
|-- tests/
|   |-- test_analyzer.py
|   |-- test_ai_reviewer.py
|   |-- test_api.py
|
|-- docs/
|
|-- .gitignore
|-- pytest.ini
|-- requirements.txt
|-- README.md
```

## Prerequisites

- Python 3.10 or later
- Ollama
- Gemma 3 4B model
- Git

## Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd ai-code-review-assistant
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and configure Ollama

Install Ollama from:

https://ollama.com/

Download the model:

```bash
ollama pull gemma3:4b
```

Start Ollama if it is not already running.

## Running the Application

### 1. Start the FastAPI backend

```bash
uvicorn backend.main:app --reload
```

Backend:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

### 2. Start the Streamlit frontend

Open another terminal:

```bash
source venv/bin/activate
streamlit run frontend/app.py
```

Frontend:

http://localhost:8501

## Running Tests

Run the complete test suite:

```bash
pytest -v
```

Run static analyzer tests:

```bash
pytest -v tests/test_analyzer.py
```

Run API tests:

```bash
pytest -v tests/test_api.py
```

Run the Ollama integration test:

```bash
pytest -v -s tests/test_ai_reviewer.py
```

Note: The AI integration test requires Ollama to be running with the Gemma 3 4B model available.

## Supported Languages

| Language | Static Analysis | AI Review |
|---|---|---|
| Python | Implemented checks | Supported |
| Java | Not implemented | Supported |

Java static analysis is not currently implemented.

## Security and Limitations

- Submitted source code is analysed but not executed.
- AI-generated reviews may contain incorrect suggestions and should be verified.
- Static analysis currently covers a limited set of Python checks.
- AI review requires a running local Ollama service.
- This application is intended as a developer assistance tool, not a replacement for professional code review or comprehensive security testing.

## Future Improvements

- Expand static analysis for Python and Java.
- Add code quality and complexity metrics.
- Implement AI evaluation benchmarks.
- Add response quality scoring.
- Support additional programming languages.
- Add code review history and reporting.

## Author

Madan Reddy P R

Computer Science Engineer

GitHub: <YOUR_GITHUB_PROFILE_URL>
