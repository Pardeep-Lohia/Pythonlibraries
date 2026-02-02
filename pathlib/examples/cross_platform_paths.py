#!/usr/bin/env python3
"""
Cross-Platform Path Handling Example

This script demonstrates how to handle file paths in a cross-platform manner
using pathlib, ensuring code works identically on Windows, macOS, and Linux.
"""

from pathlib import Path
import os


def get_user_config_directory(app_name: str) -> Path:
    """
    Get the appropriate configuration directory for the current platform.

    Args:
        app_name: Name of the application

    Returns:
        Path to the configuration directory
    """
    if os.name == 'nt':  # Windows
        # Use APPDATA environment variable
        appdata = os.environ.get('APPDATA')
        if appdata:
            return Path(appdata) / app_name
        else:
            # Fallback to home directory
            return Path.home() / 'AppData' / 'Roaming' / app_name
    else:  # Unix-like systems (Linux, macOS)
        # Use XDG_CONFIG_HOME if set, otherwise ~/.config
        config_home = os.environ.get('XDG_CONFIG_HOME')
        if config_home:
            return Path(config_home) / app_name
        else:
            return Path.home() / '.config' / app_name


def get_user_data_directory(app_name: str) -> Path:
    """
    Get the appropriate data directory for the current platform.

    Args:
        app_name: Name of the application

    Returns:
        Path to the data directory
    """
    if os.name == 'nt':  # Windows
        # Use LOCALAPPDATA for user-specific data
        local_appdata = os.environ.get('LOCALAPPDATA')
        if local_appdata:
            return Path(local_appdata) / app_name
        else:
            return Path.home() / 'AppData' / 'Local' / app_name
    else:  # Unix-like systems
        # Use XDG_DATA_HOME if set, otherwise ~/.local/share
        data_home = os.environ.get('XDG_DATA_HOME')
        if data_home:
            return Path(data_home) / app_name
        else:
            return Path.home() / '.local' / 'share' / app_name


def get_user_cache_directory(app_name: str) -> Path:
    """
    Get the appropriate cache directory for the current platform.

    Args:
        app_name: Name of the application

    Returns:
        Path to the cache directory
    """
    if os.name == 'nt':  # Windows
        # Use LOCALAPPDATA for cache
        local_appdata = os.environ.get('LOCALAPPDATA')
        if local_appdata:
            return Path(local_appdata) / app_name / 'Cache'
        else:
            return Path.home() / 'AppData' / 'Local' / app_name / 'Cache'
    else:  # Unix-like systems
        # Use XDG_CACHE_HOME if set, otherwise ~/.cache
        cache_home = os.environ.get('XDG_CACHE_HOME')
        if cache_home:
            return Path(cache_home) / app_name
        else:
            return Path.home() / '.cache' / app_name


def get_desktop_directory() -> Path:
    """
    Get the user's desktop directory in a cross-platform way.

    Returns:
        Path to the desktop directory
    """
    if os.name == 'nt':  # Windows
        # Windows doesn't have a standard environment variable for desktop
        # Use home directory as fallback
        return Path.home() / 'Desktop'
    else:  # Unix-like systems
        # Try XDG_DESKTOP_DIR first
        desktop_dir = os.environ.get('XDG_DESKTOP_DIR')
        if desktop_dir:
            return Path(desktop_dir)
        else:
            # Fallback to ~/Desktop
            return Path.home() / 'Desktop'


def get_documents_directory() -> Path:
    """
    Get the user's documents directory in a cross-platform way.

    Returns:
        Path to the documents directory
    """
    if os.name == 'nt':  # Windows
        # Windows doesn't have a standard environment variable for documents
        # Use home directory as fallback
        return Path.home() / 'Documents'
    else:  # Unix-like systems
        # Try XDG_DOCUMENTS_DIR first
        documents_dir = os.environ.get('XDG_DOCUMENTS_DIR')
        if documents_dir:
            return Path(documents_dir)
        else:
            # Fallback to ~/Documents
            return Path.home() / 'Documents'


def create_cross_platform_paths():
    """
    Demonstrate creating various cross-platform paths.
    """
    app_name = 'MyCrossPlatformApp'

    print("Cross-Platform Path Creation Example")
    print("=" * 40)

    # Get platform-specific directories
    config_dir = get_user_config_directory(app_name)
    data_dir = get_user_data_directory(app_name)
    cache_dir = get_user_cache_directory(app_name)
    desktop_dir = get_desktop_directory()
    documents_dir = get_documents_directory()

    print(f"Configuration directory: {config_dir}")
    print(f"Data directory: {data_dir}")
    print(f"Cache directory: {cache_dir}")
    print(f"Desktop directory: {desktop_dir}")
    print(f"Documents directory: {documents_dir}")

    # Create application-specific paths
    config_file = config_dir / 'settings.json'
    data_file = data_dir / 'user_data.db'
    cache_file = cache_dir / 'temp_cache.dat'
    desktop_shortcut = desktop_dir / f'{app_name}.lnk' if os.name == 'nt' else desktop_dir / app_name.lower()
    document_file = documents_dir / 'app_report.pdf'

    print(f"\nApplication paths:")
    print(f"Config file: {config_file}")
    print(f"Data file: {data_file}")
    print(f"Cache file: {cache_file}")
    print(f"Desktop shortcut: {desktop_shortcut}")
    print(f"Document file: {document_file}")

    return {
        'config_dir': config_dir,
        'data_dir': data_dir,
        'cache_dir': cache_dir,
        'desktop_dir': desktop_dir,
        'documents_dir': documents_dir,
        'config_file': config_file,
        'data_file': data_file,
        'cache_file': cache_file,
        'desktop_shortcut': desktop_shortcut,
        'document_file': document_file
    }


