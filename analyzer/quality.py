import ast

from .findings import Finding


def check_nested_loops(tree):

    findings = []

    for function in ast.walk(tree):

        if not isinstance(function, ast.FunctionDef):
            continue

        found_nested_loop = False

        for node in ast.walk(function):

            if isinstance(node, (ast.For, ast.While)):

                for child in ast.walk(node):

                    if child is node:
                        continue

                    if isinstance(child, (ast.For, ast.While)):
                        found_nested_loop = True
                        break

                if found_nested_loop:
                    break

        if found_nested_loop:

            findings.append(
                Finding(
                    "Performance",
                    "MEDIUM",
                    function.lineno,
                    f"Function '{function.name}' contains nested loops.",
                    "Consider reducing loop nesting or using a more efficient algorithm."
                )
            )

    return findings

def check_long_functions(tree):
    findings = []

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef) and hasattr(node, "end_lineno"):

            lines = node.end_lineno - node.lineno + 1

            if lines > 30:
                findings.append(
                    Finding(
                        "Code Quality",
                        "LOW",
                        node.lineno,
                        f"Function '{node.name}' contains {lines} lines.",
                        "Consider breaking this function into smaller functions."
                    )
                )

    return findings


def check_function_arguments(tree):
    findings = []

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):

            argument_count = len(node.args.args)

            if argument_count > 5:
                findings.append(
                    Finding(
                        "Code Quality",
                        "LOW",
                        node.lineno,
                        f"Function '{node.name}' has {argument_count} arguments.",
                        "Consider grouping related arguments into an object or data structure."
                    )
                )

    return findings


def check_print_statements(tree):
    findings = []

    for node in ast.walk(tree):

        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):

            if node.func.id == "print":
                findings.append(
                    Finding(
                        "Code Quality",
                        "LOW",
                        node.lineno,
                        "print() statement detected.",
                        "Consider using a logging framework instead of print() for application output."
                    )
                )

    return findings


def check_wildcard_imports(tree):
    findings = []

    for node in ast.walk(tree):

        if isinstance(node, ast.ImportFrom):

            for alias in node.names:

                if alias.name == "*":
                    findings.append(
                        Finding(
                            "Code Quality",
                            "MEDIUM",
                            node.lineno,
                            "Wildcard import detected.",
                            "Import specific names instead of using import *."
                        )
                    )

    return findings