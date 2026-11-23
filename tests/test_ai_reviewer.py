from backend.services.ai_reviewer import review_code


def test_ai_code_review():

    code = """
def calculate_average(numbers):
    return sum(numbers) / len(numbers)
"""

    result = review_code(code, "python")

    assert isinstance(result, dict)
    assert "summary" in result
    assert "bugs" in result
    assert "improvements" in result
    assert "corrected_code" in result
    assert "test_cases" in result

    print("\nAI REVIEW RESULT:")
    print(result)