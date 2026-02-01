#!/usr/bin/env python3
"""
File Copying Implementations using shutil

This module demonstrates various file copying techniques using the shutil module,
including basic copying, metadata preservation, and advanced copy operations.
"""

import shutil
import os
import time
from pathlib import Path
from typing import List, Optional, Callable


class FileCopier:
    """A class for advanced file copying operations."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def copy_basic(self, src: str, dst: str) -> bool:
        """Basic file copy with minimal metadata preservation."""
        try:
            shutil.copy(src, dst)
            if self.verbose:
                print(f"Copied {src} -> {dst}")
            return True
        except (IOError, OSError) as e:
            if self.verbose:
                print(f"Error copying {src}: {e}")
            return False

    def copy_with_metadata(self, src: str, dst: str) -> bool:
        """Copy file with full metadata preservation."""
        try:
            shutil.copy2(src, dst)
            if self.verbose:
                print(f"Copied with metadata: {src} -> {dst}")
            return True
        except (IOError, OSError) as e:
            if self.verbose:
                print(f"Error copying {src}: {e}")
            return False

    def copy_multiple(self, sources: List[str], destination_dir: str) -> int:
        """Copy multiple files to a destination directory."""
        success_count = 0
        os.makedirs(destination_dir, exist_ok=True)

        for src in sources:
            if os.path.isfile(src):
                filename = os.path.basename(src)
                dst = os.path.join(destination_dir, filename)
                if self.copy_with_metadata(src, dst):
                    success_count += 1
            else:
                if self.verbose:
                    print(f"Skipping non-file: {src}")

        return success_count

    def copy_if_newer(self, src: str, dst: str) -> bool:
        """Copy file only if source is newer than destination."""
        if not os.path.exists(dst):
            return self.copy_with_metadata(src, dst)

        src_mtime = os.path.getmtime(src)
        dst_mtime = os.path.getmtime(dst)

        if src_mtime > dst_mtime:
            if self.verbose:
                print(f"Source is newer, copying: {src}")
            return self.copy_with_metadata(src, dst)
        else:
            if self.verbose:
                print(f"Destination is up to date: {dst}")
            return True  # Not an error, just no copy needed

    def copy_with_backup(self, src: str, dst: str) -> bool:
        """Copy file and create backup of existing destination."""
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

        return self.copy_with_metadata(src, dst)


def demonstrate_basic_copying():
    """Demonstrate basic file copying operations."""
    print("=== Basic File Copying Demo ===")

    # Create a sample file
    sample_file = "sample.txt"
    with open(sample_file, 'w') as f:
        f.write("This is a sample file for copying demonstrations.\n")
        f.write(f"Created at: {time.ctime()}\n")

    copier = FileCopier(verbose=True)

    # Basic copy
    copier.copy_basic(sample_file, "copy_basic.txt")

    # Copy with metadata
    copier.copy_with_metadata(sample_file, "copy_metadata.txt")

    # Show metadata differences
    print("\nMetadata comparison:")
    for filename in ["sample.txt", "copy_basic.txt", "copy_metadata.txt"]:
        if os.path.exists(filename):
            stat = os.stat(filename)
            print(f"{filename}: mode={oct(stat.st_mode)}, mtime={time.ctime(stat.st_mtime)}")


def demonstrate_batch_copying():
    """Demonstrate copying multiple files."""
    print("\n=== Batch File Copying Demo ===")

    # Create multiple sample files
    sample_files = []
    for i in range(3):
        filename = f"batch_file_{i}.txt"
        with open(filename, 'w') as f:
            f.write(f"This is batch file {i}\nCreated: {time.ctime()}\n")
        sample_files.append(filename)

    copier = FileCopier(verbose=True)
    success_count = copier.copy_multiple(sample_files, "batch_copies")

    print(f"\nSuccessfully copied {success_count} files to batch_copies/")

    # List copied files
    if os.path.exists("batch_copies"):
        print("Copied files:")
        for file in os.listdir("batch_copies"):
            print(f"  {file}")


def demonstrate_conditional_copying():
    """Demonstrate conditional copying based on timestamps."""
    print("\n=== Conditional Copying Demo ===")

    # Create source file
    src_file = "conditional_src.txt"
    with open(src_file, 'w') as f:
        f.write("Source file content\n")

    dst_file = "conditional_dst.txt"

    copier = FileCopier(verbose=True)

    # First copy
    print("First copy:")
    copier.copy_if_newer(src_file, dst_file)

    # Wait a bit and modify source
    time.sleep(1)
    with open(src_file, 'a') as f:
        f.write("Additional content\n")

    print("\nAfter modifying source:")
    copier.copy_if_newer(src_file, dst_file)

    # Try copying again (should skip)
    print("\nTrying to copy again (should skip):")
    copier.copy_if_newer(src_file, dst_file)


def demonstrate_backup_copying():
    """Demonstrate copying with backup creation."""
    print("\n=== Backup Copying Demo ===")

    # Create destination file
    dst_file = "backup_dst.txt"
    with open(dst_file, 'w') as f:
        f.write("Original destination content\n")

    src_file = "backup_src.txt"
    with open(src_file, 'w') as f:
        f.write("New source content\n")

    copier = FileCopier(verbose=True)

    print("Copying with backup:")
    copier.copy_with_backup(src_file, dst_file)

    # Check backup was created
    if os.path.exists(dst_file + '.backup'):
        print("Backup file created successfully")
        with open(dst_file + '.backup', 'r') as f:
            print(f"Backup content: {f.read().strip()}")


def demonstrate_pathlib_integration():
    """Demonstrate integration with pathlib."""
    print("\n=== Pathlib Integration Demo ===")

    # Create directory structure
    base_dir = Path("pathlib_demo")
    base_dir.mkdir(exist_ok=True)

    # Create source files
    (base_dir / "file1.txt").write_text("Content of file 1")
    (base_dir / "file2.txt").write_text("Content of file 2")

    # Copy using pathlib paths
    copier = FileCopier(verbose=True)

    copier.copy_with_metadata(str(base_dir / "file1.txt"), "pathlib_copy1.txt")
    copier.copy_with_metadata(str(base_dir / "file2.txt"), "pathlib_copy2.txt")

    print("Files copied using pathlib paths")


def demonstrate_error_handling():
    """Demonstrate error handling in copy operations."""
    print("\n=== Error Handling Demo ===")

    copier = FileCopier(verbose=True)

    # Try to copy non-existent file
    print("Attempting to copy non-existent file:")
    copier.copy_basic("nonexistent.txt", "should_fail.txt")

    # Try to copy to read-only directory
    readonly_dir = "readonly_test"
    os.makedirs(readonly_dir, exist_ok=True)
    os.chmod(readonly_dir, 0o444)  # Read-only

    print("\nAttempting to copy to read-only directory:")
    copier.copy_basic("sample.txt", os.path.join(readonly_dir, "test.txt"))

    # Restore permissions for cleanup
    os.chmod(readonly_dir, 0o755)


def cleanup_demo_files():
    """Clean up files created during demonstrations."""
    print("\n=== Cleaning Up Demo Files ===")

    files_to_remove = [
        "sample.txt", "copy_basic.txt", "copy_metadata.txt",
        "batch_file_0.txt", "batch_file_1.txt", "batch_file_2.txt",
        "conditional_src.txt", "conditional_dst.txt",
        "backup_src.txt", "backup_dst.txt", "backup_dst.txt.backup",
        "pathlib_copy1.txt", "pathlib_copy2.txt",
        "should_fail.txt"
    ]

    dirs_to_remove = ["batch_copies", "pathlib_demo", "readonly_test"]

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
    print("Shutil File Copying Implementations")
    print("=" * 40)

    demonstrate_basic_copying()
    demonstrate_batch_copying()
    demonstrate_conditional_copying()
    demonstrate_backup_copying()
    demonstrate_pathlib_integration()
    demonstrate_error_handling()

    cleanup_demo_files()

    print("\nAll demonstrations completed!")


if __name__ == "__main__":
    main()
