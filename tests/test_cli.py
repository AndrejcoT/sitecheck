from sitecheck.cli import exit_code, load_ignored_checks, render_json, render_text, main
import sitecheck.cli as cli


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


def test_render_text_outputs_human_readable_summary(capsys):
    scan_result = {
        "path": ".",
        "profile": "generic",
        "results": [
            {"check": "path_exists", "status": "PASS", "message": "Path exists"},
            {
                "check": "gitignore_exists",
                "status": "WARN",
                "message": ".gitignore file not found; consider adding one before production deployment",
                "details": "line 1: Redirect 301 / https://example.com, wp-content/uploads/shell.php",
            },
        ],
        "summary": {
            "pass": 1,
            "warn": 1,
            "fail": 0,
        },
        "verdict": "ready_with_warnings",
    }

    render_text(scan_result)
    captured = capsys.readouterr()

    assert "Detected profile: generic" in captured.out
    assert "Verdict: ready_with_warnings" in captured.out
    assert "PASS: Path exists" in captured.out
    assert "WARN: .gitignore file not found; consider adding one before production deployment" in captured.out
    assert "  Details:" in captured.out
    assert "    - line 1: Redirect 301 / https://example.com" in captured.out
    assert "    - wp-content/uploads/shell.php" in captured.out
    assert "Summary:" in captured.out
    assert "Review WARN items before deployment." in captured.out


def test_render_text_outputs_failure_guidance(capsys):
    scan_result = {
        "path": ".",
        "profile": "wordpress",
        "results": [
            {"check": "wp_config", "status": "FAIL", "message": "wp-config.php not found"},
        ],
        "summary": {
            "pass": 0,
            "warn": 0,
            "fail": 1,
        },
        "verdict": "not_ready",
    }

    render_text(scan_result)
    captured = capsys.readouterr()

    assert "Verdict: not_ready" in captured.out
    assert "Fix FAIL items before deployment." in captured.out


def test_render_text_filters_results_by_only_status(capsys):
    scan_result = {
        "path": ".",
        "profile": "generic",
        "results": [
            {"check": "path_exists", "status": "PASS", "message": "Path exists"},
            {"check": "env_exists", "status": "WARN", "message": ".env file found"},
            {"check": "is_directory", "status": "FAIL", "message": "Path is not a directory"},
        ],
        "summary": {
            "pass": 1,
            "warn": 1,
            "fail": 1,
        },
        "verdict": "not_ready",
    }

    render_text(scan_result, only="warn")
    captured = capsys.readouterr()

    assert "WARN: .env file found" in captured.out
    assert "PASS: Path exists" not in captured.out
    assert "FAIL: Path is not a directory" not in captured.out
    assert "PASS: 1" in captured.out
    assert "WARN: 1" in captured.out
    assert "FAIL: 1" in captured.out


def test_render_text_outputs_message_when_only_status_has_no_matches(capsys):
    scan_result = {
        "path": ".",
        "profile": "generic",
        "results": [
            {"check": "path_exists", "status": "PASS", "message": "Path exists"},
        ],
        "summary": {
            "pass": 1,
            "warn": 0,
            "fail": 0,
        },
        "verdict": "ready",
    }

    render_text(scan_result, only="fail")
    captured = capsys.readouterr()

    assert "No FAIL results to display." in captured.out
    assert "PASS: Path exists" not in captured.out
    assert "PASS: 1" in captured.out
    assert "WARN: 0" in captured.out
    assert "FAIL: 0" in captured.out


def test_render_text_summary_mode_hides_individual_results(capsys):
    scan_result = {
        "path": ".",
        "profile": "generic",
        "results": [
            {"check": "path_exists", "status": "PASS", "message": "Path exists"},
            {"check": "env_exists", "status": "WARN", "message": ".env file found"},
        ],
        "summary": {
            "pass": 1,
            "warn": 1,
            "fail": 0,
        },
        "verdict": "ready_with_warnings",
    }

    render_text(scan_result, summary=True)
    captured = capsys.readouterr()

    assert "Detected profile: generic" in captured.out
    assert "Verdict: ready_with_warnings" in captured.out
    assert "PASS: Path exists" not in captured.out
    assert "WARN: .env file found" not in captured.out
    assert "Summary:" in captured.out
    assert "PASS: 1" in captured.out
    assert "WARN: 1" in captured.out
    assert "FAIL: 0" in captured.out
    assert "Review WARN items before deployment." in captured.out


