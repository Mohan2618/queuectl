import argparse

from cli.enqueue import enqueue
from cli.list_jobs import list_jobs
from cli.worker import run_worker
from cli.status import status
from cli.config_cmd import config_set, config_get


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

    worker_parser.add_argument(
        "--id",
        required=True,
        help="Worker ID"
    )

    # ---------------- Status ----------------

    status_parser = subparsers.add_parser(
        "status",
        help="Show job details"
    )

    status_parser.add_argument(
        "--id",
        required=True,
        help="Job ID"
    )

    config_parser = subparsers.add_parser(
        "config",
        help="Manage configuration"
    )

    config_sub = config_parser.add_subparsers(dest="config_action")

    set_parser = config_sub.add_parser("set")
    set_parser.add_argument("key")
    set_parser.add_argument("value")

    get_parser = config_sub.add_parser("get")
    get_parser.add_argument("key")

    # Parse arguments AFTER creating all commands
    args = parser.parse_args()

    # Execute the selected command
    if args.action == "enqueue":
        enqueue(args.id, args.job_command)

    elif args.action == "list":
        list_jobs(args.state)

    elif args.action == "worker":
        run_worker(args.id)

    elif args.action == "status":
        status(args.id)

    elif args.action == "config":

        if args.config_action == "set":
            config_set(args.key, args.value)

        elif args.config_action == "get":
            config_get(args.key)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()