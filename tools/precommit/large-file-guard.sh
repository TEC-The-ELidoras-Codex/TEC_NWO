#!/usr/bin/env bash
set -euo pipefail
THRESHOLD=$((10*1024*1024))
RED="\033[31m"; NC="\033[0m"

files=$(git diff --cached --name-only --diff-filter=AM)
fail=0
for f in $files; do
  if [ -f "$f" ]; then
    size=$(wc -c <"$f")
    if [ $size -gt $THRESHOLD ]; then
      attr=$(git check-attr filter -- "$f" | awk '{print $3}') || true
      if [ "$attr" != "lfs" ]; then
        echo -e "${RED}ERROR:${NC} $f is $((size/1024/1024))MB and not LFS-tracked (>10MB). Add pattern to .gitattributes and re-stage." >&2
        fail=1
      fi
    fi
  fi
done

if [ $fail -eq 1 ]; then
  echo -e "${RED}Commit aborted by large-file-guard.${NC}" >&2
  exit 1
fi
exit 0
