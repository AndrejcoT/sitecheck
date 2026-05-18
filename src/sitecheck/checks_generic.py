from pathlib import Path

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
        "message": "Path does not exists",
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
        "message": "Not a git repository",
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
        "message": ".gitignore file not found",
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
            "message": ".env file found but .gitignore file not found",
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
        "message": ".env file found but not protected by .gitignore",
    }

def check_suspicious_files(path_obj: Path):

    suspicious_names = [
        "backup.zip",
        "backup.tar",
        "backup.tar.gz",
        "database.sql",
        "dump.sql",
        "site-backup.zip",
    ]

    suspicious_extensions = [
        ".sql",
        ".dump",
        ".bak",
        ".backup",
        ".zip",
        ".tar",
        ".gz",
    ]

    files_found = []

    for item in path_obj.iterdir():
        if item.is_file():
            file_name = item.name.lower()
            extension = item.suffix.lower()

            if file_name in suspicious_names:
                if item.name not in files_found:
                    files_found.append(item.name)

            elif extension in suspicious_extensions:
                if item.name not in files_found:
                    files_found.append(item.name)

    if files_found:
        return {
            "check": "suspicious_files_exists",
            "status": "WARN",
            "message": f"Potential backup or dump files found in project root: {', '.join(files_found)}.",
        }

    return {
        "check": "suspicious_files_exists",
        "status": "PASS",
        "message": "No backup or dump files found in project root",
    }

def check_debug_temp_files(path_obj: Path):

    suspicious_names = [
        "error.log",
        "debug.tmp",
        "backup.old",
    ]

    suspicious_extensions = [
        ".log",
        ".tmp",
        ".temp",
        ".old",
        ".orig",
    ]

    files_found = []

    for item in path_obj.iterdir():
        if item.is_file():
            file_name = item.name.lower()
            extension = item.suffix.lower()

            if file_name in suspicious_names:
                if item.name not in files_found:
                    files_found.append(item.name)

            elif extension in suspicious_extensions:
                if item.name not in files_found:
                    files_found.append(item.name)

    if files_found:
        return {
            "check": "debug_temp_files_exists",
            "status": "WARN",
            "message": f"Potential debug, log, or temporary files found in project root: {', '.join(files_found)}.",
        }

    return {
        "check": "debug_temp_files_exists",
        "status": "PASS",
        "message": "No debug, log, or temporary files found in project root",
    }

from pathlib import Path


def check_public_dev_files(path_obj: Path):

    suspicious_names = [
        "phpinfo.php",
        "debug.php",
        "test.php",
    ]

    files_found = []

    for item in path_obj.iterdir():
        if item.is_file():
            file_name = item.name.lower()

            if file_name in suspicious_names:
                if item.name not in files_found:
                    files_found.append(item.name)

    if files_found:
        return {
            "check": "public_dev_files_exists",
            "status": "WARN",
            "message": f"Suspicious public development files found in project root: {', '.join(files_found)}.",
        }

    return {
        "check": "public_dev_files_exists",
        "status": "PASS",
        "message": "No suspicious public development files found in project root",
    }