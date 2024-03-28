# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['argmaxima']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'argmaxima',
    'version': '0.0.1',
    'description': 'ARGMAX',
    'long_description': '# ARGMAXIMA',
    'author': 'Michele Dallachiesa',
    'author_email': 'michele.dallachiesa@sigforge.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://www.sigforge.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10.0,<3.13.0',
}


setup(**setup_kwargs)
