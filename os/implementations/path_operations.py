"""
Path Operations Implementation

This module demonstrates comprehensive path operations using the os module,
including manipulation, validation, and cross-platform handling.
"""

import os
import os.path
from typing import List, Tuple, Optional, Union


def normalize_path(path: str) -> str:
    """
    Normalize a path by resolving redundant separators and relative components.

    Args:
        path (str): Path to normalize

    Returns:
        str: Normalized path
    """
    return os.path.normpath(path)


def get_path_components(path: str) -> dict:
    """
    Get detailed components of a path.

    Args:
        path (str): Path to analyze

    Returns:
        dict: Path components
    """
    path = normalize_path(path)

    return {
        'full_path': path,
        'directory': os.path.dirname(path),
        'filename': os.path.basename(path),
        'name_only': os.path.splitext(os.path.basename(path))[0],
        'extension': os.path.splitext(path)[1],
        'is_absolute': os.path.isabs(path),
        'exists': os.path.exists(path),
        'is_file': os.path.isfile(path) if os.path.exists(path) else False,
        'is_dir': os.path.isdir(path) if os.path.exists(path) else False,
    }


def build_safe_path(base_dir: str, user_path: str) -> str:
    """
    Build a path safely within a base directory to prevent directory traversal.

    Args:
        base_dir (str): Base directory
        user_path (str): User-provided path component

    Returns:
        str: Safe absolute path within base_dir

    Raises:
        ValueError: If path traversal is detected
    """
    # Normalize both paths
    base_dir = os.path.abspath(base_dir)
    full_path = os.path.normpath(os.path.join(base_dir, user_path))

    # Ensure the result is within the base directory
    if not full_path.startswith(base_dir):
        raise ValueError("Path traversal attempt detected")

    return full_path


def find_common_path(paths: List[str]) -> str:
    """
    Find the common prefix path among multiple paths.

    Args:
        paths (list): List of paths to compare

    Returns:
        str: Common prefix path
    """
    if not paths:
        return ''

    # Convert all paths to absolute paths
    abs_paths = [os.path.abspath(path) for path in paths]

    # Split paths into components
    path_parts = [path.split(os.sep) for path in abs_paths]

    # Find common prefix
    common_parts = []
    for parts in zip(*path_parts):
        if all(part == parts[0] for part in parts):
            common_parts.append(parts[0])
        else:
            break

    return os.sep.join(common_parts)


def get_relative_path(from_path: str, to_path: str) -> str:
    """
    Get the relative path from one path to another.

    Args:
        from_path (str): Starting path
        to_path (str): Target path

    Returns:
        str: Relative path from from_path to to_path
    """
    return os.path.relpath(to_path, from_path)


def expand_user_path(path: str) -> str:
    """
    Expand user home directory (~) in paths.

    Args:
        path (str): Path that may contain ~

    Returns:
        str: Path with ~ expanded
    """
    return os.path.expanduser(path)


def expand_variables_path(path: str) -> str:
    """
    Expand environment variables in paths.

    Args:
        path (str): Path that may contain environment variables

    Returns:
        str: Path with variables expanded
    """
    return os.path.expandvars(path)


def validate_path_safety(path: str) -> dict:
    """
    Validate path for security issues.

    Args:
        path (str): Path to validate

    Returns:
        dict: Validation results with issues found
    """
    issues = []

    # Check for null bytes (security issue)
    if '\x00' in path:
        issues.append('null_byte')

    # Check for suspicious characters
    suspicious_chars = ['|', '&', ';', '`', '$', '(', ')']
    for char in suspicious_chars:
        if char in path:
            issues.append(f'suspicious_char_{char}')

    # Check path length (Windows has 260 char limit, Unix has 4096)
    max_length = 260 if os.name == 'nt' else 4096
    if len(path) > max_length:
        issues.append('path_too_long')

    # Check for directory traversal
    normalized = normalize_path(path)
    if '..' in normalized.split(os.sep):
        issues.append('directory_traversal')

    return {
        'path': path,
        'normalized': normalized,
        'issues': issues,
        'is_safe': len(issues) == 0
    }


