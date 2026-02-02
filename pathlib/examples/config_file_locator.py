#!/usr/bin/env python3
"""
Configuration File Locator Example

This script demonstrates how to locate configuration files in various
standard locations using pathlib, with cross-platform compatibility.
"""

from pathlib import Path
import os
from typing import List, Optional


class ConfigLocator:
    """
    A class for locating configuration files in standard locations.
    """

    def __init__(self, app_name: str):
        """
        Initialize the config locator.

        Args:
            app_name: Name of the application
        """
        self.app_name = app_name

    def get_config_directories(self) -> List[Path]:
        """
        Get all standard configuration directories for the current platform.

        Returns:
            List of configuration directories in priority order
        """
        config_dirs = []

        if os.name == 'nt':  # Windows
            # Windows-specific locations
            appdata = os.environ.get('APPDATA')
            local_appdata = os.environ.get('LOCALAPPDATA')

            if appdata:
                config_dirs.append(Path(appdata) / self.app_name)
            if local_appdata:
                config_dirs.append(Path(local_appdata) / self.app_name)

            # Fallback to home directory
            config_dirs.append(Path.home() / 'AppData' / 'Roaming' / self.app_name)

        else:  # Unix-like systems (Linux, macOS)
            # XDG Base Directory specification
            xdg_config_home = os.environ.get('XDG_CONFIG_HOME')
            if xdg_config_home:
                config_dirs.append(Path(xdg_config_home) / self.app_name)
            else:
                config_dirs.append(Path.home() / '.config' / self.app_name)

            # Additional common locations
            config_dirs.extend([
                Path.home() / f'.{self.app_name}',  # Hidden directory
                Path('/etc') / self.app_name,       # System-wide
                Path('/usr/local/etc') / self.app_name,  # Local system
            ])

        return config_dirs

    def get_config_files(self, filename: str = 'config.ini') -> List[Path]:
        """
        Get all possible configuration file paths.

        Args:
            filename: Name of the configuration file

        Returns:
            List of possible configuration file paths
        """
        config_files = []
        config_dirs = self.get_config_directories()

        for config_dir in config_dirs:
            config_files.append(config_dir / filename)

        # Also check current directory and script directory
        config_files.extend([
            Path.cwd() / filename,
            Path(__file__).parent / filename,
        ])

        return config_files

    def find_config_file(self, filename: str = 'config.ini') -> Optional[Path]:
        """
        Find the first existing configuration file.

        Args:
            filename: Name of the configuration file

        Returns:
            Path to the first existing configuration file, or None if not found
        """
        config_files = self.get_config_files(filename)

        for config_file in config_files:
            if config_file.exists() and config_file.is_file():
                return config_file

        return None

    def ensure_config_directory(self) -> Path:
        """
        Ensure the primary configuration directory exists.

        Returns:
            Path to the primary configuration directory
        """
        config_dirs = self.get_config_directories()
        primary_config_dir = config_dirs[0]

        primary_config_dir.mkdir(parents=True, exist_ok=True)
        return primary_config_dir

    def create_default_config(self, filename: str = 'config.ini',
                            content: str = None) -> Path:
        """
        Create a default configuration file if it doesn't exist.

        Args:
            filename: Name of the configuration file
            content: Default content for the configuration file

        Returns:
            Path to the configuration file
        """
        config_dir = self.ensure_config_directory()
        config_file = config_dir / filename

        if not config_file.exists():
            if content is None:
                content = f"""# {self.app_name} Configuration File
# This file was auto-generated

[settings]
app_name = {self.app_name}
version = 1.0.0

# Add your configuration options here
"""

            config_file.write_text(content, encoding='utf-8')
            print(f"Created default config file: {config_file}")

        return config_file


def demonstrate_config_location():
    """
    Demonstrate configuration file location.
    """
    print("Configuration File Location Demonstration")
    print("=" * 45)

    app_name = 'MyApp'
    locator = ConfigLocator(app_name)

    # Show all possible config directories
    print(f"\nConfiguration directories for {app_name}:")
    config_dirs = locator.get_config_directories()
    for i, config_dir in enumerate(config_dirs, 1):
        exists = "✓" if config_dir.exists() else "✗"
        print(f"{i}. {exists} {config_dir}")

    # Show all possible config files
    print(f"\nPossible configuration files:")
    config_files = locator.get_config_files('settings.ini')
    for i, config_file in enumerate(config_files, 1):
        exists = "✓" if config_file.exists() else "✗"
        print(f"{i}. {exists} {config_file}")

    # Create a default config file
    print(f"\nCreating default configuration:")
    config_file = locator.create_default_config('settings.ini')

    # Now find the config file
    found_config = locator.find_config_file('settings.ini')
    if found_config:
        print(f"Found configuration file: {found_config}")
        print("Content:")
        print(found_config.read_text())
    else:
        print("No configuration file found")


