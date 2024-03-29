import importlib
import os
import re
import click
from python_project_manager import Config

VENV = f'venv\\Scripts\\activate'

def sanitize_string_for_file(string):
    """
    Sanitizes a string for use as a file name by removing leading/trailing whitespace
    and replacing spaces and hyphens with underscores.

    Args:
        string (str): The string to be sanitized.

    Returns:
        str: The sanitized string.
    """
    sanitized_string = string.strip()
    sanitized_string = re.sub(r' |-', '_', sanitized_string)
    return sanitized_string

def sanitize_string_for_module(string):
    """
    Sanitizes a string for use as a module name.

    Args:
        string (str): The string to be sanitized.

    Returns:
        str: The sanitized string.

    """

    sanitized_string = string.strip()
    sanitized_string = re.sub(r' ', '_', sanitized_string)
    return sanitized_string

def pass_command_to_engine(_command: str, _method, **_kwargs):
    try:
    # built-in engines
        if Config.get('engine', '').startswith('ppm-builtin-setuptools'):
            engine = importlib.import_module('python_project_manager.builtin_engines.builtin_setuptools')
        else:
            engine = importlib.import_module(sanitize_string_for_file(Config.get('engine')))
        method = getattr(engine, _command, None)
        if method:
            keep_processing = method(_method, **_kwargs)
            # If keep_processing is None or True, continue processing
            if keep_processing is None or keep_processing:
                _method(**_kwargs)
        else:
            _method(**_kwargs)

    except Exception as e:
        if Config.get('engine') == '':
            _method(**_kwargs)
        else:
            raise e

@click.group()
def cli():
    pass

@cli.command()
@click.argument('project_name', type=str, required=True)
@click.option('--engine', '-e', type=str, default='', help='Choose the engine \'module\' to use')
@click.option('--force', '-f', is_flag=True, help='Force initialization of the project')
# @click.option('--python', '-p', type=str, default='', help='Python version to use')
def init(project_name, engine, force):
    '''
    <project_name> - Name of the project to be setup
    '''

    # Check if the project has already been initialized
    if not force and Config.load(log = False):
        print('Project already initialized')
        return
    
    # Check if the engine if not empty and not a built-in engine
    if engine != '' and not engine.startswith('ppm-builtin'):
        try:
            importlib.import_module(sanitize_string_for_file(Config.get('engine')))
        except Exception as e:
            print(f"Engine '{engine}': Error: {e}")
            return

    # Set the project name and engine
    Config.set('project_name', project_name)
    Config.set('engine', engine)
    Config.save()

    # Create the requirements.txt and requirements-dev.txt files
    with open(os.path.join(os.getcwd(), 'requirements.txt'), 'w') as file:
        pass
    with open(os.path.join(os.getcwd(), 'requirements-dev.txt'), 'w') as file:
        pass

    # Create the venv
    os.system('python -m venv venv')

    pass_command_to_engine('init', _init,
        project_name=project_name, engine=engine)

def _init(**kwargs):
    src_dir = os.path.join(os.getcwd(), Config.get('src_dir'))
    os.makedirs(src_dir, exist_ok=True)
    pass

@cli.command()
@click.argument('script_name', type=str, required=True)
def run(script_name):
    '''
    <script_name> - Name of the script to be run
    '''
    
    cli_command = Config.get(f'scripts.{script_name}')
    
    pass_command_to_engine('run', _run,
        script_name=script_name, cli_command=cli_command)

def _run(**kwargs):
    cli_command = kwargs.get('cli_command', None)
    script_name = kwargs.get('script_name', None)

    if not cli_command:
        print(f"Script '{script_name}' not found")
        return
    
    ## Smart change directory
    cwd = os.getcwd() # Get the current working directory

    # Check if the command has a change directory command
    has_change_directory_command = re.search(r'(^|\s)cd\s\w*', cli_command)
    if not has_change_directory_command:
        # Searches for the 'python' command along with the script path
        python_command = re.search(r'python.*\.py', cli_command)
        if python_command:
            # Get the python path
            python_path = re.search(r'\S*\.py', python_command[0])
            if python_path:
                # Get the first dir in python path
                targ_dir = re.search(r'^\w*(.|\|/)(?!py)', python_path[0])
                if targ_dir:
                    # Join the target dir with the current working directory
                    cwd = os.path.join(cwd, targ_dir[0][:-1])
                    # Remove targ_dir from python_path
                    cli_command = cli_command.replace(python_path[0],python_path[0].replace(targ_dir[0], ""))
                    if targ_dir[0][:-1] == Config.get('test_dir'):
                        cli_command = f'set PYTHONPATH=C:\{Config.get('src_dir')};%PYTHONPATH% && {cli_command}'
                        
    os.chdir(cwd) # Change the current working directory
    os.system(cli_command) # Run the command

