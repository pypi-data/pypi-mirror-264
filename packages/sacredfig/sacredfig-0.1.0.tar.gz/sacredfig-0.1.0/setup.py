# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sacredfig']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6,<4.0']

setup_kwargs = {
    'name': 'sacredfig',
    'version': '0.1.0',
    'description': 'An opinionated library for scientific figures in matplotlib.',
    'long_description': '# sacredfig\n\nSacredFig is a Python library that provides opinionated styles for scientific figures in matplotlib.\n\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install SacredFig.\n\n```bash\npip install sacredfig',
    'author': 'Luc Rocher',
    'author_email': 'luc@rocher.lc',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
