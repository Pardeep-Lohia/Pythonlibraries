#!/usr/bin/env python3
"""
Directory Copying Implementations using shutil

This module demonstrates various directory copying techniques using the shutil module,
including recursive copying, selective copying, and advanced copy operations.
"""

import shutil
import os
import time
import fnmatch
from pathlib import Path
from typing import List, Optional, Callable, Set


class DirectoryCopier:
    """A class for advanced directory copying operations."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def copy_directory_basic(self, src: str, dst: str) -> bool:
        """Basic recursive directory copy."""
        try:
            shutil.copytree(src, dst)
            if self.verbose:
                print(f"Copied directory {src} -> {dst}")
            return True
        except (IOError, OSError) as e:
            if self.verbose:
                print(f"Error copying directory {src}: {e}")
            return False

    def copy_directory_selective(self, src: str, dst: str, ignore_patterns: List[str] = None) -> bool:
        """Copy directory with selective file inclusion/exclusion."""
        def ignore_function(directory, contents):
            ignored = []
            if ignore_patterns:
                for pattern in ignore_patterns:
                    ignored.extend(fnmatch.filter(contents, pattern))
            return set(ignored)

        try:
            shutil.copytree(src, dst, ignore=ignore_function)
            if self.verbose:
                print(f"Selectively copied directory {src} -> {dst}")
            return True
        except (IOError, OSError) as e:
            if self.verbose:
                print(f"Error copying directory {src}: {e}")
            return False

    def copy_directory_incremental(self, src: str, dst: str) -> int:
        """Copy directory incrementally (only newer or missing files)."""
        copied_count = 0

        for src_path in Path(src).rglob('*'):
            if src_path.is_file():
                relative_path = src_path.relative_to(src)
                dst_path = Path(dst) / relative_path

                # Create destination directory if needed
                dst_path.parent.mkdir(parents=True, exist_ok=True)

                # Copy if destination doesn't exist or source is newer
                if not dst_path.exists() or src_path.stat().st_mtime > dst_path.stat().st_mtime:
                    shutil.copy2(src_path, dst_path)
                    copied_count += 1
                    if self.verbose:
                        print(f"Copied: {relative_path}")

        return copied_count

    def mirror_directory(self, src: str, dst: str) -> tuple[int, int]:
        """Mirror source directory to destination (sync)."""
        copied = 0
        removed = 0

        # Get all files in source
        src_files = set()
        for src_path in Path(src).rglob('*'):
            if src_path.is_file():
                relative_path = src_path.relative_to(src)
                src_files.add(relative_path)

                dst_path = Path(dst) / relative_path
                dst_path.parent.mkdir(parents=True, exist_ok=True)

                # Copy if needed
                if not dst_path.exists() or src_path.stat().st_mtime > dst_path.stat().st_mtime:
                    shutil.copy2(src_path, dst_path)
                    copied += 1
                    if self.verbose:
                        print(f"Copied: {relative_path}")

        # Remove files not in source
        dst_files = set()
        for dst_path in Path(dst).rglob('*'):
            if dst_path.is_file():
                relative_path = dst_path.relative_to(dst)
                dst_files.add(relative_path)

        to_remove = dst_files - src_files
        for relative_path in to_remove:
            (Path(dst) / relative_path).unlink()
            removed += 1
            if self.verbose:
                print(f"Removed: {relative_path}")

        return copied, removed

    def copy_with_transform(self, src: str, dst: str, transform_func: Callable[[str], str] = None) -> bool:
        """Copy directory with content transformation."""
        try:
            for src_path in Path(src).rglob('*'):
                if src_path.is_file():
                    relative_path = src_path.relative_to(src)
                    dst_path = Path(dst) / relative_path

                    dst_path.parent.mkdir(parents=True, exist_ok=True)

                    if transform_func and src_path.suffix == '.txt':
                        # Transform text files
                        content = src_path.read_text()
                        transformed = transform_func(content)
                        dst_path.write_text(transformed)
                    else:
                        # Copy other files normally
                        shutil.copy2(src_path, dst_path)

                    if self.verbose:
                        print(f"Processed: {relative_path}")

            return True
        except (IOError, OSError) as e:
            if self.verbose:
                print(f"Error copying directory {src}: {e}")
            return False


def demonstrate_basic_directory_copying():
    """Demonstrate basic directory copying operations."""
    print("=== Basic Directory Copying Demo ===")

    # Create a sample directory structure
    os.makedirs("source_dir/subdir/nested", exist_ok=True)
    with open("source_dir/file1.txt", 'w') as f:
        f.write("File 1 content\n")
    with open("source_dir/subdir/file2.txt", 'w') as f:
        f.write("File 2 content\n")
    with open("source_dir/subdir/nested/file3.txt", 'w') as f:
        f.write("Nested file content\n")

    copier = DirectoryCopier(verbose=True)

    # Basic copy
    copier.copy_directory_basic("source_dir", "basic_copy")

    # List copied structure
    print("\nCopied structure:")
    for root, dirs, files in os.walk("basic_copy"):
        level = root.replace("basic_copy", "").count(os.sep)
        indent = " " * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = " " * 2 * (level + 1)
        for file in files:
            print(f"{subindent}{file}")


def demonstrate_selective_copying():
    """Demonstrate selective directory copying."""
    print("\n=== Selective Directory Copying Demo ===")

    # Create directory with various files
    os.makedirs("selective_src", exist_ok=True)
    files_to_create = [
        "important.txt", "temp.tmp", "cache.dat", "config.ini",
        "script.py", "data.bin", "__pycache__/module.pyc"
    ]

    for file in files_to_create:
        full_path = os.path.join("selective_src", file)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(f"Content of {file}\n")

    copier = DirectoryCopier(verbose=True)

    # Copy excluding temporary and cache files
    ignore_patterns = ["*.tmp", "*.dat", "__pycache__"]
    copier.copy_directory_selective("selective_src", "selective_copy", ignore_patterns)

    print("\nFiles in selective copy:")
    for root, dirs, files in os.walk("selective_copy"):
        for file in files:
            print(f"  {os.path.join(root, file).replace('selective_copy/', '')}")


def demonstrate_incremental_copying():
    """Demonstrate incremental directory copying."""
    print("\n=== Incremental Directory Copying Demo ===")

    # Create source directory
    os.makedirs("incremental_src", exist_ok=True)
    with open("incremental_src/file1.txt", 'w') as f:
        f.write("File 1\n")

    # Initial copy
    copier = DirectoryCopier(verbose=True)
    copied = copier.copy_directory_incremental("incremental_src", "incremental_dst")
    print(f"Initial copy: {copied} files")

    # Wait and add/modify files
    time.sleep(1)
    with open("incremental_src/file2.txt", 'w') as f:
        f.write("File 2\n")
    with open("incremental_src/file1.txt", 'a') as f:
        f.write("Modified\n")

    # Incremental copy
    copied = copier.copy_directory_incremental("incremental_src", "incremental_dst")
    print(f"Incremental copy: {copied} files")

    print("\nFinal destination contents:")
    for file in sorted(os.listdir("incremental_dst")):
        print(f"  {file}")


def demonstrate_directory_mirroring():
    """Demonstrate directory mirroring/synchronization."""
    print("\n=== Directory Mirroring Demo ===")

    # Create source directory
    os.makedirs("mirror_src", exist_ok=True)
    with open("mirror_src/keep.txt", 'w') as f:
        f.write("Keep this file\n")
    with open("mirror_src/modify.txt", 'w') as f:
        f.write("Will be modified\n")

    # Create destination with some differences
    os.makedirs("mirror_dst", exist_ok=True)
    with open("mirror_dst/keep.txt", 'w') as f:
        f.write("Keep this file\n")
    with open("mirror_dst/modify.txt", 'w') as f:
        f.write("Original content\n")
    with open("mirror_dst/remove.txt", 'w') as f:
        f.write("Will be removed\n")

    print("Before mirroring:")
    print("Source:", sorted(os.listdir("mirror_src")))
    print("Destination:", sorted(os.listdir("mirror_dst")))

    copier = DirectoryCopier(verbose=True)
    copied, removed = copier.mirror_directory("mirror_src", "mirror_dst")

    print(f"\nMirroring complete: {copied} copied, {removed} removed")
    print("After mirroring:")
    print("Destination:", sorted(os.listdir("mirror_dst")))


def demonstrate_transform_copying():
    """Demonstrate copying with content transformation."""
    print("\n=== Transform Copying Demo ===")

    # Create source with text files
    os.makedirs("transform_src", exist_ok=True)
    with open("transform_src/document.txt", 'w') as f:
        f.write("This is a SECRET document.\nContains CONFIDENTIAL information.\n")
    with open("transform_src/notes.txt", 'w') as f:
        f.write("Meeting notes: TODO implement feature X.\n")
    with open("transform_src/data.bin", 'wb') as f:
        f.write(b"binary data here")

    def redact_sensitive(content):
        """Redact sensitive information."""
        return content.replace("SECRET", "[REDACTED]").replace("CONFIDENTIAL", "[REDACTED]")

    copier = DirectoryCopier(verbose=True)
    copier.copy_with_transform("transform_src", "transform_dst", redact_sensitive)

    print("\nTransformed files:")
    for file in sorted(os.listdir("transform_dst")):
        file_path = os.path.join("transform_dst", file)
        if file.endswith('.txt'):
            with open(file_path, 'r') as f:
                content = f.read().strip()
                print(f"  {file}: {content}")
        else:
            print(f"  {file}: (binary file)")


def demonstrate_pathlib_integration():
    """Demonstrate integration with pathlib."""
    print("\n=== Pathlib Integration Demo ===")

    # Create directory structure using pathlib
    base_dir = Path("pathlib_demo")
    base_dir.mkdir(exist_ok=True)

    (base_dir / "docs" / "readme.txt").parent.mkdir(parents=True, exist_ok=True)
    (base_dir / "docs" / "readme.txt").write_text("README content")
    (base_dir / "src" / "main.py").parent.mkdir(parents=True, exist_ok=True)
    (base_dir / "src" / "main.py").write_text("print('Hello')")

    copier = DirectoryCopier(verbose=True)

    # Copy using pathlib paths
    copier.copy_directory_basic(str(base_dir), "pathlib_copy")

    print("Directory copied using pathlib paths")


def demonstrate_error_handling():
    """Demonstrate error handling in directory operations."""
    print("\n=== Error Handling Demo ===")

    copier = DirectoryCopier(verbose=True)

    # Try to copy to existing directory
    os.makedirs("existing_dest", exist_ok=True)
    with open("existing_dest/file.txt", 'w') as f:
        f.write("existing\n")

    print("Attempting to copy to existing directory:")
    copier.copy_directory_basic("source_dir", "existing_dest")

    # Try to copy non-existent source
    print("\nAttempting to copy non-existent directory:")
    copier.copy_directory_basic("nonexistent", "should_fail")

    # Try to copy to read-only location
    readonly_dir = "readonly_dest"
    os.makedirs(readonly_dir, exist_ok=True)
    os.chmod(readonly_dir, 0o444)

    print("\nAttempting to copy to read-only directory:")
    copier.copy_directory_basic("source_dir", readonly_dir)

    # Restore permissions
    os.chmod(readonly_dir, 0o755)


def cleanup_demo_files():
    """Clean up files created during demonstrations."""
    print("\n=== Cleaning Up Demo Files ===")

    dirs_to_remove = [
        "source_dir", "basic_copy", "selective_src", "selective_copy",
        "incremental_src", "incremental_dst", "mirror_src", "mirror_dst",
        "transform_src", "transform_dst", "pathlib_demo", "pathlib_copy",
        "existing_dest", "readonly_dest"
    ]

    removed_count = 0
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            removed_count += 1

    print(f"Cleaned up {removed_count} directories")


def main():
    """Run all demonstrations."""
    print("Shutil Directory Copying Implementations")
    print("=" * 45)

    demonstrate_basic_directory_copying()
    demonstrate_selective_copying()
    demonstrate_incremental_copying()
    demonstrate_directory_mirroring()
    demonstrate_transform_copying()
    demonstrate_pathlib_integration()
    demonstrate_error_handling()

    cleanup_demo_files()

    print("\nAll demonstrations completed!")


if __name__ == "__main__":
    main()
