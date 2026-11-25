#!/bin/bash
# Save the memory folder so the next session remembers it.
# Usage: bash kit/save.sh "short note of what changed"
cd "$(dirname "$0")/.." || exit 1
git add memory >/dev/null 2>&1
if git diff --cached --quiet; then echo "NOTHING NEW TO SAVE"; exit 0; fi
git -c user.name="starter-kit" -c user.email="kit@localhost" commit -q -m "memory: ${1:-update}" || { echo "SAVE FAILED: commit"; exit 1; }
if git push -q origin HEAD:main 2>/dev/null; then echo "SAVED (main)"; exit 0; fi
if git push -q origin HEAD 2>/dev/null; then echo "SAVED (branch)"; exit 0; fi
if git push -q -u origin "$(git rev-parse --abbrev-ref HEAD)" 2>/dev/null; then echo "SAVED (branch)"; exit 0; fi
echo "SAVE FAILED: push"; exit 1
