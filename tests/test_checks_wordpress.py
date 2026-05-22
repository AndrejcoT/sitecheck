from sitecheck.checks_wordpress import (
    check_debug_exists,
    check_display_errors,
    check_disallow_file_edit,
    check_readme_html,
    check_script_debug,
    check_wp_config,
    check_wp_config_sample,
    check_wp_content,
    check_wp_content_php_files,
    check_wp_debug,
    check_wp_debug_display,
    check_wp_debug_log,
    check_wp_environment_type,
    check_wp_install_files,
    check_wp_license,
    check_wp_cache_php_files,
    check_wp_plugin_disguised_php_files,
    check_wp_suspicious_php_patterns,
    check_wp_uploads_php_files,
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


def test_check_debug_exists_warn_when_debug_log_exists(tmp_path):
    wp_content = tmp_path / "wp-content"
    wp_content.mkdir()
    (wp_content / "debug.log").write_text("debug output", encoding="utf-8")

    result = check_debug_exists(tmp_path)

    assert result["check"] == "wp_debug_log_file"
    assert result["status"] == "WARN"
    assert "wp-content/debug.log found" in result["message"]


def test_check_debug_exists_pass_when_debug_log_missing(tmp_path):
    (tmp_path / "wp-content").mkdir()

    result = check_debug_exists(tmp_path)

    assert result["check"] == "wp_debug_log_file"
    assert result["status"] == "PASS"
    assert "not found" in result["message"]


def test_check_wp_uploads_php_files_pass_when_uploads_folder_missing(tmp_path):
    result = check_wp_uploads_php_files(tmp_path)

    assert result["check"] == "wp_uploads_php_files"
    assert result["status"] == "PASS"


def test_check_wp_uploads_php_files_pass_when_uploads_has_no_php_files(tmp_path):
    uploads = tmp_path / "wp-content" / "uploads"
    uploads.mkdir(parents=True)
    (uploads / "logo.png").write_text("image", encoding="utf-8")

    result = check_wp_uploads_php_files(tmp_path)

    assert result["check"] == "wp_uploads_php_files"
    assert result["status"] == "PASS"


def test_check_wp_uploads_php_files_warn_for_php_file_in_uploads(tmp_path):
    uploads = tmp_path / "wp-content" / "uploads"
    uploads.mkdir(parents=True)
    (uploads / "shell.php").write_text("<?php", encoding="utf-8")

    result = check_wp_uploads_php_files(tmp_path)

    assert result["check"] == "wp_uploads_php_files"
    assert result["status"] == "WARN"
    assert "wp-content/uploads/shell.php" in result["details"]


def test_check_wp_uploads_php_files_warn_for_nested_disguised_php_file(tmp_path):
    nested_uploads = tmp_path / "wp-content" / "uploads" / "2026" / "05"
    nested_uploads.mkdir(parents=True)
    (nested_uploads / "logo.png.php").write_text("<?php", encoding="utf-8")

    result = check_wp_uploads_php_files(tmp_path)

    assert result["check"] == "wp_uploads_php_files"
    assert result["status"] == "WARN"
    assert "wp-content/uploads/2026/05/logo.png.php" in result["details"]


def test_check_wp_plugin_disguised_php_files_pass_when_plugins_folder_missing(tmp_path):
    result = check_wp_plugin_disguised_php_files(tmp_path)

    assert result["check"] == "wp_plugin_disguised_php_files"
    assert result["status"] == "PASS"


def test_check_wp_plugin_disguised_php_files_pass_for_normal_plugin_php_file(tmp_path):
    plugin = tmp_path / "wp-content" / "plugins" / "contact-form-7"
    plugin.mkdir(parents=True)
    (plugin / "wp-contact-form-7.php").write_text("<?php", encoding="utf-8")

    result = check_wp_plugin_disguised_php_files(tmp_path)

    assert result["check"] == "wp_plugin_disguised_php_files"
    assert result["status"] == "PASS"


def test_check_wp_plugin_disguised_php_files_pass_for_normal_asset(tmp_path):
    assets = tmp_path / "wp-content" / "plugins" / "example" / "assets"
    assets.mkdir(parents=True)
    (assets / "logo.png").write_text("image", encoding="utf-8")

    result = check_wp_plugin_disguised_php_files(tmp_path)

    assert result["check"] == "wp_plugin_disguised_php_files"
    assert result["status"] == "PASS"


def test_check_wp_plugin_disguised_php_files_warn_for_png_php_file(tmp_path):
    assets = tmp_path / "wp-content" / "plugins" / "example" / "assets"
    assets.mkdir(parents=True)
    (assets / "logo.png.php").write_text("<?php", encoding="utf-8")

    result = check_wp_plugin_disguised_php_files(tmp_path)

    assert result["check"] == "wp_plugin_disguised_php_files"
    assert result["status"] == "WARN"
    assert "wp-content/plugins/example/assets/logo.png.php" in result["details"]


def test_check_wp_plugin_disguised_php_files_warn_for_jpg_phtml_file(tmp_path):
    assets = tmp_path / "wp-content" / "plugins" / "example" / "assets"
    assets.mkdir(parents=True)
    (assets / "banner.jpg.phtml").write_text("<?php", encoding="utf-8")

    result = check_wp_plugin_disguised_php_files(tmp_path)

    assert result["check"] == "wp_plugin_disguised_php_files"
    assert result["status"] == "WARN"
    assert "wp-content/plugins/example/assets/banner.jpg.phtml" in result["details"]


def test_check_wp_suspicious_php_patterns_pass_for_clean_php_file(tmp_path):
    uploads = tmp_path / "wp-content" / "uploads"
    uploads.mkdir(parents=True)
    (uploads / "index.php").write_text("<?php echo 'ok';", encoding="utf-8")

    result = check_wp_suspicious_php_patterns(tmp_path)

    assert result["check"] == "wp_suspicious_php_patterns"
    assert result["status"] == "PASS"


def test_check_wp_suspicious_php_patterns_warn_for_admin_user_creation(tmp_path):
    uploads = tmp_path / "wp-content" / "uploads"
    uploads.mkdir(parents=True)
    (uploads / "user.php").write_text(
        "<?php $user = wp_create_user('name', 'pass'); $user->set_role('administrator');",
        encoding="utf-8",
    )

    result = check_wp_suspicious_php_patterns(tmp_path)

    assert result["check"] == "wp_suspicious_php_patterns"
    assert result["status"] == "WARN"
    assert "wp-content/uploads/user.php" in result["details"]


def test_check_wp_suspicious_php_patterns_warn_for_eval_base64_decode(tmp_path):
    uploads = tmp_path / "wp-content" / "uploads"
    uploads.mkdir(parents=True)
    (uploads / "loader.php").write_text(
        "<?php eval(base64_decode('ZXZpbA=='));",
        encoding="utf-8",
    )

    result = check_wp_suspicious_php_patterns(tmp_path)

    assert result["check"] == "wp_suspicious_php_patterns"
    assert result["status"] == "WARN"
    assert "wp-content/uploads/loader.php" in result["details"]


def test_check_wp_suspicious_php_patterns_pass_for_base64_decode_alone(tmp_path):
    uploads = tmp_path / "wp-content" / "uploads"
    uploads.mkdir(parents=True)
    (uploads / "helper.php").write_text(
        "<?php $decoded = base64_decode($value);",
        encoding="utf-8",
    )

    result = check_wp_suspicious_php_patterns(tmp_path)

    assert result["check"] == "wp_suspicious_php_patterns"
    assert result["status"] == "PASS"


def test_check_wp_content_php_files_pass_when_wp_content_missing(tmp_path):
    result = check_wp_content_php_files(tmp_path)

    assert result["check"] == "wp_content_php_files"
    assert result["status"] == "PASS"


def test_check_wp_content_php_files_pass_for_index_php(tmp_path):
    wp_content = tmp_path / "wp-content"
    wp_content.mkdir()
    (wp_content / "index.php").write_text("<?php", encoding="utf-8")

    result = check_wp_content_php_files(tmp_path)

    assert result["check"] == "wp_content_php_files"
    assert result["status"] == "PASS"


def test_check_wp_content_php_files_warn_for_unexpected_php_file(tmp_path):
    wp_content = tmp_path / "wp-content"
    wp_content.mkdir()
    (wp_content / "loader.php").write_text("<?php", encoding="utf-8")

    result = check_wp_content_php_files(tmp_path)

    assert result["check"] == "wp_content_php_files"
    assert result["status"] == "WARN"
    assert "wp-content/loader.php" in result["details"]


def test_check_wp_cache_php_files_pass_when_cache_missing(tmp_path):
    result = check_wp_cache_php_files(tmp_path)

    assert result["check"] == "wp_cache_php_files"
    assert result["status"] == "PASS"


def test_check_wp_cache_php_files_warn_for_cache_php_file(tmp_path):
    cache = tmp_path / "wp-content" / "cache" / "page"
    cache.mkdir(parents=True)
    (cache / "payload.php").write_text("<?php", encoding="utf-8")

    result = check_wp_cache_php_files(tmp_path)

    assert result["check"] == "wp_cache_php_files"
    assert result["status"] == "WARN"
    assert "wp-content/cache/page/payload.php" in result["details"]
