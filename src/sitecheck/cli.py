import sys

MESSAGE = "The project is at its starting point. Real features are coming soon."


def show_help() -> None:
    print("sitecheck - pre-deployment checker for websites")
    print()
    print("Usage:")
    print("  python cli.py --help")
    print("  python cli.py scan <path>")
    print()
    print("Commands:")
    print("  scan <path>   Scan the given project path")
    print("  --help        Show this help message")


def scan(path: str) -> None:
    print("Scanning project...")
    print(f"Path: {path}")
    print(MESSAGE)


def main() -> None:
    args = sys.argv[1:]

    if len(args) == 0:
        print("No command provided.")
        print("Use --help to see available commands.")
        return

    command = args[0]

    if command == "--help":
        show_help()

    elif command == "scan":
        if len(args) < 2:
            print("Please provide a path.")
            print("Example: python cli.py scan .")
            return

        path = args[1]
        scan(path)

    else:
        print(f"Unknown command: {command}")
        print("Use --help to see available commands.")


if __name__ == "__main__":
    main()