#!/usr/bin/env python3
"""
Path Navigation with pathlib

This module demonstrates path navigation operations using pathlib.Path objects.
All examples are runnable Python 3 code.
"""

from pathlib import Path
import os


def demonstrate_path_creation():
    """Demonstrate different ways to create Path objects."""
    print("=== Path Creation Examples ===")

    # From string
    path1 = Path('/home/user/file.txt')
    print(f"From string: {path1}")

    # From multiple components
    path2 = Path('home', 'user', 'file.txt')
    print(f"From components: {path2}")

    # From another Path
    path3 = Path(path1)
    print(f"From another Path: {path3}")

    # Special constructors
    home = Path.home()
    print(f"Home directory: {home}")

    cwd = Path.cwd()
    print(f"Current working directory: {cwd}")

    # Current script directory
    script_dir = Path(__file__).parent
    print(f"Script directory: {script_dir}")


def demonstrate_path_joining():
    """Demonstrate path joining operations."""
    print("\n=== Path Joining Examples ===")

    base = Path('/home/user')

    # Using / operator (recommended)
    documents = base / 'Documents'
    file_path = documents / 'report.pdf'
    print(f"Using / operator: {file_path}")

    # Using joinpath() method
    file_path2 = base.joinpath('Documents', 'report.pdf')
    print(f"Using joinpath(): {file_path2}")

    # Both approaches are equivalent
    assert file_path == file_path2

    # Joining multiple components
    complex_path = Path('/home') / 'user' / 'documents' / 'work' / 'report.pdf'
    print(f"Complex path: {complex_path}")

    # Joining with variables
    username = 'john_doe'
    user_path = Path('/home') / username / 'documents'
    print(f"Dynamic path: {user_path}")


def demonstrate_path_components():
    """Demonstrate accessing path components."""
    print("\n=== Path Components Examples ===")

    path = Path('/home/user/documents/report.pdf')

    print(f"Full path: {path}")
    print(f"Name: {path.name}")           # 'report.pdf'
    print(f"Stem: {path.stem}")           # 'report'
    print(f"Suffix: {path.suffix}")       # '.pdf'
    print(f"Suffixes: {path.suffixes}")   # ['.pdf']
    print(f"Parent: {path.parent}")       # PosixPath('/home/user/documents')
    print(f"Parts: {path.parts}")         # ('/', 'home', 'user', 'documents', 'report.pdf')

    # Multi-level parent access
    print(f"Grandparent: {path.parent.parent}")  # PosixPath('/home/user')

    # Path with multiple extensions
    multi_ext = Path('archive.tar.gz')
    print(f"Multi-ext name: {multi_ext.name}")      # 'archive.tar.gz'
    print(f"Multi-ext stem: {multi_ext.stem}")      # 'archive.tar'
    print(f"Multi-ext suffix: {multi_ext.suffix}")  # '.gz'
    print(f"Multi-ext suffixes: {multi_ext.suffixes}")  # ['.tar', '.gz']


def demonstrate_path_manipulation():
    """Demonstrate path manipulation operations."""
    print("\n=== Path Manipulation Examples ===")

    original = Path('/home/user/file.txt')

    # Change name
    renamed = original.with_name('new_file.txt')
    print(f"With new name: {renamed}")

    # Change suffix
    backup = original.with_suffix('.bak')
    print(f"With backup suffix: {backup}")

    # Change to different suffix
    pdf_version = original.with_suffix('.pdf')
    print(f"With PDF suffix: {pdf_version}")

    # Remove suffix
    no_suffix = original.with_suffix('')
    print(f"Without suffix: {no_suffix}")

    # Multiple suffix changes
    tar_gz = Path('file.txt')
    archived = tar_gz.with_suffix('.tar.gz')
    print(f"Archived: {archived}")


