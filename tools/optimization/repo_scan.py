import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

BINARY_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".mp4", ".m4a", ".mp3", ".wav", ".flac",
    ".zip", ".7z", ".tar", ".gz", ".rar", ".pdf",
}

IGNORE_DIRS = {".git", ".venv", "node_modules", "artifacts", ".tmp.driveupload"}


def is_binary(p: Path) -> bool:
    return p.suffix.lower() in BINARY_EXT


def main() -> None:
    large = []
    binaries = []
    dotfolders = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        rel = Path(dirpath).relative_to(ROOT)
        if any(part in IGNORE_DIRS for part in rel.parts):
            continue
        if rel.parts and rel.parts[0].startswith('.'):
            dotfolders.append(str(rel))
        for fn in filenames:
            p = Path(dirpath) / fn
            try:
                sz = p.stat().st_size
            except FileNotFoundError:
                continue
            if sz > 20 * 1024 * 1024:
                large.append((sz, str(p.relative_to(ROOT))))
            if is_binary(p):
                binaries.append(str(p.relative_to(ROOT)))
    large.sort(reverse=True)
    print("== Large files (>20MB) ==")
    for sz, path in large:
        print(f"{sz/1024/1024:.1f} MB\t{path}")
    print("\n== Binary-like files ==")
    for path in binaries:
        print(path)
    print("\n== Dot-folders found ==")
    for d in sorted(set(dotfolders)):
        print(d)


if __name__ == "__main__":
    main()
