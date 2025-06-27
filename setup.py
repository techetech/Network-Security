'''
The setup.py file is used to configure the packaging and installation of a Python project. 
It includes metadata about the project, such as its name, version, author, and description,
as well as dependencies required for the project to run. 
The setup script can be executed to create a distributable package or to install the project in a Python environment.
from setuptools import setup, find_packages
'''

from setuptools import setup, find_packages
from typing import List

def get_requirements()->List[str]:
    """
    This function returns a list of requirements for the project.
    It reads from a file named 'requirements.txt' and returns the list of requirements.
    """
    requirement_lst: List[str] = []
    try:
        with open('requirements.txt', 'r') as f:
            # Read lines from file
            lines= f.readlines()

            for line in lines:
                # Remove any leading or trailing whitespace
                requirement = line.strip()
                # Ignore comments and empty lines and -e .
                if requirement and not requirement.startswith('#') and not requirement.startswith('-e .'):
                    requirement_lst.append(requirement)

    except FileNotFoundError:
        print("requirements.txt file not found. Returning an empty list.")

    return requirement_lst

setup(
    name='Network-Security-Setup',
    version='0.0.1',
    author='Harsh ',
    packages=find_packages(),
    install_requires=get_requirements(),
)