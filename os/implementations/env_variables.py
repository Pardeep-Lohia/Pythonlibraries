"""
Environment Variables Implementation

This module demonstrates how to work with environment variables using the os module.
Environment variables are key-value pairs that are part of the operating system environment.
"""

import os
import json
from collections import defaultdict


class EnvironmentManager:
    """
    A class to manage environment variables with additional functionality.
    """

    def __init__(self):
        """Initialize with current environment variables."""
        self._original_env = dict(os.environ)

    def get(self, key, default=None):
        """
        Get an environment variable.

        Args:
            key (str): Environment variable name
            default: Default value if key doesn't exist

        Returns:
            str or default: Value of environment variable
        """
        return os.environ.get(key, default)

    def set(self, key, value):
        """
        Set an environment variable.

        Args:
            key (str): Environment variable name
            value (str): Value to set
        """
        os.environ[key] = str(value)

    def delete(self, key):
        """
        Delete an environment variable.

        Args:
            key (str): Environment variable name to delete
        """
        if key in os.environ:
            del os.environ[key]

    def exists(self, key):
        """
        Check if an environment variable exists.

        Args:
            key (str): Environment variable name

        Returns:
            bool: True if exists, False otherwise
        """
        return key in os.environ

    def list_all(self, prefix=None):
        """
        List all environment variables, optionally filtered by prefix.

        Args:
            prefix (str): Filter variables starting with this prefix

        Returns:
            dict: Dictionary of environment variables
        """
        if prefix:
            return {k: v for k, v in os.environ.items() if k.startswith(prefix)}
        return dict(os.environ)

    def restore_original(self):
        """Restore environment to original state."""
        os.environ.clear()
        os.environ.update(self._original_env)


def load_env_file(filepath):
    """
    Load environment variables from a .env file.

    Args:
        filepath (str): Path to .env file

    Format:
        KEY1=value1
        KEY2="quoted value"
        KEY3=value with spaces
        # Comments are ignored
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Environment file not found: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue

            # Parse key=value
            if '=' not in line:
                print(f"Warning: Invalid line {line_num} in {filepath}: {line}")
                continue

            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()

            # Remove quotes if present
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]

            # Set environment variable
            os.environ[key] = value


def save_env_file(filepath, variables=None, overwrite=False):
    """
    Save environment variables to a .env file.

    Args:
        filepath (str): Path to save .env file
        variables (dict): Variables to save (default: all current env vars)
        overwrite (bool): Whether to overwrite existing file
    """
    if os.path.exists(filepath) and not overwrite:
        raise FileExistsError(f"File already exists: {filepath}")

    if variables is None:
        variables = dict(os.environ)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("# Environment variables\n")
        f.write(f"# Generated on {os.environ.get('USER', 'unknown')}@{os.environ.get('HOSTNAME', 'localhost')}\n\n")

        for key, value in sorted(variables.items()):
            # Quote values with spaces or special characters
            if ' ' in value or '\t' in value or '"' in value:
                value = f'"{value}"'
            f.write(f"{key}={value}\n")


def get_path_directories():
    """
    Get all directories in PATH environment variable.

    Returns:
        list: List of directories in PATH
    """
    path_var = os.environ.get('PATH', '')
    if os.name == 'nt':  # Windows
        directories = path_var.split(';')
    else:  # Unix-like
        directories = path_var.split(':')

    # Filter out empty strings and expand user directory
    directories = [os.path.expanduser(d) for d in directories if d.strip()]
    return directories


def find_executable_in_path(executable_name):
    """
    Find an executable in PATH directories.

    Args:
        executable_name (str): Name of executable to find

    Returns:
        str or None: Full path to executable, or None if not found
    """
    if os.name == 'nt' and not executable_name.endswith('.exe'):
        executable_name += '.exe'

    for directory in get_path_directories():
        executable_path = os.path.join(directory, executable_name)
        if os.path.isfile(executable_path) and os.access(executable_path, os.X_OK):
            return executable_path

    return None


def validate_environment():
    """
    Validate common environment variables and system setup.

    Returns:
        dict: Dictionary with validation results
    """
    results = {
        'python_version': os.environ.get('PYTHON_VERSION', 'Not set'),
        'python_path': os.environ.get('PYTHONPATH', 'Not set'),
        'home_directory': os.environ.get('HOME', os.environ.get('USERPROFILE', 'Not set')),
        'temp_directory': os.environ.get('TMP', os.environ.get('TEMP', 'Not set')),
        'path_valid': False,
        'python_executable': None,
        'warnings': []
    }

    # Check PATH validity
    path_dirs = get_path_directories()
    valid_dirs = [d for d in path_dirs if os.path.isdir(d)]
    results['path_valid'] = len(valid_dirs) > 0

    if len(valid_dirs) != len(path_dirs):
        invalid_dirs = [d for d in path_dirs if not os.path.isdir(d)]
        results['warnings'].append(f"Invalid PATH directories: {invalid_dirs}")

    # Find Python executable
    python_names = ['python3', 'python', 'python.exe']
    for name in python_names:
        python_path = find_executable_in_path(name)
        if python_path:
            results['python_executable'] = python_path
            break

    # Check essential directories
    essential_vars = ['HOME', 'TMP', 'TEMP']
    for var in essential_vars:
        if var in os.environ:
            if not os.path.isdir(os.path.expanduser(os.environ[var])):
                results['warnings'].append(f"{var} directory does not exist: {os.environ[var]}")

    return results


def create_isolated_environment(base_vars=None):
    """
    Create an isolated environment with minimal variables.

    Args:
        base_vars (dict): Base variables to include

    Returns:
        dict: Isolated environment dictionary
    """
    if base_vars is None:
        base_vars = {}

    # Essential variables for basic functionality
    essential_vars = {
        'HOME': os.environ.get('HOME', os.environ.get('USERPROFILE', '/tmp')),
        'PATH': os.environ.get('PATH', '/usr/bin:/bin'),
        'TMP': os.environ.get('TMP', os.environ.get('TEMP', '/tmp')),
        'USER': os.environ.get('USER', os.environ.get('USERNAME', 'unknown')),
        'LANG': os.environ.get('LANG', 'C.UTF-8'),
    }

    # Merge with provided base variables
    isolated_env = {**essential_vars, **base_vars}
    return isolated_env


def compare_environments(env1, env2):
    """
    Compare two environment variable dictionaries.

    Args:
        env1 (dict): First environment
        env2 (dict): Second environment

    Returns:
        dict: Comparison results with added, removed, changed variables
    """
    env1_keys = set(env1.keys())
    env2_keys = set(env2.keys())

    added = env2_keys - env1_keys
    removed = env1_keys - env2_keys
    common = env1_keys & env2_keys

    changed = {}
    for key in common:
        if env1[key] != env2[key]:
            changed[key] = {'old': env1[key], 'new': env2[key]}

    return {
        'added': dict((k, env2[k]) for k in added),
        'removed': dict((k, env1[k]) for k in removed),
        'changed': changed,
        'unchanged': len(common) - len(changed)
    }


def backup_environment(filepath):
    """
    Backup current environment variables to a JSON file.

    Args:
        filepath (str): Path to save backup
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(dict(os.environ), f, indent=2, sort_keys=True)


