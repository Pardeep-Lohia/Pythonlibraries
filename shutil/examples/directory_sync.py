#!/usr/bin/env python3
"""
Directory Synchronization Example

This script demonstrates how to synchronize two directories using shutil,
ensuring that the destination directory mirrors the source directory.
"""

import shutil
import os
import time
from pathlib import Path
from typing import Set, Tuple


def get_directory_contents(path: Path) -> Set[Path]:
    """Get all files in a directory recursively as relative paths."""
    contents = set()
    try:
        for item in path.rglob('*'):
            if item.is_file():
                contents.add(item.relative_to(path))
    except PermissionError:
        pass
    return contents


def synchronize_directories(source_dir: str, dest_dir: str, verbose: bool = True) -> Tuple[int, int, int]:
    """
    Synchronize destination directory with source directory.

    Returns:
        Tuple of (files_copied, files_removed, files_skipped)
    """
    source_path = Path(source_dir)
    dest_path = Path(dest_dir)

    if not source_path.exists():
        raise ValueError(f"Source directory {source_dir} does not exist")

    # Ensure destination directory exists
    dest_path.mkdir(parents=True, exist_ok=True)

    # Get contents of both directories
    source_files = get_directory_contents(source_path)
    dest_files = get_directory_contents(dest_path)

    files_copied = 0
    files_removed = 0
    files_skipped = 0

    # Copy new or modified files from source to destination
    for rel_path in source_files:
        source_file = source_path / rel_path
        dest_file = dest_path / rel_path

        # Check if file needs to be copied
        needs_copy = (
            not dest_file.exists() or
            source_file.stat().st_mtime > dest_file.stat().st_mtime or
            source_file.stat().st_size != dest_file.stat().st_size
        )

        if needs_copy:
            # Create destination directory if needed
            dest_file.parent.mkdir(parents=True, exist_ok=True)

            try:
                shutil.copy2(source_file, dest_file)
                files_copied += 1
                if verbose:
                    print(f"Copied: {rel_path}")
            except (OSError, IOError) as e:
                print(f"Error copying {rel_path}: {e}")
        else:
            files_skipped += 1
            if verbose:
                print(f"Skipped (up to date): {rel_path}")

    # Remove files from destination that don't exist in source
    for rel_path in dest_files - source_files:
        dest_file = dest_path / rel_path
        try:
            dest_file.unlink()
            files_removed += 1
            if verbose:
                print(f"Removed: {rel_path}")
        except OSError as e:
            print(f"Error removing {rel_path}: {e}")

    return files_copied, files_removed, files_skipped


def create_test_directories():
    """Create test directories for demonstration."""
    print("Creating test directories...")

    # Create source directory structure
    source_dir = Path("sync_source")
    source_dir.mkdir(exist_ok=True)

    # Create some files
    (source_dir / "file1.txt").write_text("Content of file 1")
    (source_dir / "file2.txt").write_text("Content of file 2")

    # Create subdirectory
    sub_dir = source_dir / "subdir"
    sub_dir.mkdir(exist_ok=True)
    (sub_dir / "file3.txt").write_text("Content of file 3")

    # Create destination directory with some differences
    dest_dir = Path("sync_dest")
    dest_dir.mkdir(exist_ok=True)

    (dest_dir / "file1.txt").write_text("Different content")  # Different content
    (dest_dir / "old_file.txt").write_text("This should be removed")  # Extra file

    print("Test directories created.")


