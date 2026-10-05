class Finding:

    SEVERITY_WEIGHTS = {
        "HIGH": 15,
        "MEDIUM": 8,
        "LOW": 3
    }

    def __init__(self, category, severity, line, message, suggestion):
        self.category = category
        self.severity = severity
        self.line = line
        self.message = message
        self.suggestion = suggestion

    def display(self):
        print(f"[{self.severity}] {self.category}")
        print(f"Line: {self.line}")
        print(f"Issue: {self.message}")
        print(f"Suggestion: {self.suggestion}")
        print()

    def get_weight(self):
        return self.SEVERITY_WEIGHTS.get(self.severity, 0)