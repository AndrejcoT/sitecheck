from pathlib import Path


def _find_root_files(
    path_obj: Path,
    suspicious_names: list[str],
    suspicious_extensions: list[str] | None = None,
) -> list[str]:
    suspicious_extensions = suspicious_extensions or []
    names = {name.lower() for name in suspicious_names}
    extensions = {extension.lower() for extension in suspicious_extensions}
    files_found = set()

    for item in path_obj.iterdir():
        if not item.is_file():
            continue

        file_name = item.name.lower()
        extension = item.suffix.lower()

        if file_name in names or extension in extensions:
            files_found.add(item.name)

    return sorted(files_found)


def _find_root_directories(path_obj: Path, suspicious_names: list[str]) -> list[str]:
    names = {name.lower() for name in suspicious_names}
    directories_found = set()

    for item in path_obj.iterdir():
        if item.is_dir() and item.name.lower() in names:
            directories_found.add(item.name)

    return sorted(directories_found)


def check_path_exists(path_obj: Path):
    if path_obj.exists():
        return {
            "check": "path_exists",
            "status": "PASS",
            "message": "Path exists",
        }

    return {
        "check": "path_exists",
        "status": "FAIL",
        "message": "Path does not exist",
    }


def check_is_directory(path_obj: Path):
    if path_obj.is_dir():
        return {
            "check": "is_directory",
            "status": "PASS",
            "message": "Path is a directory",
        }

    return {
        "check": "is_directory",
        "status": "FAIL",
        "message": "Path is not a directory",
    }


def check_git_repo(path_obj: Path):
    if (path_obj / ".git").exists():
        return {
            "check": "git_repository",
            "status": "PASS",
            "message": "Git repository detected",
        }

    return {
        "check": "git_repository",
        "status": "WARN",
        "message": "Not a git repository; consider initializing git before production deployment",
    }


def check_gitignore(path_obj: Path):
    if (path_obj / ".gitignore").exists():
        return {
            "check": "gitignore_exists",
            "status": "PASS",
            "message": ".gitignore file found",
        }

    return {
        "check": "gitignore_exists",
        "status": "WARN",
        "message": ".gitignore file not found; consider adding one before production deployment",
    }


def check_env(path_obj: Path):
    env_file = path_obj / ".env"
    gitignore_file = path_obj / ".gitignore"

    if not env_file.exists():
        return {
            "check": "env_exists",
            "status": "PASS",
            "message": ".env file not found",
        }

    if not gitignore_file.exists():
        return {
            "check": "env_exists",
            "status": "WARN",
            "message": ".env file found but .gitignore file not found; consider adding .env to .gitignore before production deployment",
        }

    content = gitignore_file.read_text(encoding="utf-8")

    if ".env" in content:
        return {
            "check": "env_exists",
            "status": "PASS",
            "message": ".env file found and protected by .gitignore",
        }

    return {
        "check": "env_exists",
        "status": "WARN",
        "message": ".env file found but not protected by .gitignore; consider adding .env to .gitignore before production deployment",
    }


def check_suspicious_files(path_obj: Path):
    suspicious_names = [
        "backup.zip",
        "site-backup.zip",
        "site_backup.zip",
        "website-backup.zip",
        "website_backup.zip",
        "backup.tar",
        "backup.tar.gz",
        "archive.zip",
        "archive.tar",
        "archive.tar.gz",
    ]

    suspicious_extensions = [
        ".bak",
        ".backup",
        ".zip",
        ".tar",
        ".rar",
        ".7z",
    ]

    files_found = _find_root_files(
        path_obj,
        suspicious_names,
        suspicious_extensions,
    )

    if files_found:
        return {
            "check": "suspicious_files_exists",
            "status": "WARN",
            "message": "Potential backup or archive files found in project root; consider removing them before production deployment",
            "details": ", ".join(files_found),
        }

    return {
        "check": "suspicious_files_exists",
        "status": "PASS",
        "message": "No backup or archive files found in project root",
    }


def check_database_files(path_obj: Path):
    suspicious_names = [
        "database.sql",
        "backup.sql",
        "dump.sql",
        "db.sql",
        "local.sql",
        "dev.sql",
        "production.sql",
        "database.dump",
        "backup.dump",
        "dump.dump",
        "local.db",
        "dev.db",
        "database.db",
        "site.db",
        "local.sqlite",
        "dev.sqlite",
        "database.sqlite",
        "local.sqlite3",
        "dev.sqlite3",
        "database.sqlite3",
    ]

    suspicious_extensions = [
        ".sql",
        ".dump",
        ".db",
        ".sqlite",
        ".sqlite3",
    ]

    files_found = _find_root_files(
        path_obj,
        suspicious_names,
        suspicious_extensions,
    )

    if files_found:
        return {
            "check": "database_files",
            "status": "WARN",
            "message": "Potential database files found in project root; consider removing them before production deployment",
            "details": ", ".join(files_found),
        }

    return {
        "check": "database_files",
        "status": "PASS",
        "message": "No database files found in project root",
    }


