from sitecheck.cli import exit_code, render_json, render_text, main


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
            },
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
    assert "WARN: .gitignore file not found; consider adding one before production deployment" in captured.out
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


def test_main_outputs_help_for_help_flag(capsys):
    result = main(["--help"])

    captured = capsys.readouterr()

    assert result == 0
    assert "sitecheck - pre-deployment checker" in captured.out
    assert "Usage:" in captured.out
    assert "sitecheck --help" in captured.out
    assert "sitecheck scan <path>" in captured.out
    assert "Global options:" in captured.out


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
