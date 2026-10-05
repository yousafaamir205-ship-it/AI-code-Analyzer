# Code Analyzer

Static analysis for Python files, built on the `ast` module. Checks security,
complexity, performance and code quality, estimates time/space complexity per
function, and gives a 0-100 code health score.

## Run the web front end (no dependencies)

    python server.py          # http://127.0.0.1:8000

Paste code or open a .py file, then press Analyze (Ctrl+Enter). Findings are
marked in the line-number gutter; click "Line N" to jump to the code.

## Run from the command line

    python main.py sample.py

## Layout

    analyzer/
      security.py     eval/exec/subprocess checks
      complexity.py   cyclomatic, time and space complexity
      quality.py      nested loops, long functions, argument count, print, import *
      findings.py     Finding class + severity weights
      engine.py       runs every rule, builds the CLI report
      report.py       same analysis as JSON (used by the web UI)
    server.py         tiny HTTP server for the front end
    web/index.html    the front end
