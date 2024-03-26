# `pyaimopt`: Python Wrapper for the AIM optimization service

`pyaimopt` is a package that provides access to the Analog Iterative Machine (`AIM`) optimization service.
The `AIM` optimizer accepts problems in the quadratic unconstrained mixed optimization (`QUMO`) format.
The `QUMO` format is a generalization of the quadratic unconstrained binary optimization (`QUBO`) format,
and allows for the optimization of continuous variables in addition to binary variables.
The `AIM` optimizer is a stochastic optimization algorithm that uses a combination of gradient descent and
annealing to find the global minimum of a given objective function.
In addition to `QUMO` and `QUBO` problems, the `AIM` optimizer can also be used to solve `MaxCut` and `Ising`
problems.

[![Build Status](https://img.shields.io/travis/username/pyaimopt.svg)](https://travis-ci.org/username/pyaimopt)
[![Coverage Status](https://img.shields.io/coveralls/github/username/pyaimopt.svg)](https://coveralls.io/github/username/pyaimopt)
[![License: MS-PL](https://img.shields.io/badge/License-MSPL-green.svg)](https://opensource.org/licenses/MS-PL)
[![PyPI version](https://badge.fury.io/py/pyaimopt.svg)](https://pypi.org/project/pyaimopt/)

## Table of Contents

- [`pyaimopt`: Python Wrapper for the AIM optimization service](#pyaimopt-python-wrapper-for-the-aim-optimization-service)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Authentication and API Keys](#authentication-and-api-keys)
  - [Usage Examples](#usage-examples)
  - [Documentation](#documentation)
  - [Contributing](#contributing)
  - [License](#license)
  - [Contact Information](#contact-information)

## Prerequisites

The package requires Python 3.10 or higher. It is recommended to use a virtual environment to install the package.


## Installation

To install pyaimopt, simply use pip:

```bash
pip install pyaimopt -i https://msr-optics.pkgs.visualstudio.com/OpticalCompute/_packaging/OpticalCompute/pypi/simple/
```

You can check successful installation by running the following command:

```bash
aim status
```

It should return the version of the installed package and the status of the AIM service.

_TODO_: Example with passing the API key.

## Authentication and API Keys

_TODO_: Add instructions on how to get an API key. This should be done by the AIM team.

_TODO_: Explain how to pass the API key to the package.

_TODO_: Explain alternative authentication methods.

## Usage Examples

To get started, you can use the following commands to submit a simple `QUMO` problem to the `AIM` optimizer,
check the status of the submitted problem, and retrieve the results.

```bash
aim submit
# This returns: "Submitted job <job_id>"
aim list
# The output should contain the <job_id> of the submitted job and its status
# Upon completion, the status should be "Completed"
aim retrieve <job_id>
# This returns the results of the optimization
```

_TODO_: Add example of submitting a simple `QUMO` problem using the synchronous interface.

_TODO_: Add example of using the asynchronous interface.

_TODO_: Mention the `GitHub` repository that contains examples.

## Documentation

_TODO_: Add a link to the documentation.

## Contributing

Contributions are welcome!

_TODO_: Add instructions on how to contribute examples.

_TODO_: Add instructions on how to report bugs, and propose new features.

_TODO_: Add instructions on how to suggest changes to the solver.

## License

This package is released under the `MS-PL` License. See the [LICENSE](LICENSE) file for more information.

The package depends on a number of external packages.
The list of those packages and their corresponding licences can be found in the [NOTICE.html](file:///NOTICE.html) file.

## Contact Information

For questions or comments related to the functionality or features of the `AIM` optimizer,
please raise an issue on the [AIM GitHub repository]().

To get access to the service, please contact the [AIM Team](mailto:project-aim-contant@microsoft.com).
At this point, the service is available to selected users only.

For further questions or comments, please contact the [AIM Team](mailto:project-aim-service@microsoft.com).

_TODO_: Add a link to the *Issues* page.