def demonstrate_multi_format_configs():
    """
    Demonstrate locating configuration files in different formats.
    """
    print("\nMulti-Format Configuration Demonstration")
    print("=" * 40)

    locator = ConfigLocator('MyApp')

    # Different configuration file formats
    formats = ['config.ini', 'config.json', 'config.yaml', 'config.toml']

    for fmt in formats:
        config_file = locator.find_config_file(fmt)
        if config_file:
            print(f"Found {fmt}: {config_file}")
        else:
            print(f"{fmt}: Not found")

    # Create example files in different formats
    config_dir = locator.ensure_config_directory()

    # JSON config
    json_config = config_dir / 'config.json'
    if not json_config.exists():
        json_content = '''{
    "app": {
        "name": "MyApp",
        "version": "1.0.0"
    },
    "database": {
        "host": "localhost",
        "port": 5432
    }
}'''
        json_config.write_text(json_content, encoding='utf-8')
        print(f"Created JSON config: {json_config}")

    # YAML config
    yaml_config = config_dir / 'config.yaml'
    if not yaml_config.exists():
        yaml_content = '''app:
  name: MyApp
  version: 1.0.0

database:
  host: localhost
  port: 5432
'''
        yaml_config.write_text(yaml_content, encoding='utf-8')
        print(f"Created YAML config: {yaml_config}")


def demonstrate_config_hierarchy():
    """
    Demonstrate configuration file hierarchy and precedence.
    """
    print("\nConfiguration Hierarchy Demonstration")
    print("=" * 38)

    locator = ConfigLocator('MyApp')

    # Create config files in different locations
    config_files = locator.get_config_files('hierarchy.ini')

    # Create system-wide config
    if len(config_files) > 2:  # Has system locations
        system_config = config_files[-3]  # /etc/myapp/hierarchy.ini
        system_config.parent.mkdir(parents=True, exist_ok=True)
        system_config.write_text('[system]\nlevel = system\n', encoding='utf-8')
        print(f"Created system config: {system_config}")

    # Create user config
    user_config = config_files[0]  # Primary user config
    user_config.parent.mkdir(parents=True, exist_ok=True)
    user_config.write_text('[user]\nlevel = user\npreference = dark\n', encoding='utf-8')
    print(f"Created user config: {user_config}")

    # Create local config
    local_config = config_files[-1]  # Current directory
    local_config.write_text('[local]\nlevel = local\ndebug = true\n', encoding='utf-8')
    print(f"Created local config: {local_config}")

    # Show hierarchy
    print("\nConfiguration hierarchy (highest to lowest precedence):")
    for i, config_file in enumerate(config_files, 1):
        if config_file.exists():
            print(f"{i}. ✓ {config_file}")
        else:
            print(f"{i}. ✗ {config_file}")


def demonstrate_config_loading():
    """
    Demonstrate loading configuration with precedence.
    """
    print("\nConfiguration Loading with Precedence")
    print("=" * 40)

    import configparser

    locator = ConfigLocator('MyApp')

    # Simple config merger
    def load_config_with_precedence(filename: str) -> configparser.ConfigParser:
        """
        Load configuration files with precedence (later files override earlier ones).
        """
        config = configparser.ConfigParser()
        config_files = locator.get_config_files(filename)

        # Load in reverse order (system first, then user, then local)
        loaded_files = []
        for config_file in reversed(config_files):
            if config_file.exists():
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        config.read_file(f)
                    loaded_files.append(config_file)
                except Exception as e:
                    print(f"Error loading {config_file}: {e}")

        print(f"Loaded {len(loaded_files)} config files: {[str(f) for f in loaded_files]}")
        return config

    # Create test configs
    config_dir = locator.ensure_config_directory()

    # Base config
    base_config = config_dir / 'merged.ini'
    base_config.write_text('''[app]
name = MyApp
version = 1.0.0

[ui]
theme = light
''', encoding='utf-8')

    # Override config in current directory
    override_config = Path('merged.ini')
    override_config.write_text('''[ui]
theme = dark

[debug]
enabled = true
''', encoding='utf-8')

    # Load with precedence
    config = load_config_with_precedence('merged.ini')

    print("\nFinal merged configuration:")
    for section in config.sections():
        print(f"[{section}]")
        for key, value in config.items(section):
            print(f"  {key} = {value}")

    # Clean up
    override_config.unlink()
    base_config.unlink()


def cleanup_demo():
    """
    Clean up demonstration files.
    """
    print("\nCleaning up demonstration files...")
    locator = ConfigLocator('MyApp')

    # Remove created config files
    config_files = [
        'settings.ini',
        'config.json',
        'config.yaml',
        'hierarchy.ini',
        'merged.ini'
    ]

    for filename in config_files:
        config_file = locator.find_config_file(filename)
        if config_file:
            config_file.unlink()
            print(f"Removed: {config_file}")

    # Try to remove system config (may not have permission)
    try:
        system_config = Path('/etc/MyApp/hierarchy.ini')
        if system_config.exists():
            system_config.unlink()
            print(f"Removed system config: {system_config}")
    except PermissionError:
        print("Could not remove system config (permission denied)")


def main():
    """
    Main demonstration function.
    """
    print("Pathlib Configuration File Locator")
    print("This example shows cross-platform config file handling")
    print()

    try:
        demonstrate_config_location()
        demonstrate_multi_format_configs()
        demonstrate_config_hierarchy()
        demonstrate_config_loading()
        cleanup_demo()

        print("\nConfiguration file locator demonstration completed!")

    except Exception as e:
        print(f"Error during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
