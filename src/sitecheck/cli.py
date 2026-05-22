import sys
import json

from .scanner import scan


def show_help():
    print("sitecheck - pre-deployment checker for websites")
    print("Scans a project folder and reports PASS, WARN, and FAIL results.")
    print()
    print("Usage:")
    print("  sitecheck --help")
    print("  sitecheck scan <path>")
    print("  sitecheck scan <path> --json")
    print()
    print("Commands:")
    print("  scan <path>   Scan the given project path")
    print("  --help        Show this help message")
    print()
    print("Options:")
    print("  --json        Output scan results as JSON for automation")
    print()


def render_text(scan_result):
    print(f"Detected profile: {scan_result['profile']}")
    if "verdict" in scan_result:
        print(f"Verdict: {scan_result['verdict']}")
    print()

    for result in scan_result["results"]:
        print(f"{result['status']}: {result['message']}")
        if "details" in result:
            print(f"  Details: {result['details']}")

    print()
    print("Summary:")
    print(f"PASS: {scan_result['summary']['pass']}")
    print(f"WARN: {scan_result['summary']['warn']}")
    print(f"FAIL: {scan_result['summary']['fail']}")


def render_json(scan_result):
    print(json.dumps(scan_result, indent=2))


def exit_code(scan_results):
    if scan_results["summary"]["fail"] == 0:
        return 0
    
    return 1


def main():
    args = sys.argv[1:]

    if len(args) == 0:
        show_help()
        return

    command = args[0]

    if command == "--help":
        show_help()
        return

    if command == "scan":
        if len(args) < 2:
            print("Usage: sitecheck scan <path>")
            return 1

        path = args[1]
        json_mode = "--json" in args[2:]

        scan_result = scan(path)

        if json_mode:
            render_json(scan_result)
        else:
            render_text(scan_result)

        return exit_code(scan_result)

    print(f"Unknown command: {command}")
    print("Try: sitecheck --help")
    return 1


if __name__ == "__main__":
    sys.exit(main())
