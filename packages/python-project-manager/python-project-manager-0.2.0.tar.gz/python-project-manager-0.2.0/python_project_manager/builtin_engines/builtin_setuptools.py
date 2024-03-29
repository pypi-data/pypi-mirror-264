import os
import toml
from python_project_manager import Config, sanitize_string_for_file, sanitize_string_for_module

SetuptoolsEngineConfig = {
    'username': '',
    'password': ''
}

SetupToolsConfig = {
    'wheel': ''
}

def init(_method, **_kwargs):
    edit_config()
    create_template_app()
    set_default_scripts()
    create_toml()
    return False

def version(_method, **_kwargs):
    _method(**_kwargs)
    toml_file = load_toml()
    toml_file['project']['version'] = Config.get('version')
    save_toml(toml_file)
    return False

def edit_config():
    Config.set('src_dir', sanitize_string_for_file(Config.get('project_name')))
    SetuptoolsEngineConfig['username'] = '__token__'
    SetuptoolsEngineConfig['password'] = 'pypi-<api-key>'
    SetupToolsConfig['wheel'] = sanitize_string_for_file(Config.get('project_name'))
    Config.set('twine', SetuptoolsEngineConfig)
    Config.set('setuptools', SetupToolsConfig)
    Config.save()

def create_template_app():
    os.makedirs(Config.get('src_dir'), exist_ok=True)
    with open(f'{Config.get('src_dir')}/app.py', 'w') as f:
        f.write('import os\n\n')
        f.write('def app():\n')
        f.write('    print(os.getcwd())\n')
        f.write('    print("Hello World.")\n\n')
        f.write('if __name__ == "__main__":\n')
        f.write('    app()')

def set_default_scripts():
    default_scripts = {
        'start': f'py -m %src_dir%.app',
        'test': f'py -m %test_dir%.test1',
        'dev': f'python %src_dir%/%project_file_name%/app.py',
        'build': f'ppm version inc -t && python -m build',
        'install': f'pip install %dist_dir%/%setuptools.wheel%-%version%-py3-none-any.whl --force-reinstall',
        'uninstall': f'pip uninstall %dist_dir%/%setuptools.wheel%-%version%-py3-none-any.whl',
        'publish-major': f'ppm version inc -M 1 && ppm run publish',
        'publish-minor': f'ppm version inc -m 1 && ppm run publish',
        'publish-patch': f'ppm version inc -p 1 && ppm run publish',
        'publish': f'del /S /Q %dist_dir%\\* && python -m build && twine upload -u %twine.username% -p %twine.password% -r pypi %dist_dir%/*'
    }
    Config.set('scripts', default_scripts)
    Config.save()

def create_toml():
    toml_config = {
        'build-system': {
            'requires': ['setuptools', 'wheel'],
            'build-backend': 'setuptools.build_meta'
        },

        'project': {
            'name': sanitize_string_for_module(Config.get('project_name')),
            'version': Config.get('version'),
            'description': 'A Python package.',
            'authors': [],
            'readme': 'README.md',
            'keywords': [],
            'dynamic': ['dependencies', 'optional-dependencies']
        },
        
        'tool': {
            'setuptools': {
                'dynamic': {
                    'dependencies': {
                        'file': ['requirements.txt']
                    },
                    'optional-dependencies': {
                        'dev': {
                            'file': ['requirements-dev.txt']
                        }
                    }
                }
            }
        }
    }
    with open('pyproject.toml', 'w') as f:
        toml.dump(toml_config, f)

def load_toml():
    with open('pyproject.toml', 'r') as f:
        return toml.load(f)
    
def save_toml(toml_config):
    with open('pyproject.toml', 'w') as f:
        toml.dump(toml_config, f)