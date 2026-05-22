from sitecheck.profiles import detect_profile


def test_detect_profile_returns_generic_for_normal_project(tmp_path):
    profile = detect_profile(tmp_path)

    assert profile == "generic"


def test_detect_profile_returns_wordpress_when_wp_files_exist(tmp_path):
    (tmp_path / "wp-config.php").write_text("<?php")
    (tmp_path / "wp-content").mkdir()

    profile = detect_profile(tmp_path)

    assert profile == "wordpress"


def test_detect_profile_returns_wordpress_when_wp_content_exists(tmp_path):
    (tmp_path / "wp-content").mkdir()

    profile = detect_profile(tmp_path)

    assert profile == "wordpress"


def test_detect_profile_returns_wordpress_when_wp_admin_exists(tmp_path):
    (tmp_path / "wp-admin").mkdir()

    profile = detect_profile(tmp_path)

    assert profile == "wordpress"


def test_detect_profile_returns_wordpress_when_wp_includes_exists(tmp_path):
    (tmp_path / "wp-includes").mkdir()

    profile = detect_profile(tmp_path)

    assert profile == "wordpress"
