from sys import argv, version_info
from os import mkdir, getcwd
from os import path
from colorama import Fore, init
init()

from euph.plusdata import *

if version_info.major * 1000 + version_info.minor < 3008:
    verPython = f'{Fore.GREEN} Version is suitable!'
else:
    verPython = f'{Fore.YELLOW} Version is not suitable!'

HELP_TEXT = f'''
{Fore.MAGENTA}* Version:{Fore.GREEN} Euphoria 1.0.0
{Fore.MAGENTA}* Author:{Fore.GREEN} Markada (markada.py@gmail.com)
{Fore.MAGENTA}* Python:{verPython}
{Fore.MAGENTA}* Commands:
    {Fore.CYAN}py -m euph help {Fore.YELLOW} — show this text
    {Fore.CYAN}py -m euph init {Fore.YELLOW} — creates an empty Python project named "Project"
    {Fore.CYAN}py -m euph init <name> {Fore.YELLOW} — creates an empty Python project with the name you specified in <name>
    {Fore.CYAN}py -m euph add <name> {Fore.YELLOW} — creates a folder with the specified name and the files "__init__.py" and "__main__.py" in it
'''


def check_naming_error(name):
    if [i for i in name if i in '+=[]:*?;«,./\<>| ']:    
        print(Fore.RED + 'The project name contains prohibited characters! (+=[]:*?;«,./\<>| )')
        exit(1)

    if path.exists(name):
        print(Fore.RED + 'The directory already contains a folder or file with the same name!')
        exit(1)


def init_project(name):
    check_naming_error(name)

    pathToProject = path.join(getcwd(), name)
    pathToPackage = path.join(getcwd(), name, 'src', name)

    mkdir(pathToProject)
    mkdir( path.join(getcwd(), name, 'src') )
    mkdir(pathToPackage)

    # Create LICENSE
    with open(path.join(pathToProject, 'LICENSE'), 'w', encoding='utf-8') as file:
        file.write(MIT)

    # Create README
    with open(path.join(pathToProject, 'README.md'), 'w', encoding='utf-8') as file:
        file.write(f'# {name}')

    # Create CHANGELOG
    with open(path.join(pathToProject, 'CHANGELOG'), 'w', encoding='utf-8') as file:
        file.write(f'# {name}\n\n# {name} 0.0.0\n')

    # Create .pypirc
    with open(path.join(pathToProject, '.pypirc'), 'w', encoding='utf-8') as file:
        file.write('[pypi]\n  username = __token__\n  password = \n')

    # Create pyproject.toml
    with open(path.join(pathToProject, 'pyproject.toml'), 'w', encoding='utf-8') as file:
        file.write(PYPROJECT_TEXT)

    # Create Project/__init__.py
    with open(path.join(pathToPackage, '__init__.py'), 'w', encoding='utf-8') as file:
        file.write('')

    # Create Project/__main__.py
    with open(path.join(pathToPackage, '__main__.py'), 'w', encoding='utf-8') as file:
        file.write(MAIN__TEXT)


def main():
    match argv[1:]:
        case ['init', name]:
            init_project(name)
            print(Fore.GREEN + f'The project "{name}" has been successfully created!')

        case ['init']:
            init_project("Project")
            print(Fore.GREEN + f'The project "Project" has been successfully created!')

        case ['add', name]:
            check_naming_error(name)

            pathToPack = path.join(getcwd(), name)
            mkdir(pathToPack)
            
            with open(path.join(pathToPack, '__main__.py'), 'w', encoding='utf-8') as file:
                file.write(MAIN__TEXT)

            with open(path.join(pathToPack, '__init__.py'), 'w', encoding='utf-8') as file:
                file.write('')
        
        case ['help']:
            print(HELP_TEXT)

        case _:
            print(Fore.RED + f'Command "{argv[1:]}" does not exist')
            exit(1)

if __name__ == '__main__':
    main()