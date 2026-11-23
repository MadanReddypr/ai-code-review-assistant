
from fastapi import FastAPI
from backend.schemas import CodeReviewRequest, CodeReviewResponse
from backend.services.static_analyzer import analyze_code
from backend.services.ai_reviewer import review_code

app = FastAPI(
    title="AI Code Review Assistant",
    description="An AI-powered code review and debugging assistant.",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "AI Code Review Assistant API is running",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "AI Code Review Assistant"
    }


@app.post("/review", response_model=CodeReviewResponse)
def review_submission(request: CodeReviewRequest):

    # Run static analysis first
    static_findings = analyze_code(
        request.code,
        request.language
    )

    # Run AI review
    try:
        ai_result = review_code(
            request.code,
            request.language
        )

        status = "completed"

    except RuntimeError as exc:
        ai_result = None
        status = f"static_only: {str(exc)}"

    return CodeReviewResponse(
        language=request.language,
        static_findings=static_findings,
        ai_review=ai_result,
        status=status
    )

