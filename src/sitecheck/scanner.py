from pathlib import Path

from .checks_generic import (
    check_path_exists,
    check_is_directory,
    check_git_repo,
    check_gitignore,
    check_env,
    check_suspicious_files
)
from .checks_wordpress import (
    check_wp_config,
    check_wp_content,
    check_readme_html,
    check_wp_debug,
    check_xmlrpc,
)
from .profiles import detect_profile


def get_summary(results):
    summary = {
        "pass": 0,
        "warn": 0,
        "fail": 0,
    }

    for item in results:
        status = item["status"].lower()

        if status in summary:
            summary[status] += 1

    return summary


def scan(path):
    path_obj = Path(path)
    results = []

    path_exists_result = check_path_exists(path_obj)
    results.append(path_exists_result)

    if path_exists_result["status"] == "FAIL":
        return {
            "path": str(path_obj),
            "profile": "unknown",
            "results": results,
            "summary": get_summary(results),
        }

    is_directory_result = check_is_directory(path_obj)
    results.append(is_directory_result)

    if is_directory_result["status"] == "FAIL":
        return {
            "path": str(path_obj),
            "profile": "unknown",
            "results": results,
            "summary": get_summary(results),
        }

    results.append(check_git_repo(path_obj))
    results.append(check_gitignore(path_obj))
    results.append(check_env(path_obj))
    results.append(check_suspicious_files(path_obj))

    profile = detect_profile(path_obj)

    if profile == "wordpress":
        results.append(check_wp_config(path_obj))
        results.append(check_wp_content(path_obj))
        results.append(check_readme_html(path_obj))
        results.append(check_wp_debug(path_obj))
        results.append(check_xmlrpc(path_obj))

    return {
        "path": str(path_obj),
        "profile": profile,
        "results": results,
        "summary": get_summary(results),
    }