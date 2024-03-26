# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shotstriper']

package_data = \
{'': ['*']}

install_requires = \
['aggdraw>=1.3.18.post0,<2.0.0',
 'pillow>=10.2.0,<11.0.0',
 'typer[all]>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['shotstriper = shotstriper.main:app']}

setup_kwargs = {
    'name': 'shotstriper',
    'version': '0.1.1',
    'description': 'Add beautiful, striped backgrounds to your screenshots',
    'long_description': '# Shot-Striper\n\nAdd beautiful, striped backgrounds to your screenshots.\n\n![Shot-Striper](https://raw.githubusercontent.com/psyonara/shotstriper/master/imgs/headline.jpg)\n',
    'author': 'Helmut Irle',
    'author_email': 'me@helmut.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