def test_render_text_summary_mode_ignores_only_filter_visibly(capsys):
    scan_result = {
        "path": ".",
        "profile": "generic",
        "results": [
            {"check": "path_exists", "status": "PASS", "message": "Path exists"},
        ],
        "summary": {
            "pass": 1,
            "warn": 0,
            "fail": 0,
        },
        "verdict": "ready",
    }

    render_text(scan_result, only="warn", summary=True)
    captured = capsys.readouterr()

    assert "No WARN results to display." not in captured.out
    assert "PASS: Path exists" not in captured.out
    assert "Summary:" in captured.out
    assert "PASS: 1" in captured.out
    assert "WARN: 0" in captured.out
    assert "FAIL: 0" in captured.out


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


def test_load_ignored_checks_returns_empty_set_when_config_missing(tmp_path):
    assert load_ignored_checks(tmp_path) == set()


def test_load_ignored_checks_reads_sitecheck_config(tmp_path):
    (tmp_path / ".sitecheck.toml").write_text(
        "\n".join([
            "[ignore]",
            'checks = ["xmlrpc", "node_modules"]',
        ]),
        encoding="utf-8",
    )

    assert load_ignored_checks(tmp_path) == {"xmlrpc", "node_modules"}


def test_load_ignored_checks_reads_config_with_utf8_bom(tmp_path):
    (tmp_path / ".sitecheck.toml").write_text(
        "\ufeff[ignore]\nchecks = [\"xmlrpc\"]",
        encoding="utf-8",
    )

    assert load_ignored_checks(tmp_path) == {"xmlrpc"}


def test_load_ignored_checks_ignores_invalid_values(tmp_path):
    (tmp_path / ".sitecheck.toml").write_text(
        "\n".join([
            "[ignore]",
            'checks = ["xmlrpc", 123]',
        ]),
        encoding="utf-8",
    )

    assert load_ignored_checks(tmp_path) == {"xmlrpc"}


def test_main_outputs_help_for_help_flag(capsys):
    result = main(["--help"])

    captured = capsys.readouterr()

    assert result == 0
    assert "sitecheck - pre-deployment checker" in captured.out
    assert "Usage:" in captured.out
    assert "sitecheck --help" in captured.out
    assert "sitecheck scan <path>" in captured.out
    assert "Global options:" in captured.out
    assert "--deep" in captured.out


def test_main_outputs_version_for_version_flag(capsys):
    result = main(["--version"])

    captured = capsys.readouterr()

    assert result == 0
    assert "sitecheck 0.1.0" in captured.out


def test_main_returns_one_for_unknown_command(capsys):
    result = main(["unknown"])

    captured = capsys.readouterr()

    assert result == 1
    assert "Try: sitecheck --help" in captured.out


def test_main_returns_one_when_scan_path_is_missing(capsys):
    result = main(["scan"])

    captured = capsys.readouterr()

    assert result == 1
    assert "Usage: sitecheck scan <path>" in captured.out


def test_main_scan_passes_only_filter_to_text_output(tmp_path, capsys, monkeypatch):
    def fake_scan(path, deep=False, ignored_checks=None):
        return {
            "path": path,
            "profile": "generic",
            "results": [
                {"check": "path_exists", "status": "PASS", "message": "Path exists"},
                {"check": "env_exists", "status": "WARN", "message": ".env file found"},
            ],
            "summary": {
                "pass": 1,
                "warn": 1,
                "fail": 0,
            },
            "verdict": "ready_with_warnings",
        }

    monkeypatch.setattr(cli, "scan", fake_scan)

    result = main(["scan", str(tmp_path), "--only", "warn"])
    captured = capsys.readouterr()

    assert result == 0
    assert "WARN: .env file found" in captured.out
    assert "PASS: Path exists" not in captured.out