def demonstrate_path_resolution():
    """Demonstrate path resolution operations."""
    print("\n=== Path Resolution Examples ===")

    # Resolve relative paths
    relative = Path('../config/settings.ini')
    absolute = relative.resolve()
    print(f"Resolved relative: {absolute}")

    # Resolve symlinks (if they exist)
    symlink_path = Path('link.txt')
    if symlink_path.exists():
        real_path = symlink_path.resolve()
        print(f"Resolved symlink: {real_path}")

    # Get absolute path
    rel_path = Path('file.txt')
    abs_path = rel_path.resolve()
    print(f"Absolute path: {abs_path}")

    # Resolve current directory
    current = Path('.')
    resolved_current = current.resolve()
    print(f"Resolved current: {resolved_current}")


def demonstrate_relative_paths():
    """Demonstrate relative path operations."""
    print("\n=== Relative Path Examples ===")

    base = Path('/home/user/projects/myapp')
    full = Path('/home/user/projects/myapp/src/main.py')

    # Get relative path
    relative = full.relative_to(base)
    print(f"Relative to base: {relative}")

    # Check if path is relative to another
    print(f"Is relative: {full.is_relative_to(base)}")

    # Multiple levels
    deeper = Path('/home/user/projects/myapp/src/utils/helpers.py')
    rel_deeper = deeper.relative_to(base)
    print(f"Deeper relative: {rel_deeper}")

    # Partial relative check
    partial_base = Path('/home/user')
    print(f"Is relative to partial: {full.is_relative_to(partial_base)}")


def demonstrate_path_type_checks():
    """Demonstrate path type checking operations."""
    print("\n=== Path Type Checks Examples ===")

    # Create test files and directories
    test_file = Path('test_file.txt')
    test_dir = Path('test_dir')

    test_file.write_text('test content')
    test_dir.mkdir()

    # Type checks
    print(f"Is absolute: {test_file.is_absolute()}")
    print(f"Is relative: {not test_file.is_absolute()}")

    print(f"File exists: {test_file.exists()}")
    print(f"Is file: {test_file.is_file()}")
    print(f"Is directory: {test_dir.is_dir()}")

    # Check if symlink (create one if possible)
    try:
        symlink = Path('test_link.txt')
        symlink.symlink_to(test_file)
        print(f"Is symlink: {symlink.is_symlink()}")
        symlink.unlink()  # Clean up
    except OSError:
        print("Symlink creation not supported or failed")

    # Clean up
    test_file.unlink()
    test_dir.rmdir()


def demonstrate_path_comparison():
    """Demonstrate path comparison operations."""
    print("\n=== Path Comparison Examples ===")

    path1 = Path('/home/user/file.txt')
    path2 = Path('/home/user/file.txt')
    path3 = Path('/home/user/other.txt')

    print(f"path1 == path2: {path1 == path2}")
    print(f"path1 == path3: {path1 == path3}")

    # Lexicographical comparison
    print(f"path1 < path3: {path1 < path3}")

    # Sorting paths
    paths = [Path('c.txt'), Path('a.txt'), Path('b.txt')]
    paths.sort()
    print(f"Sorted paths: {paths}")

    # Case sensitivity (platform dependent)
    upper_path = Path('FILE.TXT')
    lower_path = Path('file.txt')
    print(f"Case comparison: {upper_path == lower_path}")


def demonstrate_path_arithmetic():
    """Demonstrate path arithmetic operations."""
    print("\n=== Path Arithmetic Examples ===")

    # Basic joining
    path = Path('/home') / 'user' / 'file.txt'
    print(f"Joined path: {path}")

    # Building paths incrementally
    base = Path('/tmp')
    for component in ['project', 'src', 'main.py']:
        base = base / component
    print(f"Built path: {base}")

    # Path concatenation with strings
    root = Path('/')
    home_path = root / 'home' / 'user'
    print(f"Home path: {home_path}")

    # Combining relative and absolute
    relative = Path('documents') / 'file.txt'
    absolute_base = Path('/home/user')
    full_path = absolute_base / relative
    print(f"Combined path: {full_path}")


