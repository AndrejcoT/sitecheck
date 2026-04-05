from pathlib import Path


def check_wp_config(path_obj: Path):
    if (path_obj / "wp-config.php").exists():
        return "PASS", "wp-config.php found"
    return "FAIL", "wp-config.php not found"


def check_wp_content(path_obj: Path):
    wp_content_path = path_obj / "wp-content"

    if wp_content_path.exists() and wp_content_path.is_dir():
        return "PASS", "wp-content directory found"
    return "FAIL", "wp-content directory not found"


def check_readme_html(path_obj: Path):
    if (path_obj / "readme.html").exists():
        return "WARN", "readme.html found"
    return "PASS", "readme.html not found"


def check_wp_debug(path_obj: Path):
    wp_config = path_obj / "wp-config.php"

    if not wp_config.exists():
        return "FAIL", "WP_DEBUG check skipped: wp-config.php not found"

    try:
        contents = wp_config.read_text(encoding="utf-8")
    except OSError as e:
        return "FAIL", f"WP_DEBUG check failed: could not read wp-config.php ({e})"

    for line in contents.splitlines():
        stripped = line.strip()

        # Skip commented-out lines
        if stripped.startswith("//") or stripped.startswith("#"):
            continue

        if "WP_DEBUG" in stripped and "define" in stripped:
            if "true" in stripped:
                return "WARN", "WP_DEBUG is enabled"
            if "false" in stripped:
                return "PASS", "WP_DEBUG is disabled"

    return "WARN", "WP_DEBUG setting not clearly found in wp-config.php"


def check_xmlrpc(path_obj: Path):
    if (path_obj / "xmlrpc.php").exists():
        return "WARN", "xmlrpc.php is present and may be publicly accessible"
    return "PASS", "xmlrpc.php not found"