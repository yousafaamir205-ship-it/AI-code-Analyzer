import ast
import os

from .security import check_security

from .quality import (
    check_nested_loops,
    check_long_functions,
    check_function_arguments,
    check_print_statements,
    check_wildcard_imports
)

from .complexity import (
    check_complexity,
    check_time_complexity,
    generate_complexity_report
)


def analyze(tree):

    findings = []

    rules = [
        check_security,
        check_complexity,
        check_nested_loops,
        check_long_functions,
        check_function_arguments,
        check_print_statements,
        check_wildcard_imports,
        check_time_complexity
    ]

    for rule in rules:
        findings.extend(rule(tree))

    return findings


def analyze_file(filename):

    if not filename.endswith(".py"):
        print("Error: Please provide a Python (.py) file.")
        return

    if not os.path.isfile(filename):
        print(f"File not found: {filename}")
        return

    try:

        with open(filename, "r", encoding="utf-8") as file:
            code = file.read()

        tree = ast.parse(code, filename=filename)

        print(f"Analyzing: {filename}")
        print("Code is syntactically correct.")
        print()

        generate_complexity_report(tree)

        findings = analyze(tree)

        print("========== FINDINGS ==========")
        print()

        if not findings:
            print("No issues found.")

        for finding in findings:
            finding.display()

        generate_summary(findings, filename)

    except SyntaxError as e:

        print(
            f"Syntax error on line {e.lineno}: {e.msg}"
        )


def generate_summary(findings, filename):

    high = 0
    medium = 0
    low = 0

    security = 0
    performance = 0
    quality = 0
    complexity = 0

    for finding in findings:

        if finding.severity == "HIGH":
            high += 1

        elif finding.severity == "MEDIUM":
            medium += 1

        elif finding.severity == "LOW":
            low += 1

        if finding.category == "Security":
            security += 1

        elif finding.category == "Performance":
            performance += 1

        elif finding.category == "Code Quality":
            quality += 1

        elif finding.category == "Complexity":
            complexity += 1

    total = len(findings)

    score = 100

    for finding in findings:
        score -= finding.get_weight()

    score = max(0, min(100, score))

    if score >= 90:
        rating = "Excellent"

    elif score >= 75:
        rating = "Good"

    elif score >= 50:
        rating = "Needs Improvement"

    else:
        rating = "Poor"

    print()
    print("========================================")
    print("           ANALYSIS SUMMARY")
    print("========================================")
    print()

    print(f"File: {filename}")
    print()

    print(f"Total Issues: {total}")
    print()

    print(f"HIGH:   {high}")
    print(f"MEDIUM: {medium}")
    print(f"LOW:    {low}")
    print()

    print(f"Security Issues:    {security}")
    print(f"Performance Issues: {performance}")
    print(f"Code Quality:       {quality}")
    print(f"Complexity Issues:  {complexity}")
    print()

    print(f"Code Health Score: {score}/100")
    print(f"Code Health Rating: {rating}")