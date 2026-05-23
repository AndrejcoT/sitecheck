import re
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


def _line_defines_setting(line: str, setting_name: str) -> bool:
    pattern = re.compile(
        rf"\bdefine\s*\(\s*(['\"]){re.escape(setting_name)}\1\s*,",
        re.IGNORECASE,
    )
    return pattern.search(line) is not None


def _relative_path(path_obj: Path, file_path: Path) -> str:
    return file_path.relative_to(path_obj).as_posix()


def _find_files_by_extensions(root_path: Path, extensions: tuple[str, ...]) -> list[Path]:
    if not root_path.exists() or not root_path.is_dir():
        return []

    return sorted(
        file_path
        for file_path in root_path.rglob("*")
        if file_path.is_file() and file_path.suffix.lower() in extensions
    )


def _read_text_safely(file_path: Path) -> str | None:
    try:
        return file_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None


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
            "message": "readme.html found; consider removing it before production deployment",
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
        if _line_defines_setting(line, "WP_DEBUG"):
            if "true" in lower:
                return {
                    "check": "wp_debug",
                    "status": "WARN",
                    "message": "WP_DEBUG is enabled; consider disabling it before production deployment",
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
        "message": "WP_DEBUG setting not clearly found in wp-config.php; consider explicitly disabling it before production deployment",
    }


