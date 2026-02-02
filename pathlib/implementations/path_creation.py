#!/usr/bin/env python3
"""
Path Creation Examples with pathlib

This module demonstrates various ways to create and manipulate Path objects
in the pathlib library, showcasing path construction, joining, and conversion.
"""

from pathlib import Path, PurePath
import os


def basic_path_creation():
    """Demonstrate basic path creation methods."""
    print("=== Basic Path Creation ===")

    # From string
    path1 = Path('/home/user/documents/file.txt')
    print(f"From string: {path1}")

    # From multiple components
    path2 = Path('home', 'user', 'documents', 'file.txt')
    print(f"From components: {path2}")

    # From another Path object
    path3 = Path(path1)
    print(f"From Path object: {path3}")

    # Current directory
    current = Path.cwd()
    print(f"Current directory: {current}")

    # Home directory
    home = Path.home()
    print(f"Home directory: {home}")

    return path1, path2, path3, current, home


def path_joining_operations():
    """Demonstrate different ways to join paths."""
    print("\n=== Path Joining Operations ===")

    base = Path('/home/user')

    # Using / operator (recommended)
    docs = base / 'Documents'
    file_path = docs / 'report.pdf'
    print(f"Using / operator: {file_path}")

    # Using joinpath() method
    file_path2 = base.joinpath('Documents', 'report.pdf')
    print(f"Using joinpath(): {file_path2}")

    # Verify they're the same
    print(f"Paths are equal: {file_path == file_path2}")

    # Multiple components
    deep_path = base / 'projects' / 'myapp' / 'src' / 'main.py'
    print(f"Deep path: {deep_path}")

    return file_path, deep_path


def path_from_different_sources():
    """Create paths from various sources."""
    print("\n=== Paths from Different Sources ===")

    # From environment variable
    temp_dir = Path(os.environ.get('TEMP', '/tmp'))
    print(f"From environment: {temp_dir}")

    # From current script location
    script_dir = Path(__file__).parent
    print(f"Script directory: {script_dir}")

    # Relative paths
    relative = Path('../config/settings.ini')
    print(f"Relative path: {relative}")

    # Absolute path from relative
    absolute = relative.resolve()
    print(f"Resolved absolute: {absolute}")

    return temp_dir, script_dir, relative, absolute


def cross_platform_path_handling():
    """Demonstrate cross-platform path creation."""
    print("\n=== Cross-Platform Path Handling ===")

    # pathlib handles separators automatically
    unix_style = Path('home/user/file.txt')
    print(f"Unix-style input: {unix_style}")

    # On Windows, this would be converted internally
    # but displayed with backslashes if needed
    print(f"String representation: {str(unix_style)}")

    # Explicit Windows path (works on all platforms)
    windows_path = Path('C:/Users/user/file.txt')
    print(f"Windows-style path: {windows_path}")

    # Platform-specific path creation
    if os.name == 'nt':  # Windows
        system_path = Path('C:\\Program Files\\App\\config.ini')
    else:  # Unix-like
        system_path = Path('/etc/app/config.ini')
    print(f"System-specific path: {system_path}")

    return unix_style, windows_path, system_path


def path_transformation_examples():
    """Show how to transform and modify paths."""
    print("\n=== Path Transformations ===")

    original = Path('/home/user/documents/report.pdf')

    # Get different parts
    print(f"Original: {original}")
    print(f"Name: {original.name}")
    print(f"Stem: {original.stem}")
    print(f"Suffix: {original.suffix}")
    print(f"Parent: {original.parent}")

    # Modify components
    renamed = original.with_name('presentation.pdf')
    print(f"Renamed: {renamed}")

    backup = original.with_suffix('.bak')
    print(f"Backup: {backup}")

    # Create related paths
    txt_version = original.with_suffix('.txt')
    print(f"Text version: {txt_version}")

    return original, renamed, backup, txt_version


def pure_vs_concrete_paths():
    """Compare pure and concrete path creation."""
    print("\n=== Pure vs Concrete Paths ===")

    # Pure paths (no filesystem interaction)
    pure_path = PurePath('/home/user/file.txt')
    print(f"Pure path: {pure_path}")
    print(f"Pure path type: {type(pure_path)}")

    # Concrete paths (can interact with filesystem)
    concrete_path = Path('/home/user/file.txt')
    print(f"Concrete path: {concrete_path}")
    print(f"Concrete path type: {type(concrete_path)}")

    # Pure paths are useful for path manipulation without filesystem access
    # Concrete paths inherit from pure paths and add filesystem methods

    return pure_path, concrete_path


def advanced_path_construction():
    """Advanced path construction techniques."""
    print("\n=== Advanced Path Construction ===")

    # Building paths dynamically
    def build_config_path(app_name: str, config_file: str = 'settings.ini') -> Path:
        """Build a standard config file path."""
        return Path.home() / '.config' / app_name / config_file

    config_path = build_config_path('myapp')
    print(f"Config path: {config_path}")

    # Path from URL-like string (manual parsing)
    def path_from_url(url_path: str) -> Path:
        """Convert URL path to filesystem path."""
        # Remove leading slash and split
        parts = url_path.lstrip('/').split('/')
        return Path(*parts)

    url_path = path_from_url('/api/v1/users/123')
    print(f"Path from URL: {url_path}")

    # Creating temporary paths
    import tempfile
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir) / 'temp_file.txt'
        print(f"Temporary path: {temp_path}")

    return config_path, url_path


def path_validation_and_sanitization():
    """Demonstrate path validation and sanitization."""
    print("\n=== Path Validation and Sanitization ===")

    def sanitize_filename(filename: str) -> str:
        """Sanitize filename by removing invalid characters."""
        import string
        valid_chars = f"-_.() {string.ascii_letters}{string.digits}"
        return ''.join(c for c in filename if c in valid_chars)

    def create_safe_path(base_dir: Path, filename: str) -> Path:
        """Create a safe path within base directory."""
        safe_name = sanitize_filename(filename)
        if not safe_name:
            safe_name = 'unnamed_file'
        return base_dir / safe_name

    base = Path('/tmp/safe')
    unsafe_names = ['file<>with?bad*chars.txt', '', 'normal_file.txt']

    for name in unsafe_names:
        safe_path = create_safe_path(base, name)
        print(f"'{name}' -> {safe_path.name}")

    return base


def main():
    """Run all path creation examples."""
    print("Pathlib Path Creation Examples")
    print("=" * 40)

    # Run all demonstrations
    basic_path_creation()
    path_joining_operations()
    path_from_different_sources()
    cross_platform_path_handling()
    path_transformation_examples()
    pure_vs_concrete_paths()
    advanced_path_construction()
    path_validation_and_sanitization()

    print("\n=== Summary ===")
    print("pathlib provides flexible and intuitive path creation:")
    print("- Path() constructor from strings or components")
    print("- / operator for joining paths")
    print("- Special constructors like Path.home() and Path.cwd()")
    print("- Automatic cross-platform handling")
    print("- Pure paths for manipulation, concrete paths for filesystem access")


if __name__ == '__main__':
    main()
