from pathlib import Path

SUPPORTED_EXTENSIONS = {".txt", ".md"}


def load_document(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {suffix}")

    return path.read_text(encoding="utf-8")


def collect_files(path: Path) -> list[Path]:
    if path.is_file():
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file type: {path.suffix}")
        return [path]

    if not path.is_dir():
        raise FileNotFoundError(f"Path not found: {path}")

    files = sorted(
        file_path
        for file_path in path.rglob("*")
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS
    )
    if not files:
        raise ValueError(f"No supported documents found in: {path}")

    return files
