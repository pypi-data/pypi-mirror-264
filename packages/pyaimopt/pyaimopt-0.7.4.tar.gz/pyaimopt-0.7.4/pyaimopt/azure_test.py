# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""
azure_test.py

Simple scripts to test and debug connection to Azure service.
Although not part of the package itself, the code here can enable
users to debug connectivity and job submission issues.

You can run this script with:
python -m pyaimopt.azure_test main
"""

import argparse
import logging
import sys
import networkx as nx
from .azure_workspace import create_azure_workspace
from .aim_credentials import delete_user_credentials, print_user_credentials
from .problem import MaxCut
from .solver import Solver
from .workspace import Workspace, jobid_from_string
from .constants import get_terms_of_usage_file

_logger = logging.getLogger(__name__)


def __test_max_cut_on_circle(
    solver: Solver, size: int = 4, time_limit: int = 10
) -> str:
    graph = nx.circulant_graph(size, [1])
    max_cut = MaxCut.mk_from_graph(graph, f"Example with {size} nodes")
    pid = solver.submit(max_cut, time_limit)
    _logger.info("Submitted job %s", pid)
    return str(pid)


def __submit_job(_args, _workspace: Workspace, solver: Solver):
    _logger.info("Submitting job")
    print("Submitting test job")
    pid = __test_max_cut_on_circle(solver, 10, 10)
    print(f"Submitted job {pid}")


def __list_jobs(args, workspace: Workspace, _solver: Solver):
    _logger.info("Listing jobs")
    jobs = workspace.get_all_jobs()
    if len(jobs) == 0:
        print("No jobs")
        return

    print("Jobs:")
    if args.details:
        workspace.print_detailed()
    else:
        for jobid, status in jobs:
            print(f"Job {jobid}: {status}")


def __list_completed(args, workspace: Workspace, _solver: Solver):
    _logger.info("Listing completed jobs")
    jobs = workspace.get_completed_jobs()
    if len(jobs) == 0:
        print("No completed jobs")
        return

    print("Completed jobs:")
    if args.details:
        workspace.print_detailed()
    else:
        for jobid in jobs:
            print(f"Job {jobid} completed")


def __retrieve_result(args, workspace: Workspace, _solver: Solver):
    _logger.info("Downloading result")
    jobid = jobid_from_string(args.jobid)
    result = workspace.get_result(jobid)
    print(f"Result for job {jobid} is {result}")


def __delete_job(args, workspace: Workspace, _solver: Solver):
    _logger.info("Deleting job")
    jobid = jobid_from_string(args.jobid)
    workspace.delete_job(jobid)


def __print_license(_args, _workspace, _solver):
    _logger.info("Printing license")
    with open(get_terms_of_usage_file(), "r", encoding="utf-8") as license_file:
        print(license_file.read())


def __user_info(args, _workspace, _solver):
    _logger.info("Printing user information")
    if args.delete:
        delete_user_credentials()
    elif args.print:
        print_user_credentials(detailed=True)
    else:
        print_user_credentials()


def __main(args, workspace: Workspace, solver: Solver):
    args.func(args, workspace, solver)


def main():
    """
    Main entry point for this "pseudo-script".
    """

    if __name__ == "__main__":
        cmdline = "python -m pyaimopt.azure_test"
    else:
        cmdline = sys.argv[0]

    if len(sys.argv) == 1:
        sys.argv.append("--help")

    usage = f"""
    To submit a simple (automatically constructed) job:
    \t {cmdline} submit

    To list all jobs:
    \t {cmdline} list

    To download the result of a job:
    \t {cmdline} retrieve <jobid>

    To see the terms of use for the AIM service:
    \t {cmdline} license
    """

    parser = argparse.ArgumentParser(
        description="Test AIM online service",
        prog="python -m pyaimopt.azure_test",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=usage,
    )
    parser.set_defaults(func=lambda _: parser.print_help())
    parser.add_argument(
        "-d",
        "--debug",
        help="Enable debug logging",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.WARNING,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Enable verbose logging",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
    )
    parser.add_argument(
        "-u",
        "--username",
        help="Username for AIM service",
        default=None,
    )
    parser.add_argument(
        "-c",
        "--container",
        help="Container for AIM service",
        default=None,
    )

    subs = parser.add_subparsers()
    submit = subs.add_parser("submit", help="Submit a job")
    submit.set_defaults(func=__submit_job)

    list_jobs = subs.add_parser("list", help="List jobs")
    list_jobs.add_argument(
        "-d",
        "--details",
        help="Show details for each job",
        action="store_true",
    )
    list_jobs.set_defaults(func=__list_jobs)

    completed_jobs = subs.add_parser("completed", help="List completed jobs")
    completed_jobs.add_argument(
        "-d",
        "--details",
        help="Show details for each job",
        action="store_true",
    )
    completed_jobs.set_defaults(func=__list_completed)

    show_license = subs.add_parser("license", help="Show terms of use")
    show_license.set_defaults(func=__print_license)

    retrieve_result = subs.add_parser("retrieve", help="Download results")
    retrieve_result.add_argument("jobid", help="Job ID")
    retrieve_result.set_defaults(func=__retrieve_result)

    delete_job = subs.add_parser("delete", help="Delete a job")
    delete_job.add_argument("jobid", help="Job ID")
    delete_job.set_defaults(func=__delete_job)

    user_info = subs.add_parser("user", help="Show user information")
    user_info.add_argument(
        "-d",
        "--delete",
        help="Delete user information",
        action="store_true",
    )
    user_info.add_argument(
        "-p",
        "--print",
        help="Print user information",
        action="store_true",
    )
    user_info.set_defaults(func=__user_info)

    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)

    wks = create_azure_workspace(username=args.username, container=args.container)
    solver = Solver(wks)
    __main(args, wks, solver)


if __name__ == "__main__":
    main()