def demonstrate_path_operations(paths_dict):
    """
    Demonstrate various path operations that work cross-platform.

    Args:
        paths_dict: Dictionary of paths from create_cross_platform_paths()
    """
    print("\nPath Operations Demonstration")
    print("=" * 30)

    config_file = paths_dict['config_file']

    # Path components work the same on all platforms
    print(f"Config file: {config_file}")
    print(f"Name: {config_file.name}")
    print(f"Stem: {config_file.stem}")
    print(f"Suffix: {config_file.suffix}")
    print(f"Parent: {config_file.parent}")

    # Path joining works the same
    backup_file = config_file.with_suffix('.bak')
    print(f"Backup file: {backup_file}")

    # Relative paths work the same
    config_dir = paths_dict['config_dir']
    relative_path = config_file.relative_to(config_dir)
    print(f"Relative path: {relative_path}")

    # Path existence checks work the same
    print(f"Config file exists: {config_file.exists()}")
    print(f"Config dir exists: {config_dir.exists()}")


def create_directory_structure():
    """
    Create a cross-platform directory structure for the application.
    """
    print("\nDirectory Structure Creation")
    print("=" * 30)

    app_name = 'MyCrossPlatformApp'
    paths = create_cross_platform_paths()

    # Create all necessary directories
    directories_to_create = [
        paths['config_dir'],
        paths['data_dir'],
        paths['cache_dir']
    ]

    for directory in directories_to_create:
        try:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {directory}")
        except Exception as e:
            print(f"Failed to create {directory}: {e}")

    # Create some example files
    try:
        # Config file
        config_content = '''{
    "app_name": "MyCrossPlatformApp",
    "version": "1.0.0",
    "settings": {
        "theme": "dark",
        "language": "en"
    }
}'''
        paths['config_file'].write_text(config_content, encoding='utf-8')
        print(f"Created config file: {paths['config_file']}")

        # Data file (simple text for demo)
        data_content = "User data placeholder\n"
        paths['data_file'].write_text(data_content, encoding='utf-8')
        print(f"Created data file: {paths['data_file']}")

        # Cache file
        cache_content = "Temporary cache data\n"
        paths['cache_file'].write_text(cache_content, encoding='utf-8')
        print(f"Created cache file: {paths['cache_file']}")

        # Document file
        doc_content = "Sample report content\n"
        paths['document_file'].write_text(doc_content, encoding='utf-8')
        print(f"Created document file: {paths['document_file']}")

    except Exception as e:
        print(f"Failed to create files: {e}")


def demonstrate_file_operations():
    """
    Demonstrate file operations that work cross-platform.
    """
    print("\nFile Operations Demonstration")
    print("=" * 30)

    app_name = 'MyCrossPlatformApp'
    paths = create_cross_platform_paths()

    # Read config file
    try:
        if paths['config_file'].exists():
            content = paths['config_file'].read_text(encoding='utf-8')
            print(f"Config file content length: {len(content)} characters")

            # Parse JSON (simple demo)
            if '{' in content:
                print("Config file appears to be JSON")
    except Exception as e:
        print(f"Failed to read config file: {e}")

    # List files in directories
    for dir_name, dir_path in [('Config', paths['config_dir']),
                               ('Data', paths['data_dir']),
                               ('Cache', paths['cache_dir'])]:
        try:
            if dir_path.exists():
                files = list(dir_path.iterdir())
                print(f"{dir_name} directory contains {len(files)} items:")
                for item in files:
                    item_type = "File" if item.is_file() else "Directory"
                    print(f"  {item_type}: {item.name}")
        except Exception as e:
            print(f"Failed to list {dir_name} directory: {e}")


def cleanup_example():
    """
    Clean up the example files and directories.
    """
    print("\nCleanup")
    print("=" * 10)

    app_name = 'MyCrossPlatformApp'
    paths = create_cross_platform_paths()

    # Remove files
    files_to_remove = [
        paths['config_file'],
        paths['data_file'],
        paths['cache_file'],
        paths['document_file']
    ]

    for file_path in files_to_remove:
        try:
            if file_path.exists():
                file_path.unlink()
                print(f"Removed file: {file_path}")
        except Exception as e:
            print(f"Failed to remove {file_path}: {e}")

    # Remove directories (only if empty)
    dirs_to_remove = [
        paths['cache_dir'],
        paths['data_dir'],
        paths['config_dir']
    ]

    for dir_path in dirs_to_remove:
        try:
            if dir_path.exists() and not list(dir_path.iterdir()):
                dir_path.rmdir()
                print(f"Removed empty directory: {dir_path}")
        except Exception as e:
            print(f"Failed to remove {dir_path}: {e}")


def main():
    """
    Main function demonstrating cross-platform path handling.
    """
    print("Cross-Platform Path Handling with pathlib")
    print("This example works identically on Windows, macOS, and Linux")
    print()

    try:
        # Create and demonstrate paths
        paths = create_cross_platform_paths()
        demonstrate_path_operations(paths)

        # Create directory structure and files
        create_directory_structure()

        # Demonstrate file operations
        demonstrate_file_operations()

        # Clean up
        cleanup_example()

        print("\nCross-platform path handling demonstration completed!")

    except Exception as e:
        print(f"Error during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
