import sys
import json
import tomllib
from pathlib import Path

from .scanner import scan


def _detail_items(details):
    if isinstance(details, list):
        return [str(item) for item in details]

    if not isinstance(details, str):
        return [str(details)]

    return [item.strip() for item in details.split(", ") if item.strip()]


def _verdict_note(verdict):
    if verdict == "ready_with_warnings":
        return "Review WARN items before deployment."

    if verdict == "not_ready":
        return "Fix FAIL items before deployment."

    return None


def load_ignored_checks(path):
    config_file = Path(path) / ".sitecheck.toml"

    if not config_file.exists():
        return set()

    try:
        config = tomllib.loads(config_file.read_text(encoding="utf-8-sig"))
    except (OSError, tomllib.TOMLDecodeError):
        return set()

    ignored_checks = config.get("ignore", {}).get("checks", [])

    if not isinstance(ignored_checks, list):
        return set()

    return {check for check in ignored_checks if isinstance(check, str)}


def show_help():
    print("sitecheck - pre-deployment checker for websites and WordPress projects")
    print()
    print("Scans a project folder and reports common deployment risks as PASS, WARN, and FAIL.")
    print()
    print("Usage:")
    print("  sitecheck --help")
    print("  sitecheck --version")
    print("  sitecheck scan <path>")
    print("  sitecheck scan <path> --json")
    print("  sitecheck scan <path> --deep")
    print("  sitecheck scan <path> --summary")
    print("  sitecheck scan <path> --only warn")
    print()
    print("Commands:")
    print("  scan <path>      Scan the given project path")
    print()
    print("Global options:")
    print("  --help           Show this help message")
    print("  --version        Show the installed sitecheck version")
    print()
    print("Scan options:")
    print("  --json           Output scan results as JSON for automation")
    print("  --deep           Run deeper, noisier WordPress checks")
    print("  --summary        Only display profile, verdict, summary counts, and verdict note")
    print("  --only <status>  Only display results with the selected status: pass, warn, or fail")
    print()
    print("Examples:")
    print("  sitecheck scan .")
    print("  sitecheck scan ./my-site")
    print("  sitecheck scan ./my-site --json")
    print("  sitecheck scan ./my-site --deep")
    print("  sitecheck scan ./my-site --summary")
    print("  sitecheck scan ./my-site --only warn")
    print("  sitecheck scan ./my-site --only fail")
    print()


def render_text(scan_result, only=None, summary=False):
    print(f"Detected profile: {scan_result['profile']}")
    if "verdict" in scan_result:
        print(f"Verdict: {scan_result['verdict']}")
    print()

    if not summary:
        results = scan_result["results"]

        if only:
            results = [
                result for result in results
                if result["status"].lower() == only
            ]

        if only and not results:
            print(f"No {only.upper()} results to display.")
        else:
            for result in results:
                print(f"{result['status']}: {result['message']}")
                if "details" in result:
                    print("  Details:")
                    for item in _detail_items(result["details"]):
                        print(f"    - {item}")

        print()

    print("Summary:")
    print(f"PASS: {scan_result['summary']['pass']}")
    print(f"WARN: {scan_result['summary']['warn']}")
    print(f"FAIL: {scan_result['summary']['fail']}")

    note = _verdict_note(scan_result.get("verdict"))

    if note:
        print()
        print(note)


def render_json(scan_result):
    print(json.dumps(scan_result, indent=2))


def exit_code(scan_results):
    if scan_results["summary"]["fail"] == 0:
        return 0

    return 1


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    if len(args) == 0:
        show_help()
        return 0

    command = args[0]

    if command == "--help":
        show_help()
        return 0

    if command == "--version":
        print("sitecheck 0.1.0")
        return 0

    if command == "scan":
        if len(args) < 2:
            print("Usage: sitecheck scan <path>")
            return 1

        path = args[1]
        json_mode = "--json" in args[2:]
        deep_mode = "--deep" in args[2:]
        summary_mode = "--summary" in args[2:]

        only_filter = None

        if "--only" in args[2:]:
            only_index = args.index("--only")

            if only_index + 1 >= len(args):
                print("Error: --only requires one of: pass, warn, fail")
                return 1

            only_filter = args[only_index + 1].lower()

            if only_filter not in ("pass", "warn", "fail"):
                print("Error: --only must be one of: pass, warn, fail")
                return 1

        ignored_checks = load_ignored_checks(path)

        scan_result = scan(path, deep=deep_mode, ignored_checks=ignored_checks)

        if json_mode:
            render_json(scan_result)
        else:
            render_text(scan_result, only=only_filter, summary=summary_mode)

        return exit_code(scan_result)

    print(f"Unknown command: {command}")
    print("Try: sitecheck --help")
    return 1


if __name__ == "__main__":
    sys.exit(main())
