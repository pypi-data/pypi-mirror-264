"""
pyaimopt is a Python package for solving optimization problems using the
AIM (Analog Iterative Machine) online solver.
"""

from .problem import QUMO, Ising, MaxCut, Sense, qubo
from .builder import QumoBuilder
from .solver import Solver, Precision
from .workspace import Workspace, JobID, JobStatus, JobResult
from .azure_workspace import create_azure_workspace
