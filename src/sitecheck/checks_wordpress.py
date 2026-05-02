from pathlib import Path


def check_wp_config(path_obj: Path):
    if (path_obj / "wp-config.php").exists():
        return {
            "check": "wp_config",
            "status": "PASS",
            "message": "wp-config.php found",
            }
    return {
        "check": "wp_config",
        "status": "FAIL",
        "message": "wp-config.php not found",
        }

def check_wp_content(path_obj: Path):
    wp_content_path = path_obj / "wp-content"

    if wp_content_path.exists() and wp_content_path.is_dir():
        return {
            "check": "wp_content",
            "status": "PASS",
            "message": "wp-content directory found",
            }
    return {
        "check": "wp_content",
        "status": "FAIL",
        "message": "wp-content directory not found",
        }


def check_readme_html(path_obj: Path):
    if (path_obj / "readme.html").exists():
        return {
            "check": "readme_html",
            "status": "WARN",
            "message": "readme.html found",
            }
    return {
        "check": "readme_html",
        "status": "PASS",
        "message": "readme.html not found",
        }


def check_wp_debug(path_obj: Path):
    wp_config = path_obj / "wp-config.php"

    if not wp_config.exists():
        return {
        "check": "wp_debug",
        "status": "FAIL",
        "message": "WP_DEBUG check skipped: wp-config.php not found",
        }

    try:
        contents = wp_config.read_text(encoding="utf-8")
    except OSError as e:
        return {
            "check": "wp_debug",
            "status": "FAIL",
            "message": f"WP_DEBUG check failed: could not read wp-config.php({e})",
        }

    for line in contents.splitlines():
        stripped = line.strip()

        # Skip commented-out lines
        if stripped.startswith("//") or stripped.startswith("#"):
            continue

        if "WP_DEBUG" in stripped and "define" in stripped:
            if "true" in stripped:
                return {
                    "check": "wp_debug",
                    "status": "WARN",
                    "message": "WP_DEBUG is enabled",
                }
            if "false" in stripped:
                return {
                    "check": "wp_debug",
                    "status": "PASS",
                    "message": "WP_DEBUG is disabled",
                }

    return {
        "check": "wp_debug",
        "status": "WARN",
        "message": "WP_DEBUG setting not clearly found in wp-config.php",
    }


def check_xmlrpc(path_obj: Path):
    if (path_obj / "xmlrpc.php").exists():
        return {
        "check": "xmlrpc",
        "status": "WARN",
        "message": "xmlrpc.php is present and may be publicly accessible",
        }
    return {
        "check": "xmlrpc",
        "status": "PASS",
        "message": "xmlrpc.php not found",
    }