# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""
description.py

Data structures used to describe problems and solutions.
These are used to serialize and deserialize problems and solutions.
"""

from typing import NamedTuple, Dict, Union
import sys
from scipy.sparse import issparse
import numpy as np


if sys.version_info >= (3, 10, 0):
    from typing import TypeAlias

if sys.version_info >= (3, 10, 0):
    Solution: TypeAlias = np.ndarray
    Matrix: TypeAlias = np.ndarray
    Vector: TypeAlias = np.ndarray
    BooleanVector: TypeAlias = np.ndarray

    Inputs: TypeAlias = Dict[str, Union[Matrix, Vector, BooleanVector]]
    Metadata: TypeAlias = Dict[str, Union[str, int, float]]

else:
    Solution = np.ndarray
    Matrix = np.ndarray
    Vector = np.ndarray
    BooleanVector = np.ndarray

    Inputs = Dict[str, Union[Matrix, Vector, BooleanVector]]
    Metadata = Dict[str, Union[str, int, float]]

_PROBLEM_DESCRIPTION_VERSION: str = "1.0.0"


class ProblemDescription(NamedTuple):
    """
    Specifies the input problem
    """

    #: Problem description
    inputs: Inputs

    #: Configuration information for the problem
    configuration: Metadata


class ProblemSolution(NamedTuple):
    """
    Specifies the solution to a problem
    """

    #: The solution to the problem
    output: Solution

    #: Information about the solution
    information: Metadata


def _check_version(version: str) -> bool:
    """
    Checks compatibility with the given version
    If true, we can deserialize the problem description

    :param version: The version to check
    """
    return version == _PROBLEM_DESCRIPTION_VERSION


def is_matrix_type(obj) -> bool:
    """
    Checks if the given object is a matrix type
    """
    if isinstance(obj, np.ndarray) or issparse(obj):
        return len(obj.shape) == 2

    return False


def is_vector_type(obj) -> bool:
    """
    Checks if the given object is a vector type
    """
    if not isinstance(obj, np.ndarray):
        return False

    return len(obj.shape) == 1


def is_boolean_vector_type(obj) -> bool:
    """
    Checks if the given object is a boolean vector type
    """
    if not isinstance(obj, np.ndarray):
        return False

    return len(obj.shape) == 1 and obj.dtype == bool
