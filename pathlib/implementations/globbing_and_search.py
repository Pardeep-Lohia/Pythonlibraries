#!/usr/bin/env python3
"""
Globbing and Search Operations with pathlib

This module demonstrates globbing and file search operations using pathlib.Path objects.
All examples are runnable Python 3 code.
"""

from pathlib import Path
import os
import time
from datetime import datetime, timedelta


def create_test_structure():
    """Create a test directory structure for globbing examples."""
    base_dir = Path('glob_test')
    base_dir.mkdir(exist_ok=True)

    # Create subdirectories
    (base_dir / 'src').mkdir(exist_ok=True)
    (base_dir / 'tests').mkdir(exist_ok=True)
    (base_dir / 'docs').mkdir(exist_ok=True)
    (base_dir / 'src' / 'utils').mkdir(exist_ok=True)
    (base_dir / 'src' / 'models').mkdir(exist_ok=True)

    # Create test files
    files = [
        'README.md',
        'setup.py',
        'requirements.txt',
        'src/main.py',
        'src/utils/helpers.py',
        'src/utils/validation.py',
        'src/models/user.py',
        'src/models/product.py',
        'tests/test_main.py',
        'tests/test_utils.py',
        'tests/test_models.py',
        'docs/guide.md',
        'docs/api.md',
        'data.json',
        'config.ini',
        'script.sh',
        '.gitignore',
        '.env'
    ]

    for file_path in files:
        full_path = base_dir / file_path
        full_path.write_text(f'# Content of {file_path}')

    return base_dir


def demonstrate_basic_globbing():
    """Demonstrate basic globbing operations."""
    print("=== Basic Globbing Examples ===")

    base_dir = create_test_structure()

    # Find all Python files in current directory
    py_files = list(base_dir.glob('*.py'))
    print(f"Python files in root: {[f.name for f in py_files]}")

    # Find all text files
    txt_files = list(base_dir.glob('*.txt'))
    print(f"Text files in root: {[f.name for f in txt_files]}")

    # Find all markdown files
    md_files = list(base_dir.glob('*.md'))
    print(f"Markdown files in root: {[f.name for f in md_files]}")

    # Find all files starting with 'test_'
    test_files = list(base_dir.glob('test_*'))
    print(f"Test files in root: {[f.name for f in test_files]}")

    # Find all hidden files (starting with .)
    hidden_files = list(base_dir.glob('.*'))
    print(f"Hidden files in root: {[f.name for f in hidden_files]}")

    # Clean up
    import shutil
    shutil.rmtree(base_dir)


def demonstrate_recursive_globbing():
    """Demonstrate recursive globbing with rglob()."""
    print("\n=== Recursive Globbing Examples ===")

    base_dir = create_test_structure()

    # Find all Python files recursively
    all_py_files = list(base_dir.rglob('*.py'))
    print(f"All Python files: {[str(f.relative_to(base_dir)) for f in all_py_files]}")

    # Find all files in src directory recursively
    src_files = list(base_dir.glob('src/**/*'))
    print(f"All files in src: {[str(f.relative_to(base_dir)) for f in src_files]}")

    # Find all markdown files recursively
    all_md_files = list(base_dir.rglob('*.md'))
    print(f"All markdown files: {[str(f.relative_to(base_dir)) for f in all_md_files]}")

    # Find all files in any tests directory
    test_files = list(base_dir.rglob('test_*'))
    print(f"All test files: {[str(f.relative_to(base_dir)) for f in test_files]}")

    # Find all files in nested directories
    nested_files = list(base_dir.rglob('src/**/*.py'))
    print(f"Python files in src subdirs: {[str(f.relative_to(base_dir)) for f in nested_files]}")

    # Clean up
    import shutil
    shutil.rmtree(base_dir)


def demonstrate_pattern_matching():
    """Demonstrate various glob patterns."""
    print("\n=== Pattern Matching Examples ===")

    base_dir = create_test_structure()

    # Single character wildcard
    single_char = list(base_dir.glob('*.p?'))
    print(f"Files matching *.p?: {[f.name for f in single_char]}")

    # Character range
    range_match = list(base_dir.glob('[cd]*'))
    print(f"Files starting with c or d: {[f.name for f in range_match]}")

    # Multiple patterns
    patterns = ['*.py', '*.md', '*.txt']
    matching_files = []
    for pattern in patterns:
        matching_files.extend(base_dir.glob(pattern))
    print(f"Files matching multiple patterns: {[f.name for f in matching_files]}")

    # Complex patterns
    complex_pattern = list(base_dir.glob('*.??'))
    print(f"Files with 2-char extensions: {[f.name for f in complex_pattern]}")

    # Clean up
    import shutil
    shutil.rmtree(base_dir)


