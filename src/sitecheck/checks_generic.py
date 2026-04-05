from pathlib import Path


def check_path_exists(path_obj: Path):
    if path_obj.exists():
        return "PASS", "Path exists"
    return "FAIL", "Path does not exist"


def check_is_directory(path_obj: Path):
    if path_obj.is_dir():
        return "PASS", "Path is a directory"
    return "FAIL", "Path is not a directory"


def check_git_repo(path_obj: Path):
    if (path_obj / ".git").exists():
        return "PASS", "Git repository detected"
    return "WARN", "Git repository not detected"


def check_gitignore(path_obj: Path):
    if (path_obj / ".gitignore").exists():
        return "PASS", ".gitignore file found"
    return "WARN", ".gitignore file not found"