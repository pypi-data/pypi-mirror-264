# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['guardog']

package_data = \
{'': ['*']}

install_requires = \
['pytz>=2024.1,<2025.0', 'requests>=2.31.0,<3.0.0']

setup_kwargs = {
    'name': 'guardog',
    'version': '0.3.0',
    'description': '',
    'long_description': '',
    'author': 'Gautham Reddy',
    'author_email': 'gauthm@guardog.app',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