def demonstrate_basic_sync():
    """Demonstrate basic directory synchronization."""
    print("\n=== Basic Directory Synchronization ===")

    create_test_directories()

    print("\nBefore synchronization:")
    print("Source contents:")
    for file in sorted(Path("sync_source").rglob('*')):
        if file.is_file():
            print(f"  {file.relative_to('sync_source')}")

    print("Destination contents:")
    for file in sorted(Path("sync_dest").rglob('*')):
        if file.is_file():
            print(f"  {file.relative_to('sync_dest')}")

    # Perform synchronization
    copied, removed, skipped = synchronize_directories("sync_source", "sync_dest")

    print("Synchronization complete:")
    print(f"  Files copied: {copied}")
    print(f"  Files removed: {removed}")
    print(f"  Files skipped: {skipped}")

    print("\nAfter synchronization:")
    print("Destination contents:")
    for file in sorted(Path("sync_dest").rglob('*')):
        if file.is_file():
            print(f"  {file.relative_to('sync_dest')}")


def demonstrate_incremental_sync():
    """Demonstrate incremental synchronization."""
    print("\n=== Incremental Synchronization ===")

    # Modify source directory
    time.sleep(1)  # Ensure timestamp difference
    source_path = Path("sync_source")
    (source_path / "file4.txt").write_text("New file added")
    (source_path / "file2.txt").write_text("Modified content")  # Modify existing file

    print("Modified source directory (added file4.txt, modified file2.txt)")

    # Sync again
    copied, removed, skipped = synchronize_directories("sync_source", "sync_dest", verbose=True)

    print("Incremental sync complete:")
    print(f"  Files copied: {copied}")
    print(f"  Files removed: {removed}")
    print(f"  Files skipped: {skipped}")


def demonstrate_backup_sync():
    """Demonstrate backup-style synchronization."""
    print("\n=== Backup Synchronization ===")

    # Create backup directory with timestamp
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backup_{timestamp}"

    copied, removed, skipped = synchronize_directories("sync_source", backup_dir)

    print(f"Backup created in {backup_dir}")
    print(f"  Files copied: {copied}")
    print(f"  Files removed: {removed}")
    print(f"  Files skipped: {skipped}")

    # Clean up backup for demo
    shutil.rmtree(backup_dir)


def demonstrate_dry_run():
    """Demonstrate dry-run synchronization (preview changes)."""
    print("\n=== Dry Run Synchronization ===")

    # Modify destination to have differences
    dest_path = Path("sync_dest")
    (dest_path / "extra_file.txt").write_text("This should be removed")
    (dest_path / "file1.txt").write_text("Modified in dest")

    def preview_sync(source_dir: str, dest_dir: str) -> Tuple[int, int, int]:
        """Preview what would be synchronized without making changes."""
        source_path = Path(source_dir)
        dest_path = Path(dest_dir)

        source_files = get_directory_contents(source_path)
        dest_files = get_directory_contents(dest_path)

        would_copy = 0
        would_remove = 0

        # Check what would be copied
        for rel_path in source_files:
            source_file = source_path / rel_path
            dest_file = dest_path / rel_path

            needs_copy = (
                not dest_file.exists() or
                source_file.stat().st_mtime > dest_file.stat().st_mtime or
                source_file.stat().st_size != dest_file.stat().st_size
            )

            if needs_copy:
                would_copy += 1
                print(f"Would copy: {rel_path}")

        # Check what would be removed
        for rel_path in dest_files - source_files:
            would_remove += 1
            print(f"Would remove: {rel_path}")

        return would_copy, would_remove, 0

    print("Preview of changes:")
    would_copy, would_remove, _ = preview_sync("sync_source", "sync_dest")
    print(f"\nWould copy {would_copy} files, remove {would_remove} files")


def cleanup_demo():
    """Clean up demonstration files."""
    print("\n=== Cleaning Up ===")

    dirs_to_remove = ["sync_source", "sync_dest"]
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Removed {dir_name}")

    print("Cleanup complete.")


def main():
    """Run all synchronization demonstrations."""
    print("Directory Synchronization Examples")
    print("=" * 40)

    try:
        demonstrate_basic_sync()
        demonstrate_incremental_sync()
        demonstrate_backup_sync()
        demonstrate_dry_run()
    finally:
        cleanup_demo()

    print("\nAll demonstrations completed!")


if __name__ == "__main__":
    main()
