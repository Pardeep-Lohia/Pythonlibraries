"""
Directory Operations Implementation

This module demonstrates comprehensive directory operations using the os module,
including creation, traversal, analysis, and management functions.
"""

import os
import os.path
import shutil
import time
from collections import defaultdict
from datetime import datetime


def create_directory_tree(base_path, structure):
    """
    Create a directory tree structure.

    Args:
        base_path (str): Base directory path
        structure (dict): Nested dictionary representing directory structure

    Example:
        structure = {
            'src': {
                'main.py': 'print("Hello")',
                'utils.py': 'def helper(): pass'
            },
            'tests': {
                'test_main.py': 'def test_hello(): assert True'
            }
        }
    """
    for name, content in structure.items():
        path = os.path.join(base_path, name)

        if isinstance(content, dict):
            # It's a subdirectory
            os.makedirs(path, exist_ok=True)
            create_directory_tree(path, content)
        else:
            # It's a file
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)


def list_directory_contents(directory, recursive=False, show_hidden=False):
    """
    List directory contents with detailed information.

    Args:
        directory (str): Directory to list
        recursive (bool): Whether to list recursively
        show_hidden (bool): Whether to show hidden files (starting with .)

    Returns:
        list: List of file/directory info dictionaries
    """
    contents = []

    if recursive:
        for root, dirs, files in os.walk(directory):
            # Filter hidden directories if not requested
            if not show_hidden:
                dirs[:] = [d for d in dirs if not d.startswith('.')]

            for item in dirs + files:
                if not show_hidden and item.startswith('.'):
                    continue

                full_path = os.path.join(root, item)
                try:
                    stat_info = os.stat(full_path)
                    contents.append({
                        'path': full_path,
                        'name': item,
                        'type': 'directory' if os.path.isdir(full_path) else 'file',
                        'size': stat_info.st_size,
                        'modified': datetime.fromtimestamp(stat_info.st_mtime),
                        'permissions': oct(stat_info.st_mode)[-3:]
                    })
                except OSError:
                    continue
    else:
        try:
            items = os.listdir(directory)
        except OSError:
            return contents

        for item in items:
            if not show_hidden and item.startswith('.'):
                continue

            full_path = os.path.join(directory, item)
            try:
                stat_info = os.stat(full_path)
                contents.append({
                    'path': full_path,
                    'name': item,
                    'type': 'directory' if os.path.isdir(full_path) else 'file',
                    'size': stat_info.st_size,
                    'modified': datetime.fromtimestamp(stat_info.st_mtime),
                    'permissions': oct(stat_info.st_mode)[-3:]
                })
            except OSError:
                continue

    return contents


def calculate_directory_size(directory, follow_links=True):
    """
    Calculate the total size of a directory.

    Args:
        directory (str): Directory path
        follow_links (bool): Whether to follow symbolic links

    Returns:
        dict: Size information
    """
    total_size = 0
    file_count = 0
    dir_count = 0

    for root, dirs, files in os.walk(directory, followlinks=follow_links):
        dir_count += len(dirs)

        for file in files:
            try:
                file_path = os.path.join(root, file)
                if follow_links or not os.path.islink(file_path):
                    total_size += os.path.getsize(file_path)
                    file_count += 1
            except OSError:
                continue

    return {
        'total_size': total_size,
        'file_count': file_count,
        'dir_count': dir_count,
        'size_mb': total_size / (1024 * 1024),
        'size_gb': total_size / (1024 * 1024 * 1024)
    }


def find_files_by_extension(directory, extensions, recursive=True):
    """
    Find all files with specified extensions.

    Args:
        directory (str): Directory to search
        extensions (list): List of extensions (with or without dots)
        recursive (bool): Whether to search recursively

    Returns:
        list: List of matching file paths
    """
    # Normalize extensions
    extensions = [ext.lower() if ext.startswith('.') else f'.{ext.lower()}' for ext in extensions]

    matches = []

    if recursive:
        for root, dirs, files in os.walk(directory):
            for file in files:
                _, ext = os.path.splitext(file)
                if ext.lower() in extensions:
                    matches.append(os.path.join(root, file))
    else:
        try:
            files = os.listdir(directory)
        except OSError:
            return matches

        for file in files:
            if os.path.isfile(os.path.join(directory, file)):
                _, ext = os.path.splitext(file)
                if ext.lower() in extensions:
                    matches.append(os.path.join(directory, file))

    return matches


