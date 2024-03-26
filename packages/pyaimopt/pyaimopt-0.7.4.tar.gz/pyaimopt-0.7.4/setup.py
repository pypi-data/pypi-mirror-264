# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyaimopt']

package_data = \
{'': ['*']}

install_requires = \
['anyio>=3.6.2,<4.0.0',
 'azure-core>=1.26.3,<2.0.0',
 'azure-identity>=1.12.0,<2.0.0',
 'azure-storage-blob>=12.15.0,<13.0.0',
 'json5>=0.9.11,<0.10.0',
 'networkx>=3.0,<4.0',
 'numpy>=1.24.2,<2.0.0',
 'packaging>=23.2,<24.0',
 'platformdirs>=3.5.1,<4.0.0',
 'python-dotenv>=1.0.0,<2.0.0']

extras_require = \
{':python_version >= "3.8" and python_version < "3.12"': ['scipy>=1.10.1,<2.0.0']}

entry_points = \
{'console_scripts': ['aim = pyaimopt.azure_test:main']}

setup_kwargs = {
    'name': 'pyaimopt',
    'version': '0.7.4',
    'description': '',
    'long_description': '# `pyaimopt`: Python Wrapper for the AIM optimization service\n\n`pyaimopt` is a package that provides access to the Analog Iterative Machine (`AIM`) optimization service.\nThe `AIM` optimizer accepts problems in the quadratic unconstrained mixed optimization (`QUMO`) format.\nThe `QUMO` format is a generalization of the quadratic unconstrained binary optimization (`QUBO`) format,\nand allows for the optimization of continuous variables in addition to binary variables.\nThe `AIM` optimizer is a stochastic optimization algorithm that uses a combination of gradient descent and\nannealing to find the global minimum of a given objective function.\nIn addition to `QUMO` and `QUBO` problems, the `AIM` optimizer can also be used to solve `MaxCut` and `Ising`\nproblems.\n\n[![Build Status](https://img.shields.io/travis/username/pyaimopt.svg)](https://travis-ci.org/username/pyaimopt)\n[![Coverage Status](https://img.shields.io/coveralls/github/username/pyaimopt.svg)](https://coveralls.io/github/username/pyaimopt)\n[![License: MS-PL](https://img.shields.io/badge/License-MSPL-green.svg)](https://opensource.org/licenses/MS-PL)\n[![PyPI version](https://badge.fury.io/py/pyaimopt.svg)](https://pypi.org/project/pyaimopt/)\n\n## Table of Contents\n\n- [`pyaimopt`: Python Wrapper for the AIM optimization service](#pyaimopt-python-wrapper-for-the-aim-optimization-service)\n  - [Table of Contents](#table-of-contents)\n  - [Prerequisites](#prerequisites)\n  - [Installation](#installation)\n  - [Authentication and API Keys](#authentication-and-api-keys)\n  - [Usage Examples](#usage-examples)\n  - [Documentation](#documentation)\n  - [Contributing](#contributing)\n  - [License](#license)\n  - [Contact Information](#contact-information)\n\n## Prerequisites\n\nThe package requires Python 3.10 or higher. It is recommended to use a virtual environment to install the package.\n\n\n## Installation\n\nTo install pyaimopt, simply use pip:\n\n```bash\npip install pyaimopt -i https://msr-optics.pkgs.visualstudio.com/OpticalCompute/_packaging/OpticalCompute/pypi/simple/\n```\n\nYou can check successful installation by running the following command:\n\n```bash\naim status\n```\n\nIt should return the version of the installed package and the status of the AIM service.\n\n_TODO_: Example with passing the API key.\n\n## Authentication and API Keys\n\n_TODO_: Add instructions on how to get an API key. This should be done by the AIM team.\n\n_TODO_: Explain how to pass the API key to the package.\n\n_TODO_: Explain alternative authentication methods.\n\n## Usage Examples\n\nTo get started, you can use the following commands to submit a simple `QUMO` problem to the `AIM` optimizer,\ncheck the status of the submitted problem, and retrieve the results.\n\n```bash\naim submit\n# This returns: "Submitted job <job_id>"\naim list\n# The output should contain the <job_id> of the submitted job and its status\n# Upon completion, the status should be "Completed"\naim retrieve <job_id>\n# This returns the results of the optimization\n```\n\n_TODO_: Add example of submitting a simple `QUMO` problem using the synchronous interface.\n\n_TODO_: Add example of using the asynchronous interface.\n\n_TODO_: Mention the `GitHub` repository that contains examples.\n\n## Documentation\n\n_TODO_: Add a link to the documentation.\n\n## Contributing\n\nContributions are welcome!\n\n_TODO_: Add instructions on how to contribute examples.\n\n_TODO_: Add instructions on how to report bugs, and propose new features.\n\n_TODO_: Add instructions on how to suggest changes to the solver.\n\n## License\n\nThis package is released under the `MS-PL` License. See the [LICENSE](LICENSE) file for more information.\n\nThe package depends on a number of external packages.\nThe list of those packages and their corresponding licences can be found in the [NOTICE.html](file:///NOTICE.html) file.\n\n## Contact Information\n\nFor questions or comments related to the functionality or features of the `AIM` optimizer,\nplease raise an issue on the [AIM GitHub repository]().\n\nTo get access to the service, please contact the [AIM Team](mailto:project-aim-contant@microsoft.com).\nAt this point, the service is available to selected users only.\n\nFor further questions or comments, please contact the [AIM Team](mailto:project-aim-service@microsoft.com).\n\n_TODO_: Add a link to the *Issues* page.\n',
    'author': 'Project AIM',
    'author_email': 'project-aim-contact@microsoft.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