def check_xmlrpc(path_obj: Path):
    if (path_obj / "xmlrpc.php").exists():
        return {
            "check": "xmlrpc",
            "status": "WARN",
            "message": "xmlrpc.php is present and may be publicly accessible; consider disabling or restricting it before production deployment",
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
        if _line_defines_setting(line, "WP_DEBUG_LOG"):
            if "true" in lower:
                return {
                    "check": "wp_debug_log",
                    "status": "WARN",
                    "message": "WP_DEBUG_LOG is enabled; consider disabling it before production deployment",
                }
            if "false" in lower:
                return {
                    "check": "wp_debug_log",
                    "status": "PASS",
                    "message": "WP_DEBUG_LOG is disabled",
                }

    return {
        "check": "wp_debug_log",
        "status": "WARN",
        "message": "WP_DEBUG_LOG setting not clearly found in wp-config.php; consider explicitly disabling it before production deployment",
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
        if _line_defines_setting(line, "WP_DEBUG_DISPLAY"):
            if "true" in lower:
                return {
                    "check": "wp_debug_display",
                    "status": "WARN",
                    "message": "WP_DEBUG_DISPLAY is enabled; consider disabling it before production deployment",
                }
            if "false" in lower:
                return {
                    "check": "wp_debug_display",
                    "status": "PASS",
                    "message": "WP_DEBUG_DISPLAY is disabled",
                }

    return {
        "check": "wp_debug_display",
        "status": "WARN",
        "message": "WP_DEBUG_DISPLAY setting not clearly found in wp-config.php; consider explicitly disabling it before production deployment",
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
        if _line_defines_setting(line, "DISALLOW_FILE_EDIT"):
            if "true" in lower:
                return {
                    "check": "disallow_file_edit",
                    "status": "PASS",
                    "message": "DISALLOW_FILE_EDIT is enabled",
                }
            if "false" in lower:
                return {
                    "check": "disallow_file_edit",
                    "status": "WARN",
                    "message": "DISALLOW_FILE_EDIT is disabled; consider enabling it before production deployment",
                }

    return {
        "check": "disallow_file_edit",
        "status": "WARN",
        "message": "DISALLOW_FILE_EDIT is missing or not configured; consider enabling it before production deployment",
    }


def check_wp_config_sample(path_obj: Path):
    if (path_obj / "wp-config-sample.php").exists():
        return {
            "check": "wp_config_sample",
            "status": "WARN",
            "message": "wp-config-sample.php found; consider removing it before production deployment",
        }
    return {
        "check": "wp_config_sample",
        "status": "PASS",
        "message": "wp-config-sample.php not found",
    }


def check_wp_license(path_obj: Path):
    if (path_obj / "license.txt").exists():
        return {
            "check": "wp_license",
            "status": "WARN",
            "message": "license.txt found; consider removing it before production deployment",
        }
    return {
        "check": "wp_license",
        "status": "PASS",
        "message": "license.txt not found",
    }


def check_wp_install_files(path_obj: Path):
    suspicious_names = [
        "install.php",
        "installer.php",
        "setup.php",
    ]

    files_found = []

    for item in path_obj.iterdir():
        if item.is_file():
            file_name = item.name.lower()

            if file_name in suspicious_names:
                if item.name not in files_found:
                    files_found.append(item.name)

    files_found = sorted(files_found)

    if files_found:
        return {
            "check": "wp_install_files",
            "status": "WARN",
            "message": "Potential install files found in project root; consider removing them before production deployment",
            "details": ", ".join(files_found),
        }

    return {
        "check": "wp_install_files",
        "status": "PASS",
        "message": "No install files found in project root",
    }


def check_wp_environment_type(path_obj: Path):
    lines = _read_wp_config_lines(path_obj)

    if lines is None:
        return {
            "check": "wp_environment_type",
            "status": "FAIL",
            "message": "WP_ENVIRONMENT_TYPE check skipped: wp-config.php not found or unreadable",
        }

    for line in lines:
        lower = line.lower()
        if _line_defines_setting(line, "WP_ENVIRONMENT_TYPE"):
            if "development" in lower or "local" in lower:
                return {
                    "check": "wp_environment_type",
                    "status": "WARN",
                    "message": "WP_ENVIRONMENT_TYPE is not production; consider setting it to production before production deployment",
                }
            if "production" in lower:
                return {
                    "check": "wp_environment_type",
                    "status": "PASS",
                    "message": "WP_ENVIRONMENT_TYPE is production",
                }
            return {
                "check": "wp_environment_type",
                "status": "WARN",
                "message": "WP_ENVIRONMENT_TYPE setting is not clearly production; consider setting it to production before production deployment",
            }

    return {
        "check": "wp_environment_type",
        "status": "WARN",
        "message": "WP_ENVIRONMENT_TYPE setting not clearly found in wp-config.php; consider setting it to production before production deployment",
    }


def check_script_debug(path_obj: Path):
    lines = _read_wp_config_lines(path_obj)

    if lines is None:
        return {
            "check": "script_debug",
            "status": "FAIL",
            "message": "SCRIPT_DEBUG check skipped: wp-config.php not found or unreadable",
        }

    for line in lines:
        lower = line.lower()
        if _line_defines_setting(line, "SCRIPT_DEBUG"):
            if "true" in lower:
                return {
                    "check": "script_debug",
                    "status": "WARN",
                    "message": "SCRIPT_DEBUG is enabled; consider disabling it before production deployment",
                }
            if "false" in lower:
                return {
                    "check": "script_debug",
                    "status": "PASS",
                    "message": "SCRIPT_DEBUG is disabled",
                }

    return {
        "check": "script_debug",
        "status": "PASS",
        "message": "SCRIPT_DEBUG is not enabled",
    }


def check_display_errors(path_obj: Path):
    lines = _read_wp_config_lines(path_obj)

    if lines is None:
        return {
            "check": "display_errors",
            "status": "FAIL",
            "message": "display_errors check skipped: wp-config.php not found or unreadable",
        }

    for line in lines:
        lower = line.lower()
        if "display_errors" in lower:
            if "true" in lower or "'1'" in lower or '"1"' in lower:
                return {
                    "check": "display_errors",
                    "status": "WARN",
                    "message": "display_errors appears to be enabled; consider disabling it before production deployment",
                }
            if "false" in lower or "'0'" in lower or '"0"' in lower:
                return {
                    "check": "display_errors",
                    "status": "PASS",
                    "message": "display_errors appears to be disabled",
                }
            return {
                "check": "display_errors",
                "status": "WARN",
                "message": "display_errors setting is present but unclear; consider explicitly disabling it before production deployment",
            }

    return {
        "check": "display_errors",
        "status": "PASS",
        "message": "display_errors setting not found",
    }


def check_debug_exists(path_obj: Path):
    debug_log = path_obj / "wp-content" / "debug.log"

    if debug_log.exists():
        return {
            "check": "wp_debug_log_file",
            "status": "WARN",
            "message": "wp-content/debug.log found; consider removing it before production deployment",
        }

    return {
        "check": "wp_debug_log_file",
        "status": "PASS",
        "message": "wp-content/debug.log not found",
    }


def check_wp_uploads_php_files(path_obj: Path):
    uploads_path = path_obj / "wp-content" / "uploads"
    php_extensions = (".php", ".phtml", ".php5", ".phar")
    files_found = [
        _relative_path(path_obj, file_path)
        for file_path in _find_files_by_extensions(uploads_path, php_extensions)
    ]

    if files_found:
        return {
            "check": "wp_uploads_php_files",
            "status": "WARN",
            "message": "PHP files found inside wp-content/uploads; review them before production deployment",
            "details": ", ".join(files_found),
        }

    return {
        "check": "wp_uploads_php_files",
        "status": "PASS",
        "message": "No PHP files found inside wp-content/uploads",
    }


def check_wp_plugin_disguised_php_files(path_obj: Path):
    plugins_path = path_obj / "wp-content" / "plugins"
    media_extensions = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".ico")
    php_extensions = (".php", ".phtml", ".php5", ".phar")
    files_found = []

    for file_path in _find_files_by_extensions(plugins_path, php_extensions):
        file_name = file_path.name.lower()

        if any(f"{media_extension}." in file_name for media_extension in media_extensions):
            files_found.append(_relative_path(path_obj, file_path))

    if files_found:
        return {
            "check": "wp_plugin_disguised_php_files",
            "status": "WARN",
            "message": "Disguised PHP files found inside wp-content/plugins; review them before production deployment",
            "details": ", ".join(files_found),
        }

    return {
        "check": "wp_plugin_disguised_php_files",
        "status": "PASS",
        "message": "No disguised PHP files found inside wp-content/plugins",
    }


def check_wp_suspicious_php_patterns(path_obj: Path):
    scan_roots = [
        path_obj / "wp-content" / "uploads",
    ]
    php_extensions = (".php", ".phtml", ".php5", ".phar")
    files_found = []

    for scan_root in scan_roots:
        for file_path in _find_files_by_extensions(scan_root, php_extensions):
            content = _read_text_safely(file_path)

            if content is None:
                continue

            lower = content.lower()

            has_admin_creation = "wp_create_user" in lower and "administrator" in lower
            has_factory = re.search(r"\$factory\s*=", content, re.IGNORECASE) is not None
            has_named_indicator = any(
                indicator in content
                for indicator in ("yrxc_uck", "XMAN_Replicator", "NeonMeridian")
            )
            has_eval_base64 = "eval" in lower and "base64_decode" in lower

            if has_admin_creation or has_factory or has_named_indicator or has_eval_base64:
                files_found.append(_relative_path(path_obj, file_path))

    files_found = sorted(files_found)

    if files_found:
        return {
            "check": "wp_suspicious_php_patterns",
            "status": "WARN",
            "message": "Suspicious PHP patterns found inside wp-content/uploads; review them before production deployment",
            "details": ", ".join(files_found),
        }

    return {
        "check": "wp_suspicious_php_patterns",
        "status": "PASS",
        "message": "No suspicious PHP patterns found in WordPress files",
    }


def check_wp_content_php_files(path_obj: Path):
    wp_content_path = path_obj / "wp-content"
    php_extensions = (".php", ".phtml", ".php5", ".phar")
    files_found = []

    if wp_content_path.exists() and wp_content_path.is_dir():
        for file_path in sorted(wp_content_path.iterdir()):
            if not file_path.is_file():
                continue

            if file_path.name.lower() == "index.php":
                continue

            if file_path.suffix.lower() in php_extensions:
                files_found.append(_relative_path(path_obj, file_path))

    if files_found:
        return {
            "check": "wp_content_php_files",
            "status": "WARN",
            "message": "Unexpected PHP file found directly inside wp-content; review before production deployment",
            "details": ", ".join(files_found),
        }

    return {
        "check": "wp_content_php_files",
        "status": "PASS",
        "message": "No unexpected PHP files found directly inside wp-content",
    }


def check_wp_cache_php_files(path_obj: Path):
    cache_path = path_obj / "wp-content" / "cache"
    php_extensions = (".php", ".phtml", ".php5", ".phar")
    files_found = [
        _relative_path(path_obj, file_path)
        for file_path in _find_files_by_extensions(cache_path, php_extensions)
    ]

    if files_found:
        return {
            "check": "wp_cache_php_files",
            "status": "WARN",
            "message": "PHP file found inside wp-content/cache; review before production deployment",
            "details": ", ".join(files_found),
        }

    return {
        "check": "wp_cache_php_files",
        "status": "PASS",
        "message": "No PHP files found inside wp-content/cache",
    }
