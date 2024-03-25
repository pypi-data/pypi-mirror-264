# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rapidgbm', 'rapidgbm.metrics', 'rapidgbm.utility']

package_data = \
{'': ['*'], 'rapidgbm': ['examples/*']}

install_requires = \
['lightgbm>=3.3.0,<5.0.0',
 'matplotlib>=3.5.2,<4.0.0',
 'numpy>=1.13.0,<3.0.0',
 'optuna-integration>=3.2.0,<4.0.0',
 'optuna>=2.10.0,<4.0.0',
 'pandas>=1.5.0,<3.0.0',
 'scikit-learn>=0.23.2,<2.0.0']

setup_kwargs = {
    'name': 'rapidgbm',
    'version': '0.1.0',
    'description': 'RapidGBM is a powerful Python package designed to streamline the process of tuning LightGBM models using the optimization framework Optuna.',
    'long_description': '# [RapidGBM](https://dhmunk.github.io/rapidgbm/)\nDocumentaion: [Click here](https://dhmunk.github.io/rapidgbm/)\n\nRapidGBM is a powerful Python package designed to streamline the process of tuning LightGBM models using the optimization framework Optuna. With RapidGBM, you can effortlessly fine-tune hyperparameters to achieve optimal model performance using an automated machine learning (AutoML) approach.\n\n## [Classification Example](https://mybinder.org/v2/gh/dhmunk/rapidgbm/main?labpath=rapidgbm%2Fexamples%2Fclassification.ipynb):\n\n [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/dhmunk/rapidgbm/main?labpath=rapidgbm%2Fexamples%2Fclassification.ipynb)\n\n## [Regression Example](https://mybinder.org/v2/gh/dhmunk/rapidgbm/main?labpath=rapidgbm%2Fexamples%2Fregression.ipynb):\n\n[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/dhmunk/rapidgbm/main?labpath=rapidgbm%2Fexamples%2Fregression.ipynb)',
    'author': 'Daniel Porsmose',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.13',
}


setup(**setup_kwargs)
