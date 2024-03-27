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
    'version': '0.2.0',
    'description': 'Add beautiful, striped backgrounds to your screenshots',
    'long_description': '# Shot-Striper\n\nAdd beautiful, striped backgrounds to your screenshots.\n\n![Shot-Striper](https://raw.githubusercontent.com/psyonara/shotstriper/master/imgs/headline.jpg)\n\n## Installation\n\n### Pipx\n\n```shell\npipx install shotstriper\n```\n\n### Pip\n\n```shell\npip install shotstriper\n```\n\n## Usage\n\n### Quick Start\n\n```shell\nshotstriper add-background screengrab.jpg --palette-name="winter.planar-fugue"\n```\n\nThis creates a new file "out.jpg", with a striped background applied, the colors used being from the "planar-fugue" palette in the "winter" category.\n\n### Palettes\n\nTo get a list of palette categories, run:\n\n```shell\nshotstriper palette-categories\n```\n\nFrom the list, pick one category. Now browse through the palettes in that categories:\n\n```shell\nshotstriper browse-palettes --category sunset\n```\n\nThe palettes are displayed page by page. Note the name of your favourite palette.\n\nNote: you can browse all categories by omitting the category name.\n\n### Adding Backgrounds\n\n#### Using an image from the clipboard\n\n```shell\nshotstriper --from-clipboard --palette-name="sunset.quick-vignette" --output-file="new_screen.jpg"\n```\n\n### More Options\n\n```shell\nshotstriper add-background --help\n```\n',
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
