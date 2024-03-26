# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""
solver.py

Implementation of solver interface.
Solver works in the context of a workspace and allows
caller to pass parameters that adjust the operation
of the solver, including desired numerical precision,
timout, etc.
"""

from enum import Enum
from .problem import Problem
from .description import ProblemDescription
from .workspace import Workspace, JobID, JobResult


# Default time limit for solver in seconds (2 minutes)
__DEFAULT_DURATION__ = 120


# pylint: disable=invalid-name # The names below are the exact names expected by Julia
class Precision(Enum):
    """
    Precision of the solver
    """

    # Float32
    Float32 = 1

    # Float16
    Float16 = 2

    # BFloat16
    BFloat16 = 3

    # Float64
    Float64 = 4


# pylint: enable=invalid-name


class Solver:
    """
    Base class for defining a solver.
    """

    __slots__ = "_workspace", "__precision"

    def __init__(self, workspace: Workspace):
        """Initialize a solver proxy"""
        self._workspace: Workspace = workspace
        self.__precision: Precision = Precision.Float16

    @property
    def workspace(self) -> Workspace:
        """
        Get access to the workspace
        """
        return self._workspace

    def set_precision(self, precision: Precision):
        """
        Set the precision of the solver
        :param precision: The precision to use
        """
        self.__precision = precision

    def _prepare_problem(self, description: ProblemDescription) -> ProblemDescription:
        """
        Prepare a problem for solving.

        :param description: The problem description
        :returns: The problem
        """
        description.configuration["precision"] = self.__precision.name
        return description

    async def submit_async(
        self, problem: Problem, time_limit: int = __DEFAULT_DURATION__
    ) -> JobID:
        """
        Submit a problem to solver, and wait for the result.

        :param problem: The problem to solve.
        :param time_limit: The time limit for the solver to run.
        :returns: Solution to the problem
        """
        description = problem.get_description()
        description = self._prepare_problem(description)
        job_id = await self._workspace.submit_async(description, time_limit)
        return job_id

    async def solve_async(
        self, problem: Problem, time_limit: int = __DEFAULT_DURATION__
    ) -> JobResult:
        """
        Submit a problem to solver, and wait for the result.

        :param problem: The problem to solve.
        :param time_limit: The time limit for the solver to run.
        :returns: Solution to the problem
        """
        description = problem.get_description()
        description = self._prepare_problem(description)
        result = await self._workspace.solve_async(description, time_limit)
        return result

    def submit(self, problem: Problem, time_limit: int = __DEFAULT_DURATION__) -> JobID:
        """
        Submit a problem to solver, and wait to get job id.

        :param problem: The problem to solve.
        :param time_limit: The time limit for the solver to run.
        :returns: Unique identity of the submitted job
        """
        description = problem.get_description()
        description = self._prepare_problem(description)
        job_id = self._workspace.submit(description, time_limit)
        return job_id

    def solve(
        self, problem: Problem, time_limit: int = __DEFAULT_DURATION__
    ) -> JobResult:
        """
        Submit a problem to solver, and wait for the result.

        :param problem: The problem to solve.
        :param time_limit: The time limit for the solver to run.
        :returns: Solution to the problem
        """
        description = problem.get_description()
        description = self._prepare_problem(description)
        result = self._workspace.solve(description, time_limit)
        return result