def safe_remove_directory(directory, confirm=True):
    """
    Safely remove a directory with confirmation and size display.

    Args:
        directory (str): Directory to remove
        confirm (bool): Whether to ask for confirmation

    Returns:
        bool: True if removed, False otherwise
    """
    if not os.path.exists(directory):
        print(f"Directory does not exist: {directory}")
        return False

    if not os.path.isdir(directory):
        print(f"Path is not a directory: {directory}")
        return False

    # Calculate size
    size_info = calculate_directory_size(directory)

    print(f"Directory: {directory}")
    print(f"Size: {size_info['size_mb']:.2f} MB ({size_info['file_count']} files, {size_info['dir_count']} dirs)")

    if confirm:
        response = input("Are you sure you want to remove this directory? (y/N): ")
        if response.lower() not in ['y', 'yes']:
            print("Operation cancelled.")
            return False

    try:
        shutil.rmtree(directory)
        print(f"Successfully removed directory: {directory}")
        return True
    except OSError as e:
        print(f"Error removing directory: {e}")
        return False


def copy_directory_structure(source_dir, dest_dir, preserve_metadata=True):
    """
    Copy directory structure from source to destination.

    Args:
        source_dir (str): Source directory
        dest_dir (str): Destination directory
        preserve_metadata (bool): Whether to preserve file metadata

    Returns:
        dict: Copy operation results
    """
    results = {
        'dirs_created': 0,
        'files_copied': 0,
        'errors': 0,
        'total_size': 0
    }

    for root, dirs, files in os.walk(source_dir):
        # Create relative path
        rel_path = os.path.relpath(root, source_dir)
        if rel_path == '.':
            dest_root = dest_dir
        else:
            dest_root = os.path.join(dest_dir, rel_path)

        # Create directory
        try:
            os.makedirs(dest_root, exist_ok=True)
            results['dirs_created'] += 1
        except OSError as e:
            print(f"Error creating directory {dest_root}: {e}")
            results['errors'] += 1
            continue

        # Copy files
        for file in files:
            source_file = os.path.join(root, file)
            dest_file = os.path.join(dest_root, file)

            try:
                if preserve_metadata:
                    shutil.copy2(source_file, dest_file)
                else:
                    shutil.copy(source_file, dest_file)

                file_size = os.path.getsize(dest_file)
                results['files_copied'] += 1
                results['total_size'] += file_size

            except OSError as e:
                print(f"Error copying {source_file}: {e}")
                results['errors'] += 1

    return results


def find_empty_directories(directory, recursive=True):
    """
    Find all empty directories in a directory tree.

    Args:
        directory (str): Directory to search
        recursive (bool): Whether to search recursively

    Returns:
        list: List of empty directory paths
    """
    empty_dirs = []

    if recursive:
        for root, dirs, files in os.walk(directory, topdown=False):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                try:
                    if not os.listdir(dir_path):
                        empty_dirs.append(dir_path)
                except OSError:
                    continue
    else:
        try:
            items = os.listdir(directory)
        except OSError:
            return empty_dirs

        for item in items:
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                try:
                    if not os.listdir(item_path):
                        empty_dirs.append(item_path)
                except OSError:
                    continue

    return empty_dirs


def organize_files_by_type(directory, type_mappings=None):
    """
    Organize files in a directory by their type/extension.

    Args:
        directory (str): Directory to organize
        type_mappings (dict): Custom type mappings (extension -> folder_name)

    Returns:
        dict: Organization results
    """
    if type_mappings is None:
        type_mappings = {
            # Documents
            '.pdf': 'Documents',
            '.doc': 'Documents',
            '.docx': 'Documents',
            '.txt': 'Documents',
            '.rtf': 'Documents',

            # Images
            '.jpg': 'Images',
            '.jpeg': 'Images',
            '.png': 'Images',
            '.gif': 'Images',
            '.bmp': 'Images',
            '.tiff': 'Images',

            # Videos
            '.mp4': 'Videos',
            '.avi': 'Videos',
            '.mkv': 'Videos',
            '.mov': 'Videos',

            # Audio
            '.mp3': 'Audio',
            '.wav': 'Audio',
            '.flac': 'Audio',
            '.aac': 'Audio',

            # Archives
            '.zip': 'Archives',
            '.rar': 'Archives',
            '.7z': 'Archives',
            '.tar': 'Archives',
            '.gz': 'Archives',

            # Code
            '.py': 'Code',
            '.js': 'Code',
            '.html': 'Code',
            '.css': 'Code',
            '.java': 'Code',
            '.cpp': 'Code',
            '.c': 'Code',
        }

    results = defaultdict(int)

    try:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    except OSError:
        return dict(results)

    for filename in files:
        filepath = os.path.join(directory, filename)
        _, ext = os.path.splitext(filename)

        ext = ext.lower()
        if ext in type_mappings:
            folder_name = type_mappings[ext]
            folder_path = os.path.join(directory, folder_name)

            # Create folder if it doesn't exist
            os.makedirs(folder_path, exist_ok=True)

            # Move file
            dest_path = os.path.join(folder_path, filename)
            try:
                shutil.move(filepath, dest_path)
                results[folder_name] += 1
            except OSError as e:
                print(f"Error moving {filename}: {e}")
                results['errors'] += 1
        else:
            results['unorganized'] += 1

    return dict(results)


