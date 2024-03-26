# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""
problem.py

Definition and implementation of types of problems
available for optimization.
"""

from abc import ABC, abstractmethod
from enum import Enum
from random import Random
from typing import Optional
import uuid
import logging
import sys

from scipy import sparse

# pylint: disable = no-name-in-module
from scipy.linalg import issymmetric

# pylint: enable = no-name-in-module
import networkx as nx
import numpy as np
from .description import (
    ProblemDescription,
    Solution,
    Matrix,
    Vector,
    BooleanVector,
    is_matrix_type,
    is_vector_type,
    is_boolean_vector_type,
)

if sys.version_info >= (3, 10, 0):
    from typing import TypeAlias


_logger: logging.Logger = logging.getLogger(__name__)


if sys.version_info >= (3, 10, 0):
    ProblemId: TypeAlias = uuid.UUID
else:
    ProblemId = uuid.UUID


class Sense(Enum):
    """Encodes the sense (either minimize or maximize) of the optimization"""

    MINIMIZE = 1
    MAXIMIZE = 2

    def __str__(self):
        if self == Sense.MINIMIZE:
            return "Minimization"
        if self == Sense.MAXIMIZE:
            return "Maximization"
        raise ValueError("Unknown sense")

    @staticmethod
    def from_string(sense: str) -> "Sense":
        """
        Parse a string to a sense value
        """
        if sense == "Minimization":
            return Sense.MINIMIZE
        if sense == "Maximization":
            return Sense.MAXIMIZE
        raise ValueError("Unknown sense")


class Problem(ABC):
    """
    Base class for all problem types
    """

    __slots__ = "__id", "__name"

    def __init__(self, name: Optional[str] = None, pid: Optional[ProblemId] = None):
        """
        Create an instance of the problem class

        :param name: An optional name given to the problem
        """

        if pid is not None:
            self.__id: ProblemId = pid
        else:
            self.__id: ProblemId = uuid.uuid4()

        self.__name: Optional[str] = name

    @property
    def id(self) -> ProblemId:
        """
        Get the ID of the problem

        :returns: The id of the problem
        """
        return self.__id

    @property
    def name(self):
        """
        Get the name of the problem
        """
        return self.__name

    @abstractmethod
    def get_random_assignment(self, rng: Random):
        """
        Returns a random assignment (solution) for the problem.

        :param rng: Random source to use to generate assignment.
        """
        raise NotImplementedError("Random instance generation not implemented")

    @abstractmethod
    def evaluate(self, solution: Solution):
        """
        Compute a problem specific metric that determines the quality of
        the solution on the problem.

        :param solution: The solution to evaluate
        :returns: The quality of the proposed solution
        """
        raise NotImplementedError("Evaluation of problem solution not implemented")

    @abstractmethod
    def get_description(
        self, description: Optional[ProblemDescription] = None
    ) -> ProblemDescription:
        """
        Returns a description of the problem instance.

        :returns: A description of the problem instance.
        """
        if description is None:
            description = ProblemDescription(inputs={}, configuration={})

        description.configuration["problem_id"] = str(self.id)
        if self.name is not None:
            description.configuration["problem_name"] = self.name

        return description

    @staticmethod
    def get_arguments(description: ProblemDescription) -> dict:
        """
        Returns a dictionary of arguments that can be used to create a problem instance.
        """
        args = {"pid": uuid.UUID(description.configuration["problem_id"])}
        if "problem_name" in description.configuration:
            args["name"] = description.configuration["problem_name"]

        return args


def _has_zero_element(vector: Vector) -> bool:
    """
    Checks whether any element of the vector has a zero value.

    :param vector: Input vector to check
    :returns: True if there is a zero element in vector; false otherwise.
    """
    return np.any(np.equal(vector, 0))


def _has_non_zero_element(vector: Vector) -> bool:
    """
    Checks whether any element of the vector has a non-zero value.

    :param vector: Input vector to check
    :returns: True if there is a zero element in vector; false otherwise.
    """
    return np.all(np.equal(vector, 0)) is False


def _quadratic_form(matrix: Matrix, x: Vector) -> float:
    """
    Computes the quadratic form of a matrix and a vector: x^T * matrix * x

    :param matrix: The input matrix
    :param x: The input vector
    :returns: Hamiltonian
    """
    matrix = sparse.csr_matrix(matrix)
    matrix_x = matrix.dot(x)
    return x.transpose().dot(matrix_x)


def _is_symmetric(matrix: Matrix) -> bool:
    """
    Checks whether a matrix is symmetric.

    :param matrix: Input matrix to check
    :returns: True if the matrix is symmetric; false otherwise.
    """
    if sparse.issparse(matrix):
        # For some reason, the standard calls to check symmetry do not work for sparse matrices.
        (row, col) = matrix.nonzero()
        return np.all(matrix[row, col] == matrix[col, row])

    return issymmetric(matrix)


def _check_matrix(matrix: Matrix) -> int:
    """
    Checks that the matrix is square, and hence
    can be used for problems that encode quadratic interactions.
    Returns the expected number of variables.

    :param matrix: Matrix to check
    :returns: Expected number of variables
    """
    shape = matrix.shape
    if len(shape) != 2:
        _logger.error(
            "Input matrix is not 2-D (it is %d-D); aborting operation", len(shape)
        )
        raise ValueError("Matrix is not 2-D")

    dim1, dim2 = shape
    if dim1 != dim2:
        _logger.error(
            "Input matrix is not square %d<>%d; aborting operation", dim1, dim2
        )
        raise ValueError(f"Input matrix is not square {dim1}<>{dim2}")

    if _is_symmetric(matrix) is False:
        _logger.error("Input matrix is not symmetric; aborting operation")
        raise ValueError("Input matrix must be symmetric")

    return dim1


def _check_vector(expected_dim: int, vector: Vector):
    """
    Checks that a vector has the expected dimensions

    :param expected_dim: The expected dimension of the vector.
    :param vector: The vector to check; can be None, in which case the case succeeds.
    """

    if len(vector.shape) == 1:
        dim = vector.shape[0]
    elif len(vector.shape) == 2:
        dim, dim2 = vector.shape
        if dim == 1:
            dim = dim2
        elif dim > 1 & dim2 > 1:
            _logger.error(
                "Input should be vector, but it is matrix %dx%d; aborting operation",
                dim,
                dim2,
            )
            raise ValueError("Input vector is a matrix")
    else:
        _logger.error(
            "Multi-dimensional array is not expected in the place of vector; aborting operation"
        )
        raise ValueError("Expected vector, got multi-dimensional matrix")

    if expected_dim != dim:
        _logger.error(
            "Expected vector of length %d, got length %d; aborting operation",
            expected_dim,
            dim,
        )
        raise ValueError(
            f"Got vector of incorrect length, got {dim}, expected {expected_dim}"
        )


def _check_optional_vector(expected_dim: int, vector: Optional[Vector]):
    """
    Checks that a vector has the expected dimensions.
    If the vector is None, the check succeeds.

    :param expected_dim: The expected dimension of the vector.
    :param vector: The vector to check; can be None, in which case the case succeeds.
    """

    if vector is None:
        return

    _check_vector(expected_dim, vector)


class MaxCut(Problem):
    """
    Defines instances of MaxCut problems.
    MaxCut operates on graph instances. It partitions the vertices of the graph
    into two sets with the goal of maximizing the sum of the weights of the edges
    that have endpoints on both sets.
    """

    __slots__ = ["__adjacency"]

    def __init__(
        self,
        adjacency: Matrix,
        name: Optional[str] = None,
        pid: Optional[ProblemId] = None,
    ):
        """
        Create an instance of a max cut problem.
        The max cut takes as input a

        :param adjacency: The adjacency matrix of the input graph
        :param name: An optional name for the problem.
        """
        super().__init__(name, pid)

        if not is_matrix_type(adjacency):
            _logger.error("Input is not a matrix; aborting operation")
            raise ValueError("Input is not a matrix")

        adjacency = adjacency.astype(float)
        _check_matrix(adjacency)

        if _has_non_zero_element(adjacency.diagonal()):
            _logger.error("Input matrix has non-zero elements in diagonal")
            raise ValueError("Input matrix has non-zero element in diagonal")

        self.__adjacency = adjacency

    @staticmethod
    def mk_from_graph(graph: nx.Graph, name: Optional[str] = None) -> "MaxCut":
        """
        Create a max-cut problem from a networkx graph

        :param graph: The input matrix
        :param name: An optional name to identify the problem
        """

        matrix = nx.adjacency_matrix(graph).astype(float).todense()
        return MaxCut(matrix, name)

    @property
    def size(self) -> int:
        """Get the size of the graph"""
        return self.__adjacency.shape[0]

    @property
    def adjacency(self) -> Matrix:
        """Get the adjacency matrix of the graph"""
        return self.__adjacency

    def get_random_assignment(self, rng: Random) -> Solution:
        instance = [rng.choice([-1, 1]) for _ in range(self.size)]
        return np.array(instance)

    def evaluate(self, solution: Solution):
        _check_vector(self.size, solution)

        x = np.sign(solution)
        if _has_zero_element(x):
            _logger.error(
                "Invalid solution, it contains zero elements; aborting evaluation"
            )
            raise ValueError("Invalid solution: contains zero elements")

        total_weights = np.sum(self.__adjacency) / 2.0
        hamiltonian = -_quadratic_form(self.__adjacency, x) / 2.0
        return (total_weights + hamiltonian) / 2

    def get_description(
        self, description: Optional[ProblemDescription] = None
    ) -> ProblemDescription:
        """
        Creates a ProblemDescription object using information from this problem.

        :param description: An optional ProblemDescription object to use as a base;
                            this will be modified and returned.
        :returns: The (modified) ProblemDescription object.
        """
        description = super().get_description(description)
        description.configuration["type"] = "MaxCut"
        description.configuration["sense"] = str(Sense.MAXIMIZE)
        description.inputs["weights"] = self.__adjacency
        return description

    @staticmethod
    def from_description(description: ProblemDescription) -> "MaxCut":
        """
        Creates a MaxCut problem from a ProblemDescription object.

        :param description: The ProblemDescription object to use.
        :returns: The MaxCut problem.
        """
        if description.configuration["type"] != "MaxCut":
            raise ValueError("Invalid problem type")
        if description.configuration["sense"] != str(Sense.MAXIMIZE):
            raise ValueError("Invalid problem sense")

        args = Problem.get_arguments(description)
        return MaxCut(description.inputs["weights"], **args)

    def __eq__(self, other):
        if not isinstance(other, MaxCut):
            return False
        other_max_cut: MaxCut = other
        return np.array_equal(self.adjacency, other_max_cut.adjacency)


class Ising(Problem):
    # pylint: disable=W1401
    """
    Define an instance of an Ising problem.
    Assuming that :math:`a_{ij}` is the strength of interaction of a pair of variables :math:`x_i` and :math:`x_j`,
    and :math:`b_i` is the strength of (magnetic field of) variable :math:`x_i`,
    the Ising aims to assign values -1 or +1
    to the :math:`x_i`'s with the goal of minimizing:

    :math:`-\\sum_{i>j}{a_{ij} \\cdot x_i \\cdot x_j} - \\sum_{i}{b_i \\cdot x_i}`

     Observe the negative sign on both sums.
     Specifying :math:`b_i`'s for variables is aka as external field, and it is optional.
    """
    # pylint: enable=W1401

    __slots__ = "__interactions", "__field"

    def __init__(
        self,
        interactions: Matrix,
        field: Optional[Vector] = None,
        name: Optional[str] = None,
        pid: Optional[ProblemId] = None,
    ):
        """
        Create an instance of an Ising problem

        :param interactions: Strength of bonds between spins
        :param field: Strength of external field (optional)
        :param name: An optional name for the problem
        """

        super().__init__(name, pid)

        if not is_matrix_type(interactions):
            _logger.error("Input is not a matrix; aborting operation")
            raise ValueError("Input is not a matrix")
        if field is not None and not is_vector_type(field):
            _logger.error("Input is not a vector; aborting operation")
            raise ValueError("Input is not a vector")

        interactions = interactions.astype(float)
        if field is not None:
            field = field.astype(float)

        dim = _check_matrix(interactions)
        _check_optional_vector(dim, field)

        self.__interactions: np.ndarray = interactions
        self.__field: Optional[np.ndarray] = field

    @staticmethod
    def mk_from_graph(graph: nx.Graph, name: Optional[str] = None):
        """
        Create a max-cut problem from a networkx graph

        :param graph: The input matrix
        :param name: An optional name to identify the problem
        """

        matrix = nx.adjacency_matrix(graph)
        return Ising(matrix.astype(float), field=None, name=name)

    @property
    def size(self) -> int:
        """Get the number of spins"""
        n, _ = self.__interactions.shape
        return n

    @property
    def has_external_field(self) -> bool:
        """Check if the problem has an external field"""
        return self.__field is not None

    @property
    def interactions(self) -> Matrix:
        """Get the interactions matrix"""
        return self.__interactions

    @property
    def field(self) -> Optional[Vector]:
        """Get the external field"""
        return self.__field

    def get_random_assignment(self, rng: Random) -> Solution:
        instance = [rng.choice([-1, 1]) for _ in range(self.size)]
        return np.array(instance)

    def evaluate(self, solution: Solution):
        _check_vector(self.size, solution)

        x = np.sign(solution)
        if _has_zero_element(x):
            _logger.error(
                "Invalid solution, it contains zero elements; aborting evaluation"
            )
            raise ValueError("Invalid solution: contains zero elements")

        # Observe that we take the negative values
        hamiltonian = -_quadratic_form(self.__interactions, x) / 2.0
        if self.__field is not None:
            field = -self.__field.dot(x)
        else:
            field = 0.0

        return hamiltonian + field

    def get_description(
        self, description: Optional[ProblemDescription] = None
    ) -> ProblemDescription:
        """
        Creates a ProblemDescription object using information from this problem.

        :param description: An optional ProblemDescription object to use as a base;
                            this will be modified and returned.
        :returns: The (modified) ProblemDescription object.
        """
        description = super().get_description(description)
        description.configuration["type"] = "Ising"
        description.configuration["sense"] = str(Sense.MINIMIZE)
        description.inputs["interactions"] = self.__interactions
        if self.__field is not None:
            description.inputs["field"] = self.__field

        return description

    @staticmethod
    def from_description(description: ProblemDescription) -> "Ising":
        """
        Creates an Ising problem from a ProblemDescription object.

        :param description: The ProblemDescription object to use.
        :returns: The Ising problem.
        """
        if description.configuration["type"] != "Ising":
            raise ValueError("Invalid problem type")
        if description.configuration["sense"] != str(Sense.MINIMIZE):
            raise ValueError("Invalid problem sense")

        args = Problem.get_arguments(description)
        return Ising(
            description.inputs["interactions"],
            description.inputs.get("field", None),
            **args,
        )

    # noinspection DuplicatedCode
    def __eq__(self, other):
        if not isinstance(other, Ising):
            return False

        other_ising: Ising = other

        i_equal = np.array_equal(self.interactions, other_ising.interactions)
        f_equal = (self.field is None and other_ising.field is None) or (
            self.field is not None
            and other_ising.field is not None
            and np.array_equal(self.field, other_ising.field)
        )

        return i_equal and f_equal


class QUMO(Problem):
    # pylint: disable=W1401
    """
    Define an instance of the Quadratic Unconstrained Mixed Optimization (QUMO) problem.
    The QUMO seeks to find values x_i that minimize the expression:

    :math:`\\sum_{i>j} a_{ij} \\cdot x_i \\cdot x_j + \\sum_i b_i \\cdot x_i`

    where :math:`a_{ij}` is

    The :math:`x_i`'s can be either binary (i.e. take value 0 or 1), or continuous and
    take values in :math:`\\left[-1, 1\\right]`. Caller decides which :math:`x_i`'s are binary and which are continuous.
    If all are binary, then the problem is the same as Quadratic Unconstrained Binary Optimization (QUBO).
    """
    # pylint: enable=W1401

    __slots__ = "__quadratic", "__linear", "__continuous", "__sense"

    def __init__(
        self,
        quadratic: Matrix,
        linear: Optional[Vector] = None,
        continuous: Optional[BooleanVector] = None,
        sense: Sense = Sense.MINIMIZE,
        name: Optional[str] = None,
        pid: Optional[ProblemId] = None,
    ):
        """
        Initializes an instance of the QUMO problem.

        :param quadratic: Weights assigned to interactions between variables (quadratic terms).
        :param linear: Weights assigned to single variables (linear terms); this field is optional.
        :param continuous: A boolean vector which specifies all continuous variables.
                           This field is optional, if it does not exist, then all variables are assumed to be binary
                           (i.e. QUBO problem).
        """

        super().__init__(name, pid)

        if not is_matrix_type(quadratic):
            _logger.error("Quadratic input is not matrix; aborting operation")
            raise ValueError("Quadratic input is not matrix")
        if linear is not None and not is_vector_type(linear):
            _logger.error("Linear input is not vector; aborting operation")
            raise ValueError("Linear input is not vector")
        if continuous is not None and not is_boolean_vector_type(continuous):
            _logger.error("Continuous input is not boolean vector; aborting operation")
            raise ValueError("Continuous input is not boolean vector")

        quadratic = quadratic.astype(float)
        if linear is not None:
            linear = linear.astype(float)

        dim = _check_matrix(quadratic)
        _check_optional_vector(dim, linear)
        _check_optional_vector(dim, continuous)

        self.__quadratic: Matrix = quadratic
        self.__linear: Optional[Vector] = linear
        self.__continuous: Optional[BooleanVector] = continuous
        self.__sense: Sense = sense

    @property
    def size(self) -> int:
        """
        Get the number of variables
        """
        return self.__quadratic.shape[0]

    def _is_continuous(self, index) -> bool:
        """
        Checks whether a variable is continuous

        :param index: Index of variable
        :returns: True if variable is continuous; false otherwise
        """
        return self.__continuous is not None and self.__continuous[index]

    def _is_binary(self, index) -> bool:
        """
        Checks whether a variable is binary

        :param index: Index of variable
        :returns: True if variable is binary; false otherwise
        """
        return self.__continuous is None or self.__continuous[index] is False

    @property
    def is_maximization(self) -> bool:
        """Returns true if this is a maximization problem"""
        return self.__sense == Sense.MAXIMIZE

    @property
    def is_minimization(self) -> bool:
        """Returns true if this is a minimization problem"""
        return self.__sense == Sense.MINIMIZE

    @property
    def is_qubo(self) -> bool:
        """Returns true if this is a QUBO problem"""
        return self.__continuous is None or not np.any(self.__continuous)

    @property
    def quadratic(self) -> Matrix:
        """
        Get the quadratic terms of the problem
        """
        return self.__quadratic

    @property
    def linear(self) -> Optional[Vector]:
        """
        Get the linear terms of the problem
        """
        return self.__linear

    @property
    def continuous(self) -> Optional[BooleanVector]:
        """
        Get the continuous terms of the problem
        """
        return self.__continuous

    @property
    def sense(self) -> Sense:
        """
        Get the sense of the problem
        """
        return self.__sense

    def get_random_assignment(self, rng: Random) -> Solution:
        result = np.empty((self.size,))
        for i in range(result.size):
            if self._is_continuous(i):
                result[i] = rng.uniform(-1.0, 1.0)
            else:
                result[i] = rng.choice([0.0, 1.0])

        return result

    def _normalize_solution(self, solution):
        """
        Normalize the solution vector to be in the range [-1, 1] for continuous variables and
        0 or 1 for binary variables.

        :param solution: Solution vector
        :returns: Normalized solution vector
        """
        normalized_solution = solution.copy()
        for i in range(normalized_solution.size):
            if self._is_binary(i):
                if normalized_solution[i] > 0.0:
                    normalized_solution[i] = 1.0
                else:
                    normalized_solution[i] = 0.0

            else:
                if normalized_solution[i] < -1.0:
                    normalized_solution[i] = -1.0
                elif normalized_solution[i] > 1.0:
                    normalized_solution[i] = 1.0

        return normalized_solution

    def evaluate(self, solution: Solution):
        _check_vector(self.size, solution)
        normalized = self._normalize_solution(solution)
        objective = _quadratic_form(self.__quadratic, normalized) / 2.0
        if self.__linear is not None:
            objective += self.__linear.dot(normalized)

        return objective

    def get_description(
        self, description: Optional[ProblemDescription] = None
    ) -> ProblemDescription:
        """
        Amends a ProblemDescription object with information from this QUMO problem.

        :param description: The ProblemDescription object to be amended; it will be created if it is None.
        :returns: The (modified) ProblemDescription object.
        """
        description = super().get_description(description)

        if self.is_qubo:
            description.configuration["type"] = "QUBO"
        else:
            description.configuration["type"] = "QUMO"

        description.configuration["sense"] = str(self.__sense)

        description.inputs["quadratic"] = self.__quadratic
        if self.__linear is not None:
            description.inputs["linear"] = self.__linear

        if not self.is_qubo:
            description.inputs["continuous"] = self.__continuous

        return description

    @staticmethod
    def from_description(description: ProblemDescription) -> "QUMO":
        """
        Creates a QUMO problem from a problem description.

        :param description: Problem description
        :returns: QUMO problem
        """

        args = Problem.get_arguments(description)
        quadratic = description.inputs["quadratic"]
        linear = description.inputs.get("linear", None)
        continuous = description.inputs.get("continuous", None)
        sense = Sense.from_string(description.configuration["sense"])

        return QUMO(quadratic, linear, continuous, sense, **args)

    # noinspection DuplicatedCode
    def __eq__(self, other):
        if not isinstance(other, QUMO):
            return False

        other_qumo: QUMO = other

        q_equal = np.array_equal(self.quadratic, other_qumo.quadratic)
        l_equal = (self.linear is None and other_qumo.linear is None) or (
            self.linear is not None
            and other_qumo.linear is not None
            and np.array_equal(self.linear, other_qumo.linear)
        )
        c_equal = (self.continuous is None and other_qumo.continuous is None) or (
            self.continuous is not None
            and other_qumo.continuous is not None
            and np.array_equal(self.continuous, other_qumo.continuous)
        )

        return q_equal and l_equal and c_equal and self.sense == other_qumo.sense


def qubo(
    quadratic: Matrix,
    linear: Optional[Vector] = None,
    sense: Sense = Sense.MINIMIZE,
    name: Optional[str] = None,
    pid: Optional[ProblemId] = None,
) -> QUMO:
    """
    Creates a QUBO problem from a problem description.

    :param quadratic: Weights assigned to interactions between variables (quadratic terms).
    :param linear: Weights assigned to single variables (linear terms); this field is optional.
    :param sense: The sense of the problem (minimization or maximization)
    :param name: An optional name for the problem
    :param pid: An optional problem id
    :returns: QUBO problem
    """
    return QUMO(quadratic, linear, None, sense, name, pid)
