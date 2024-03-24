import importlib
import os
import re
import click
from python_project_manager import Config

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

def parse_dynamic_script(script: str):
    """
    Parses a dynamic script by replacing placeholders with corresponding values from the Config class.

    Args:
        script (str): The dynamic script to parse.

    Returns:
        str: The parsed script with placeholders replaced.

    Example:
        >>> script = "Hello, %name%! Today is %day%."
        >>> parse_dynamic_script(script)
        'Hello, John! Today is Monday.'
    """
    def replace(match):
        placeholder = match.group(1)
        parts = placeholder.split('.')
        value = Config

        for part in parts:
            if isinstance(value, dict):
                try:
                    value = value[part]
                except KeyError:
                    return f'%{placeholder}%'
            else:
                try:
                    value = getattr(value, part)
                except AttributeError:
                    return f'%{placeholder}%'
            
        return str(value)

    return re.sub(r'%(.*?)%', replace, script)

@click.group()
def cli():
    pass

@cli.command()
@click.argument('project_name', type=str, required=True)
@click.option('--engine', '-e', type=str, default='', help='Choose the engine \'module\' to use')
@click.option('--force', '-f', is_flag=True, help='Force initialization of the project')
def init(project_name, engine, force):
    '''
    <project_name> - Name of the project to be setup
    '''
    if not force and Config.load(log = False):
        print('Project already initialized')
        return

    Config.project_name = project_name
    Config.engine = engine
    engine = importlib.import_module(sanitize_string_for_file(engine))

    if engine is None:
        print('Engine not found')
        return
    
    Config.save()
    engine.init()

@cli.command()
@click.argument('script_name', type=str, required=True)
def run(script_name):
    '''
    <script_name> - Name of the script to be run
    '''
    keep_processing = True
    cli_command = Config.scripts[script_name]

    if not cli_command:
        print(f"Script '{script_name}' not found")
        return
    
    try:
        engine = importlib.import_module(sanitize_string_for_file(Config.engine))
        [keep_processing, cli_command] = engine.run(script_name = script_name, cli_command = cli_command)
    except AttributeError:
        pass

    if not keep_processing:
        return

    ## Smart change directory
    cwd = os.getcwd() # Get the current working directory
    cli_command = parse_dynamic_script(cli_command) # Parse the dynamic script

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
                targ_dir = re.search(f'^\w*(.|\|/)(?!py)', python_path[0])
                if targ_dir:
                    # Join the target dir with the current working directory
                    cwd = os.path.join(cwd, targ_dir[0][:-1])
                    # Remove targ_dir from python_path
                    cli_command = cli_command.replace(python_path[0],python_path[0].replace(targ_dir[0], ""))
                        
    os.chdir(cwd) # Change the current working directory
    os.system(cli_command) # Run the command

@cli.command()
@click.argument('action', type=click.Choice(['inc', 'dec', 'show']), required=True, default='show')
@click.option('--major', '-M', type=int, default=0, help='Change the major version')
@click.option('--minor', '-m', type=int, default=0, help='Change the minor version')
@click.option('--patch', '-p', type=int, default=0, help='Change the patch version')
@click.option('--timestamp', '-t', is_flag=True, help='Include timestamp in the version')
def version(action, major, minor, patch, timestamp):
    '''
    <action> - Action to perform on the version
    '''
    keep_processing = True
    
    try:
        engine = importlib.import_module(sanitize_string_for_file(Config.engine))
        keep_processing = engine.version(action = action, major = major, minor = minor, patch = patch, timestamp = timestamp)
    except AttributeError:
        pass

    if not keep_processing:
        return
    
    if action == 'show':
        print(Config.version)
        return
    
    # Split the version by '.' and '+'
    version_list = re.split(r'\.', Config.version)
    ver_major = int(version_list[0])
    ver_minor = int(version_list[1])
    ver_patch = int(version_list[2])
    ver_timestamp = version_list[3] if len(version_list) > 3 else ''

    # Increment the version
    if action == 'inc':
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

    print(f'Version: {Config.version} -> {version}')
    Config.version = version
    Config.save()
    

if __name__ == '__main__':
    cli()