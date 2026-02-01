"""
Directory Traversal Implementation

This module demonstrates various directory traversal techniques using the os module.
It includes recursive directory walking, filtering, and analysis functions.
"""

import os
import os.path
import time
from collections import defaultdict, namedtuple
from datetime import datetime


# Named tuple for file information
FileInfo = namedtuple('FileInfo', ['path', 'name', 'size', 'modified', 'is_dir', 'extension'])


class DirectoryTraverser:
    """
    A class for traversing and analyzing directory structures.
    """

    def __init__(self, root_path, max_depth=None, follow_links=False):
        """
        Initialize the directory traverser.

        Args:
            root_path (str): Root directory to start traversal
            max_depth (int): Maximum depth to traverse (None for unlimited)
            follow_links (bool): Whether to follow symbolic links
        """
        self.root_path = os.path.abspath(root_path)
        self.max_depth = max_depth
        self.follow_links = follow_links

        if not os.path.exists(self.root_path):
            raise FileNotFoundError(f"Directory not found: {self.root_path}")

        if not os.path.isdir(self.root_path):
            raise NotADirectoryError(f"Path is not a directory: {self.root_path}")

    def traverse(self, file_filter=None, dir_filter=None):
        """
        Traverse the directory tree and yield file information.

        Args:
            file_filter (callable): Function to filter files (takes FileInfo, returns bool)
            dir_filter (callable): Function to filter directories (takes path, returns bool)

        Yields:
            FileInfo: Information about each file/directory encountered
        """
        for dirpath, dirnames, filenames in os.walk(
            self.root_path,
            followlinks=self.follow_links
        ):
            # Check depth limit
            if self.max_depth is not None:
                rel_path = os.path.relpath(dirpath, self.root_path)
                if rel_path != '.':
                    depth = len(rel_path.split(os.sep))
                    if depth > self.max_depth:
                        dirnames[:] = []  # Don't traverse deeper
                        continue

            # Apply directory filter
            if dir_filter and not dir_filter(dirpath):
                dirnames[:] = []  # Skip this directory
                continue

            # Process directories
            for dirname in dirnames[:]:  # Copy to avoid modification issues
                dir_full_path = os.path.join(dirpath, dirname)

                try:
                    stat_info = os.lstat(dir_full_path) if not self.follow_links else os.stat(dir_full_path)
                    file_info = FileInfo(
                        path=dir_full_path,
                        name=dirname,
                        size=stat_info.st_size,
                        modified=stat_info.st_mtime,
                        is_dir=True,
                        extension=''
                    )

                    if file_filter is None or file_filter(file_info):
                        yield file_info

                except OSError:
                    continue

            # Process files
            for filename in filenames:
                file_full_path = os.path.join(dirpath, filename)

                try:
                    stat_info = os.lstat(file_full_path) if not self.follow_links else os.stat(file_full_path)
                    _, extension = os.path.splitext(filename)

                    file_info = FileInfo(
                        path=file_full_path,
                        name=filename,
                        size=stat_info.st_size,
                        modified=stat_info.st_mtime,
                        is_dir=False,
                        extension=extension.lower()
                    )

                    if file_filter is None or file_filter(file_info):
                        yield file_info

                except OSError:
                    continue

    def find_files_by_extension(self, extensions):
        """
        Find all files with specified extensions.

        Args:
            extensions (list): List of extensions to search for (without dots)

        Returns:
            list: List of FileInfo objects for matching files
        """
        if isinstance(extensions, str):
            extensions = [extensions]

        # Normalize extensions
        extensions = [ext.lower() if ext.startswith('.') else f'.{ext.lower()}' for ext in extensions]

        def extension_filter(file_info):
            return not file_info.is_dir and file_info.extension in extensions

        return list(self.traverse(file_filter=extension_filter))

    def find_large_files(self, min_size_bytes):
        """
        Find files larger than specified size.

        Args:
            min_size_bytes (int): Minimum file size in bytes

        Returns:
            list: List of FileInfo objects for large files
        """
        def size_filter(file_info):
            return not file_info.is_dir and file_info.size >= min_size_bytes

        return list(self.traverse(file_filter=size_filter))

    def find_recent_files(self, hours=24):
        """
        Find files modified within the last specified hours.

        Args:
            hours (int): Number of hours to look back

        Returns:
            list: List of FileInfo objects for recent files
        """
        cutoff_time = time.time() - (hours * 60 * 60)

        def time_filter(file_info):
            return file_info.modified >= cutoff_time

        return list(self.traverse(file_filter=time_filter))

    def get_directory_stats(self):
        """
        Get comprehensive statistics about the directory structure.

        Returns:
            dict: Dictionary containing various statistics
        """
        stats = {
            'total_files': 0,
            'total_dirs': 0,
            'total_size': 0,
            'file_types': defaultdict(int),
            'size_by_extension': defaultdict(int),
            'largest_files': [],
            'oldest_files': [],
            'newest_files': []
        }

        all_files = list(self.traverse())

        for file_info in all_files:
            if file_info.is_dir:
                stats['total_dirs'] += 1
            else:
                stats['total_files'] += 1
                stats['total_size'] += file_info.size
                stats['file_types'][file_info.extension] += 1
                stats['size_by_extension'][file_info.extension] += file_info.size

                # Track largest files
                stats['largest_files'].append(file_info)
                stats['largest_files'].sort(key=lambda x: x.size, reverse=True)
                stats['largest_files'] = stats['largest_files'][:10]

                # Track oldest/newest files
                stats['oldest_files'].append(file_info)
                stats['newest_files'].append(file_info)

        # Sort by modification time
        stats['oldest_files'].sort(key=lambda x: x.modified)
        stats['oldest_files'] = stats['oldest_files'][:10]

        stats['newest_files'].sort(key=lambda x: x.modified, reverse=True)
        stats['newest_files'] = stats['newest_files'][:10]

        return dict(stats)

    def create_directory_tree(self, output_file=None):
        """
        Create a visual representation of the directory tree.

        Args:
            output_file (str): File to write tree to (prints to stdout if None)

        Returns:
            str: Directory tree as string
        """
        tree_lines = []
        tree_lines.append(f"{os.path.basename(self.root_path)}/")
        tree_lines.append("")

        def add_to_tree(dirpath, prefix=""):
            try:
                entries = sorted(os.listdir(dirpath))
            except OSError:
                return

            for i, entry in enumerate(entries):
                is_last = (i == len(entries) - 1)
                connector = "└── " if is_last else "├── "
                next_prefix = prefix + ("    " if is_last else "│   ")

                full_path = os.path.join(dirpath, entry)
                line = prefix + connector + entry

                if os.path.isdir(full_path):
                    line += "/"

                tree_lines.append(line)

                # Recurse into directories (with depth limit)
                if os.path.isdir(full_path):
                    rel_path = os.path.relpath(full_path, self.root_path)
                    if self.max_depth is None or rel_path.count(os.sep) < self.max_depth:
                        add_to_tree(full_path, next_prefix)

        add_to_tree(self.root_path)

        tree_str = "\n".join(tree_lines)

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(tree_str)
        else:
            print(tree_str)

        return tree_str

    def find_duplicate_files(self):
        """
        Find duplicate files based on size and content hash.

        Returns:
            dict: Dictionary mapping file sizes to lists of duplicate files
        """
        from hashlib import md5

        # Group files by size first
        size_groups = defaultdict(list)

        for file_info in self.traverse():
            if not file_info.is_dir:
                size_groups[file_info.size].append(file_info)

        # For groups with multiple files of same size, check content
        duplicates = {}

        for size, files in size_groups.items():
            if len(files) < 2:
                continue

            hash_groups = defaultdict(list)

            for file_info in files:
                try:
                    # Calculate hash of first 1024 bytes and file size
                    with open(file_info.path, 'rb') as f:
                        content = f.read(1024)
                        content_hash = md5(content).hexdigest()

                    hash_groups[content_hash].append(file_info)

                except OSError:
                    continue

            # Find actual duplicates
            for hash_value, dup_files in hash_groups.items():
                if len(dup_files) > 1:
                    duplicates[size] = dup_files

        return duplicates

    def cleanup_empty_directories(self, dry_run=True):
        """
        Remove empty directories recursively.

        Args:
            dry_run (bool): If True, only show what would be removed

        Returns:
            list: List of removed directories
        """
        removed = []

        # Walk bottom-up to remove empty directories
        for dirpath, dirnames, filenames in os.walk(self.root_path, topdown=False):
            # Skip root directory
            if dirpath == self.root_path:
                continue

            try:
                # Check if directory is empty
                if not dirnames and not filenames:
                    if dry_run:
                        print(f"Would remove empty directory: {dirpath}")
                    else:
                        os.rmdir(dirpath)
                        print(f"Removed empty directory: {dirpath}")
                    removed.append(dirpath)

            except OSError as e:
                print(f"Error removing {dirpath}: {e}")

        return removed