def check_debug_temp_files(path_obj: Path):
    suspicious_names = [
        "debug.tmp",
        "test.tmp",
        "temp.tmp",
        "backup.old",
    ]

    suspicious_extensions = [
        ".tmp",
        ".temp",
        ".old",
        ".orig",
    ]

    files_found = _find_root_files(
        path_obj,
        suspicious_names,
        suspicious_extensions,
    )

    if files_found:
        return {
            "check": "debug_temp_files_exists",
            "status": "WARN",
            "message": "Potential debug, temporary, or old files found in project root; consider removing them before production deployment",
            "details": ", ".join(files_found),
        }

    return {
        "check": "debug_temp_files_exists",
        "status": "PASS",
        "message": "No debug, temporary, or old files found in project root",
    }


def check_public_dev_files(path_obj: Path):
    suspicious_names = [
        "phpinfo.php",
        "debug.php",
        "test.php",
    ]

    files_found = _find_root_files(path_obj, suspicious_names)

    if files_found:
        return {
            "check": "public_dev_files_exists",
            "status": "WARN",
            "message": "Suspicious public development files found in project root; consider removing them before production deployment",
            "details": ", ".join(files_found),
        }

    return {
        "check": "public_dev_files_exists",
        "status": "PASS",
        "message": "No suspicious public development files found in project root",
    }


def check_htaccess_external_redirects(path_obj: Path):
    htaccess_file = path_obj / ".htaccess"

    if not htaccess_file.exists():
        return {
            "check": "htaccess_external_redirects",
            "status": "PASS",
            "message": ".htaccess file not found",
        }

    try:
        lines = htaccess_file.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return {
            "check": "htaccess_external_redirects",
            "status": "PASS",
            "message": "No external redirects found in .htaccess",
        }

    redirect_directives = ("redirect", "redirectmatch", "rewriterule", "rewritecond")
    external_redirects = []

    for line_number, line in enumerate(lines, start=1):
        stripped_line = line.strip()
        lower_line = stripped_line.lower()

        if not stripped_line or stripped_line.startswith("#"):
            continue

        starts_with_redirect_directive = lower_line.startswith(redirect_directives)
        contains_external_url = "http://" in lower_line or "https://" in lower_line

        if starts_with_redirect_directive and contains_external_url:
            external_redirects.append(f"line {line_number}: {stripped_line}")

    if external_redirects:
        return {
            "check": "htaccess_external_redirects",
            "status": "WARN",
            "message": "External redirects found in .htaccess; review them before production deployment",
            "details": ", ".join(external_redirects),
        }

    return {
        "check": "htaccess_external_redirects",
        "status": "PASS",
        "message": "No external redirects found in .htaccess",
    }


def check_composer_files(path_obj: Path):
    composer_lock = path_obj / "composer.lock"
    composer_json = path_obj / "composer.json"

    if composer_lock.exists() and not composer_json.exists():
        return {
            "check": "composer_files",
            "status": "WARN",
            "message": "composer.lock found but composer.json is missing; consider restoring composer.json or removing composer.lock before production deployment",
        }

    return {
        "check": "composer_files",
        "status": "PASS",
        "message": "Composer files look consistent",
    }


def check_package_files(path_obj: Path):
    package_lock = path_obj / "package-lock.json"
    package_json = path_obj / "package.json"

    if package_lock.exists() and not package_json.exists():
        return {
            "check": "package_files",
            "status": "WARN",
            "message": "package-lock.json found but package.json is missing; consider restoring package.json or removing package-lock.json before production deployment",
        }

    return {
        "check": "package_files",
        "status": "PASS",
        "message": "Package files look consistent",
    }


def check_system_files(path_obj: Path):
    suspicious_names = [
        ".ds_store",
        "thumbs.db",
    ]

    files_found = _find_root_files(path_obj, suspicious_names)

    if files_found:
        return {
            "check": "system_files",
            "status": "WARN",
            "message": "System files found in project root; consider removing them before production deployment",
            "details": ", ".join(files_found),
        }

    return {
        "check": "system_files",
        "status": "PASS",
        "message": "No system files found in project root",
    }


def check_node_modules(path_obj: Path):
    node_modules_path = path_obj / "node_modules"

    if node_modules_path.exists() and node_modules_path.is_dir():
        return {
            "check": "node_modules",
            "status": "WARN",
            "message": "node_modules directory found in project root; consider excluding it from deployment artifacts",
        }

    return {
        "check": "node_modules",
        "status": "PASS",
        "message": "node_modules directory not found in project root",
    }


def check_editor_directories(path_obj: Path):
    suspicious_names = [
        ".idea",
        ".vscode",
    ]

    directories_found = _find_root_directories(path_obj, suspicious_names)

    if directories_found:
        return {
            "check": "editor_directories",
            "status": "WARN",
            "message": "Editor directories found in project root; consider removing them before production deployment",
            "details": ", ".join(directories_found),
        }

    return {
        "check": "editor_directories",
        "status": "PASS",
        "message": "No editor directories found in project root",
    }


def check_error_logs(path_obj: Path):
    suspicious_names = [
        "error.log",
        "error_log",
        "debug.log",
    ]

    files_found = _find_root_files(path_obj, suspicious_names)

    if files_found:
        return {
            "check": "error_logs",
            "status": "WARN",
            "message": "Specific error log files found in project root; consider removing them before production deployment",
            "details": ", ".join(files_found),
        }

    return {
        "check": "error_logs",
        "status": "PASS",
        "message": "No specific error log files found in project root",
    }
