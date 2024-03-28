# Local imports
from miksi_ai_sdk.pythontool import *



def initialize_env(env_path):
    try:
        initialize_environment(env_path)
    except Exception as e:
        print(f"An error occurred during initilization: {e}")


def safe_install_modules(module_names):
    """
    Calls install_dependencies with a list of module names and handles any errors.
    
    :param module_names: A list of strings representing the names of the modules to install.
    """
    try:
        install_dependencies(module_names)
        print("Installation successful.")
    except Exception as e:
        print(f"An error occurred during installation: {e}")