def traverse_with_progress(directory, progress_callback=None):
    """
    Traverse directory with progress reporting.

    Args:
        directory (str): Directory to traverse
        progress_callback (callable): Function called with (current_path, files_processed)

    Returns:
        list: List of all FileInfo objects
    """
    traverser = DirectoryTraverser(directory)
    results = []
    processed = 0

    for file_info in traverser.traverse():
        results.append(file_info)
        processed += 1

        if progress_callback and processed % 100 == 0:
            progress_callback(file_info.path, processed)

    return results


def find_files_by_pattern(directory, pattern):
    """
    Find files matching a glob pattern.

    Args:
        directory (str): Directory to search
        pattern (str): Glob pattern (e.g., "*.txt", "**/*.py")

    Returns:
        list: List of matching file paths
    """
    import glob

    if '**' in pattern:
        # Recursive glob
        matches = glob.glob(os.path.join(directory, pattern), recursive=True)
    else:
        # Simple glob
        matches = glob.glob(os.path.join(directory, pattern))

    return [os.path.abspath(match) for match in matches]


def get_disk_usage(directory):
    """
    Get disk usage information for a directory.

    Args:
        directory (str): Directory to analyze

    Returns:
        dict: Disk usage statistics
    """
    traverser = DirectoryTraverser(directory)
    stats = traverser.get_directory_stats()

    # Add disk space information
    try:
        statvfs = os.statvfs(directory)
        stats['disk_total'] = statvfs.f_blocks * statvfs.f_frsize
        stats['disk_free'] = statvfs.f_bavail * statvfs.f_frsize
        stats['disk_used'] = stats['disk_total'] - stats['disk_free']
    except AttributeError:
        # statvfs not available on Windows
        stats['disk_total'] = None
        stats['disk_free'] = None
        stats['disk_used'] = None

    return stats


