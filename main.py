import argparse

from cli.enqueue import enqueue
from cli.list_jobs import list_jobs
from cli.worker import worker


def main():
    parser = argparse.ArgumentParser(
        prog="queuectl",
        description="CLI Background Job Queue"
    )

    # Create subparsers
    subparsers = parser.add_subparsers(
        dest="action",
        required=True
    )

    # ---------------- Enqueue ----------------
    enqueue_parser = subparsers.add_parser(
        "enqueue",
        help="Add a new job to the queue"
    )

    enqueue_parser.add_argument(
        "--id",
        required=True,
        help="Job ID"
    )

    enqueue_parser.add_argument(
        "--command",
        dest="job_command",
        required=True,
        help="Command to execute"
    )

    # ---------------- List ----------------
    list_parser = subparsers.add_parser(
        "list",
        help="List all jobs"
    )

    list_parser.add_argument(
        "--state",
        required=False,
        help="Filter jobs by state"
    )

    worker_parser = subparsers.add_parser(
        "worker",
        help="Run one pending job"
    )

    # Parse arguments AFTER creating all commands
    args = parser.parse_args()

    # Execute the selected command
    if args.action == "enqueue":
        enqueue(args.id, args.job_command)

    elif args.action == "list":
        list_jobs(args.state)

    elif args.action == "worker":
        worker()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()