def test_main_scan_summary_mode_hides_individual_results(tmp_path, capsys, monkeypatch):
    def fake_scan(path, deep=False, ignored_checks=None):
        return {
            "path": path,
            "profile": "generic",
            "results": [
                {"check": "path_exists", "status": "PASS", "message": "Path exists"},
                {"check": "env_exists", "status": "WARN", "message": ".env file found"},
            ],
            "summary": {
                "pass": 1,
                "warn": 1,
                "fail": 0,
            },
            "verdict": "ready_with_warnings",
        }

    monkeypatch.setattr(cli, "scan", fake_scan)

    result = main(["scan", str(tmp_path), "--summary"])
    captured = capsys.readouterr()

    assert result == 0
    assert "Detected profile: generic" in captured.out
    assert "Verdict: ready_with_warnings" in captured.out
    assert "PASS: Path exists" not in captured.out
    assert "WARN: .env file found" not in captured.out
    assert "Summary:" in captured.out
    assert "PASS: 1" in captured.out
    assert "WARN: 1" in captured.out
    assert "FAIL: 0" in captured.out
    assert "Review WARN items before deployment." in captured.out


def test_main_scan_json_ignores_summary_flag(tmp_path, capsys, monkeypatch):
    def fake_scan(path, deep=False, ignored_checks=None):
        return {
            "path": path,
            "profile": "generic",
            "results": [
                {"check": "path_exists", "status": "PASS", "message": "Path exists"},
            ],
            "summary": {
                "pass": 1,
                "warn": 0,
                "fail": 0,
            },
            "verdict": "ready",
        }

    monkeypatch.setattr(cli, "scan", fake_scan)

    result = main(["scan", str(tmp_path), "--json", "--summary"])
    captured = capsys.readouterr()

    assert result == 0
    assert '"results"' in captured.out
    assert '"message": "Path exists"' in captured.out
    assert '"summary"' in captured.out


def test_main_scan_deep_summary_still_runs_deep_checks(tmp_path, capsys, monkeypatch):
    captured_deep_values = []

    def fake_scan(path, deep=False, ignored_checks=None):
        captured_deep_values.append(deep)
        return {
            "path": path,
            "profile": "wordpress",
            "results": [
                {"check": "wp_content_php_files", "status": "WARN", "message": "PHP files found"},
            ],
            "summary": {
                "pass": 0,
                "warn": 1,
                "fail": 0,
            },
            "verdict": "ready_with_warnings",
        }

    monkeypatch.setattr(cli, "scan", fake_scan)

    result = main(["scan", str(tmp_path), "--deep", "--summary"])
    captured = capsys.readouterr()

    assert result == 0
    assert captured_deep_values == [True]
    assert "WARN: PHP files found" not in captured.out
    assert "WARN: 1" in captured.out


def test_main_scan_only_summary_hides_individual_results(tmp_path, capsys, monkeypatch):
    def fake_scan(path, deep=False, ignored_checks=None):
        return {
            "path": path,
            "profile": "generic",
            "results": [
                {"check": "path_exists", "status": "PASS", "message": "Path exists"},
            ],
            "summary": {
                "pass": 1,
                "warn": 0,
                "fail": 0,
            },
            "verdict": "ready",
        }

    monkeypatch.setattr(cli, "scan", fake_scan)

    result = main(["scan", str(tmp_path), "--only", "warn", "--summary"])
    captured = capsys.readouterr()

    assert result == 0
    assert "No WARN results to display." not in captured.out
    assert "PASS: Path exists" not in captured.out
    assert "Summary:" in captured.out
    assert "PASS: 1" in captured.out
    assert "WARN: 0" in captured.out
    assert "FAIL: 0" in captured.out


def test_main_returns_one_when_only_value_is_missing(tmp_path, capsys):
    result = main(["scan", str(tmp_path), "--only"])
    captured = capsys.readouterr()

    assert result == 1
    assert "Error: --only requires one of: pass, warn, fail" in captured.out


def test_main_returns_one_when_only_value_is_invalid(tmp_path, capsys):
    result = main(["scan", str(tmp_path), "--only", "error"])
    captured = capsys.readouterr()

    assert result == 1
    assert "Error: --only must be one of: pass, warn, fail" in captured.out


def test_main_scan_runs_deep_checks_when_deep_flag_is_used(tmp_path, capsys):
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
    wp_content = tmp_path / "wp-content"
    wp_content.mkdir()
    (wp_content / "loader.php").write_text("<?php", encoding="utf-8")

    result = main(["scan", str(tmp_path), "--deep"])

    captured = capsys.readouterr()

    assert result == 0
    assert "wp-content/loader.php" in captured.out
