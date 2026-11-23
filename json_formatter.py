#!/usr/bin/env python3
"""json-formatter -- pretty-print, minify, sort and validate JSON.

Stdlib only. Reads a JSON file (or stdin) and writes the result to
stdout (or a file with -o).

Usage:
    python json_formatter.py sample.json
    python json_formatter.py sample.json --minify
    python json_formatter.py sample.json --sort-keys -o pretty.json
    python json_formatter.py sample.json --validate
    cat sample.json | python json_formatter.py --indent 4

Exit codes: 0 = ok, 1 = invalid JSON, 2 = usage error.
"""

import argparse
import json
import sys


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Pretty-print, minify, sort and validate JSON (stdlib only)."
    )
    parser.add_argument(
        "input",
        nargs="?",
        help="JSON file to read (default: read from stdin)",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="FILE",
        help="Write the result to FILE instead of stdout",
    )
    parser.add_argument(
        "--minify",
        action="store_true",
        help="Compact output with no extra whitespace",
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="Spaces per indent level for pretty output (default: 2)",
    )
    parser.add_argument(
        "--sort-keys",
        action="store_true",
        help="Sort object keys alphabetically",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Only check validity: print OK or the error, write nothing",
    )
    args = parser.parse_args(argv)
    if args.input is None and sys.stdin.isatty():
        parser.error("no input file given and stdin is a terminal")
    if args.indent < 0:
        parser.error("--indent must be 0 or more")
    return args


def read_input(path):
    if path is None:
        return sys.stdin.read()
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def main(argv=None):
    args = parse_args(argv)
    try:
        text = read_input(args.input)
    except OSError as exc:
        print(f"json-formatter: cannot read input: {exc}", file=sys.stderr)
        return 2
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON: {exc}", file=sys.stderr)
        return 1

    if args.validate:
        print("Valid JSON")
        return 0

    if args.minify:
        result = json.dumps(data, separators=(",", ":"), sort_keys=args.sort_keys,
                            ensure_ascii=False)
    else:
        result = json.dumps(data, indent=args.indent, sort_keys=args.sort_keys,
                            ensure_ascii=False)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as handle:
                handle.write(result + "\n")
        except OSError as exc:
            print(f"json-formatter: cannot write output: {exc}", file=sys.stderr)
            return 2
    else:
        print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
