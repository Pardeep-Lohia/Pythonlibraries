#!/usr/bin/env python3
"""
File Operations Examples with pathlib

This module demonstrates various file operations using pathlib.Path,
including reading, writing, copying, moving, and metadata handling.
"""

from pathlib import Path
import shutil
import os
import hashlib
from datetime import datetime


def basic_file_reading_writing():
    """Demonstrate basic file read/write operations."""
    print("=== Basic File Reading/Writing ===")

    # Create a sample file
    sample_file = Path('sample.txt')
    content = "Hello, pathlib!\nThis is a sample file.\n"

    # Write text to file
    sample_file.write_text(content, encoding='utf-8')
    print(f"Created file: {sample_file}")

    # Read text from file
    read_content = sample_file.read_text(encoding='utf-8')
    print(f"Read content: {read_content!r}")

    # Read lines
    lines = sample_file.read_text(encoding='utf-8').splitlines()
    print(f"Lines: {lines}")

    # Clean up
    sample_file.unlink()
    print(f"Deleted file: {sample_file}")


def binary_file_operations():
    """Demonstrate binary file operations."""
    print("\n=== Binary File Operations ===")

    binary_file = Path('binary.dat')
    data = b'\x00\x01\x02\x03\xff\xfe\xfd'

    # Write binary data
    binary_file.write_bytes(data)
    print(f"Created binary file: {binary_file}")

    # Read binary data
    read_data = binary_file.read_bytes()
    print(f"Read data: {read_data}")
    print(f"Data matches: {data == read_data}")

    # Clean up
    binary_file.unlink()


def file_copying_operations():
    """Demonstrate file copying operations."""
    print("\n=== File Copying Operations ===")

    # Create source file
    source = Path('source.txt')
    source.write_text("This is the source file content.")

    # Copy using shutil (pathlib doesn't have copy methods)
    dest1 = Path('dest1.txt')
    shutil.copy(source, dest1)
    print(f"Copied {source} to {dest1}")

    # Copy with metadata preservation
    dest2 = Path('dest2.txt')
    shutil.copy2(source, dest2)
    print(f"Copied with metadata {source} to {dest2}")

    # Verify contents
    assert dest1.read_text() == dest2.read_text() == source.read_text()

    # Clean up
    source.unlink()
    dest1.unlink()
    dest2.unlink()


def file_moving_renaming():
    """Demonstrate file moving and renaming."""
    print("\n=== File Moving and Renaming ===")

    # Create a file
    original = Path('original.txt')
    original.write_text("Original content")

    # Rename using Path methods
    renamed = original.with_name('renamed.txt')
    original.rename(renamed)
    print(f"Renamed {original} to {renamed}")

    # Move to different directory
    target_dir = Path('moved_files')
    target_dir.mkdir(exist_ok=True)

    moved = target_dir / 'moved.txt'
    renamed.rename(moved)
    print(f"Moved {renamed} to {moved}")

    # Verify content
    assert moved.read_text() == "Original content"

    # Clean up
    moved.unlink()
    target_dir.rmdir()


def file_metadata_operations():
    """Demonstrate file metadata operations."""
    print("\n=== File Metadata Operations ===")

    # Create a test file
    test_file = Path('metadata_test.txt')
    test_file.write_text("Test content for metadata")

    # Get file statistics
    stat_info = test_file.stat()
    print(f"File size: {stat_info.st_size} bytes")
    print(f"Modified time: {datetime.fromtimestamp(stat_info.st_mtime)}")

    # Check permissions (Unix-like systems)
    if os.name != 'nt':  # Not Windows
        import stat
        mode = stat.filemode(stat_info.st_mode)
        print(f"Permissions: {mode}")

    # Change permissions
    if os.name != 'nt':
        # Make readable/writable by owner only
        test_file.chmod(0o600)
        print("Changed permissions to 600")

    # Clean up
    test_file.unlink()


def creating_empty_files():
    """Demonstrate creating empty files."""
    print("\n=== Creating Empty Files ===")

    # Create empty file
    empty_file = Path('empty.txt')
    empty_file.touch()
    print(f"Created empty file: {empty_file}")
    print(f"File exists: {empty_file.exists()}")
    print(f"File size: {empty_file.stat().st_size}")

    # Touch existing file (updates timestamp)
    existing = Path('existing.txt')
    existing.write_text("Existing content")
    original_mtime = existing.stat().st_mtime

    # Wait a moment and touch
    import time
    time.sleep(0.1)
    existing.touch()

    new_mtime = existing.stat().st_mtime
    print(f"Timestamp updated: {new_mtime > original_mtime}")

    # Clean up
    empty_file.unlink()
    existing.unlink()