def demonstrate_file_search_functions():
    """Demonstrate custom file search functions."""
    print("\n=== Custom Search Functions Examples ===")

    base_dir = create_test_structure()

    def find_files_by_extension(directory: Path, extension: str):
        """Find all files with a specific extension."""
        return list(directory.rglob(f'*.{extension}'))

    def find_files_by_name(directory: Path, name_pattern: str):
        """Find files matching a name pattern."""
        return list(directory.rglob(name_pattern))

    def find_files_by_size(directory: Path, min_size: int = 0, max_size: int = None):
        """Find files within a size range."""
        files = []
        for file_path in directory.rglob('*'):
            if file_path.is_file():
                size = file_path.stat().st_size
                if size >= min_size and (max_size is None or size <= max_size):
                    files.append(file_path)
        return files

    def find_recent_files(directory: Path, days: int = 7):
        """Find files modified within the last N days."""
        cutoff = time.time() - (days * 24 * 3600)
        return [f for f in directory.rglob('*') if f.is_file() and f.stat().st_mtime > cutoff]

    # Use the functions
    py_files = find_files_by_extension(base_dir, 'py')
    print(f"Python files: {[str(f.relative_to(base_dir)) for f in py_files]}")

    test_files = find_files_by_name(base_dir, 'test_*')
    print(f"Test files: {[str(f.relative_to(base_dir)) for f in test_files]}")

    small_files = find_files_by_size(base_dir, max_size=50)
    print(f"Small files: {[str(f.relative_to(base_dir)) for f in small_files]}")

    recent_files = find_recent_files(base_dir, days=1)
    print(f"Recent files: {[str(f.relative_to(base_dir)) for f in recent_files]}")

    # Clean up
    import shutil
    shutil.rmtree(base_dir)


def demonstrate_advanced_search():
    """Demonstrate advanced search operations."""
    print("\n=== Advanced Search Examples ===")

    base_dir = create_test_structure()

    def search_by_content(directory: Path, search_text: str, case_sensitive: bool = True):
        """Search for files containing specific text."""
        matching_files = []
        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.suffix in ['.py', '.md', '.txt']:
                try:
                    content = file_path.read_text(encoding='utf-8')
                    if case_sensitive:
                        if search_text in content:
                            matching_files.append(file_path)
                    else:
                        if search_text.lower() in content.lower():
                            matching_files.append(file_path)
                except UnicodeDecodeError:
                    continue
        return matching_files

    def find_empty_files(directory: Path):
        """Find all empty files."""
        return [f for f in directory.rglob('*') if f.is_file() and f.stat().st_size == 0]

    def find_duplicate_files(directory: Path):
        """Find files with duplicate names (basic implementation)."""
        seen = {}
        duplicates = []
        for file_path in directory.rglob('*'):
            if file_path.is_file():
                name = file_path.name
                if name in seen:
                    duplicates.append((seen[name], file_path))
                else:
                    seen[name] = file_path
        return duplicates

    # Search for content
    content_files = search_by_content(base_dir, 'README')
    print(f"Files containing 'README': {[str(f.relative_to(base_dir)) for f in content_files]}")

    # Find empty files
    empty_files = find_empty_files(base_dir)
    print(f"Empty files: {[str(f.relative_to(base_dir)) for f in empty_files]}")

    # Find duplicates (create some duplicates first)
    duplicate1 = base_dir / 'duplicate.txt'
    duplicate2 = base_dir / 'src' / 'duplicate.txt'
    duplicate1.write_text('duplicate content')
    duplicate2.write_text('duplicate content')

    duplicates = find_duplicate_files(base_dir)
    print(f"Duplicate files: {[(str(f1.relative_to(base_dir)), str(f2.relative_to(base_dir))) for f1, f2 in duplicates]}")

    # Clean up
    import shutil
    shutil.rmtree(base_dir)


