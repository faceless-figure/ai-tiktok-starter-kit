#!/bin/bash
# Run once at the start of every session: installs what the kit needs and
# loads the newest saved memory, wherever it was saved.
cd "$(dirname "$0")/.." || exit 1
pip install -q -r requirements.txt 2>/dev/null || pip3 install -q -r requirements.txt 2>/dev/null
git fetch -q origin '+refs/heads/*:refs/remotes/origin/*' 2>/dev/null
best=""; best_t=0
for ref in $(git for-each-ref --format='%(refname:short)' refs/remotes/origin 2>/dev/null); do
  t=$(git log -1 --format=%ct "$ref" -- memory 2>/dev/null)
  if [ -n "$t" ] && [ "$t" -gt "$best_t" ]; then best_t=$t; best=$ref; fi
done
mine=$(git log -1 --format=%ct HEAD -- memory 2>/dev/null); mine=${mine:-0}
if [ -n "$best" ] && [ "$best_t" -gt "$mine" ]; then
  git checkout -q "$best" -- memory 2>/dev/null && echo "MEMORY LOADED from $best"
else
  echo "MEMORY UP TO DATE"
fi
if grep -q "^STATUS: NOT SET" memory/character.md 2>/dev/null; then echo "CHARACTER: not created yet"; else echo "CHARACTER: ready"; fi