def safe_file_operations():
    """Demonstrate safe file operations with error handling."""
    print("\n=== Safe File Operations ===")

    def safe_read_text(file_path: Path, default="") -> str:
        """Safely read text from file."""
        try:
            if file_path.exists() and file_path.is_file():
                return file_path.read_text(encoding='utf-8')
        except (OSError, UnicodeDecodeError) as e:
            print(f"Error reading {file_path}: {e}")
        return default

    def safe_write_text(file_path: Path, content: str) -> bool:
        """Safely write text to file."""
        try:
            file_path.write_text(content, encoding='utf-8')
            return True
        except OSError as e:
            print(f"Error writing {file_path}: {e}")
            return False

    # Test safe operations
    test_file = Path('safe_test.txt')

    # Write safely
    success = safe_write_text(test_file, "Safe content")
    print(f"Write successful: {success}")

    # Read safely
    content = safe_read_text(test_file)
    print(f"Read content: {content!r}")

    # Try reading non-existent file
    nonexistent = safe_read_text(Path('nonexistent.txt'), "default")
    print(f"Non-existent file content: {nonexistent!r}")

    # Clean up
    if test_file.exists():
        test_file.unlink()


def file_hashing():
    """Demonstrate file hashing for integrity checks."""
    print("\n=== File Hashing ===")

    def get_file_hash(file_path: Path, algorithm='sha256') -> str:
        """Calculate hash of file contents."""
        hash_func = hashlib.new(algorithm)
        with file_path.open('rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                hash_func.update(chunk)
        return hash_func.hexdigest()

    # Create test files
    file1 = Path('file1.txt')
    file2 = Path('file2.txt')
    file3 = Path('file3.txt')

    file1.write_text("Same content")
    file2.write_text("Same content")
    file3.write_text("Different content")

    # Calculate hashes
    hash1 = get_file_hash(file1)
    hash2 = get_file_hash(file2)
    hash3 = get_file_hash(file3)

    print(f"File1 hash: {hash1}")
    print(f"File2 hash: {hash2}")
    print(f"File3 hash: {hash3}")
    print(f"File1 and File2 are identical: {hash1 == hash2}")
    print(f"File1 and File3 are identical: {hash1 == hash3}")

    # Clean up
    file1.unlink()
    file2.unlink()
    file3.unlink()


def batch_file_operations():
    """Demonstrate operations on multiple files."""
    print("\n=== Batch File Operations ===")

    # Create test directory structure
    test_dir = Path('batch_test')
    test_dir.mkdir(exist_ok=True)

    # Create multiple files
    for i in range(5):
        file_path = test_dir / f'file_{i}.txt'
        file_path.write_text(f"Content of file {i}")

    print(f"Created {len(list(test_dir.iterdir()))} files")

    # Find files by pattern
    txt_files = list(test_dir.glob('*.txt'))
    print(f"Found {len(txt_files)} .txt files")

    # Get file sizes
    file_sizes = {f.name: f.stat().st_size for f in txt_files}
    print(f"File sizes: {file_sizes}")

    # Rename all files
    for file_path in txt_files:
        new_name = file_path.with_stem(f"renamed_{file_path.stem}")
        file_path.rename(new_name)

    print("Renamed all files")

    # Delete all files
    for file_path in test_dir.iterdir():
        file_path.unlink()

    test_dir.rmdir()
    print("Cleaned up test directory")


def main():
    """Run all file operations examples."""
    print("Pathlib File Operations Examples")
    print("=" * 40)

    # Run all demonstrations
    basic_file_reading_writing()
    binary_file_operations()
    file_copying_operations()
    file_moving_renaming()
    file_metadata_operations()
    creating_empty_files()
    safe_file_operations()
    file_hashing()
    batch_file_operations()

    print("\n=== Summary ===")
    print("pathlib provides comprehensive file operations:")
    print("- Text and binary file I/O")
    print("- File copying, moving, and renaming")
    print("- Metadata access and modification")
    print("- Safe operations with error handling")
    print("- Batch operations on multiple files")
    print("- Integration with shutil for advanced operations")


if __name__ == '__main__':
    main()
