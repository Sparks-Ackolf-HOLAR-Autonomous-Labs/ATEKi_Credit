#!/bin/bash
# usage: run_set.sh SET PORT MODEL TEAM SEEDS...
# Experiment 11 at scale (sets S1-S3). Paths default to this checkout;
# override with the environment variables SO_ROOT (package root), PYTHON
# (interpreter with the ateki environment), UNIVERSE (band-gap universe
# JSONL) and OUT_ROOT (campaign output root). EXTRA passes further
# arguments to the experiment script. Needs a vLLM OpenAI-compatible server
# on localhost:PORT.
set_=$1; port=$2; model=$3; team=$4; shift 4
SO="${SO_ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)}"
PY="${PYTHON:-python}"
UNIVERSE="${UNIVERSE:-$SO/shared/output/bandgap_archive_build/bandgap_universe.jsonl}"
OUT_ROOT="${OUT_ROOT:-$SO/ateki/results/recorded_meetings_scale}"
cd "$SO/ateki"
export PEGKI_ROOT="$SO/shared"
"$PY" experiments/11_recorded_meetings.py \
  --universe "$UNIVERSE" \
  --base-url http://localhost:$port/v1 --model $model --team-size $team \
  $EXTRA --seeds "$@" --output-dir "$OUT_ROOT/$set_"
echo "exit $?"
