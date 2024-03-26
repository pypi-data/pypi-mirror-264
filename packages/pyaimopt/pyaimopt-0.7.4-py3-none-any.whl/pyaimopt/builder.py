# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""
builder.py

Helper functions for building QUMO models.
"""


from typing import Dict, Optional, Set, Tuple
import logging
import numpy as np
from . import problem as aim
from .description import Matrix, Vector, BooleanVector

_logger = logging.getLogger(__name__)


class QumoBuilder:
    """
    Provides an interface for building QUMO models.
    """

    __slots__ = "__linear", "__quadratic", "__continuous", "__sense"

    def __init__(self):
        """
        Initializes the builder.
        """

        self.__linear: Dict[int, float] = {}
        self.__quadratic: Dict[Tuple[int, int], float] = {}
        self.__continuous: Set[int] = set()
        self.__sense: aim.Sense = aim.Sense.MINIMIZE

    def add_linear(self, index: int, value: float) -> None:
        """
        Adds a linear term to the model.

        :param index: The index of the variable.
        :param value: The coefficient of the linear term.
        """
        if index < 0:
            _logger.error("index (%d) must be non-negative", index)
            raise ValueError("index must be non-negative")

        if index in self.__linear:
            _logger.info("Adding to existing linear term at index %d", index)
            self.__linear[index] = self.__linear[index] + value
        else:
            self.__linear[index] = value

    def __append_quadratic(self, index1: int, index2: int, value: float) -> None:
        """
        Adds a quadratic term to the model.

        :param index1: The index of the first variable.
        :param index2: The index of the second variable.
        :param value: The coefficient of the quadratic term.
        """
        if (index1, index2) in self.__quadratic:
            _logger.info(
                "Adding to existing quadratic term at index (%d, %d)", index1, index2
            )
            self.__quadratic[(index1, index2)] = (
                self.__quadratic[(index1, index2)] + value
            )
        else:
            self.__quadratic[(index1, index2)] = value

    def add_quadratic(self, index1: int, index2: int, value: float) -> None:
        """
        Adds a quadratic term to the model.

        :param index1: The index of the first variable.
        :param index2: The index of the second variable.
        :param value: The coefficient of the quadratic term.
        """
        if index1 < 0 or index2 < 0:
            _logger.error(
                "index1 (%d) and index2 (%d) must be non-negative", index1, index2
            )
            raise ValueError("index1 and index2 must be non-negative")

        if index1 == index2:
            _logger.error(
                "index1 (%d) and index2 (%d) must be distinct", index1, index2
            )
            raise ValueError("index1 and index2 must be distinct")

        if index1 > index2:
            index1, index2 = index2, index1

        self.__append_quadratic(index1, index2, value)

    def add_quadratic_term_for_variable(self, index: int, value: float) -> None:
        """
        Associate a coefficient with a term of the form x[index]^2.
        """
        if index < 0:
            _logger.error("index (%d) must be non-negative", index)
            raise ValueError("index must be non-negative")

        self.__append_quadratic(index, index, value)

    def set_continuous(self, index: int) -> None:
        """
        Sets the variable at the given index to be continuous.

        :param index: The index of the variable.
        """
        if index < 0:
            _logger.error("index (%d) must be non-negative", index)
            raise ValueError("index must be non-negative")

        if index in self.__continuous:
            _logger.warning("Variable at index %d is already continuous", index)
        else:
            self.__continuous.add(index)

    def add(self, weight: float, index1: int, index2: Optional[int] = None) -> None:
        """
        Adds a term to the model.

        :param weight: The coefficient of the term.
        :param index1: The index of the first variable.
        :param index2: The index of the second variable. If None, then the term is linear.
        """
        if index2 is None:
            self.add_linear(index1, weight)
        elif index1 == index2:
            self.add_quadratic_term_for_variable(index1, weight)
        else:
            self.add_quadratic(index1, index2, weight)

    def set_minimization(self) -> None:
        """
        Sets the optimization sense to minimization.
        """
        self.__sense = aim.Sense.MINIMIZE

    def set_maximization(self) -> None:
        """
        Sets the optimization sense to maximization.
        """
        self.__sense = aim.Sense.MAXIMIZE

    def __get_all_indices(self) -> Set[int]:
        """
        Gets all indices of variables in the model.

        :return: The set of indices.
        """
        indices = set(self.__linear.keys())
        for (index1, index2) in self.__quadratic:
            indices.add(index1)
            indices.add(index2)
        return indices

    def __is_binary(self, index: int) -> bool:
        """
        Checks if the variable at the given index is binary.

        :param index: The index of the variable.
        :return: True if the variable is binary, False otherwise.
        """
        return index not in self.__continuous

    def build(self, name: Optional[str] = None) -> aim.QUMO:
        """
        Checks and constructs the QUMO model.

        :param name: The name of the model.
        :return: The QUMO model.
        """
        if len(self.__linear) == 0 and len(self.__quadratic) == 0:
            _logger.error("The model is empty")
            raise ValueError("The model is empty")

        keys = self.__get_all_indices()
        if len(keys) != max(keys) + 1:
            _logger.error("The model has missing indices")
            raise ValueError("The model has missing indices")

        number_of_variables = len(keys)
        if max(self.__continuous) >= number_of_variables:
            _logger.error(
                "Got continuous variable index %d, but there are only %d variables",
                max(self.__continuous),
                number_of_variables,
            )
            raise ValueError(
                f"Got continuous variable index {max(self.__continuous)}, "
                f"but there are only {number_of_variables} variables"
            )

        assert min(keys) == 0
        assert max(keys) == number_of_variables - 1
        assert max(self.__continuous) < number_of_variables

        self.__convert_binary_squared_to_linear()

        linear = self.__get_linear_terms(number_of_variables)
        continuous = self.__get_vector_of_continuous_variables(number_of_variables)
        quadratic = self.__get_quadratic_terms(number_of_variables)

        return aim.QUMO(
            quadratic=quadratic,
            linear=linear,
            continuous=continuous,
            sense=self.__sense,
            name=name,
        )

    def __convert_binary_squared_to_linear(self):
        """
        Converts quadratic terms of the form x[index]^2 to linear terms.
        """
        binary_to_change = [
            index1
            for (index1, index2) in self.__quadratic
            if index1 == index2 and self.__is_binary(index1)
        ]
        for index in binary_to_change:
            if index in self.__linear:
                self.__linear[index] = (
                    self.__linear[index] + self.__quadratic[(index, index)]
                )
            else:
                self.__linear[index] = self.__quadratic[(index, index)]

            del self.__quadratic[(index, index)]

    def __get_quadratic_terms(self, number_of_variables) -> Matrix:
        """
        Gets the quadratic terms of the model.

        :param number_of_variables: The number of variables in the model.
        :return: The quadratic terms.
        """
        quadratic = np.zeros((number_of_variables, number_of_variables))
        for (index1, index2) in self.__quadratic:
            value = self.__quadratic[(index1, index2)]

            if index1 == index2:
                quadratic[index1, index2] = 2.0 * value
            else:
                quadratic[index1, index2] = value
                quadratic[index2, index1] = value

        return quadratic

    def __get_vector_of_continuous_variables(
        self, number_of_variables
    ) -> Optional[BooleanVector]:
        """
        Gets the boolean vector of continuous variables.

        :param number_of_variables: The number of variables in the model.
        :return: The boolean vector of continuous variables.
        """
        if len(self.__continuous) == 0:
            continuous = None
        else:
            continuous = np.zeros(number_of_variables, dtype=bool)
            for index in self.__continuous:
                continuous[index] = True
        return continuous

    def __get_linear_terms(self, number_of_variables) -> Optional[Vector]:
        """
        Gets the linear terms of the model.

        :param number_of_variables: The number of variables in the model.
        :return: The linear terms.
        """

        if len(self.__linear) == 0:
            linear = None
        else:
            linear = np.zeros(number_of_variables)
            for index, value in self.__linear.items():
                linear[index] = value
        return linear
