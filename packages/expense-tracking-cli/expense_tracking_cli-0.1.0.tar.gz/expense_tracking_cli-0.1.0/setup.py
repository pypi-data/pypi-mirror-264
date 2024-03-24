# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['expense_tracker']

package_data = \
{'': ['*']}

install_requires = \
['rich==10.7.0', 'tinydb==4.5.1', 'typer==0.3.2']

entry_points = \
{'console_scripts': ['expense = expense_tracker.cli:app']}

setup_kwargs = {
    'name': 'expense-tracking-cli',
    'version': '0.1.0',
    'description': '',
    'long_description': 'expense\n=====\n\nExpense tracking command line application.\n\nGetting started\n----------\nThis project is created using Poetry. For more information about poetry refer [here](https://python-poetry.org/)\n\nTo get started with Expense tracker, follow these steps:\n\n1. Clone this repository to your local machine.\n2. Go inside the cloned repository at `.\\expense-tracker\\` location.\n3. Run `poetry install` to install dependencies and activate virtual environment.\n4. Run `poetry shell` to launch the virtual environment shell. \n5. Start running the commands in the usage section to try out.\n\nUsage\n-----\n\nHere\'s a demo of how it works:\n    \n    # Initialize the app\n    $ expense init \n\n    $ expense add --name "Milk" --description "Bought milk" --price 50\n\n    $ expense add --name "Tea" --description "Bought tea" --price 100\n    $ expense list\n         ╷       ╷             ╷\n      ID │ Name  │ Description │ Price\n    ╺━━━━┿━━━━━━━┿━━━━━━━━━━━━━┿━━━━━━━━━━━━━━╸\n      1  │ Milk  │ Bought milk │ 50\n      2  │ Tea   | Bought tea  │ 100\n         ╵       ╵             ╵\n\n    $ expense update --id 1 --price 60\n\n    $ expense delete --id 1\n\n     $ expense list\n         ╷       ╷             ╷\n      ID │ Name  │ Description │ Price\n    ╺━━━━┿━━━━━━━┿━━━━━━━━━━━━━┿━━━━━━━━━━━━━━╸\n      2  │ Tea   | Bought tea  │ 100\n         ╵       ╵             ╵\n\n    $ expense --help\n    Usage: expense [OPTIONS] COMMAND [ARGS]...\n\n      expense is a small CLI app to track expenses.\n\n    Options:\n       -v, --version Shows application version and exit\n  \n\n    Commands:\n      add      Add an expense to the expense tracker app.\n      clear   clear all expenses in the expense tracker app.\n      delete   Delete an expense from the expense tracker app.\n      init     Initialize the expense tracker app.\n      list     List all expenses in the expense tracker app.\n      total    Generates total expense in the expense tracker app.\n      update    Update an expense in the expense tracker app.\n',
    'author': 'Alfurquan Zahedi',
    'author_email': 'zahedialfurquan20@gmail.com',
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
