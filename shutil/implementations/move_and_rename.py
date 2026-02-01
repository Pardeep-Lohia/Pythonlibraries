#!/usr/bin/env python3
"""
File Moving and Renaming Implementations using shutil

This module demonstrates various file and directory moving and renaming techniques
using the shutil module, including cross-filesystem operations and error handling.
"""

import shutil
import os
import time
from pathlib import Path
from typing import List, Optional, Callable


class FileMover:
    """A class for advanced file moving operations."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def move_file(self, src: str, dst: str) -> bool:
        """Move a file from source to destination."""
        try:
            result = shutil.move(src, dst)
            if self.verbose:
                print(f"Moved {src} -> {result}")
            return True
        except (IOError, OSError) as e:
            if self.verbose:
                print(f"Error moving {src}: {e}")
            return False

    def rename_file(self, src: str, new_name: str) -> bool:
        """Rename a file within the same directory."""
        src_path = Path(src)
        dst_path = src_path.parent / new_name

        try:
            src_path.rename(dst_path)
            if self.verbose:
                print(f"Renamed {src} -> {dst_path}")
            return True
        except (IOError, OSError) as e:
            if self.verbose:
                print(f"Error renaming {src}: {e}")
            return False

    def move_multiple(self, sources: List[str], destination_dir: str) -> int:
        """Move multiple files to a destination directory."""
        success_count = 0
        os.makedirs(destination_dir, exist_ok=True)

        for src in sources:
            if os.path.exists(src):
                filename = os.path.basename(src)
                dst = os.path.join(destination_dir, filename)
                if self.move_file(src, dst):
                    success_count += 1
            else:
                if self.verbose:
                    print(f"Source does not exist: {src}")

        return success_count

    def move_with_backup(self, src: str, dst: str) -> bool:
        """Move file and create backup of existing destination."""
        if os.path.exists(dst):
            backup_path = dst + '.backup'
            try:
                shutil.copy2(dst, backup_path)
                if self.verbose:
                    print(f"Created backup: {backup_path}")
            except (IOError, OSError) as e:
                if self.verbose:
                    print(f"Failed to create backup: {e}")
                return False

        return self.move_file(src, dst)

    def safe_move(self, src: str, dst: str, overwrite: bool = False) -> bool:
        """Safely move file with overwrite control."""
        if os.path.exists(dst) and not overwrite:
            if self.verbose:
                print(f"Destination exists, skipping: {dst}")
            return False

        return self.move_file(src, dst)


def demonstrate_basic_moving():
    """Demonstrate basic file moving operations."""
    print("=== Basic File Moving Demo ===")

    # Create sample files
    sample_files = []
    for i in range(3):
        filename = f"move_sample_{i}.txt"
        with open(filename, 'w') as f:
            f.write(f"This is sample file {i}\nCreated: {time.ctime()}\n")
        sample_files.append(filename)

    mover = FileMover(verbose=True)

    # Move files to a subdirectory
    os.makedirs("moved_files", exist_ok=True)

    for file in sample_files:
        mover.move_file(file, f"moved_files/{file}")

    # List moved files
    if os.path.exists("moved_files"):
        print("Files in moved_files/:")
        for file in os.listdir("moved_files"):
            print(f"  {file}")


def demonstrate_renaming():
    """Demonstrate file renaming operations."""
    print("\n=== File Renaming Demo ===")

    # Create a file to rename
    original = "original_name.txt"
    with open(original, 'w') as f:
        f.write("File with original name\n")

    mover = FileMover(verbose=True)

    # Rename the file
    mover.rename_file(original, "renamed_file.txt")

    # Verify rename
    if os.path.exists("renamed_file.txt") and not os.path.exists(original):
        print("Rename successful")
    else:
        print("Rename failed")


def demonstrate_directory_moving():
    """Demonstrate directory moving operations."""
    print("\n=== Directory Moving Demo ===")

    # Create a directory structure
    os.makedirs("source_dir/subdir", exist_ok=True)
    with open("source_dir/file1.txt", 'w') as f:
        f.write("File 1 content\n")
    with open("source_dir/subdir/file2.txt", 'w') as f:
        f.write("File 2 content\n")

    mover = FileMover(verbose=True)

    # Move the entire directory
    mover.move_file("source_dir", "moved_directory")

    # Verify move
    if os.path.exists("moved_directory") and not os.path.exists("source_dir"):
        print("Directory move successful")
        # List contents
        for root, dirs, files in os.walk("moved_directory"):
            level = root.replace("moved_directory", "").count(os.sep)
            indent = " " * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = " " * 2 * (level + 1)
            for file in files:
                print(f"{subindent}{file}")
    else:
        print("Directory move failed")


def demonstrate_batch_moving():
    """Demonstrate moving multiple files."""
    print("\n=== Batch File Moving Demo ===")

    # Create multiple files
    batch_files = []
    for i in range(5):
        filename = f"batch_file_{i}.txt"
        with open(filename, 'w') as f:
            f.write(f"Batch file {i} content\n")
        batch_files.append(filename)

    mover = FileMover(verbose=True)
    success_count = mover.move_multiple(batch_files, "batch_destination")

    print(f"\nSuccessfully moved {success_count} files to batch_destination/")

    # List moved files
    if os.path.exists("batch_destination"):
        print("Moved files:")
        for file in sorted(os.listdir("batch_destination")):
            print(f"  {file}")


def demonstrate_safe_moving():
    """Demonstrate safe moving with backup and overwrite control."""
    print("\n=== Safe Moving Demo ===")

    # Create source and destination files
    src_file = "safe_source.txt"
    dst_file = "safe_destination.txt"

    with open(src_file, 'w') as f:
        f.write("Source file content\n")

    with open(dst_file, 'w') as f:
        f.write("Existing destination content\n")

    mover = FileMover(verbose=True)

    # Try to move without overwrite (should fail)
    print("Attempting move without overwrite:")
    mover.safe_move(src_file, dst_file, overwrite=False)

    # Move with overwrite
    print("\nMoving with overwrite:")
    mover.safe_move(src_file, dst_file, overwrite=True)

    # Move with backup
    print("\nMoving with backup:")
    with open("backup_source.txt", 'w') as f:
        f.write("Content for backup demo\n")

    mover.move_with_backup("backup_source.txt", dst_file)


def demonstrate_pathlib_integration():
    """Demonstrate integration with pathlib."""
    print("\n=== Pathlib Integration Demo ===")

    # Create directory structure using pathlib
    base_dir = Path("pathlib_demo")
    base_dir.mkdir(exist_ok=True)

    (base_dir / "file1.txt").write_text("Pathlib file 1")
    (base_dir / "file2.txt").write_text("Pathlib file 2")

    mover = FileMover(verbose=True)

    # Move using pathlib paths
    mover.move_file(str(base_dir / "file1.txt"), "pathlib_moved1.txt")
    mover.move_file(str(base_dir / "file2.txt"), "pathlib_moved2.txt")

    print("Files moved using pathlib paths")


def demonstrate_cross_platform():
    """Demonstrate cross-platform moving considerations."""
    print("\n=== Cross-Platform Demo ===")

    import platform
    system = platform.system()

    print(f"Running on {system}")

    # Create test files
    test_file = "cross_platform_test.txt"
    with open(test_file, 'w') as f:
        f.write(f"Created on {system}\n")

    mover = FileMover(verbose=True)

    # Move to platform-specific location
    if system == 'Windows':
        dest_dir = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'shutil_test')
    else:
        dest_dir = '/tmp/shutil_test'

    os.makedirs(dest_dir, exist_ok=True)
    mover.move_file(test_file, os.path.join(dest_dir, test_file))

    print(f"File moved to platform-specific location: {dest_dir}")


def demonstrate_error_handling():
    """Demonstrate error handling in move operations."""
    print("\n=== Error Handling Demo ===")

    mover = FileMover(verbose=True)

    # Try to move non-existent file
    print("Attempting to move non-existent file:")
    mover.move_file("nonexistent.txt", "should_fail.txt")

    # Try to move to read-only directory
    readonly_dir = "readonly_test"
    os.makedirs(readonly_dir, exist_ok=True)
    os.chmod(readonly_dir, 0o444)  # Read-only

    test_file = "error_test.txt"
    with open(test_file, 'w') as f:
        f.write("Test content\n")

    print("\nAttempting to move to read-only directory:")
    mover.move_file(test_file, os.path.join(readonly_dir, "test.txt"))

    # Restore permissions for cleanup
    os.chmod(readonly_dir, 0o755)


def cleanup_demo_files():
    """Clean up files created during demonstrations."""
    print("\n=== Cleaning Up Demo Files ===")

    files_to_remove = [
        "renamed_file.txt", "safe_destination.txt", "safe_destination.txt.backup",
        "pathlib_moved1.txt", "pathlib_moved2.txt", "cross_platform_test.txt",
        "should_fail.txt", "error_test.txt"
    ]

    dirs_to_remove = [
        "moved_files", "moved_directory", "batch_destination",
        "pathlib_demo", "readonly_test"
    ]

    removed_count = 0
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            removed_count += 1

    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            removed_count += 1

    print(f"Cleaned up {removed_count} items")


def main():
    """Run all demonstrations."""
    print("Shutil File Moving and Renaming Implementations")
    print("=" * 50)

    demonstrate_basic_moving()
    demonstrate_renaming()
    demonstrate_directory_moving()
    demonstrate_batch_moving()
    demonstrate_safe_moving()
    demonstrate_pathlib_integration()
    demonstrate_cross_platform()
    demonstrate_error_handling()

    cleanup_demo_files()

    print("\nAll demonstrations completed!")


if __name__ == "__main__":
    main()
