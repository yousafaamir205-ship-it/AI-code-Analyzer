"""Structured (JSON-friendly) analysis result, used by the web front end."""

import ast

from .engine import analyze
from .complexity import (
    analyze_function_complexity,
    get_time_complexity,
    get_space_complexity,
)


def _rating(score):
    if score >= 90:
        return "Excellent"
    if score >= 75:
        return "Good"
    if score >= 50:
        return "Needs Improvement"
    return "Poor"


def analyze_source(code, filename="input.py"):
    try:
        tree = ast.parse(code, filename=filename)
    except SyntaxError as e:
        return {"ok": False, "error": {"line": e.lineno or 1, "message": e.msg}}

    findings = sorted(analyze(tree), key=lambda f: f.line)

    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append({
                "name": node.name,
                "line": node.lineno,
                "cyclomatic": analyze_function_complexity(node),
                "time": get_time_complexity(node),
                "space": get_space_complexity(node),
            })
    functions.sort(key=lambda f: f["line"])

    score = max(0, min(100, 100 - sum(f.get_weight() for f in findings)))

    by_severity = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    by_category = {}
    for f in findings:
        by_severity[f.severity] = by_severity.get(f.severity, 0) + 1
        by_category[f.category] = by_category.get(f.category, 0) + 1

    return {
        "ok": True,
        "score": score,
        "rating": _rating(score),
        "total": len(findings),
        "by_severity": by_severity,
        "by_category": by_category,
        "functions": functions,
        "findings": [
            {
                "category": f.category,
                "severity": f.severity,
                "line": f.line,
                "message": f.message,
                "suggestion": f.suggestion,
            }
            for f in findings
        ],
    }
