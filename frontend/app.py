
import streamlit as st
import requests
import json

API_URL = "http://127.0.0.1:8000/review"

st.set_page_config(
    page_title="AI Code Review Assistant",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 AI Code Review & Debugging Assistant")

st.markdown(
    """
    Review your source code using static analysis and AI.

    Get bug explanations, improvement suggestions,
    corrected code, and recommended test cases.
    """
)

st.divider()

# Language selection
language = st.selectbox(
    "Select programming language",
    ["python", "java"]
)

# Code input
default_code = """def calculate_average(numbers):
    return sum(numbers) / len(numbers)
"""

code = st.text_area(
    "Paste your source code here",
    value=default_code,
    height=300
)

# Review button
if st.button("Review Code", type="primary", use_container_width=True):

    if not code.strip():
        st.warning("Please enter some source code.")

    else:
        request_data = {
            "language": language,
            "code": code
        }

        with st.spinner("Analysing your code..."):

            try:
                response = requests.post(
                    API_URL,
                    json=request_data,
                    timeout=240
                )

                response.raise_for_status()
                result = response.json()

                st.success("Code review completed!")

                # Static analysis results
                st.header("1. Static Analysis")

                findings = result.get("static_findings", [])

                if findings:
                    for finding in findings:

                        severity = finding.get("severity", "info")
                        line = finding.get("line")
                        message = finding.get("message", "")
                        suggestion = finding.get("suggestion")

                        if severity == "error":
                            st.error(message)
                        elif severity == "warning":
                            st.warning(message)
                        else:
                            st.info(message)

                        if line is not None:
                            st.caption(f"Line: {line}")

                        if suggestion:
                            st.write(f"**Suggestion:** {suggestion}")

                else:
                    st.info("No static analysis findings.")

                # AI review results
                st.divider()
                st.header("2. AI Code Review")

                ai_review = result.get("ai_review")

                if ai_review:

                    st.subheader("Overall Summary")
                    st.write(ai_review.get("summary", "No summary available."))

                    st.subheader("Identified Bugs")

                    bugs = ai_review.get("bugs", [])

                    if bugs:
                        for bug in bugs:
                            severity = bug.get("severity", "unknown").upper()

                            st.warning(
                                f"{severity}: {bug.get('description', '')}"
                            )

                            if bug.get("line") is not None:
                                st.caption(f"Line: {bug['line']}")

                            st.write(
                                f"**Suggestion:** {bug.get('suggestion', '')}"
                            )
                    else:
                        st.success("The AI did not identify any bugs.")

                    st.subheader("Improvement Suggestions")

                    improvements = ai_review.get("improvements", [])

                    if improvements:
                        for improvement in improvements:
                            st.write(f"- {improvement}")
                    else:
                        st.write("No additional improvements suggested.")

                    st.subheader("Corrected Code")

                    corrected_code = ai_review.get("corrected_code", "")

                    st.code(
                        corrected_code,
                        language=language
                    )

                    if corrected_code:
                        st.download_button(
                            "Download Corrected Code",
                            data=corrected_code,
                            file_name=(
                                "corrected_code.py"
                                if language == "python"
                                else "CorrectedCode.java"
                            ),
                            mime="text/plain"
                        )

                    st.subheader("Recommended Test Cases")

                    test_cases = ai_review.get("test_cases", [])

                    if test_cases:
                        for index, test in enumerate(test_cases, start=1):
                            with st.expander(f"Test Case {index}"):
                                st.write(
                                    f"**Input:** {test.get('input', '')}"
                                )
                                st.write(
                                    f"**Expected Output:** "
                                    f"{test.get('expected_output', '')}"
                                )
                                st.write(
                                    f"**Description:** "
                                    f"{test.get('description', '')}"
                                )
                    else:
                        st.info("No test cases were generated.")

                else:
                    st.warning(
                        "AI review was unavailable. "
                        "Showing static analysis results only."
                    )
                    st.write(result.get("status", ""))

                # Complete JSON response
                st.divider()

                with st.expander("View Complete API Response"):
                    st.json(result)

                # Download report
                st.download_button(
                    "Download Full Review Report (JSON)",
                    data=json.dumps(result, indent=4),
                    file_name="code_review_report.json",
                    mime="application/json"
                )

            except requests.exceptions.ConnectionError:
                st.error(
                    "Cannot connect to the backend. "
                    "Start the FastAPI server first."
                )

            except requests.exceptions.Timeout:
                st.error(
                    "The request timed out. Try reviewing shorter code."
                )

            except requests.exceptions.HTTPError as exc:
                st.error(f"Backend returned an error: {exc}")

            except requests.exceptions.RequestException as exc:
                st.error(f"Request failed: {exc}")

            except ValueError as exc:
                st.error(f"Invalid response from backend: {exc}")
