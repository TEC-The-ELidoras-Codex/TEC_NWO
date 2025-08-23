# TEC_NWO Repository Overhaul Plan

Goals

- One name, one system, clean structure; Drive + Git remain cohesive
- Remove random cruft; normalize line endings; pin toolchains
- Preserve history; add provenance/axiom anchors to canonical docs

Phases

1. Inventory & surface anomalies

- Run scan script to list large/binary/orphan files and dot-folders
- Map duplicates between Drive sync and repo

1. Normalize & prune

- Enforce .gitattributes (LFS + text=auto) and .editorconfig
- Move stray media into assets/; purge temp/upload caches

1. Canonicalize docs

- Ensure docs cite Axioms and include provenance (commit hash)
- Route anthology/lore to docs/anthology and lore/

1. Wire automation

- Add CI lints (md/lint/size), optional pre-commit
- Add artifacts/ to .gitignore; keep sources under assets/

Drive sync guidance

- Keep the single source of truth in this repo; Google Drive mirrors under G:\\My Drive\\TEC_NWO\\TEC-HORRORMASTERCLASS
- Avoid editing the same binary in both places; prefer pushing from repo → Drive export
- For big media, keep in LFS paths and reference via manifests

Runbook

- See tools/optimization/repo_scan.py to list candidates for cleanup
- Open issues for deletions/moves; commit with “move: …” or “chore: cleanup”

Next

- Add CI and pre-commit hooks
- Migrate any remaining notebooks under notebooks/
