"""
platform.py

Functionality to control the desired platform for the solver.

Copyright (c) Microsoft Corporation.
Licensed under the MIT License.
"""

from dataclasses import dataclass
from enum import Enum


class TargetHardwareForSolver(Enum):
    """The target hardware for the solver"""

    CPU = 1
    GPU = 2


@dataclass
class TargetHardware:
    """The target hardware for the solver"""

    target: TargetHardwareForSolver = TargetHardwareForSolver.GPU


def set_target_hardware_for_solver(target_hardware: TargetHardwareForSolver):
    """
    Set the target hardware for the solver

    :param target_hardware: The target hardware for the solver
    """
    TargetHardware.target = target_hardware


def get_target_hardware_for_solver() -> TargetHardwareForSolver:
    """
    Get the target hardware for the solver

    :returns: The target hardware for the solver
    """
    return TargetHardware.target


def set_target_hardware_for_solver_to_cpu():
    """Set the target hardware for the solver to CPU"""
    set_target_hardware_for_solver(TargetHardwareForSolver.CPU)


def set_target_hardware_for_solver_to_gpu():
    """Set the target hardware for the solver to GPU"""
    set_target_hardware_for_solver(TargetHardwareForSolver.GPU)


def is_default_target_cpu():
    """
    Check whether the default target hardware for the solver is CPU

    :returns: True if the default target hardware for the solver is CPU
    """
    return get_target_hardware_for_solver() == TargetHardwareForSolver.CPU


def is_default_target_gpu():
    """
    Check whether the default target hardware for the solver is GPU

    :returns: True if the default target hardware for the solver is GPU
    """
    return get_target_hardware_for_solver() == TargetHardwareForSolver.GPU
