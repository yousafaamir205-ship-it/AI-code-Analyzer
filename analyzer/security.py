import ast

from .findings import Finding


def check_security(tree):
    findings = []

    for node in ast.walk(tree):

        if isinstance(node, ast.Call):

            if isinstance(node.func, ast.Name):

                if node.func.id == "eval":
                    findings.append(
                        Finding(
                            "Security",
                            "HIGH",
                            node.lineno,
                            "eval() can execute arbitrary code.",
                            "Avoid eval() with untrusted input."
                        )
                    )

                if node.func.id == "exec":
                    findings.append(
                        Finding(
                            "Security",
                            "HIGH",
                            node.lineno,
                            "exec() can execute arbitrary code.",
                            "Avoid exec() with untrusted input."
                        )
                    )

        if isinstance(node, ast.Import):

            for alias in node.names:

                if alias.name == "subprocess":
                    findings.append(
                        Finding(
                            "Security",
                            "MEDIUM",
                            node.lineno,
                            "subprocess module is being used.",
                            "Review subprocess calls carefully, especially when user input is involved."
                        )
                    )

    return findings