def demonstrate_navigation_patterns():
    """Demonstrate common navigation patterns."""
    print("\n=== Navigation Patterns Examples ===")

    # Navigate to parent directories
    current = Path('/home/user/documents/work/report.pdf')
    print(f"Current: {current}")
    print(f"Parent: {current.parent}")
    print(f"Grandparent: {current.parent.parent}")

    # Navigate to sibling files
    base_file = Path('/home/user/documents/file.txt')
    sibling_pdf = base_file.with_suffix('.pdf')
    sibling_backup = base_file.with_name(f"{base_file.stem}_backup{base_file.suffix}")
    print(f"Original: {base_file}")
    print(f"PDF version: {sibling_pdf}")
    print(f"Backup: {sibling_backup}")

    # Navigate to related directories
    file_path = Path('/home/user/projects/myapp/src/main.py')
    project_root = file_path.parent.parent.parent
    tests_dir = project_root / 'tests'
    docs_dir = project_root / 'docs'
    print(f"Project root: {project_root}")
    print(f"Tests dir: {tests_dir}")
    print(f"Docs dir: {docs_dir}")

    # Cross-platform navigation
    config_dir = Path.home() / '.config' / 'myapp'
    data_dir = config_dir / 'data'
    logs_dir = config_dir / 'logs'
    print(f"Config dir: {config_dir}")
    print(f"Data dir: {data_dir}")
    print(f"Logs dir: {logs_dir}")


def demonstrate_error_handling():
    """Demonstrate error handling in path navigation."""
    print("\n=== Error Handling Examples ===")

    # Safe path operations
    def safe_resolve(path: Path) -> Path:
        try:
            return path.resolve()
        except (OSError, RuntimeError) as e:
            print(f"Could not resolve {path}: {e}")
            return path

    def safe_relative_to(child: Path, parent: Path) -> Path:
        try:
            return child.relative_to(parent)
        except ValueError as e:
            print(f"Could not make {child} relative to {parent}: {e}")
            return child

    # Test error handling
    invalid_relative = Path('/tmp/file.txt')
    base_path = Path('/home/user')

    safe_resolve(Path('/nonexistent/path'))
    safe_relative_to(invalid_relative, base_path)


def demonstrate_platform_considerations():
    """Demonstrate platform-specific path navigation."""
    print("\n=== Platform Considerations Examples ===")

    # Cross-platform path building
    def get_config_path(app_name: str) -> Path:
        """Get platform-appropriate config directory."""
        if os.name == 'nt':  # Windows
            config_dir = Path(os.environ.get('APPDATA', '')) / app_name
        else:  # Unix-like
            config_dir = Path.home() / '.config' / app_name
        return config_dir

    config_path = get_config_path('myapp')
    print(f"Config path: {config_path}")

    # Platform-specific path separators in strings (avoid)
    bad_path = os.path.join('folder', 'subfolder', 'file.txt')
    good_path = Path('folder') / 'subfolder' / 'file.txt'
    print(f"Avoid os.path.join: {bad_path}")
    print(f"Use pathlib: {good_path}")

    # Handling drive letters (Windows)
    if os.name == 'nt':
        windows_path = Path('C:/Windows/System32')
        print(f"Windows path: {windows_path}")
        print(f"Drive: {windows_path.drive}")
    else:
        print("Not on Windows, drive letters not applicable")


def main():
    """Run all path navigation demonstrations."""
    print("Pathlib Path Navigation Demonstration")
    print("=" * 50)

    try:
        demonstrate_path_creation()
        demonstrate_path_joining()
        demonstrate_path_components()
        demonstrate_path_manipulation()
        demonstrate_path_resolution()
        demonstrate_relative_paths()
        demonstrate_path_type_checks()
        demonstrate_path_comparison()
        demonstrate_path_arithmetic()
        demonstrate_navigation_patterns()
        demonstrate_error_handling()
        demonstrate_platform_considerations()

        print("\nAll demonstrations completed successfully!")

    except Exception as e:
        print(f"Error during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
