#!/usr/bin/env python3
"""
Directory Operations with pathlib

This module demonstrates various directory operations using pathlib.Path objects.
All examples are runnable Python 3 code.
"""

from pathlib import Path
import shutil
import os
from datetime import datetime


def create_sample_directory_structure():
    """Create a sample directory structure for demonstration."""
    base_dir = Path('sample_structure')
    base_dir.mkdir(exist_ok=True)

    # Create subdirectories
    (base_dir / 'documents').mkdir()
    (base_dir / 'images').mkdir()
    (base_dir / 'scripts').mkdir()
    (base_dir / 'documents' / 'work').mkdir()
    (base_dir / 'documents' / 'personal').mkdir()

    # Create sample files
    files = [
        'documents/work/report.txt',
        'documents/work/data.xlsx',
        'documents/personal/letter.txt',
        'images/photo1.jpg',
        'images/photo2.png',
        'scripts/backup.py',
        'scripts/cleanup.sh',
        'readme.md'
    ]

    for file_path in files:
        full_path = base_dir / file_path
        full_path.write_text(f'Sample content for {file_path}')

    return base_dir


def demonstrate_directory_creation():
    """Demonstrate different ways to create directories."""
    print("=== Directory Creation Examples ===")

    # Create single directory
    single_dir = Path('single_directory')
    single_dir.mkdir()
    print(f"Created single directory: {single_dir}")

    # Create nested directories
    nested_dir = Path('parent/child/grandchild')
    nested_dir.mkdir(parents=True)
    print(f"Created nested directories: {nested_dir}")

    # Safe creation (no error if exists)
    safe_dir = Path('existing_directory')
    safe_dir.mkdir(parents=True, exist_ok=True)
    print(f"Created safely (exists_ok=True): {safe_dir}")

    # Create with specific permissions (Unix-like systems)
    if os.name != 'nt':
        perm_dir = Path('restricted_directory')
        perm_dir.mkdir(mode=0o755)
        print(f"Created with permissions 755: {perm_dir}")


def demonstrate_directory_listing():
    """Demonstrate directory listing operations."""
    print("\n=== Directory Listing Examples ===")

    # Create sample structure
    base_dir = create_sample_directory_structure()

    # Basic listing
    print(f"Contents of {base_dir}:")
    for item in base_dir.iterdir():
        item_type = "File" if item.is_file() else "Directory"
        print(f"  {item_type}: {item.name}")

    # List only files
    print(f"\nFiles in {base_dir}:")
    files = [item for item in base_dir.iterdir() if item.is_file()]
    for file_item in files:
        print(f"  {file_item.name}")

    # List only directories
    print(f"\nDirectories in {base_dir}:")
    dirs = [item for item in base_dir.iterdir() if item.is_dir()]
    for dir_item in dirs:
        print(f"  {dir_item.name}")

    # Recursive listing
    print(f"\nAll files recursively in {base_dir}:")
    for file_path in base_dir.rglob('*'):
        if file_path.is_file():
            relative_path = file_path.relative_to(base_dir)
            print(f"  {relative_path}")

    # Clean up
    shutil.rmtree(base_dir)


def demonstrate_directory_traversal():
    """Demonstrate directory traversal techniques."""
    print("\n=== Directory Traversal Examples ===")

    base_dir = create_sample_directory_structure()

    def print_tree(directory: Path, prefix: str = ""):
        """Print directory tree structure."""
        items = sorted(directory.iterdir(), key=lambda x: (x.is_file(), x.name))
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            connector = "└── " if is_last else "├── "

            print(f"{prefix}{connector}{item.name}")

            if item.is_dir():
                extension = "    " if is_last else "│   "
                print_tree(item, prefix + extension)

    print("Directory tree structure:")
    print_tree(base_dir)

    # Find files by pattern
    print("\nPython files:")
    for py_file in base_dir.rglob('*.py'):
        print(f"  {py_file.relative_to(base_dir)}")

    print("\nText files:")
    for txt_file in base_dir.rglob('*.txt'):
        print(f"  {txt_file.relative_to(base_dir)}")

    # Find files in specific subdirectory
    work_dir = base_dir / 'documents' / 'work'
    print(f"\nFiles in work directory:")
    for file_path in work_dir.iterdir():
        if file_path.is_file():
            print(f"  {file_path.name}")

    # Clean up
    shutil.rmtree(base_dir)


def demonstrate_directory_operations():
    """Demonstrate various directory operations."""
    print("\n=== Directory Operations Examples ===")

    # Create test directories
    dir1 = Path('test_dir1')
    dir2 = Path('test_dir2')
    dir1.mkdir()
    dir2.mkdir()

    # Create files in directories
    (dir1 / 'file1.txt').write_text('Content 1')
    (dir1 / 'file2.txt').write_text('Content 2')
    (dir2 / 'file3.txt').write_text('Content 3')

    print("Created directories with files:")
    for d in [dir1, dir2]:
        files = list(d.iterdir())
        print(f"  {d.name}: {len(files)} files")

    # Rename directory
    dir1_renamed = dir1.with_name('renamed_dir1')
    dir1.rename(dir1_renamed)
    print(f"Renamed: {dir1} -> {dir1_renamed}")

    # Copy directory
    dir2_copy = Path('copied_dir2')
    shutil.copytree(dir2, dir2_copy)
    print(f"Copied: {dir2} -> {dir2_copy}")

    # Move directory
    dir2_moved = Path('moved_dir2')
    dir2.rename(dir2_moved)
    print(f"Moved: {dir2} -> {dir2_moved}")

    # Clean up
    shutil.rmtree(dir1_renamed)
    shutil.rmtree(dir2_copy)
    shutil.rmtree(dir2_moved)
    print("Cleaned up all test directories")


