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