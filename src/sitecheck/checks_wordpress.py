from pathlib import Path


def _read_wp_config_lines(path_obj: Path) -> list[str] | None:
    """Read and return non-comment lines from wp-config.php, or None if unreadable."""
    wp_config = path_obj / "wp-config.php"

    if not wp_config.exists():
        return None

    try:
        contents = wp_config.read_text(encoding="utf-8")
    except OSError:
        return None

    return [
        line.strip() for line in contents.splitlines()
        if not line.strip().startswith("//") and not line.strip().startswith("#")
    ]


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
    lines = _read_wp_config_lines(path_obj)

    if lines is None:
        return {
            "check": "wp_debug",
            "status": "FAIL",
            "message": "WP_DEBUG check skipped: wp-config.php not found or unreadable",
        }

    for line in lines:
        lower = line.lower()
        if "wp_debug" in lower and "define" in lower:
            if "true" in lower:
                return {
                    "check": "wp_debug",
                    "status": "WARN",
                    "message": "WP_DEBUG is enabled",
                }
            if "false" in lower:
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


def check_wp_debug_log(path_obj: Path) -> dict:
    lines = _read_wp_config_lines(path_obj)

    if lines is None:
        return {
            "check": "wp_debug_log",
            "status": "FAIL",
            "message": "WP_DEBUG_LOG check skipped: wp-config.php not found or unreadable",
        }

    for line in lines:
        lower = line.lower()
        if "wp_debug_log" in lower and "define" in lower:
            if "true" in lower:
                return {
                    "check": "wp_debug_log",
                    "status": "WARN",
                    "message": "WP_DEBUG_LOG is enabled. Errors are being logged to the server.",
                }
            if "false" in lower:
                return {
                    "check": "wp_debug_log",
                    "status": "PASS",
                    "message": "WP_DEBUG_LOG is explicitly disabled.",
                }

    return {
        "check": "wp_debug_log",
        "status": "WARN",
        "message": "WP_DEBUG_LOG setting not explicitly found.",
    }


def check_wp_debug_display(path_obj: Path) -> dict:
    lines = _read_wp_config_lines(path_obj)

    if lines is None:
        return {
            "check": "wp_debug_display",
            "status": "FAIL",
            "message": "WP_DEBUG_DISPLAY check skipped: wp-config.php not found or unreadable",
        }

    for line in lines:
        lower = line.lower()
        if "wp_debug_display" in lower and "define" in lower:
            if "true" in lower:
                return {
                    "check": "wp_debug_display",
                    "status": "WARN",
                    "message": "WP_DEBUG_DISPLAY is enabled. Errors are visible on the frontend.",
                }
            if "false" in lower:
                return {
                    "check": "wp_debug_display",
                    "status": "PASS",
                    "message": "WP_DEBUG_DISPLAY is explicitly disabled.",
                }

    return {
        "check": "wp_debug_display",
        "status": "WARN",
        "message": "WP_DEBUG_DISPLAY setting not explicitly found.",
    }


def check_disallow_file_edit(path_obj: Path) -> dict:
    lines = _read_wp_config_lines(path_obj)

    if lines is None:
        return {
            "check": "disallow_file_edit",
            "status": "FAIL",
            "message": "DISALLOW_FILE_EDIT check skipped: wp-config.php not found or unreadable",
        }

    for line in lines:
        lower = line.lower()
        if "disallow_file_edit" in lower and "define" in lower:
            if "true" in lower:
                return {
                    "check": "disallow_file_edit",
                    "status": "PASS",
                    "message": "DISALLOW_FILE_EDIT is enabled. Plugin and theme file editing is blocked.",
                }
            if "false" in lower:
                return {
                    "check": "disallow_file_edit",
                    "status": "WARN",
                    "message": "DISALLOW_FILE_EDIT is explicitly disabled. File editing is allowed.",
                }

    return {
        "check": "disallow_file_edit",
        "status": "WARN",
        "message": "DISALLOW_FILE_EDIT is missing or not configured.",
    }