def compare_directories(dir1, dir2):
    """
    Compare two directories and find differences.

    Args:
        dir1 (str): First directory
        dir2 (str): Second directory

    Returns:
        dict: Comparison results
    """
    def get_file_info(directory):
        file_info = {}
        for root, dirs, files in os.walk(directory):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), directory)
                try:
                    stat = os.stat(os.path.join(root, file))
                    file_info[rel_path] = {
                        'size': stat.st_size,
                        'mtime': stat.st_mtime
                    }
                except OSError:
                    continue
        return file_info

    info1 = get_file_info(dir1)
    info2 = get_file_info(dir2)

    keys1 = set(info1.keys())
    keys2 = set(info2.keys())

    results = {
        'only_in_dir1': keys1 - keys2,
        'only_in_dir2': keys2 - keys1,
        'common': keys1 & keys2,
        'differences': []
    }

    # Check for differences in common files
    for path in results['common']:
        if info1[path] != info2[path]:
            results['differences'].append({
                'path': path,
                'dir1': info1[path],
                'dir2': info2[path]
            })

    return results


def demonstrate_directory_operations():
    """Demonstrate various directory operations."""

    print("=== Directory Operations Demo ===\n")

    # Create a sample directory structure
    demo_structure = {
        'project': {
            'src': {
                'main.py': 'print("Hello, World!")',
                'utils.py': 'def helper(): pass'
            },
            'tests': {
                'test_main.py': 'def test_hello(): assert True'
            },
            'data': {
                'input.txt': 'Sample input data',
                'output.txt': 'Sample output data'
            }
        }
    }

    print("1. Creating Directory Structure:")
    create_directory_tree('.', demo_structure)
    print("   Created sample project structure")
    print()

    demo_dir = 'project'

    print("2. Listing Directory Contents:")
    contents = list_directory_contents(demo_dir, recursive=True)
    print(f"   Found {len(contents)} items:")
    for item in contents[:5]:  # Show first 5
        print(f"     {item['type']}: {item['name']} ({item['size']} bytes)")
    if len(contents) > 5:
        print(f"     ... and {len(contents) - 5} more")
    print()

    print("3. Calculating Directory Size:")
    size_info = calculate_directory_size(demo_dir)
    print(f"   Total size: {size_info['size_mb']:.2f} MB")
    print(f"   Files: {size_info['file_count']}, Directories: {size_info['dir_count']}")
    print()

    print("4. Finding Files by Extension:")
    py_files = find_files_by_extension(demo_dir, ['.py'])
    txt_files = find_files_by_extension(demo_dir, ['.txt'])
    print(f"   Python files: {len(py_files)}")
    print(f"   Text files: {len(txt_files)}")
    print()

    print("5. Finding Empty Directories:")
    empty_dirs = find_empty_directories(demo_dir)
    print(f"   Empty directories: {len(empty_dirs)}")
    print()

    print("6. Organizing Files by Type:")
    # Create some test files first
    test_files = [
        ('document.pdf', 'PDF content'),
        ('image.jpg', 'JPG content'),
        ('script.py', 'Python code'),
        ('unknown.xyz', 'Unknown content')
    ]

    for filename, content in test_files:
        filepath = os.path.join(demo_dir, filename)
        with open(filepath, 'w') as f:
            f.write(content)

    results = organize_files_by_type(demo_dir)
    print(f"   Organization results: {dict(results)}")
    print()

    print("7. Comparing Directories:")
    # Create another directory for comparison
    other_dir = 'project_copy'
    copy_results = copy_directory_structure(demo_dir, other_dir, preserve_metadata=False)
    print(f"   Copied {copy_results['files_copied']} files to {other_dir}")

    comparison = compare_directories(demo_dir, other_dir)
    print(f"   Comparison: {len(comparison['common'])} common files")
    print()

    # Cleanup
    print("8. Cleanup:")
    safe_remove_directory(demo_dir, confirm=False)
    safe_remove_directory(other_dir, confirm=False)
    print("   Cleaned up demo directories")

    print("\nDemo completed!")


if __name__ == "__main__":
    demonstrate_directory_operations()
