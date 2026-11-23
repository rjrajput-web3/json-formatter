# json-formatter

Pretty-print, minify, sort and validate JSON from the command line.
Stdlib only — no dependencies, works with any Python 3.

## What it does

- Pretty-prints a JSON file (default indent 2, adjustable with `--indent`).
- Minifies JSON to one line with `--minify`.
- Sorts object keys with `--sort-keys`.
- Validates JSON with `--validate` (prints `Valid JSON`, exits 0 or 1).
- Reads from a file or stdin; writes to stdout or a file with `-o`.

## How to run

```bash
python json_formatter.py sample.json
python json_formatter.py sample.json --minify
python json_formatter.py sample.json --sort-keys -o pretty.json
python json_formatter.py sample.json --validate
cat sample.json | python json_formatter.py --indent 4
```

## Example output

Input (`sample.json`, minified):

```json
{"dependencies":{"express":"^4.19.2"},"name":"example-project","private":true,"scripts":{"start":"node index.js","test":"node --test"},"tags":["demo","json","sample"],"version":"1.4.0"}
```

`python json_formatter.py sample.json` prints:

```json
{
  "dependencies": {
    "express": "^4.19.2"
  },
  "name": "example-project",
  "private": true,
  "scripts": {
    "start": "node index.js",
    "test": "node --test"
  },
  "tags": [
    "demo",
    "json",
    "sample"
  ],
  "version": "1.4.0"
}
```

`python json_formatter.py sample.json --minify` prints the input back as one line:

```json
{"dependencies":{"express":"^4.19.2"},"name":"example-project","private":true,"scripts":{"start":"node index.js","test":"node --test"},"tags":["demo","json","sample"],"version":"1.4.0"}
```

`python json_formatter.py sample.json --validate` prints:

```
Valid JSON
```

Invalid input exits 1 and reports the position, for example:

```
Invalid JSON: Expecting property name enclosed in double quotes: line 1 column 9 (char 8)
```

## Exit codes

- `0` — ok (or valid, with `--validate`)
- `1` — invalid JSON
- `2` — usage error (bad flag, unreadable file, unwritable output)
