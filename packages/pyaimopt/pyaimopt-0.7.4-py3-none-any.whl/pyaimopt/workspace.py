# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""
workspace.py

Workspace store connectivity information that enables
access to the service
"""

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import List, NamedTuple, Optional, Tuple, Union
from uuid import uuid4, UUID
import base64
import logging
from anyio import sleep, start_blocking_portal
from .description import ProblemDescription, ProblemSolution


_logger = logging.getLogger(__name__)

# Unique identity of a job
JobID = uuid4


def create_job_id() -> JobID:
    """
    Create a new job id
    """
    return uuid4()


def jobid_as_short_string(jid: JobID) -> str:
    """
    Convert a job id to a short string
    """
    bid = jid.bytes
    sid = base64.urlsafe_b64encode(bid)
    return str(sid)[2:-3]


def jobid_from_short_string(sid: str) -> JobID:
    """
    Convert a short string to a job id
    """
    bid = base64.urlsafe_b64decode(f"{sid}==")
    return UUID(bytes=bid)


def jobid_from_string(sid: str) -> JobID:
    """
    Convert a string to a job id

    :param sid: The string representation of the job id
    :returns: The job id
    """
    return UUID(sid)


class JobStatus(Enum):
    """
    Status of a job
    """

    # Job has been submitted, but not yet started
    SUBMITTED = 1

    # Job is currently running
    RUNNING = 2

    # Job has completed successfully
    COMPLETED = 3

    # Job has failed
    FAILED = 4

    # Unknown job
    UNKNOWN = 5

    # Canceled job
    CANCELED = 6


class Ok(NamedTuple):
    """Job completed successfully"""

    #: The results of the job
    result: ProblemSolution


class Failed(NamedTuple):
    """Job failed"""

    #: The reason for the failure
    error: str


class Canceled(NamedTuple):
    """Job canceled"""

    #: The partial solution, if available
    partial: Optional[ProblemSolution]


class Pending(NamedTuple):
    """Job is pending"""


# Result of a job
JobResult = Union[Ok, Failed, Canceled, Pending]

# Wait time in seconds (2sec) before polling for job status
__WAIT_BEFORE_POLLING__ = 2


def _synchronize_single(func, *args):
    """
    Synchronize a function call

    :param func: The function to call
    :param args: The arguments to pass to the function
    :returns: The result of the function call
    """

    with start_blocking_portal() as portal:
        if portal is None:
            _logger.error("No portal available")
            raise RuntimeError(
                f"No portal available to execute call {func.__name__}; aborting operation"
            )

        return portal.call(func, *args)


class Workspace(ABC):
    """
    Base class for workspace implementations
    """

    __slots__ = "__workspace_id", "__start_time"

    def __init__(self):
        """
        Initialize the workspace
        """
        self.__workspace_id: uuid4 = uuid4()
        self.__start_time: datetime = datetime.now()

    def _annotate(self, problem: ProblemDescription):
        """
        Add workspace information to the problem description.
        This information may help to debug problems.
        """
        problem.configuration["__workspace_id"] = str(self.__workspace_id)
        problem.configuration["__workspace_start_time"] = str(self.__start_time)

    @abstractmethod
    def test_connection(self) -> bool:
        """
        Test that the connection is possible and working correctly
        """
        raise NotImplementedError(
            "`test_connection` method not implemented for abstract method"
        )

    @abstractmethod
    async def submit_async(self, problem: ProblemDescription, time_limit: int) -> JobID:
        """
        Submit a problem to the AIM solver

        :param problem: The problem to solve
        :param time_limit: The time limit for the solver to run
        :returns: The job ID of the submitted job
        """
        raise NotImplementedError(
            "`submit_async` method not implemented for abstract method"
        )

    @abstractmethod
    async def get_status_async(self, job_id: JobID) -> JobStatus:
        """
        Get the status of a job

        :param job_id: The job ID
        :returns: The status of the job
        """
        raise NotImplementedError(
            "`get_status_async` method not implemented for abstract method"
        )

    @abstractmethod
    async def get_result_async(self, job_id: JobID) -> JobResult:
        """
        Get the result of a job

        :param job_id: The job ID
        :returns: The result of the job
        """
        raise NotImplementedError(
            "`get_result_async` method not implemented for abstract method"
        )

    @abstractmethod
    async def get_completed_jobs_async(self) -> List[JobID]:
        """
        Retrieve the list of job IDs that have been completed and for which
        the user can retrieve results.
        """
        raise NotImplementedError(
            "`get_completed_jobs_async` method not implemented for abstract method"
        )

    @abstractmethod
    async def get_all_jobs_async(self) -> List[Tuple[JobID, JobStatus]]:
        """
        Retrieve the list of all job IDs that have been submitted.
        """
        raise NotImplementedError(
            "`get_all_jobs_async` method not implemented for abstract method"
        )

    @abstractmethod
    async def cancel_job_async(self, job_id: JobID) -> bool:
        """
        Cancel a job

        :param job_id: The job ID
        :returns: True if the job was cancelled, False otherwise
        """
        raise NotImplementedError(
            "`cancel_job_async` method not implemented for abstract method"
        )

    @abstractmethod
    async def delete_job_async(self, job_id: JobID) -> bool:
        """
        Delete all information related to a job

        :param job_id: The job ID
        :returns: True if the job was deleted, False otherwise
        """
        raise NotImplementedError(
            "`delete_job_async` method not implemented for abstract method"
        )

    async def solve_async(
        self, problem: ProblemDescription, time_limit: int
    ) -> JobResult:
        """
        Submit a problem to the AIM solver and wait for the result

        :param problem: The problem to solve
        :param time_limit: The time limit for the solver to run
        :returns: The result of the job
        """
        job_id = await self.submit_async(problem, time_limit)
        await sleep(time_limit)
        status = await self.get_status_async(job_id)

        while status in (JobStatus.SUBMITTED, JobStatus.RUNNING):
            await sleep(__WAIT_BEFORE_POLLING__)
            status = await self.get_status_async(job_id)

        return await self.get_result_async(job_id)

    def submit(self, problem: ProblemDescription, time_limit: int) -> JobID:
        """
        Submit a problem to the AIM solver

        :param problem: The problem to solve
        :param time_limit: The time limit for the solver to run
        :returns: The job ID of the submitted job
        """
        return _synchronize_single(self.submit_async, problem, time_limit)

    def solve(self, problem: ProblemDescription, time_limit: int) -> JobResult:
        """
        Submit a problem to the AIM solver and wait for the result

        :param problem: The problem to solve
        :param time_limit: The time limit for the solver to run
        :returns: The result of the job
        """
        return _synchronize_single(self.solve_async, problem, time_limit)

    def get_status(self, job_id: JobID) -> JobStatus:
        """
        Get the status of a job

        :param job_id: The job ID
        :returns: The status of the job
        """
        return _synchronize_single(self.get_status_async, job_id)

    def get_result(self, job_id: JobID) -> JobResult:
        """
        Get the result of a job

        :param job_id: The job ID
        :returns: The result of the job
        """
        return _synchronize_single(self.get_result_async, job_id)

    def get_completed_jobs(self) -> List[JobID]:
        """
        Retrieve the list of job IDs that have been completed and for which
        the user can retrieve results.

        :returns: The list of job IDs of the completed jobs
        """
        return _synchronize_single(self.get_completed_jobs_async)

    def get_all_jobs(self) -> List[Tuple[JobID, JobStatus]]:
        """
        Retrieve the list of all job IDs that have been submitted.

        :returns: The list of job IDs of the submitted jobs
        """
        return _synchronize_single(self.get_all_jobs_async)

    def cancel_job(self, job_id: JobID) -> bool:
        """
        Cancel a job

        :param job_id: The job ID
        :returns: True if the job was cancelled, False otherwise
        """
        return _synchronize_single(self.cancel_job_async, job_id)

    def delete_job(self, job_id: JobID) -> bool:
        """
        Delete all information related to a job

        :param job_id: The job ID
        :returns: True if the job was deleted, False otherwise
        """
        return _synchronize_single(self.delete_job_async, job_id)

    async def print_detailed_async(self) -> None:
        """
        Prints detailed information about the jobs in standard output.
        This is used for debugging purposes.
        """
        for job, status in self.get_all_jobs():
            print(f"Job {job} is {status}")

    def print_detailed(self) -> None:
        """
        Prints detailed information about the jobs in standard output.
        This is used for debugging purposes.
        """
        _synchronize_single(self.print_detailed_async)