def demonstrate_directory_removal():
    """Demonstrate directory removal operations."""
    print("\n=== Directory Removal Examples ===")

    # Create directory structure
    test_dir = Path('removal_test')
    test_dir.mkdir()

    # Create nested structure
    (test_dir / 'subdir1').mkdir()
    (test_dir / 'subdir2').mkdir()
    (test_dir / 'subdir1' / 'nested').mkdir()

    # Add files
    (test_dir / 'file1.txt').write_text('File 1')
    (test_dir / 'subdir1' / 'file2.txt').write_text('File 2')
    (test_dir / 'subdir1' / 'nested' / 'file3.txt').write_text('File 3')

    print("Created directory structure:")
    for file_path in test_dir.rglob('*'):
        if file_path.is_file():
            relative_path = file_path.relative_to(test_dir)
            print(f"  {relative_path}")

    # Remove empty directory
    empty_dir = test_dir / 'empty_dir'
    empty_dir.mkdir()
    empty_dir.rmdir()
    print(f"Removed empty directory: {empty_dir}")

    # Remove directory tree
    shutil.rmtree(test_dir)
    print(f"Removed entire directory tree: {test_dir}")


def demonstrate_directory_analysis():
    """Demonstrate directory analysis operations."""
    print("\n=== Directory Analysis Examples ===")

    base_dir = create_sample_directory_structure()

    # Count files and directories
    total_files = 0
    total_dirs = 0
    total_size = 0

    for item in base_dir.rglob('*'):
        if item.is_file():
            total_files += 1
            total_size += item.stat().st_size
        elif item.is_dir():
            total_dirs += 1

    print(f"Directory: {base_dir}")
    print(f"Total files: {total_files}")
    print(f"Total directories: {total_dirs}")
    print(f"Total size: {total_size} bytes")

    # Analyze file types
    file_extensions = {}
    for file_path in base_dir.rglob('*'):
        if file_path.is_file():
            ext = file_path.suffix.lower()
            if ext:
                file_extensions[ext] = file_extensions.get(ext, 0) + 1

    print("\nFile types:")
    for ext, count in sorted(file_extensions.items()):
        print(f"  {ext}: {count} files")

    # Find largest files
    files_with_sizes = []
    for file_path in base_dir.rglob('*'):
        if file_path.is_file():
            size = file_path.stat().st_size
            files_with_sizes.append((file_path, size))

    files_with_sizes.sort(key=lambda x: x[1], reverse=True)
    print("\nLargest files:")
    for file_path, size in files_with_sizes[:3]:
        relative_path = file_path.relative_to(base_dir)
        print(f"  {relative_path}: {size} bytes")

    # Clean up
    shutil.rmtree(base_dir)


def demonstrate_working_directory():
    """Demonstrate working directory operations."""
    print("\n=== Working Directory Examples ===")

    # Get current working directory
    cwd = Path.cwd()
    print(f"Current working directory: {cwd}")

    # Change working directory (temporarily)
    import os
    original_cwd = os.getcwd()

    try:
        # Create a test directory
        test_cwd = Path('test_cwd')
        test_cwd.mkdir()

        # Change to test directory
        os.chdir(test_cwd)
        print(f"Changed to: {Path.cwd()}")

        # Create a file in new working directory
        (Path('test_file.txt')).write_text('Created in test directory')

        # List files in current directory
        print("Files in current directory:")
        for item in Path('.').iterdir():
            print(f"  {item.name}")

        # Change back
        os.chdir(original_cwd)
        print(f"Changed back to: {Path.cwd()}")

        # Clean up
        shutil.rmtree(test_cwd)

    except Exception as e:
        print(f"Error in working directory demo: {e}")
        os.chdir(original_cwd)


def demonstrate_path_operations():
    """Demonstrate path operations on directories."""
    print("\n=== Path Operations on Directories ===")

    # Create test structure
    base_dir = create_sample_directory_structure()

    # Get absolute path
    abs_path = base_dir.resolve()
    print(f"Absolute path: {abs_path}")

    # Get relative path from parent
    parent_dir = base_dir.parent
    rel_path = base_dir.relative_to(parent_dir)
    print(f"Relative to parent: {rel_path}")

    # Check relationships
    subdir = base_dir / 'documents'
    print(f"{subdir} is relative to {base_dir}: {subdir.is_relative_to(base_dir)}")

    # Path components
    print(f"Path parts: {base_dir.parts}")
    print(f"Parent: {base_dir.parent}")
    print(f"Name: {base_dir.name}")

    # Path manipulation
    new_name = base_dir.with_name('new_structure')
    print(f"With new name: {new_name}")

    # Clean up
    shutil.rmtree(base_dir)


def main():
    """Run all directory operation demonstrations."""
    print("Pathlib Directory Operations Demonstration")
    print("=" * 50)

    try:
        demonstrate_directory_creation()
        demonstrate_directory_listing()
        demonstrate_directory_traversal()
        demonstrate_directory_operations()
        demonstrate_directory_removal()
        demonstrate_directory_analysis()
        demonstrate_working_directory()
        demonstrate_path_operations()

        print("\nAll demonstrations completed successfully!")

    except Exception as e:
        print(f"Error during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