@cli.command()
@click.argument('action', type=click.Choice(['inc', 'dec', 'show', 'set']), required=True, default='show')
@click.option('--major', '-M', type=int, default=0, help='Change the major version')
@click.option('--minor', '-m', type=int, default=0, help='Change the minor version')
@click.option('--patch', '-p', type=int, default=0, help='Change the patch version')
@click.option('--timestamp', '-t', is_flag=True, help='Include timestamp in the version')
def version(action, major, minor, patch, timestamp):
    '''
    <action> - Action to perform on the version
    '''       
    if action == 'show':
        print(Config.get('version'))
        return

    pass_command_to_engine('version', _version,
        action=action, major=major, minor=minor, patch=patch, timestamp=timestamp)

def _version(**kwargs):
    action = kwargs.get('action', None)
    major = kwargs.get('major', None)
    minor = kwargs.get('minor', None)
    patch = kwargs.get('patch', None)
    timestamp = kwargs.get('timestamp', None)
    
    # Split the version by '.' and '+'
    version_list = re.split(r'\.', Config.get('version'))
    ver_major = int(version_list[0])
    ver_minor = int(version_list[1])
    ver_patch = int(version_list[2])
    ver_timestamp = version_list[3] if len(version_list) > 3 else ''

    # Increment the version
    if action == 'set':
        if major:
            ver_major = major
        if minor:
            ver_minor = minor
        if patch:
            ver_patch = patch
    elif action == 'inc':
        if major:
            ver_minor = 0
            ver_patch = 0
        elif minor:
            ver_patch = 0
        elif patch:
            pass

        ver_major += major
        ver_minor += minor
        ver_patch += patch
    elif action == 'dec':
        ver_major -= major
        ver_minor -= minor
        ver_patch -= patch

    if timestamp:
        import time
        ver_timestamp = time.strftime('%Y%m%d%H%M%S')

    #concat the version
    version = f'{ver_major}.{ver_minor}.{ver_patch}'
    if timestamp:
        version = f'{version}.{ver_timestamp}'

    print(f'Version: {Config.get('version')} -> {version}')
    Config.set('version', version)
    Config.save()

# Pip commands
@cli.command(context_settings=dict(
    ignore_unknown_options=True
))
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.option('--help', '-h', is_flag=True) # Allows '--help' to be passed as an argument
def list(args, help):
    '''
    Uses pip's 'list' command
    '''
    if help:
        os.system(f'{VENV} && pip list --help')
    else:
        os.system(f'{VENV} && pip list {' '.join(args)}')

@cli.command(context_settings=dict(
    ignore_unknown_options=True
))
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.option('--dev', '-d', is_flag=True) # Add the package to the dev requirements
@click.option('--help', '-h', is_flag=True) # Allows '--help' to be passed as an argument
def install(args, help, dev):
    '''
    Uses pip's 'install' command
    '''
    if help:
        os.system(f'{VENV} && pip install --help')
        return
    
    cmd = f'{VENV} && pip install {" ".join(args)}'

    if cmd.strip() == f'{VENV} && pip install':
        os.system(f'{VENV} && pip install -r requirements.txt -r requirements-dev.txt')

    try:
        output = os.popen(cmd)

        # Read and print each line of the output
        for line in output:
            print(line.strip())
            if 'Successfully installed' in line:
                update_requirements(line.strip(), dev)

        # Close the output stream
        output.close()

    except Exception as e:
        print(f"An error occurred: {e}")
    
def update_requirements(packages_to_update: str, is_dev=False):
    requirement_file = 'requirements-dev.txt' if is_dev else 'requirements.txt'
    packages_to_update = packages_to_update.replace('Successfully installed ', '').split(' ')
    packages_to_update = [re.split(r'-(?=[^-]*$)', package) for package in packages_to_update]
    packages_to_update = [(package[0], package[1]) for package in packages_to_update]
    
    packages_to_keep = []
    with open(requirement_file, 'r') as file:
        for line in file:
            package_name = re.match(r'^(\w|_|-|\d)*', line.strip())[0]
            if package_name not in [package[0] for package in packages_to_update]:
                packages_to_keep.append(line)

    packages_to_write = []

    for package in packages_to_update:
        packages_to_write.append(f'{package[0]}~={package[1]}'.strip())
    for package in packages_to_keep:
        packages_to_write.append(f'{package}'.strip())

    packages_to_write.sort()

    with open(requirement_file, 'w') as file:
        file.write('\n'.join(packages_to_write))

if __name__ == '__main__':
    cli()