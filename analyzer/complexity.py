import ast

from .findings import Finding


def analyze_function_complexity(function_node):
    complexity = 1

    for node in ast.walk(function_node):

        if isinstance(
            node,
            (ast.If, ast.For, ast.While, ast.ExceptHandler)
        ):
            complexity += 1

        if isinstance(node, ast.BoolOp):
            complexity += len(node.values) - 1

    return complexity


def check_complexity(tree):
    findings = []

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):

            complexity = analyze_function_complexity(node)

            if complexity >= 5:
                findings.append(
                    Finding(
                        "Complexity",
                        "MEDIUM",
                        node.lineno,
                        f"Function '{node.name}' has high cyclomatic complexity ({complexity}).",
                        "Consider breaking this function into smaller functions."
                    )
                )

    return findings


def is_logarithmic_loop(node):

    if not isinstance(node, ast.While):
        return False

    for child in ast.walk(node):

        if isinstance(child, ast.AugAssign):

            if isinstance(child.op, (ast.FloorDiv, ast.Div)):
                return True

        if isinstance(child, ast.Assign):

            if isinstance(child.value, ast.BinOp):

                if isinstance(child.value.op, (ast.FloorDiv, ast.Div)):
                    return True

    return False


def get_time_complexity(node):

    logarithmic = False
    max_depth = 0

    def visit(current_node, depth):

        nonlocal max_depth
        nonlocal logarithmic

        if isinstance(current_node, (ast.For, ast.While)):

            depth += 1
            max_depth = max(max_depth, depth)

            if is_logarithmic_loop(current_node):
                logarithmic = True

        for child in ast.iter_child_nodes(current_node):
            visit(child, depth)

    visit(node, 0)

    if logarithmic and max_depth == 1:
        return "O(log n)"

    if logarithmic and max_depth > 1:
        return f"O(n^{max_depth - 1} log n)"

    if max_depth == 0:
        return "O(1)"

    if max_depth == 1:
        return "O(n)"

    return f"O(n^{max_depth})"


def check_time_complexity(tree):

    findings = []

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):

            complexity = get_time_complexity(node)

            if complexity in ["O(n^3)", "O(n^4)", "O(n^5)"]:

                findings.append(
                    Finding(
                        "Performance",
                        "HIGH",
                        node.lineno,
                        f"Function '{node.name}' has estimated time complexity {complexity}.",
                        "Consider reducing nested loops or using a more efficient algorithm."
                    )
                )

    return findings


def get_space_complexity(node):

    for child in ast.walk(node):

        if isinstance(child, (ast.List, ast.ListComp)):
            return "O(n)"

        if isinstance(child, (ast.Set, ast.SetComp)):
            return "O(n)"

        if isinstance(child, (ast.Dict, ast.DictComp)):
            return "O(n)"

    return "O(1)"


def generate_complexity_report(tree):

    print()
    print("========== COMPLEXITY REPORT ==========")
    print()

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):

            cyclomatic = analyze_function_complexity(node)

            time_complexity = get_time_complexity(node)

            space_complexity = get_space_complexity(node)

            print(f"Function: {node.name}")
            print(f"Cyclomatic Complexity: {cyclomatic}")
            print(f"Time Complexity: {time_complexity}")
            print(f"Space Complexity: {space_complexity}")
            print()