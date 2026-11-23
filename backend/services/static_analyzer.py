
import ast
from typing import List
from backend.schemas import Finding


def analyze_python(code: str) -> List[Finding]:
    findings = []

    if not code.strip():
        return [
            Finding(
                severity="error",
                message="The submitted code is empty."
            )
        ]

    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        return [
            Finding(
                severity="error",
                line=exc.lineno,
                message=f"Syntax error: {exc.msg}",
                suggestion="Check the syntax around the reported line."
            )
        ]

    for node in ast.walk(tree):

        # Detect bare except blocks
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            findings.append(
                Finding(
                    severity="warning",
                    line=node.lineno,
                    message="Bare except clause detected.",
                    suggestion="Catch specific exception types."
                )
            )

        # Detect mutable default arguments
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for default in node.args.defaults:
                if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                    findings.append(
                        Finding(
                            severity="warning",
                            line=node.lineno,
                            message=(
                                f"Function '{node.name}' uses a mutable "
                                "default argument."
                            ),
                            suggestion=(
                                "Use None as the default and create "
                                "the mutable object inside the function."
                            )
                        )
                    )

        # Detect comparisons such as value == True
        if isinstance(node, ast.Compare):
            for comparator in node.comparators:
                if isinstance(comparator, ast.Constant) and isinstance(
                    comparator.value, bool
                ):
                    findings.append(
                        Finding(
                            severity="info",
                            line=node.lineno,
                            message="Comparison with a boolean literal detected.",
                            suggestion="Consider using the boolean expression directly."
                        )
                    )

    if not findings:
        findings.append(
            Finding(
                severity="info",
                message="No issues detected by the implemented static checks."
            )
        )

    return findings


def analyze_code(code: str, language: str) -> List[Finding]:
    if language == "python":
        return analyze_python(code)

    if language == "java":
        return [
            Finding(
                severity="info",
                message=(
                    "Java static analysis is not implemented yet. "
                    "AI-based review can still be performed."
                )
            )
        ]

    return [
        Finding(
            severity="error",
            message="Unsupported programming language."
        )
    ]
