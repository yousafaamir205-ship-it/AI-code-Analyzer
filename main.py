import sys

from analyzer.engine import analyze_file


def main():

    print("========================================")
    print("          AI CODE ANALYZER")
    print("========================================")
    print()

    if len(sys.argv) < 2:
        print("Usage: python main.py <python_file>")
        return

    filename = sys.argv[1]

    analyze_file(filename)


if __name__ == "__main__":
    main()