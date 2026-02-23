from pathlib import Path
import shutil


def normalize_input_path(path):
    return Path(str(path).strip().strip('"').strip("'")).expanduser()


def file_sort(path):
    path = normalize_input_path(path)
    if not path.exists() or not path.is_dir():
        raise ValueError(f"Ungültiger Ordnerpfad: {path}")

    moved_count = 0

    for file in path.iterdir():
        if not file.is_file():
            continue

        suffix = file.suffix.lower().strip('.')
        if not suffix:
            suffix = "rest"

        destination = path / suffix
        destination.mkdir(exist_ok=True)

        target = destination / file.name
        if target.exists():
            stem = file.stem
            extension = file.suffix
            counter = 1
            while target.exists():
                target = destination / f"{stem}_{counter}{extension}"
                counter += 1

        shutil.move(str(file), str(target))
        moved_count += 1

    return moved_count