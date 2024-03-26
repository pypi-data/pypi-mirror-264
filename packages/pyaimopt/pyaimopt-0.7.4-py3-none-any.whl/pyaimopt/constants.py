"""
constants.py

Global variables that may be of interest to the entire project.

Copyright (c) Microsoft Corporation.
Licensed under the MIT License.
"""

from os import makedirs
from os.path import exists, join, dirname
from platformdirs import user_data_dir

__PACKAGE_NAME = "pyaimopt"
__AUTHOR = "MicrosoftResearch"
_data_directory = user_data_dir(__PACKAGE_NAME, __AUTHOR)


def has_data_file(filename: str) -> bool:
    """
    Checks whether a data file exists in the data directory.
    """
    return exists(join(_data_directory, filename))


def create_empty_data_file(filename: str) -> bool:
    """
    Creates an empty data file in the data directory.
    """
    filename = join(_data_directory, filename)
    if has_data_file(filename):
        return False

    makedirs(_data_directory, exist_ok=True)
    with open(join(_data_directory, filename), "w", encoding="utf-8"):
        pass

    return True


def full_name_for_file(filename: str) -> str:
    """
    Returns the full path to a data file.

    :param filename: The name of the file.
    :return: The full path to the file.
    """
    makedirs(_data_directory, exist_ok=True)
    return join(_data_directory, filename)


def get_terms_of_usage_file() -> str:
    """
    Returns the path to the terms of usage file.
    """
    return join(dirname(__file__), "use.txt")