def split_path_into_parts(path: str) -> List[str]:
    """
    Split a path into its component parts from root to leaf.

    Args:
        path (str): Path to split

    Returns:
        list: Path components from root to leaf
    """
    path = normalize_path(path)

    # Handle Windows drive letters
    if os.name == 'nt' and len(path) >= 2 and path[1] == ':':
        drive = path[:2]
        remaining = path[2:].lstrip(os.sep)
        parts = [drive]
    else:
        remaining = path.lstrip(os.sep)
        parts = [] if path.startswith(os.sep) else []

    if remaining:
        parts.extend(remaining.split(os.sep))

    # Filter out empty parts
    return [part for part in parts if part]


def get_path_depth(path: str) -> int:
    """
    Get the depth (number of directory levels) of a path.

    Args:
        path (str): Path to analyze

    Returns:
        int: Number of directory levels
    """
    parts = split_path_into_parts(path)

    # Don't count drive letters or root
    depth = 0
    for part in parts:
        if os.name == 'nt' and len(part) == 2 and part[1] == ':':
            continue  # Skip drive letter
        elif part:  # Skip empty parts
            depth += 1

    return depth


def find_matching_files(directory: str, pattern: str, recursive: bool = True) -> List[str]:
    """
    Find files matching a pattern.

    Args:
        directory (str): Directory to search
        pattern (str): Pattern to match (supports * and ? wildcards)
        recursive (bool): Whether to search recursively

    Returns:
        list: List of matching file paths
    """
    import fnmatch
    matches = []

    if recursive:
        for root, dirs, files in os.walk(directory):
            for filename in files:
                if fnmatch.fnmatch(filename, pattern):
                    matches.append(os.path.join(root, filename))
    else:
        try:
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                if os.path.isfile(filepath) and fnmatch.fnmatch(filename, pattern):
                    matches.append(filepath)
        except OSError:
            pass

    return matches


def get_file_size_info(filepath: str) -> dict:
    """
    Get detailed file size information.

    Args:
        filepath (str): Path to file

    Returns:
        dict: Size information in various units
    """
    try:
        size_bytes = os.path.getsize(filepath)

        return {
            'bytes': size_bytes,
            'kilobytes': size_bytes / 1024,
            'megabytes': size_bytes / (1024 * 1024),
            'gigabytes': size_bytes / (1024 * 1024 * 1024),
            'human_readable': _format_file_size(size_bytes)
        }
    except OSError:
        return {'error': 'Could not get file size'}


def _format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return ".1f"
        size_bytes /= 1024.0
    return ".1f"


def compare_paths(path1: str, path2: str) -> dict:
    """
    Compare two paths to see if they refer to the same location.

    Args:
        path1 (str): First path
        path2 (str): Second path

    Returns:
        dict: Comparison results
    """
    try:
        # Normalize and convert to absolute paths
        abs_path1 = os.path.abspath(normalize_path(path1))
        abs_path2 = os.path.abspath(normalize_path(path2))

        # Use os.path.samefile if both exist
        if os.path.exists(abs_path1) and os.path.exists(abs_path2):
            same_file = os.path.samefile(abs_path1, abs_path2)
        else:
            same_file = abs_path1 == abs_path2

        return {
            'path1': path1,
            'path2': path2,
            'normalized_path1': abs_path1,
            'normalized_path2': abs_path2,
            'are_same': same_file,
            'both_exist': os.path.exists(abs_path1) and os.path.exists(abs_path2)
        }
    except OSError:
        return {
            'path1': path1,
            'path2': path2,
            'error': 'Could not compare paths'
        }


def create_path_tree(base_path: str, structure: dict) -> List[str]:
    """
    Create a directory structure from a nested dictionary.

    Args:
        base_path (str): Base directory path
        structure (dict): Nested dictionary representing directory structure

    Returns:
        list: List of created paths
    """
    created = []

    def _create_recursive(current_path, struct):
        for name, content in struct.items():
            path = os.path.join(current_path, name)

            if isinstance(content, dict):
                # It's a directory
                os.makedirs(path, exist_ok=True)
                created.append(path)
                _create_recursive(path, content)
            else:
                # It's a file
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(str(content))
                created.append(path)

    _create_recursive(base_path, structure)
    return created


def resolve_path_symlinks(path: str) -> str:
    """
    Resolve all symbolic links in a path.

    Args:
        path (str): Path that may contain symlinks

    Returns:
        str: Path with symlinks resolved
    """
    try:
        return os.path.realpath(path)
    except OSError:
        return path


