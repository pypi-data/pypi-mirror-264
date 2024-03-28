import subprocess
import venv
import tempfile
import os


# Global variables
env_path = None
media_path = None
python_executable = None

def initialize_environment(env_path_param):
    global env_path, media_path, python_executable
    env_path = env_path_param
    ensure_virtual_environment()

def ensure_virtual_environment():
    global python_executable
    # Check if the virtual environment already exists
    env_exists = os.path.exists(env_path)
    
    if not env_exists:
        venv.create(env_path, with_pip=True)
    
    # Set the Python executable path
    python_executable = os.path.join(env_path, 'bin', 'python')
    
    # Install defaults only if the environment was newly created
    if not env_exists:
        install_defaults()


def install_defaults():
    defaults = ["matplotlib", "scikit-learn", "numpy", "statsmodels", "pandas", "scipy"]
    safe_install_modules(defaults)


def safe_install_modules(module_names):
    try:
        install_dependencies(module_names)
        print("Installation successful.")
    except Exception as e:
        print(f"An error occurred during installation: {e}")


def install_dependencies(dependencies):
    for dependency in dependencies:
        subprocess.call([python_executable, '-m', 'pip', 'install', dependency])


def execute_code(code):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.py', mode='w') as temp_script:
        temp_script.write(code)
        temp_script_path = temp_script.name

    command = [python_executable, temp_script_path]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"An error occurred--: {e.stderr}"
    finally:
        os.remove(temp_script_path)


