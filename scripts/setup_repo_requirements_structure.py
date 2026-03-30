from __future__ import annotations

import shutil
import sys
from pathlib import Path
def copy_directory_contents(source_dir: Path, target_dir: Path) -> None:
    """
    Recursively copy all contents from source_dir into target_dir.
    Existing files are overwritten.
    Existing directories are reused.
    """
    target_dir.mkdir(parents=True, exist_ok=True)

    for item in source_dir.iterdir():
        destination = target_dir / item.name

        if item.is_dir():
            copy_directory_contents(item, destination)
        else:
            shutil.copy2(item, destination)


def main() -> int:
    script_path = Path(__file__).resolve()
    scripts_dir = script_path.parent
    repo_root = scripts_dir.parent

    source_dir = scripts_dir / "templates" / "requirements"
    target_dir = repo_root / "requirements"

    if not source_dir.exists():
        print(f"ERROR: Source folder does not exist: {source_dir}")
        return 1

    if not source_dir.is_dir():
        print(f"ERROR: Source path is not a directory: {source_dir}")
        return 1

    try:
        copy_directory_contents(source_dir, target_dir)
    except Exception as ex:
        print(f"ERROR: Failed to copy requirements templates: {ex}")
        return 1

    print("Requirements template copied successfully.")
    print(f"Source: {source_dir}")
    print(f"Target: {target_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
