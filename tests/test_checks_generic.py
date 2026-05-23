from pathlib import Path

from sitecheck.checks_generic import (
    check_composer_files,
    check_database_files,
    check_debug_temp_files,
    check_editor_directories,
    check_env,
    check_error_logs,
    check_git_repo,
    check_gitignore,
    check_htaccess_external_redirects,
    check_is_directory,
    check_node_modules,
    check_package_files,
    check_path_exists,
    check_public_dev_files,
    check_suspicious_files,
    check_system_files,
)


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
    assert "backup.zip" in result["details"]


def test_check_suspicious_files_warn_for_suspicious_extension(tmp_path):
    (tmp_path / "release.7z").write_text("fake archive", encoding="utf-8")

    result = check_suspicious_files(tmp_path)

    assert result["check"] == "suspicious_files_exists"
    assert result["status"] == "WARN"
    assert "release.7z" in result["details"]


def test_check_suspicious_files_does_not_warn_for_sql_file(tmp_path):
    (tmp_path / "backup.sql").write_text("fake database dump", encoding="utf-8")

    result = check_suspicious_files(tmp_path)

    assert result["check"] == "suspicious_files_exists"
    assert result["status"] == "PASS"


def test_check_suspicious_files_sorts_details(tmp_path):
    (tmp_path / "z.zip").write_text("fake archive", encoding="utf-8")
    (tmp_path / "a.bak").write_text("fake backup", encoding="utf-8")

    result = check_suspicious_files(tmp_path)

    assert result["details"] == "a.bak, z.zip"


def test_check_suspicious_files_is_root_only(tmp_path):
    nested = tmp_path / "subdir"
    nested.mkdir()
    (nested / "backup.zip").write_text("fake backup", encoding="utf-8")

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
    (tmp_path / "temp.tmp").write_text("temporary file", encoding="utf-8")

    result = check_debug_temp_files(tmp_path)

    assert result["check"] == "debug_temp_files_exists"
    assert result["status"] == "WARN"
    assert "temp.tmp" in result["details"]


def test_check_debug_temp_files_warn_for_debug_tmp(tmp_path):
    (tmp_path / "debug.tmp").write_text("temporary debug", encoding="utf-8")

    result = check_debug_temp_files(tmp_path)

    assert result["check"] == "debug_temp_files_exists"
    assert result["status"] == "WARN"
    assert "debug.tmp" in result["details"]


def test_check_debug_temp_files_is_root_only(tmp_path):
    nested = tmp_path / "assets"
    nested.mkdir()
    (nested / "debug.tmp").write_text("temporary debug", encoding="utf-8")

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


def test_check_package_files_pass_when_files_are_consistent(tmp_path):
    (tmp_path / "package-lock.json").write_text("{}", encoding="utf-8")
    (tmp_path / "package.json").write_text("{}", encoding="utf-8")

    result = check_package_files(tmp_path)

    assert result["check"] == "package_files"
    assert result["status"] == "PASS"


def test_check_system_files_warn_when_ds_store_exists(tmp_path):
    (tmp_path / ".DS_Store").write_text("system file", encoding="utf-8")

    result = check_system_files(tmp_path)

    assert result["check"] == "system_files"
    assert result["status"] == "WARN"
    assert ".DS_Store" in result["details"]


def test_check_system_files_pass_when_no_system_files_exist(tmp_path):
    (tmp_path / "index.php").write_text("<?php", encoding="utf-8")

    result = check_system_files(tmp_path)

    assert result["check"] == "system_files"
    assert result["status"] == "PASS"


def test_check_system_files_warn_when_thumbs_db_exists(tmp_path):
    (tmp_path / "Thumbs.db").write_text("system file", encoding="utf-8")

    result = check_system_files(tmp_path)

    assert result["check"] == "system_files"
    assert result["status"] == "WARN"
    assert "Thumbs.db" in result["details"]


def test_check_node_modules_warn_when_directory_exists(tmp_path):
    (tmp_path / "node_modules").mkdir()

    result = check_node_modules(tmp_path)

    assert result["check"] == "node_modules"
    assert result["status"] == "WARN"


def test_check_node_modules_pass_when_directory_missing(tmp_path):
    result = check_node_modules(tmp_path)

    assert result["check"] == "node_modules"
    assert result["status"] == "PASS"


def test_check_editor_directories_warn_when_vscode_exists(tmp_path):
    (tmp_path / ".vscode").mkdir()

    result = check_editor_directories(tmp_path)

    assert result["check"] == "editor_directories"
    assert result["status"] == "WARN"
    assert ".vscode" in result["details"]


def test_check_editor_directories_pass_when_no_editor_directories_exist(tmp_path):
    result = check_editor_directories(tmp_path)

    assert result["check"] == "editor_directories"
    assert result["status"] == "PASS"


