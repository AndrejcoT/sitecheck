from pathlib import Path

def detect_profile(path_obj: Path) -> str:
    has_wp_config = (path_obj / "wp-config.php").exists()
    has_wp_content = (path_obj / "wp-content").exists()

    if has_wp_config and has_wp_content:
        return "wordpress"

    return "generic"