def demonstrate_glob_performance():
    """Demonstrate globbing performance considerations."""
    print("\n=== Performance Examples ===")

    base_dir = create_test_structure()

    # Create many files for performance testing
    for i in range(100):
        (base_dir / f'file_{i:03d}.txt').write_text(f'Content {i}')

    import time

    # Method 1: Multiple globs
    start = time.time()
    py_files = list(base_dir.glob('*.py'))
    md_files = list(base_dir.glob('*.md'))
    txt_files = list(base_dir.glob('*.txt'))
    method1_time = time.time() - start

    # Method 2: Single rglob with filtering
    start = time.time()
    all_files = list(base_dir.rglob('*'))
    py_files2 = [f for f in all_files if f.suffix == '.py']
    md_files2 = [f for f in all_files if f.suffix == '.md']
    txt_files2 = [f for f in all_files if f.suffix == '.txt']
    method2_time = time.time() - start

    print(f"Method 1 (multiple globs): {method1_time:.4f}s")
    print(f"Method 2 (single rglob): {method2_time:.4f}s")
    print(f"Results match: {len(py_files) == len(py_files2)}")

    # Clean up
    import shutil
    shutil.rmtree(base_dir)


def demonstrate_cross_platform_globbing():
    """Demonstrate cross-platform globbing considerations."""
    print("\n=== Cross-Platform Globbing Examples ===")

    # pathlib handles platform differences automatically
    base_dir = create_test_structure()

    # These patterns work the same on Windows, macOS, and Linux
    patterns = [
        '*.py',      # Python files
        '*.md',      # Markdown files
        'test_*',    # Test files
        'src/**/*',  # All files in src recursively
    ]

    for pattern in patterns:
        if '**' in pattern:
            files = list(base_dir.rglob(pattern.split('/')[1]))
        else:
            files = list(base_dir.glob(pattern))
        print(f"Pattern '{pattern}': {len(files)} matches")

    # Case sensitivity depends on filesystem
    if os.name == 'nt':  # Windows (case-insensitive)
        upper_case = list(base_dir.glob('*.PY'))
        lower_case = list(base_dir.glob('*.py'))
        print(f"Windows case-insensitive: {len(upper_case)} == {len(lower_case)}")
    else:  # Unix-like (case-sensitive)
        upper_case = list(base_dir.glob('*.PY'))
        lower_case = list(base_dir.glob('*.py'))
        print(f"Unix case-sensitive: {len(upper_case)} != {len(lower_case)}")

    # Clean up
    import shutil
    shutil.rmtree(base_dir)


def demonstrate_glob_error_handling():
    """Demonstrate error handling in globbing operations."""
    print("\n=== Error Handling Examples ===")

    def safe_glob(directory: Path, pattern: str):
        """Safely perform glob operation with error handling."""
        try:
            return list(directory.glob(pattern))
        except (OSError, PermissionError) as e:
            print(f"Error globbing {pattern} in {directory}: {e}")
            return []

    def safe_rglob(directory: Path, pattern: str):
        """Safely perform recursive glob operation."""
        try:
            return list(directory.rglob(pattern))
        except (OSError, PermissionError) as e:
            print(f"Error rglob {pattern} in {directory}: {e}")
            return []

    # Test with valid directory
    base_dir = create_test_structure()
    py_files = safe_glob(base_dir, '*.py')
    print(f"Safe glob found {len(py_files)} Python files")

    # Test with invalid pattern (should not crash)
    invalid_results = safe_glob(base_dir, '**/*')
    print(f"Invalid pattern handled gracefully: {len(invalid_results)} results")

    # Clean up
    import shutil
    shutil.rmtree(base_dir)


def main():
    """Run all globbing and search demonstrations."""
    print("Pathlib Globbing and Search Operations Demonstration")
    print("=" * 60)

    try:
        demonstrate_basic_globbing()
        demonstrate_recursive_globbing()
        demonstrate_pattern_matching()
        demonstrate_file_search_functions()
        demonstrate_advanced_search()
        demonstrate_glob_performance()
        demonstrate_cross_platform_globbing()
        demonstrate_glob_error_handling()

        print("\nAll demonstrations completed successfully!")

    except Exception as e:
        print(f"Error during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
