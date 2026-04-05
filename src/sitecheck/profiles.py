from pathlib import Path


def detect_profile(path_obj: Path) -> str:
    if (path_obj / "wp-config.php").exists() and (path_obj / "wp-content").exists():
        return "wordpress"
    return "generic"