def restore_environment(filepath):
    """
    Restore environment variables from a JSON backup.

    Args:
        filepath (str): Path to backup file
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        env_data = json.load(f)

    # Update current environment
    os.environ.clear()
    os.environ.update(env_data)


# Example usage and demonstrations
def demonstrate_environment_operations():
    """Demonstrate various environment variable operations."""

    print("=== Environment Variables Demo ===\n")

    # Initialize environment manager
    env_mgr = EnvironmentManager()

    print("1. Current Environment Info:")
    print(f"   Total variables: {len(os.environ)}")
    print(f"   Python path: {env_mgr.get('PYTHONPATH', 'Not set')}")
    print(f"   Home directory: {env_mgr.get('HOME', 'Not set')}")
    print()

    print("2. Setting Custom Variables:")
    env_mgr.set('MY_APP_CONFIG', '/etc/myapp/config.json')
    env_mgr.set('MY_APP_DEBUG', 'true')
    print(f"   MY_APP_CONFIG: {env_mgr.get('MY_APP_CONFIG')}")
    print(f"   MY_APP_DEBUG: {env_mgr.get('MY_APP_DEBUG')}")
    print()

    print("3. PATH Analysis:")
    path_dirs = get_path_directories()
    print(f"   PATH contains {len(path_dirs)} directories")
    print(f"   First few: {path_dirs[:3]}")
    print()

    print("4. Finding Executables:")
    executables = ['python', 'git', 'ls']
    for exe in executables:
        path = find_executable_in_path(exe)
        status = f"Found at: {path}" if path else "Not found"
        print(f"   {exe}: {status}")
    print()

    print("5. Environment Validation:")
    validation = validate_environment()
    print(f"   Python executable: {validation['python_executable']}")
    print(f"   PATH valid: {validation['path_valid']}")
    if validation['warnings']:
        print("   Warnings:")
        for warning in validation['warnings']:
            print(f"     - {warning}")
    print()

    print("6. Creating Isolated Environment:")
    isolated = create_isolated_environment({
        'MY_APP_CONFIG': '/app/config.json',
        'MY_APP_ENV': 'production'
    })
    print(f"   Isolated env has {len(isolated)} variables")
    print(f"   Custom vars: MY_APP_CONFIG={isolated.get('MY_APP_CONFIG')}")
    print()

    # Cleanup
    env_mgr.delete('MY_APP_CONFIG')
    env_mgr.delete('MY_APP_DEBUG')
    print("7. Cleaned up custom variables")


if __name__ == "__main__":
    demonstrate_environment_operations()