def test_check_editor_directories_warn_when_idea_exists(tmp_path):
    (tmp_path / ".idea").mkdir()

    result = check_editor_directories(tmp_path)

    assert result["check"] == "editor_directories"
    assert result["status"] == "WARN"
    assert ".idea" in result["details"]


def test_check_error_logs_warn_for_error_log_file(tmp_path):
    (tmp_path / "error_log").write_text("error log", encoding="utf-8")

    result = check_error_logs(tmp_path)

    assert result["check"] == "error_logs"
    assert result["status"] == "WARN"
    assert "error_log" in result["details"]


def test_check_error_logs_pass_when_no_error_logs_exist(tmp_path):
    (tmp_path / "index.php").write_text("<?php", encoding="utf-8")

    result = check_error_logs(tmp_path)

    assert result["check"] == "error_logs"
    assert result["status"] == "PASS"


def test_check_error_logs_warn_for_debug_log_file(tmp_path):
    (tmp_path / "debug.log").write_text("debug log", encoding="utf-8")

    result = check_error_logs(tmp_path)

    assert result["check"] == "error_logs"
    assert result["status"] == "WARN"
    assert result["message"] == "Error log files found in project root; review or remove them before production deployment"
    assert "debug.log" in result["details"]


def test_check_database_files_pass_when_no_database_files_exist(tmp_path):
    (tmp_path / "index.php").write_text("<?php", encoding="utf-8")
    (tmp_path / "README.md").write_text("# test", encoding="utf-8")

    result = check_database_files(tmp_path)

    assert result["check"] == "database_files"
    assert result["status"] == "PASS"


def test_check_database_files_warn_for_database_dump_file(tmp_path):
    (tmp_path / "backup.sql").write_text("fake database dump", encoding="utf-8")

    result = check_database_files(tmp_path)

    assert result["check"] == "database_files"
    assert result["status"] == "WARN"
    assert "backup.sql" in result["details"]


def test_check_database_files_warn_for_sqlite_file(tmp_path):
    (tmp_path / "database.sqlite3").write_text("fake sqlite db", encoding="utf-8")

    result = check_database_files(tmp_path)

    assert result["check"] == "database_files"
    assert result["status"] == "WARN"
    assert "database.sqlite3" in result["details"]


def test_check_database_files_is_root_only(tmp_path):
    nested = tmp_path / "data"
    nested.mkdir()
    (nested / "backup.sql").write_text("fake database dump", encoding="utf-8")

    result = check_database_files(tmp_path)

    assert result["check"] == "database_files"
    assert result["status"] == "PASS"


def test_check_htaccess_external_redirects_pass_when_htaccess_missing(tmp_path):
    result = check_htaccess_external_redirects(tmp_path)

    assert result["check"] == "htaccess_external_redirects"
    assert result["status"] == "PASS"
    assert result["message"] == ".htaccess file not found"


def test_check_htaccess_external_redirects_pass_for_normal_wordpress_rules(tmp_path):
    (tmp_path / ".htaccess").write_text(
        "\n".join([
            "# BEGIN WordPress",
            "RewriteEngine On",
            "RewriteRule . /index.php [L]",
            "# END WordPress",
        ]),
        encoding="utf-8",
    )

    result = check_htaccess_external_redirects(tmp_path)

    assert result["check"] == "htaccess_external_redirects"
    assert result["status"] == "PASS"
    assert result["message"] == "No external redirects found in .htaccess"


def test_check_htaccess_external_redirects_warn_for_external_redirect(tmp_path):
    (tmp_path / ".htaccess").write_text(
        "Redirect 301 / https://bad-site.com",
        encoding="utf-8",
    )

    result = check_htaccess_external_redirects(tmp_path)

    assert result["check"] == "htaccess_external_redirects"
    assert result["status"] == "WARN"
    assert result["message"] == "External redirects found in .htaccess; review them before production deployment"
    assert "line 1: Redirect 301 / https://bad-site.com" in result["details"]


def test_check_htaccess_external_redirects_warn_for_external_rewriterule(tmp_path):
    (tmp_path / ".htaccess").write_text(
        "RewriteRule ^(.*)$ https://bad-site.com/$1 [R=301,L]",
        encoding="utf-8",
    )

    result = check_htaccess_external_redirects(tmp_path)

    assert result["check"] == "htaccess_external_redirects"
    assert result["status"] == "WARN"
    assert "line 1: RewriteRule ^(.*)$ https://bad-site.com/$1 [R=301,L]" in result["details"]


def test_check_htaccess_external_redirects_pass_for_commented_external_url(tmp_path):
    (tmp_path / ".htaccess").write_text(
        "# Redirect 301 / https://bad-site.com",
        encoding="utf-8",
    )

    result = check_htaccess_external_redirects(tmp_path)

    assert result["check"] == "htaccess_external_redirects"
    assert result["status"] == "PASS"
