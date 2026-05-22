from pathlib import Path

from sitecheck.checks_generic import (
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
from sitecheck.checks_wordpress import (
    check_wp_config,
    check_wp_content,
    check_readme_html,
    check_wp_debug,
    check_xmlrpc,
    check_wp_debug_log,
    check_wp_debug_display,
    check_disallow_file_edit,
    check_wp_config_sample,
    check_wp_license,
    check_wp_install_files,
    check_wp_environment_type,
    check_script_debug,
    check_display_errors,
)
from sitecheck.profiles import detect_profile
from sitecheck.scanner import get_summary, get_verdict, scan
from sitecheck.cli import render_text, render_json, exit_code


def test_exit_code_returns_zero_when_no_failures():
    scan_result = {
        "summary": {
            "fail": 0
        }
    }

    assert exit_code(scan_result) == 0


def test_exit_code_returns_one_when_one_failure_exists():
    scan_result = {
        "summary": {
            "fail": 1
        }
    }

    assert exit_code(scan_result) == 1


def test_exit_code_returns_one_when_multiple_failures_exist():
    scan_result = {
        "summary": {
            "fail": 3
        }
    }

    assert exit_code(scan_result) == 1


def test_check_path_exists_pass(tmp_path):
    result = check_path_exists(tmp_path)

    assert result["check"] == "path_exists"
    assert result["status"] == "PASS"


def test_check_path_exists_fail():
    missing_path = Path("this_path_should_not_exist_123456789")

    result = check_path_exists(missing_path)

    assert result["check"] == "path_exists"
    assert result["status"] == "FAIL"


def test_check_is_directory_pass(tmp_path):
    result = check_is_directory(tmp_path)

    assert result["check"] == "is_directory"
    assert result["status"] == "PASS"


def test_check_is_directory_fail(tmp_path):
    file_path = tmp_path / "file.txt"
    file_path.write_text("hello")

    result = check_is_directory(file_path)

    assert result["check"] == "is_directory"
    assert result["status"] == "FAIL"


def test_check_git_repo_pass(tmp_path):
    git_dir = tmp_path / ".git"
    git_dir.mkdir()

    result = check_git_repo(tmp_path)

    assert result["check"] == "git_repository"
    assert result["status"] == "PASS"


def test_check_git_repo_warn(tmp_path):
    result = check_git_repo(tmp_path)

    assert result["check"] == "git_repository"
    assert result["status"] == "WARN"


def test_check_gitignore_pass(tmp_path):
    gitignore_file = tmp_path / ".gitignore"
    gitignore_file.write_text("")

    result = check_gitignore(tmp_path)

    assert result["check"] == "gitignore_exists"
    assert result["status"] == "PASS"


def test_check_gitignore_warn(tmp_path):
    result = check_gitignore(tmp_path)

    assert result["check"] == "gitignore_exists"
    assert result["status"] == "WARN"


def test_check_env_pass_when_no_env_file(tmp_path):
    result = check_env(tmp_path)

    assert result["check"] == "env_exists"
    assert result["status"] == "PASS"


def test_check_env_warn_when_env_exists_but_gitignore_missing(tmp_path):
    (tmp_path / ".env").write_text("SECRET_KEY=test", encoding="utf-8")

    result = check_env(tmp_path)

    assert result["check"] == "env_exists"
    assert result["status"] == "WARN"


def test_check_env_pass_when_env_exists_and_gitignore_mentions_env(tmp_path):
    (tmp_path / ".env").write_text("SECRET_KEY=test", encoding="utf-8")
    (tmp_path / ".gitignore").write_text(".env\n", encoding="utf-8")

    result = check_env(tmp_path)

    assert result["check"] == "env_exists"
    assert result["status"] == "PASS"


def test_check_env_warn_when_env_exists_and_gitignore_does_not_mention_env(tmp_path):
    (tmp_path / ".env").write_text("SECRET_KEY=test", encoding="utf-8")
    (tmp_path / ".gitignore").write_text("node_modules/\n", encoding="utf-8")

    result = check_env(tmp_path)

    assert result["check"] == "env_exists"
    assert result["status"] == "WARN"


def test_check_suspicious_files_pass_when_no_suspicious_files_exist(tmp_path):
    (tmp_path / "index.php").write_text("<?php", encoding="utf-8")
    (tmp_path / "README.md").write_text("# test", encoding="utf-8")

    result = check_suspicious_files(tmp_path)

    assert result["check"] == "suspicious_files_exists"
    assert result["status"] == "PASS"


def test_check_suspicious_files_warn_for_exact_suspicious_filename(tmp_path):
    (tmp_path / "dump.sql").write_text("fake dump", encoding="utf-8")

    result = check_suspicious_files(tmp_path)

    assert result["check"] == "suspicious_files_exists"
    assert result["status"] == "WARN"
    assert "dump.sql" in result["details"]


def test_check_suspicious_files_warn_for_suspicious_extension(tmp_path):
    (tmp_path / "database.sql").write_text("fake dump", encoding="utf-8")

    result = check_suspicious_files(tmp_path)

    assert result["check"] == "suspicious_files_exists"
    assert result["status"] == "WARN"
    assert "database.sql" in result["details"]


def test_check_suspicious_files_does_not_warn_for_zip_file(tmp_path):
    (tmp_path / "backup.zip").write_text("fake backup", encoding="utf-8")

    result = check_suspicious_files(tmp_path)

    assert result["check"] == "suspicious_files_exists"
    assert result["status"] == "PASS"


def test_check_suspicious_files_sorts_details(tmp_path):
    (tmp_path / "z.dump").write_text("fake dump", encoding="utf-8")
    (tmp_path / "a.sql").write_text("fake dump", encoding="utf-8")

    result = check_suspicious_files(tmp_path)

    assert result["details"] == "a.sql, z.dump"


def test_check_suspicious_files_is_root_only(tmp_path):
    nested = tmp_path / "subdir"
    nested.mkdir()
    (nested / "dump.sql").write_text("fake dump", encoding="utf-8")

    result = check_suspicious_files(tmp_path)

    assert result["check"] == "suspicious_files_exists"
    assert result["status"] == "PASS"


def test_check_debug_temp_files_pass_when_no_debug_temp_files_exist(tmp_path):
    (tmp_path / "index.php").write_text("<?php", encoding="utf-8")
    (tmp_path / "README.md").write_text("# test", encoding="utf-8")

    result = check_debug_temp_files(tmp_path)

    assert result["check"] == "debug_temp_files_exists"
    assert result["status"] == "PASS"


def test_check_debug_temp_files_warn_for_error_log(tmp_path):
    (tmp_path / "error.log").write_text("error log", encoding="utf-8")

    result = check_debug_temp_files(tmp_path)

    assert result["check"] == "debug_temp_files_exists"
    assert result["status"] == "WARN"
    assert "error.log" in result["details"]


def test_check_debug_temp_files_warn_for_debug_tmp(tmp_path):
    (tmp_path / "debug.tmp").write_text("temporary debug", encoding="utf-8")

    result = check_debug_temp_files(tmp_path)

    assert result["check"] == "debug_temp_files_exists"
    assert result["status"] == "WARN"
    assert "debug.tmp" in result["details"]


def test_check_debug_temp_files_is_root_only(tmp_path):
    nested = tmp_path / "assets"
    nested.mkdir()
    (nested / "error.log").write_text("error log", encoding="utf-8")

    result = check_debug_temp_files(tmp_path)

    assert result["check"] == "debug_temp_files_exists"
    assert result["status"] == "PASS"


def test_check_public_dev_files_pass_when_no_public_dev_files_exist(tmp_path):
    (tmp_path / "index.php").write_text("<?php", encoding="utf-8")

    result = check_public_dev_files(tmp_path)

    assert result["check"] == "public_dev_files_exists"
    assert result["status"] == "PASS"


def test_check_public_dev_files_warn_for_phpinfo(tmp_path):
    (tmp_path / "phpinfo.php").write_text("<?php phpinfo();", encoding="utf-8")

    result = check_public_dev_files(tmp_path)

    assert result["check"] == "public_dev_files_exists"
    assert result["status"] == "WARN"
    assert "phpinfo.php" in result["details"]


def test_check_public_dev_files_warn_for_debug_php(tmp_path):
    (tmp_path / "debug.php").write_text("<?php", encoding="utf-8")

    result = check_public_dev_files(tmp_path)

    assert result["check"] == "public_dev_files_exists"
    assert result["status"] == "WARN"
    assert "debug.php" in result["details"]


def test_check_public_dev_files_warn_for_test_php(tmp_path):
    (tmp_path / "test.php").write_text("<?php", encoding="utf-8")

    result = check_public_dev_files(tmp_path)

    assert result["check"] == "public_dev_files_exists"
    assert result["status"] == "WARN"
    assert "test.php" in result["details"]


def test_check_public_dev_files_is_root_only(tmp_path):
    nested = tmp_path / "assets"
    nested.mkdir()
    (nested / "debug.php").write_text("<?php", encoding="utf-8")

    result = check_public_dev_files(tmp_path)

    assert result["check"] == "public_dev_files_exists"
    assert result["status"] == "PASS"


def test_check_composer_files_warn_when_lock_exists_without_json(tmp_path):
    (tmp_path / "composer.lock").write_text("{}", encoding="utf-8")

    result = check_composer_files(tmp_path)

    assert result["check"] == "composer_files"
    assert result["status"] == "WARN"


def test_check_composer_files_pass_when_files_are_consistent(tmp_path):
    (tmp_path / "composer.lock").write_text("{}", encoding="utf-8")
    (tmp_path / "composer.json").write_text("{}", encoding="utf-8")

    result = check_composer_files(tmp_path)

    assert result["check"] == "composer_files"
    assert result["status"] == "PASS"


def test_check_package_files_warn_when_lock_exists_without_json(tmp_path):
    (tmp_path / "package-lock.json").write_text("{}", encoding="utf-8")

    result = check_package_files(tmp_path)

    assert result["check"] == "package_files"
    assert result["status"] == "WARN"


def test_check_system_files_warn_when_ds_store_exists(tmp_path):
    (tmp_path / ".DS_Store").write_text("system file", encoding="utf-8")

    result = check_system_files(tmp_path)

    assert result["check"] == "system_files"
    assert result["status"] == "WARN"
    assert ".DS_Store" in result["details"]


def test_check_node_modules_warn_when_directory_exists(tmp_path):
    (tmp_path / "node_modules").mkdir()

    result = check_node_modules(tmp_path)

    assert result["check"] == "node_modules"
    assert result["status"] == "WARN"


def test_check_editor_directories_warn_when_vscode_exists(tmp_path):
    (tmp_path / ".vscode").mkdir()

    result = check_editor_directories(tmp_path)

    assert result["check"] == "editor_directories"
    assert result["status"] == "WARN"
    assert ".vscode" in result["details"]


def test_check_error_logs_warn_for_error_log_file(tmp_path):
    (tmp_path / "error_log").write_text("error log", encoding="utf-8")

    result = check_error_logs(tmp_path)

    assert result["check"] == "error_logs"
    assert result["status"] == "WARN"
    assert "error_log" in result["details"]


def test_detect_profile_returns_generic_for_normal_project(tmp_path):
    profile = detect_profile(tmp_path)

    assert profile == "generic"


def test_detect_profile_returns_wordpress_when_wp_files_exist(tmp_path):
    (tmp_path / "wp-config.php").write_text("<?php")
    (tmp_path / "wp-content").mkdir()

    profile = detect_profile(tmp_path)

    assert profile == "wordpress"


def test_check_wp_config_pass(tmp_path):
    (tmp_path / "wp-config.php").write_text("<?php")

    result = check_wp_config(tmp_path)

    assert result["check"] == "wp_config"
    assert result["status"] == "PASS"


def test_check_wp_config_fail(tmp_path):
    result = check_wp_config(tmp_path)

    assert result["check"] == "wp_config"
    assert result["status"] == "FAIL"


def test_check_wp_content_pass(tmp_path):
    (tmp_path / "wp-content").mkdir()

    result = check_wp_content(tmp_path)

    assert result["check"] == "wp_content"
    assert result["status"] == "PASS"


def test_check_wp_content_fail(tmp_path):
    result = check_wp_content(tmp_path)

    assert result["check"] == "wp_content"
    assert result["status"] == "FAIL"


def test_check_readme_html_warn_when_present(tmp_path):
    (tmp_path / "readme.html").write_text("readme")

    result = check_readme_html(tmp_path)

    assert result["check"] == "readme_html"
    assert result["status"] == "WARN"


def test_check_readme_html_pass_when_missing(tmp_path):
    result = check_readme_html(tmp_path)

    assert result["check"] == "readme_html"
    assert result["status"] == "PASS"


def test_check_wp_debug_warn_when_enabled(tmp_path):
    (tmp_path / "wp-config.php").write_text(
        "define('WP_DEBUG', true);",
        encoding="utf-8",
    )

    result = check_wp_debug(tmp_path)

    assert result["check"] == "wp_debug"
    assert result["status"] == "WARN"
    assert "enabled" in result["message"]


def test_check_wp_debug_pass_when_disabled(tmp_path):
    (tmp_path / "wp-config.php").write_text(
        "define('WP_DEBUG', false);",
        encoding="utf-8",
    )

    result = check_wp_debug(tmp_path)

    assert result["check"] == "wp_debug"
    assert result["status"] == "PASS"
    assert "disabled" in result["message"]


def test_check_wp_debug_warn_when_not_clearly_found(tmp_path):
    (tmp_path / "wp-config.php").write_text(
        "<?php\n// no debug setting here",
        encoding="utf-8",
    )

    result = check_wp_debug(tmp_path)

    assert result["check"] == "wp_debug"
    assert result["status"] == "WARN"
    assert "not clearly found" in result["message"]


def test_check_wp_debug_does_not_match_wp_debug_log(tmp_path):
    (tmp_path / "wp-config.php").write_text(
        "define('WP_DEBUG_LOG', true);",
        encoding="utf-8",
    )

    result = check_wp_debug(tmp_path)

    assert result["check"] == "wp_debug"
    assert result["status"] == "WARN"
    assert "not clearly found" in result["message"]


def test_check_wp_debug_does_not_match_wp_debug_display(tmp_path):
    (tmp_path / "wp-config.php").write_text(
        "define('WP_DEBUG_DISPLAY', true);",
        encoding="utf-8",
    )

    result = check_wp_debug(tmp_path)

    assert result["check"] == "wp_debug"
    assert result["status"] == "WARN"
    assert "not clearly found" in result["message"]


def test_check_wp_debug_log_warn_when_enabled(tmp_path):
    (tmp_path / "wp-config.php").write_text(
        "define('WP_DEBUG_LOG', true);",
        encoding="utf-8",
    )

    result = check_wp_debug_log(tmp_path)

    assert result["check"] == "wp_debug_log"
    assert result["status"] == "WARN"
    assert "enabled" in result["message"]


def test_check_wp_debug_log_pass_when_disabled(tmp_path):
    (tmp_path / "wp-config.php").write_text(
        "define('WP_DEBUG_LOG', false);",
        encoding="utf-8",
    )

    result = check_wp_debug_log(tmp_path)

    assert result["check"] == "wp_debug_log"
    assert result["status"] == "PASS"
    assert "disabled" in result["message"]


def test_check_wp_debug_log_warn_when_not_clearly_found(tmp_path):
    (tmp_path / "wp-config.php").write_text(
        "<?php\n// no debug log setting here",
        encoding="utf-8",
    )

    result = check_wp_debug_log(tmp_path)

    assert result["check"] == "wp_debug_log"
    assert result["status"] == "WARN"
    assert "not clearly found" in result["message"]


def test_check_wp_debug_display_warn_when_enabled(tmp_path):
    (tmp_path / "wp-config.php").write_text(
        "define('WP_DEBUG_DISPLAY', true);",
        encoding="utf-8",
    )

    result = check_wp_debug_display(tmp_path)

    assert result["check"] == "wp_debug_display"
    assert result["status"] == "WARN"
    assert "enabled" in result["message"]


def test_check_wp_debug_display_pass_when_disabled(tmp_path):
    (tmp_path / "wp-config.php").write_text(
        "define('WP_DEBUG_DISPLAY', false);",
        encoding="utf-8",
    )

    result = check_wp_debug_display(tmp_path)

    assert result["check"] == "wp_debug_display"
    assert result["status"] == "PASS"
    assert "disabled" in result["message"]


def test_check_wp_debug_display_warn_when_not_clearly_found(tmp_path):
    (tmp_path / "wp-config.php").write_text(
        "<?php\n// no debug display setting here",
        encoding="utf-8",
    )

    result = check_wp_debug_display(tmp_path)

    assert result["check"] == "wp_debug_display"
    assert result["status"] == "WARN"
    assert "not clearly found" in result["message"]


def test_check_disallow_file_edit_pass_when_enabled(tmp_path):
    (tmp_path / "wp-config.php").write_text(
        "define('DISALLOW_FILE_EDIT', true);",
        encoding="utf-8",
    )

    result = check_disallow_file_edit(tmp_path)

    assert result["check"] == "disallow_file_edit"
    assert result["status"] == "PASS"
    assert "enabled" in result["message"]


def test_check_disallow_file_edit_warn_when_disabled(tmp_path):
    (tmp_path / "wp-config.php").write_text(
        "define('DISALLOW_FILE_EDIT', false);",
        encoding="utf-8",
    )

    result = check_disallow_file_edit(tmp_path)

    assert result["check"] == "disallow_file_edit"
    assert result["status"] == "WARN"
    assert "disabled" in result["message"]


def test_check_disallow_file_edit_warn_when_not_found(tmp_path):
    (tmp_path / "wp-config.php").write_text(
        "<?php\n// no file edit setting here",
        encoding="utf-8",
    )

    result = check_disallow_file_edit(tmp_path)

    assert result["check"] == "disallow_file_edit"
    assert result["status"] == "WARN"
    assert "missing or not configured" in result["message"]


def test_check_wp_config_sample_warn_when_present(tmp_path):
    (tmp_path / "wp-config-sample.php").write_text("<?php", encoding="utf-8")

    result = check_wp_config_sample(tmp_path)

    assert result["check"] == "wp_config_sample"
    assert result["status"] == "WARN"


def test_check_wp_license_warn_when_present(tmp_path):
    (tmp_path / "license.txt").write_text("license", encoding="utf-8")

    result = check_wp_license(tmp_path)

    assert result["check"] == "wp_license"
    assert result["status"] == "WARN"


def test_check_wp_install_files_warn_when_present(tmp_path):
    (tmp_path / "install.php").write_text("<?php", encoding="utf-8")

    result = check_wp_install_files(tmp_path)

    assert result["check"] == "wp_install_files"
    assert result["status"] == "WARN"
    assert "install.php" in result["details"]


def test_check_wp_environment_type_pass_when_production(tmp_path):
    (tmp_path / "wp-config.php").write_text(
        "define('WP_ENVIRONMENT_TYPE', 'production');",
        encoding="utf-8",
    )

    result = check_wp_environment_type(tmp_path)

    assert result["check"] == "wp_environment_type"
    assert result["status"] == "PASS"


def test_check_wp_environment_type_warn_when_development(tmp_path):
    (tmp_path / "wp-config.php").write_text(
        "define('WP_ENVIRONMENT_TYPE', 'development');",
        encoding="utf-8",
    )

    result = check_wp_environment_type(tmp_path)

    assert result["check"] == "wp_environment_type"
    assert result["status"] == "WARN"


def test_check_script_debug_warn_when_enabled(tmp_path):
    (tmp_path / "wp-config.php").write_text(
        "define('SCRIPT_DEBUG', true);",
        encoding="utf-8",
    )

    result = check_script_debug(tmp_path)

    assert result["check"] == "script_debug"
    assert result["status"] == "WARN"


def test_check_display_errors_warn_when_enabled(tmp_path):
    (tmp_path / "wp-config.php").write_text(
        "ini_set('display_errors', '1');",
        encoding="utf-8",
    )

    result = check_display_errors(tmp_path)

    assert result["check"] == "display_errors"
    assert result["status"] == "WARN"


def test_check_xmlrpc_warn_when_present(tmp_path):
    (tmp_path / "xmlrpc.php").write_text("<?php")

    result = check_xmlrpc(tmp_path)

    assert result["check"] == "xmlrpc"
    assert result["status"] == "WARN"


def test_check_xmlrpc_pass_when_missing(tmp_path):
    result = check_xmlrpc(tmp_path)

    assert result["check"] == "xmlrpc"
    assert result["status"] == "PASS"


def test_get_summary_counts_results_correctly():
    results = [
        {"check": "a", "status": "PASS", "message": "ok"},
        {"check": "b", "status": "WARN", "message": "warn"},
        {"check": "c", "status": "FAIL", "message": "fail"},
        {"check": "d", "status": "PASS", "message": "ok"},
    ]

    summary = get_summary(results)

    assert summary == {
        "pass": 2,
        "warn": 1,
        "fail": 1,
    }


def test_get_verdict_returns_ready_when_no_warnings_or_failures():
    summary = {
        "pass": 3,
        "warn": 0,
        "fail": 0,
    }

    verdict = get_verdict(summary)

    assert verdict == "ready"


def test_get_verdict_returns_ready_with_warnings_when_warning_exists():
    summary = {
        "pass": 3,
        "warn": 1,
        "fail": 0,
    }

    verdict = get_verdict(summary)

    assert verdict == "ready_with_warnings"


def test_get_verdict_returns_not_ready_when_failure_exists():
    summary = {
        "pass": 3,
        "warn": 0,
        "fail": 1,
    }

    verdict = get_verdict(summary)

    assert verdict == "not_ready"


def test_scan_returns_unknown_profile_for_missing_path():
    result = scan("this_path_should_not_exist_123456789")

    assert result["profile"] == "unknown"
    assert result["verdict"] == "not_ready"
    assert result["summary"]["fail"] >= 1
    assert result["results"][0]["check"] == "path_exists"
    assert result["results"][0]["status"] == "FAIL"


def test_scan_returns_generic_profile_for_normal_project(tmp_path):
    (tmp_path / ".git").mkdir()
    (tmp_path / ".gitignore").write_text("")

    result = scan(str(tmp_path))

    assert result["profile"] == "generic"
    assert result["summary"]["fail"] == 0
    assert result["verdict"] == "ready"
    assert len(result["results"]) == 14
    assert any(item["check"] == "env_exists" for item in result["results"])
    assert any(item["check"] == "suspicious_files_exists" for item in result["results"])
    assert any(item["check"] == "debug_temp_files_exists" for item in result["results"])
    assert any(item["check"] == "public_dev_files_exists" for item in result["results"])
    assert any(item["check"] == "composer_files" for item in result["results"])
    assert any(item["check"] == "package_files" for item in result["results"])
    assert any(item["check"] == "system_files" for item in result["results"])
    assert any(item["check"] == "node_modules" for item in result["results"])
    assert any(item["check"] == "editor_directories" for item in result["results"])
    assert any(item["check"] == "error_logs" for item in result["results"])


def test_scan_returns_wordpress_profile_for_wordpress_project(tmp_path):
    (tmp_path / ".git").mkdir()
    (tmp_path / ".gitignore").write_text("")
    (tmp_path / "wp-config.php").write_text(
        "\n".join([
            "define('WP_DEBUG', false);",
            "define('WP_DEBUG_LOG', false);",
            "define('WP_DEBUG_DISPLAY', false);",
            "define('DISALLOW_FILE_EDIT', true);",
            "define('WP_ENVIRONMENT_TYPE', 'production');",
            "define('SCRIPT_DEBUG', false);",
        ]),
        encoding="utf-8",
    )
    (tmp_path / "wp-content").mkdir()

    result = scan(str(tmp_path))

    assert result["profile"] == "wordpress"
    assert result["verdict"] == "ready"
    assert any(item["check"] == "wp_config" for item in result["results"])
    assert any(item["check"] == "wp_content" for item in result["results"])
    assert any(item["check"] == "wp_debug" for item in result["results"])
    assert any(item["check"] == "wp_debug_log" for item in result["results"])
    assert any(item["check"] == "wp_debug_display" for item in result["results"])
    assert any(item["check"] == "disallow_file_edit" for item in result["results"])
    assert any(item["check"] == "wp_config_sample" for item in result["results"])
    assert any(item["check"] == "wp_license" for item in result["results"])
    assert any(item["check"] == "wp_install_files" for item in result["results"])
    assert any(item["check"] == "wp_environment_type" for item in result["results"])
    assert any(item["check"] == "script_debug" for item in result["results"])
    assert any(item["check"] == "display_errors" for item in result["results"])
    assert any(item["check"] == "env_exists" for item in result["results"])
    assert any(item["check"] == "suspicious_files_exists" for item in result["results"])
    assert any(item["check"] == "debug_temp_files_exists" for item in result["results"])
    assert any(item["check"] == "public_dev_files_exists" for item in result["results"])


def test_render_text_outputs_human_readable_summary(capsys):
    scan_result = {
        "path": ".",
        "profile": "generic",
        "results": [
            {"check": "path_exists", "status": "PASS", "message": "Path exists"},
            {"check": "gitignore_exists", "status": "WARN", "message": ".gitignore file not found"},
        ],
        "summary": {
            "pass": 1,
            "warn": 1,
            "fail": 0,
        },
    }

    render_text(scan_result)
    captured = capsys.readouterr()

    assert "Detected profile: generic" in captured.out
    assert "PASS: Path exists" in captured.out
    assert "WARN: .gitignore file not found" in captured.out
    assert "Summary:" in captured.out


def test_render_json_outputs_valid_json(capsys):
    scan_result = {
        "path": ".",
        "profile": "generic",
        "results": [],
        "summary": {
            "pass": 0,
            "warn": 0,
            "fail": 0,
        },
    }

    render_json(scan_result)
    captured = capsys.readouterr()

    assert '"profile": "generic"' in captured.out
    assert '"summary"' in captured.out
