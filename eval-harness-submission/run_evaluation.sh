#!/bin/sh
set -eu
cd "$(dirname "$0")"

if [ "$#" -ne 2 ]; then
    printf 'Usage: %s <new-generation-dir> <new-report-dir>\n' "$0" >&2
    exit 2
fi

uv run python -m unit_agent.collect --tasks tasks.jsonl --output "$1"
uv run python -m unit_agent.evaluate --input "$1" --output "$2"