def get_path_permissions(path: str) -> Optional[str]:
    """
    Get the permission string for a path.

    Args:
        path (str): Path to check

    Returns:
        str or None: Permission string (e.g., 'rw-r--r--') or None if error
    """
    try:
        import stat
        stat_info = os.stat(path)
        mode = stat_info.st_mode

        # Convert to permission string
        perms = []
        for who in ['USR', 'GRP', 'OTH']:
            perm = ''
            for what in [('R', getattr(stat, f'S_IR{who}')),
                        ('W', getattr(stat, f'S_IW{who}')),
                        ('X', getattr(stat, f'S_IX{who}'))]:
                perm += what[0] if mode & what[1] else '-'
            perms.append(perm)
        return ''.join(perms)
    except (OSError, AttributeError):
        return None


def demonstrate_path_operations():
    """Demonstrate various path operations."""

    print("=== Path Operations Demo ===\n")

    # Test paths
    test_paths = [
        'file.txt',
        './subdir/file.txt',
        '../parent/file.txt',
        '/absolute/path/file.txt',
        'C:\\windows\\path\\file.txt' if os.name == 'nt' else '/unix/path/file.txt'
    ]

    print("1. Path Normalization:")
    for path in test_paths:
        normalized = normalize_path(path)
        print(f"   '{path}' -> '{normalized}'")
    print()

    print("2. Path Components Analysis:")
    for path in test_paths[:3]:
        components = get_path_components(path)
        print(f"   Path: {path}")
        print(f"   Directory: {components['directory']}")
        print(f"   Filename: {components['filename']}")
        print(f"   Extension: {components['extension']}")
        print(f"   Is absolute: {components['is_absolute']}")
        print()

    print("3. Safe Path Construction:")
    try:
        safe_path = build_safe_path('/home/user', 'documents/file.txt')
        print(f"   Safe path: {safe_path}")

        # Try path traversal
        unsafe_path = build_safe_path('/home/user', '../../../etc/passwd')
        print(f"   Unsafe attempt: {unsafe_path}")
    except ValueError as e:
        print(f"   Blocked unsafe path: {e}")
    print()

    print("4. Common Path Finding:")
    common_paths = [
        '/home/user/docs/file1.txt',
        '/home/user/docs/file2.txt',
        '/home/user/pics/image.jpg'
    ]
    common = find_common_path(common_paths)
    print(f"   Common path: {common}")
    print()

    print("5. Relative Path Calculation:")
    rel_path = get_relative_path('/home/user/docs', '/home/user/pics/image.jpg')
    print(f"   Relative path: {rel_path}")
    print()

    print("6. Path Expansion:")
    user_path = expand_user_path('~/documents/file.txt')
    var_path = expand_variables_path('$HOME/documents/file.txt')
    print(f"   User expansion: {user_path}")
    print(f"   Variable expansion: {var_path}")
    print()

    print("7. Path Safety Validation:")
    test_safety_paths = [
        'normal/file.txt',
        'file;rm -rf /',
        'file\x00null.txt',
        'a' * 300  # Very long path
    ]

    for path in test_safety_paths:
        validation = validate_path_safety(path)
        status = "SAFE" if validation['is_safe'] else "UNSAFE"
        print(f"   '{path[:30]}...': {status}")
        if validation['issues']:
            print(f"     Issues: {validation['issues']}")
    print()

    print("8. Path Splitting:")
    split_path = 'home/user/documents/file.txt'
    parts = split_path_into_parts(split_path)
    print(f"   Path: {split_path}")
    print(f"   Parts: {parts}")
    print(f"   Depth: {get_path_depth(split_path)}")
    print()

    print("9. File Size Information:")
    # Create a test file
    test_file = 'test_size.txt'
    with open(test_file, 'w') as f:
        f.write('x' * 1024)  # 1KB file

    size_info = get_file_size_info(test_file)
    if 'error' not in size_info:
        print(f"   File size: {size_info['human_readable']}")
        print(f"   Bytes: {size_info['bytes']}")
    print()

    print("10. Path Comparison:")
    compare_result = compare_paths('./file.txt', 'file.txt')
    print(f"   Paths are same: {compare_result['are_same']}")
    print()

    # Cleanup
    try:
        os.remove(test_file)
    except OSError:
        pass

    print("Demo completed!")


if __name__ == "__main__":
    demonstrate_path_operations()
