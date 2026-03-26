import sys
from pathlib import Path
import time

MESSAGE = "The project is at its starting point. Real features are coming soon."


def show_help():
    print("sitecheck - pre-deployment checker for websites")
    print()
    print("Usage:")
    print("  sitecheck --help")
    print("  sitecheck scan <path>")
    print()
    print("Commands:")
    print("  scan <path>   Scan the given project path")
    print("  --help        Show this help message")
    print()


def print_result(status, message):
    print(f"{status}: {message}")


def scan(path):
    path_obj = Path(path)

    print("Scanning project...")
    time.sleep(1)

    print(f"Path: {path_obj}")
    print()

    if not path_obj.exists():
        print_result("FAIL", "Path does not exist")
        return

    print_result("PASS", "Path exists")
    time.sleep(1)

    if not path_obj.is_dir():
        print_result("FAIL", "Path is not a directory")
        return

    print_result("PASS", "Path is a directory")
    time.sleep(1)

    if (path_obj / ".git").exists():
        print_result("PASS", "Git repository detected")
        time.sleep(1)
    else:
        print_result("WARN", "Git repository not detected")
        time.sleep(1)

    if (path_obj / ".gitignore").exists():
        print_result("PASS", ".gitignore file found")
        time.sleep(1)
    else:
        print_result("WARN", ".gitignore file not found")
        time.sleep(1)

    print()
    print(MESSAGE)


def main():
    args = sys.argv[1:]

    if len(args) == 0:
        show_help()
        return

    command = args[0]

    if command == "--help":
        show_help()

    elif command == "scan":
        if len(args) < 2:
            print("Usage: sitecheck scan <path>")
            return

        path = args[1]
        scan(path)

    else:
        print(f"Unknown command: {command}")
        print("Try: sitecheck --help")


if __name__ == "__main__":
    main()