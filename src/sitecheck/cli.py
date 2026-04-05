import sys
from .scanner import scan


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