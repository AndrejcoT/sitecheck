from sitecheck.checks_wordpress import (
    check_display_errors,
    check_disallow_file_edit,
    check_readme_html,
    check_script_debug,
    check_wp_config,
    check_wp_config_sample,
    check_wp_content,
    check_wp_debug,
    check_wp_debug_display,
    check_wp_debug_log,
    check_wp_environment_type,
    check_wp_install_files,
    check_wp_license,
    check_xmlrpc,
)


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
