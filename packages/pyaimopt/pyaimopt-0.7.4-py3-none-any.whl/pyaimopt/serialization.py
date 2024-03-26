# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""
serialization.py

Implementation of serialization and deserialization of
problem descriptions, problem solutions and
associated (typically solver) metadata.
"""

from typing import BinaryIO
import logging
import os
import tempfile
import uuid
import json5 as json
import numpy as np
import scipy.sparse as sp
from .description import (
    _PROBLEM_DESCRIPTION_VERSION,
    _check_version,
    ProblemDescription,
    ProblemSolution,
    Metadata,
)
from .problem import Problem, MaxCut, Ising, QUMO


_logger: logging.Logger = logging.getLogger(__name__)


def serialize(stream: BinaryIO, description: ProblemDescription):
    """
    Serializes the problem instance to the given IO stream.

    :param stream: The stream to write to
    :param description: The problem description
    """
    configuration = description.configuration
    configuration["version"] = _PROBLEM_DESCRIPTION_VERSION

    configuration_json = json.dumps(
        configuration, indent=4, quote_keys=True, trailing_commas=False
    )
    configuration_json = configuration_json.replace("'", '"')
    configuration_encoding = configuration_json.encode("ascii")
    configuration_bytes = np.frombuffer(configuration_encoding, dtype=np.uint8)

    inputs = description.inputs.keys()
    for matrix in inputs:
        # Future: we would like to send a more efficient representation of the matrix
        if sp.isspmatrix(description.inputs[matrix]):
            description.inputs[matrix] = description.inputs[matrix].toarray()

    np.savez_compressed(stream, configuration=configuration_bytes, **description.inputs)


def write_to_file(filename: str, description: ProblemDescription):
    """
    Serializes the problem instance to the given file.

    :param filename: The file to write to
    :param description: The problem description
    """
    with open(filename, "wb") as stream:
        serialize(stream, description)


def create_from_problem_description(description: ProblemDescription) -> Problem:
    """
    Creates a problem instance from the given problem description.
    :param description: The problem description
    :return: The problem instance
    """
    problem_type = description.configuration["type"]

    if problem_type == "Ising":
        return Ising.from_description(description)
    if problem_type == "MaxCut":
        return MaxCut.from_description(description)
    if problem_type == "QUBO":
        return QUMO.from_description(description)
    if problem_type == "QUMO":
        return QUMO.from_description(description)

    _logger.error(
        "Problem type %s not supported; aborting deserialization", problem_type
    )
    raise ValueError(f"Problem type {problem_type} not supported")


def read_from_file(filename: str) -> Problem:
    """
    Deserializes a problem instance from the given IO stream.
    """
    npz = np.load(filename)
    configuration = _read_json_from_npz(npz, "configuration")
    problem_type = configuration["type"]
    pid = uuid.UUID(configuration["problem_id"])

    name = configuration.get("problem_name", None)
    version = configuration["version"]

    _logger.info(
        "Deserializing problem %s of type %s from %s with name %s",
        str(pid),
        problem_type,
        filename,
        name,
    )

    if _check_version(version) is False:
        _logger.error("Version %s not supported; aborting deserialization", version)
        raise ValueError(f"Version {version} not supported")

    description = ProblemDescription(configuration=configuration, inputs=npz)
    return create_from_problem_description(description)


def _read_json_from_npz(npz, configuration: str) -> Metadata:
    """
    Reads a json string encoded as a numpy array from the given npz file.

    :param npz: The compressed, archive npz file
    :param configuration: The name of array inside the npz to parse as json and convert to a dictionary
    :return: The configuration as a dictionary
    """
    configuration_array = npz[configuration]
    configuration_bytes = configuration_array.tobytes()
    configuration = configuration_bytes.decode("ascii")
    configuration = json.loads(configuration)
    return configuration


def read_solution_from_file(filename: str) -> ProblemSolution:
    """
    Deserializes a problem solution from the given IO stream.
    """
    if not os.path.exists(filename):
        _logger.error("File %s does not exist; aborting deserialization", filename)
        raise FileNotFoundError(f"File {filename} does not exist")

    npz = np.load(filename)

    if "assignment" not in npz:
        _logger.error(
            "File %s does not contain a solution; aborting deserialization", filename
        )
        raise ValueError(f"File {filename} does not contain a solution")
    if "result" not in npz:
        _logger.error(
            "File %s does not contain solution metadata; aborting deserialization",
            filename,
        )
        raise ValueError(f"File {filename} does not contain solution metadata")

    result = _read_json_from_npz(npz, "result")
    problem_type = result["type"]
    pid = uuid.UUID(result["problem_id"]) if "problem_id" in result else None

    name = result.get("problem_name", None)
    version = result["version"]

    _logger.info(
        "Deserializing solution to problem %s of type %s with name %s",
        str(pid),
        problem_type,
        name,
    )

    if _check_version(version) is False:
        _logger.error("Version %s not supported; aborting deserialization", version)
        raise ValueError(f"Version {version} not supported")

    return ProblemSolution(output=npz["assignment"], information=result)


def _delete_temporary_file(filename: str):
    """
    Deletes the temporary file with the given name.

    :param filename: The name of the temporary file
    """
    try:
        if os.path.isfile(filename):
            os.remove(filename)
            _logger.debug("Removed temporary file %s", filename)
    except PermissionError as exn:
        _logger.error("Failed to remove temporary file %s: %s; ignoring", filename, exn)


def read_solution_from_stream(stream: BinaryIO) -> ProblemSolution:
    """
    Deserializes a problem solution from the given IO stream.
    :param stream: The stream to read from
    :return: The problem solution
    """

    with tempfile.NamedTemporaryFile(suffix=".npz", delete=False) as file:
        filename = file.name
        _logger.debug("Creating temporary file %s", filename)

        file.write(stream.read())
        file.close()

    filesize = os.path.getsize(filename)
    _logger.debug("Wrote %d to temporary file %s", filesize, filename)
    solution = read_solution_from_file(filename)

    _delete_temporary_file(filename)

    return solution
