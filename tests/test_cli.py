from pathlib import Path

from sitecheck.checks_generic import (
    check_path_exists,
    check_is_directory,
    check_git_repo,
    check_gitignore,
    check_env,
    check_suspicious_files,
)
from sitecheck.checks_wordpress import (
    check_wp_config,
    check_wp_content,
    check_readme_html,
    check_wp_debug,
    check_xmlrpc,
)
from sitecheck.profiles import detect_profile
from sitecheck.scanner import get_summary, scan
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
    (tmp_path / "backup.zip").write_text("fake backup", encoding="utf-8")

    result = check_suspicious_files(tmp_path)

    assert result["check"] == "suspicious_files_exists"
    assert result["status"] == "WARN"
    assert "backup.zip" in result["message"]


def test_check_suspicious_files_warn_for_suspicious_extension(tmp_path):
    (tmp_path / "database.sql").write_text("fake dump", encoding="utf-8")

    result = check_suspicious_files(tmp_path)

    assert result["check"] == "suspicious_files_exists"
    assert result["status"] == "WARN"
    assert "database.sql" in result["message"]


def test_check_suspicious_files_is_root_only(tmp_path):
    nested = tmp_path / "subdir"
    nested.mkdir()
    (nested / "dump.sql").write_text("fake dump", encoding="utf-8")

    result = check_suspicious_files(tmp_path)

    assert result["check"] == "suspicious_files_exists"
    assert result["status"] == "PASS"


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


def test_scan_returns_unknown_profile_for_missing_path():
    result = scan("this_path_should_not_exist_123456789")

    assert result["profile"] == "unknown"
    assert result["summary"]["fail"] >= 1
    assert result["results"][0]["check"] == "path_exists"
    assert result["results"][0]["status"] == "FAIL"


def test_scan_returns_generic_profile_for_normal_project(tmp_path):
    (tmp_path / ".git").mkdir()
    (tmp_path / ".gitignore").write_text("")

    result = scan(str(tmp_path))

    assert result["profile"] == "generic"
    assert result["summary"]["fail"] == 0
    assert len(result["results"]) == 6
    assert any(item["check"] == "env_exists" for item in result["results"])
    assert any(item["check"] == "suspicious_files_exists" for item in result["results"])


def test_scan_returns_wordpress_profile_for_wordpress_project(tmp_path):
    (tmp_path / ".git").mkdir()
    (tmp_path / ".gitignore").write_text("")
    (tmp_path / "wp-config.php").write_text(
        "define('WP_DEBUG', false);",
        encoding="utf-8",
    )
    (tmp_path / "wp-content").mkdir()

    result = scan(str(tmp_path))

    assert result["profile"] == "wordpress"
    assert any(item["check"] == "wp_config" for item in result["results"])
    assert any(item["check"] == "wp_content" for item in result["results"])
    assert any(item["check"] == "wp_debug" for item in result["results"])
    assert any(item["check"] == "env_exists" for item in result["results"])
    assert any(item["check"] == "suspicious_files_exists" for item in result["results"])


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