# Example usage and demonstrations
def demonstrate_directory_traversal():
    """Demonstrate various directory traversal operations."""

    print("=== Directory Traversal Demo ===\n")

    # Use current directory for demo
    demo_dir = os.getcwd()

    print(f"Analyzing directory: {demo_dir}\n")

    # Create traverser
    traverser = DirectoryTraverser(demo_dir, max_depth=3)

    print("1. Directory Statistics:")
    stats = traverser.get_directory_stats()
    print(f"   Total files: {stats['total_files']}")
    print(f"   Total directories: {stats['total_dirs']}")
    print(f"   Total size: {stats['total_size']:,} bytes")
    print(f"   File types: {dict(stats['file_types'])}")
    print()

    print("2. Finding Python files:")
    py_files = traverser.find_files_by_extension(['.py'])
    print(f"   Found {len(py_files)} Python files")
    if py_files:
        print(f"   Largest: {max(py_files, key=lambda x: x.size).name} ({max(py_files, key=lambda x: x.size).size} bytes)")
    print()

    print("3. Finding large files (>1MB):")
    large_files = traverser.find_large_files(1024 * 1024)
    print(f"   Found {len(large_files)} large files")
    if large_files:
        largest = max(large_files, key=lambda x: x.size)
        print(f"   Largest: {largest.name} ({largest.size:,} bytes)")
    print()

    print("4. Finding recent files (last 24 hours):")
    recent_files = traverser.find_recent_files(24)
    print(f"   Found {len(recent_files)} recently modified files")
    print()

    print("5. Directory Tree (first 20 lines):")
    tree = traverser.create_directory_tree()
    tree_lines = tree.split('\n')[:20]
    print('\n'.join(tree_lines))
    if len(tree.split('\n')) > 20:
        print("   ... (truncated)")
    print()

    print("6. Disk Usage:")
    usage = get_disk_usage(demo_dir)
    if usage['disk_total']:
        print(f"   Disk total: {usage['disk_total']:,} bytes")
        print(f"   Disk free: {usage['disk_free']:,} bytes")
        print(f"   Disk used: {usage['disk_used']:,} bytes")
    else:
        print("   Disk usage information not available on this platform")
    print()

    print("Demo completed!")


if __name__ == "__main__":
    demonstrate_directory_traversal()
