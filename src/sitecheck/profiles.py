from pathlib import Path

def detect_profile(path_obj: Path) -> str:
    wordpress_markers = (
        path_obj / "wp-config.php",
        path_obj / "wp-content",
        path_obj / "wp-admin",
        path_obj / "wp-includes",
    )

    if any(marker.exists() for marker in wordpress_markers):
        return "wordpress"

    return "generic"
