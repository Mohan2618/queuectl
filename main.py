import argparse

from cli.enqueue import enqueue


def main():
    parser = argparse.ArgumentParser(
        prog="queuectl",
        description="CLI Background Job Queue"
    )

    # action stores the subcommand name (enqueue, list, status...)
    subparsers = parser.add_subparsers(dest="action")

    # enqueue command
    enqueue_parser = subparsers.add_parser("enqueue")
    enqueue_parser.add_argument("--id", required=True, help="Job ID")
    enqueue_parser.add_argument(
        "--command",
        dest="job_command",
        required=True,
        help="Command to execute"
    )

    args = parser.parse_args()

    if args.action == "enqueue":
        enqueue(args.id, args.job_command)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()