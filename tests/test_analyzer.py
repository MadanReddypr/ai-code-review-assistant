
from backend.services.static_analyzer import analyze_python


def test_detects_syntax_error():
    code = "def add(a, b)"
    results = analyze_python(code)

    assert any(item.severity == "error" for item in results)


def test_detects_bare_except():
    code = """
try:
    print("Hello")
except:
    print("Error")
"""
    results = analyze_python(code)

    assert any("Bare except" in item.message for item in results)


def test_detects_mutable_default():
    code = """
def add_item(item, items=[]):
    items.append(item)
    return items
"""
    results = analyze_python(code)

    assert any("mutable default" in item.message for item in results)


def test_valid_code():
    code = """
def add(a, b):
    return a + b
"""
    results = analyze_python(code)

    assert not any(item.severity == "error" for item in results)
