# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tabulate_django']

package_data = \
{'': ['*']}

install_requires = \
['Django', 'six>=1.16.0,<2.0.0', 'tabulate']

setup_kwargs = {
    'name': 'tabulate-django',
    'version': '0.2.0',
    'description': 'An application to pretty print Django QuerySets and Model instances in the shell',
    'long_description': None,
    'author': 'James Hardy',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*',
}


setup(**setup_kwargs)
