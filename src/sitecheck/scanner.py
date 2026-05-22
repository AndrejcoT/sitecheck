from pathlib import Path

from .checks_generic import (
    check_path_exists,
    check_is_directory,
    check_git_repo,
    check_gitignore,
    check_env,
    check_suspicious_files,
    check_debug_temp_files,
    check_public_dev_files,
    check_composer_files,
    check_package_files,
    check_system_files,
    check_node_modules,
    check_editor_directories,
    check_error_logs,
)
from .checks_wordpress import (
    check_wp_config,
    check_wp_content,
    check_readme_html,
    check_wp_debug,
    check_xmlrpc,
    check_disallow_file_edit,
    check_wp_debug_display,
    check_wp_debug_log,
    check_wp_config_sample,
    check_wp_license,
    check_wp_install_files,
    check_wp_environment_type,
    check_script_debug,
    check_display_errors,
)
from .profiles import detect_profile


GENERIC_CHECKS = (
    check_git_repo,
    check_gitignore,
    check_env,
    check_suspicious_files,
    check_debug_temp_files,
    check_public_dev_files,
    check_composer_files,
    check_package_files,
    check_system_files,
    check_node_modules,
    check_editor_directories,
    check_error_logs,
)

WORDPRESS_CHECKS = (
    check_wp_config,
    check_wp_content,
    check_readme_html,
    check_wp_debug,
    check_wp_debug_log,
    check_wp_debug_display,
    check_disallow_file_edit,
    check_xmlrpc,
    check_wp_config_sample,
    check_wp_license,
    check_wp_install_files,
    check_wp_environment_type,
    check_script_debug,
    check_display_errors,
)


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


def get_verdict(summary):
    if summary["fail"] > 0:
        return "not_ready"

    if summary["warn"] > 0:
        return "ready_with_warnings"

    return "ready"


def _build_scan_result(path_obj, profile, results):
    summary = get_summary(results)

    return {
        "path": str(path_obj),
        "profile": profile,
        "results": results,
        "summary": summary,
        "verdict": get_verdict(summary),
    }


def scan(path):
    path_obj = Path(path)
    results = []

    path_exists_result = check_path_exists(path_obj)
    results.append(path_exists_result)

    if path_exists_result["status"] == "FAIL":
        return _build_scan_result(path_obj, "unknown", results)

    is_directory_result = check_is_directory(path_obj)
    results.append(is_directory_result)

    if is_directory_result["status"] == "FAIL":
        return _build_scan_result(path_obj, "unknown", results)

    for check in GENERIC_CHECKS:
        results.append(check(path_obj))

    profile = detect_profile(path_obj)

    if profile == "wordpress":
        for check in WORDPRESS_CHECKS:
            results.append(check(path_obj))

    return _build_scan_result(path_obj, profile, results)
