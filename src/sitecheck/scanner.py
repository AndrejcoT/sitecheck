from pathlib import Path

from .checks_generic import (
    check_path_exists,
    check_is_directory,
    check_git_repo,
    check_gitignore,
)
from .checks_wordpress import (
    check_wp_config,
    check_wp_content,
    check_readme_html,
    check_wp_debug,
    check_xmlrpc,
)
from .profiles import detect_profile


def print_result(status, message):
    print(f"{status}: {message}")


def print_summary(results):
    pass_count = sum(1 for status, _ in results if status == "PASS")
    warn_count = sum(1 for status, _ in results if status == "WARN")
    fail_count = sum(1 for status, _ in results if status == "FAIL")

    print()
    print("Summary:")
    print(f"PASS: {pass_count}")
    print(f"WARN: {warn_count}")
    print(f"FAIL: {fail_count}")


def scan(path):
    path_obj = Path(path)
    results = []

    print("Scanning project...")
    print(f"Path: {path_obj}")
    print()

    path_exists_result = check_path_exists(path_obj)
    results.append(path_exists_result)

    if path_exists_result[0] == "FAIL":
        for status, message in results:
            print_result(status, message)
        print_summary(results)
        return

    is_directory_result = check_is_directory(path_obj)
    results.append(is_directory_result)

    if is_directory_result[0] == "FAIL":
        for status, message in results:
            print_result(status, message)
        print_summary(results)
        return

    results.append(check_git_repo(path_obj))
    results.append(check_gitignore(path_obj))

    profile = detect_profile(path_obj)

    print(f"Detected profile: {profile}")
    print()

    if profile == "wordpress":
        results.append(check_wp_config(path_obj))
        results.append(check_wp_content(path_obj))
        results.append(check_readme_html(path_obj))
        results.append(check_wp_debug(path_obj))
        results.append(check_xmlrpc(path_obj))

    for status, message in results:
        print_result(status, message)

    print_summary(results)