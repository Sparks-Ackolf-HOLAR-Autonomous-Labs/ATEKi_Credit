#!/bin/bash
# usage: run_coordinator.sh ARM ROTATION SEEDS...
# Experiment 13 (recorded coordinator-led meetings, coordinator rotated).
# Paths default to this checkout; override with the environment variables
# SO_ROOT (package root), PYTHON (interpreter with the ateki environment),
# UNIVERSE (band-gap universe JSONL) and OUT_ROOT (campaign output root).
# Needs a vLLM OpenAI-compatible server on localhost:8020.
arm=$1; rot=$2; shift 2
SO="${SO_ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)}"
PY="${PYTHON:-python}"
UNIVERSE="${UNIVERSE:-$SO/shared/output/bandgap_archive_build/bandgap_universe.jsonl}"
OUT_ROOT="${OUT_ROOT:-$SO/ateki/results/recorded_meetings_coordinator}"
cd "$SO/ateki"
export PEGKI_ROOT="$SO/shared"
"$PY" experiments/13_recorded_meetings_coordinator.py \
  --universe "$UNIVERSE" \
  --base-url http://localhost:8020/v1 --model Qwen/Qwen3-4B-Instruct-2507 \
  --arms $arm --rotation $rot --seeds "$@" \
  --output-dir "$OUT_ROOT/$( [ $arm = flat ] && echo flat || echo rot$rot )"
echo "exit $?"
