from pathlib import Path


def check_if_file_exists(file: Path) -> Path:
    """Checks if file exists because `pyray` doesn't raise `FileNotFoundException`.

    Args:
        file (Path): Path to a file.

    Raises:
        FileNotFoundError: If file doesn't exist.

    Returns:
        Path: The input `file` path if file exists.
    """
    if not file.exists():
        raise FileNotFoundError(f"File `{file}` does not exist!")
    return file
