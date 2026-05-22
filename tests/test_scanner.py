from sitecheck.scanner import get_summary, get_verdict, scan


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
    assert len(result["results"]) == 16
    assert any(item["check"] == "env_exists" for item in result["results"])
    assert any(item["check"] == "suspicious_files_exists" for item in result["results"])
    assert any(item["check"] == "debug_temp_files_exists" for item in result["results"])
    assert any(item["check"] == "public_dev_files_exists" for item in result["results"])
    assert any(item["check"] == "htaccess_external_redirects" for item in result["results"])
    assert any(item["check"] == "composer_files" for item in result["results"])
    assert any(item["check"] == "package_files" for item in result["results"])
    assert any(item["check"] == "system_files" for item in result["results"])
    assert any(item["check"] == "node_modules" for item in result["results"])
    assert any(item["check"] == "editor_directories" for item in result["results"])
    assert any(item["check"] == "error_logs" for item in result["results"])
    assert any(item["check"] == "database_files" for item in result["results"])


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
    assert any(item["check"] == "wp_debug_log_file" for item in result["results"])
    assert any(item["check"] == "wp_uploads_php_files" for item in result["results"])
    assert any(item["check"] == "wp_plugin_disguised_php_files" for item in result["results"])
    assert any(item["check"] == "wp_suspicious_php_patterns" for item in result["results"])
    assert any(item["check"] == "env_exists" for item in result["results"])
    assert any(item["check"] == "suspicious_files_exists" for item in result["results"])
    assert any(item["check"] == "debug_temp_files_exists" for item in result["results"])
    assert any(item["check"] == "public_dev_files_exists" for item in result["results"])
    assert any(item["check"] == "htaccess_external_redirects" for item in result["results"])
    assert any(item["check"] == "database_files" for item in result["results"])


def test_scan_returns_wordpress_profile_for_partial_wordpress_project(tmp_path):
    (tmp_path / ".git").mkdir()
    (tmp_path / ".gitignore").write_text("")
    (tmp_path / "wp-content").mkdir()

    result = scan(str(tmp_path))

    assert result["profile"] == "wordpress"
    assert result["verdict"] == "not_ready"
    assert any(
        item["check"] == "wp_config" and item["status"] == "FAIL"
        for item in result["results"]
    )
    assert any(item["check"] == "wp_content" for item in result["results"])


def test_scan_does_not_run_deep_wordpress_checks_by_default(tmp_path):
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
    (tmp_path / "wp-content" / "loader.php").write_text("<?php", encoding="utf-8")

    result = scan(str(tmp_path))

    assert not any(item["check"] == "wp_content_php_files" for item in result["results"])
    assert not any(item["check"] == "wp_cache_php_files" for item in result["results"])


def test_scan_runs_deep_wordpress_checks_when_enabled(tmp_path):
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
    (tmp_path / "wp-content" / "loader.php").write_text("<?php", encoding="utf-8")
    cache = tmp_path / "wp-content" / "cache"
    cache.mkdir()
    (cache / "payload.php").write_text("<?php", encoding="utf-8")

    result = scan(str(tmp_path), deep=True)

    assert any(item["check"] == "wp_content_php_files" for item in result["results"])
    assert any(item["check"] == "wp_cache_php_files" for item in result["results"])


def test_scan_ignores_configured_checks(tmp_path):
    (tmp_path / ".git").mkdir()
    (tmp_path / ".gitignore").write_text("")
    (tmp_path / "backup.sql").write_text("database dump", encoding="utf-8")

    result = scan(str(tmp_path), ignored_checks={"database_files"})

    assert not any(item["check"] == "database_files" for item in result["results"])
    assert result["summary"]["warn"] == 0
