#!/usr/bin/env python3
"""
Archive Operations Implementations using shutil

This module demonstrates various archive creation and extraction techniques
using the shutil module, including different formats and advanced operations.
"""

import shutil
import os
import time
from pathlib import Path
from typing import List, Optional, Callable


class ArchiveManager:
    """A class for advanced archive operations."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def create_archive(self, source_path: str, archive_name: str, format: str = 'zip') -> str:
        """Create an archive from a file or directory."""
        source_path = Path(source_path)
        if not source_path.exists():
            raise FileNotFoundError(f"Source path does not exist: {source_path}")

        try:
            archive_path = shutil.make_archive(archive_name, format, str(source_path))
            if self.verbose:
                print(f"Created {format.upper()} archive: {archive_path}")
            return archive_path
        except Exception as e:
            if self.verbose:
                print(f"Error creating archive: {e}")
            raise

    def extract_archive(self, archive_path: str, extract_path: str) -> str:
        """Extract an archive to a directory."""
        archive_path = Path(archive_path)
        if not archive_path.exists():
            raise FileNotFoundError(f"Archive not found: {archive_path}")

        extract_path = Path(extract_path)
        extract_path.mkdir(parents=True, exist_ok=True)

        try:
            shutil.unpack_archive(str(archive_path), str(extract_path))
            if self.verbose:
                print(f"Extracted archive to: {extract_path}")
            return str(extract_path)
        except Exception as e:
            if self.verbose:
                print(f"Error extracting archive: {e}")
            raise

    def create_compressed_archive(self, source_path: str, archive_name: str,
                                format: str = 'gztar') -> str:
        """Create a compressed archive."""
        return self.create_archive(source_path, archive_name, format)

    def batch_create_archives(self, sources: List[str], archive_dir: str,
                            format: str = 'zip') -> List[str]:
        """Create archives for multiple sources."""
        archive_dir = Path(archive_dir)
        archive_dir.mkdir(parents=True, exist_ok=True)

        created_archives = []
        for source in sources:
            source_path = Path(source)
            if source_path.exists():
                archive_name = archive_dir / f"{source_path.name}_{int(time.time())}"
                try:
                    archive_path = self.create_archive(str(source_path), str(archive_name), format)
                    created_archives.append(archive_path)
                except Exception as e:
                    if self.verbose:
                        print(f"Failed to archive {source}: {e}")
            else:
                if self.verbose:
                    print(f"Source not found: {source}")

        return created_archives

    def batch_extract_archives(self, archives: List[str], extract_base: str) -> List[str]:
        """Extract multiple archives."""
        extract_base = Path(extract_base)
        extract_base.mkdir(parents=True, exist_ok=True)

        extracted_dirs = []
        for archive in archives:
            archive_path = Path(archive)
            if archive_path.exists():
                extract_name = archive_path.stem
                extract_path = extract_base / extract_name
                try:
                    self.extract_archive(str(archive_path), str(extract_path))
                    extracted_dirs.append(str(extract_path))
                except Exception as e:
                    if self.verbose:
                        print(f"Failed to extract {archive}: {e}")
            else:
                if self.verbose:
                    print(f"Archive not found: {archive}")

        return extracted_dirs

    def list_archive_contents(self, archive_path: str) -> List[str]:
        """List contents of an archive without extracting."""
        archive_path = Path(archive_path)
        if not archive_path.exists():
            raise FileNotFoundError(f"Archive not found: {archive_path}")

        contents = []
        try:
            if archive_path.suffix == '.zip':
                import zipfile
                with zipfile.ZipFile(str(archive_path), 'r') as zf:
                    contents = zf.namelist()
            elif archive_path.suffix in ['.tar', '.gz', '.bz2', '.xz']:
                import tarfile
                with tarfile.open(str(archive_path), 'r:*') as tf:
                    contents = [member.name for member in tf.getmembers()]
            else:
                raise ValueError(f"Unsupported archive format: {archive_path.suffix}")
        except Exception as e:
            if self.verbose:
                print(f"Error listing archive contents: {e}")
            raise

        return sorted(contents)

    def get_archive_info(self, archive_path: str) -> dict:
        """Get information about an archive."""
        archive_path = Path(archive_path)
        if not archive_path.exists():
            raise FileNotFoundError(f"Archive not found: {archive_path}")

        stat = archive_path.stat()
        info = {
            'path': str(archive_path),
            'size': stat.st_size,
            'size_mb': stat.st_size / (1024 * 1024),
            'modified': time.ctime(stat.st_mtime),
            'format': self._detect_format(archive_path)
        }

        try:
            contents = self.list_archive_contents(str(archive_path))
            info['file_count'] = len(contents)
            info['contents_preview'] = contents[:5]
        except Exception:
            info['file_count'] = 0
            info['contents_preview'] = []

        return info

    def _detect_format(self, archive_path: Path) -> str:
        """Detect archive format from file extension."""
        suffix = archive_path.suffix.lower()
        if suffix == '.zip':
            return 'zip'
        elif suffix == '.tar':
            return 'tar'
        elif suffix in ['.gz', '.tgz']:
            return 'gztar'
        elif suffix in ['.bz2', '.tbz2']:
            return 'bztar'
        elif suffix in ['.xz', '.txz']:
            return 'xztar'
        else:
            return 'unknown'

    def create_incremental_backup(self, source_dir: str, backup_dir: str,
                                last_backup_time: Optional[float] = None) -> Optional[str]:
        """Create an incremental backup of files modified since last backup."""
        source_path = Path(source_dir)
        backup_path = Path(backup_dir)
        backup_path.mkdir(parents=True, exist_ok=True)

        # Find files modified since last backup
        modified_files = []
        for file_path in source_path.rglob('*'):
            if file_path.is_file():
                if last_backup_time is None or file_path.stat().st_mtime > last_backup_time:
                    modified_files.append(str(file_path))

        if not modified_files:
            if self.verbose:
                print("No files modified since last backup")
            return None

        # Create temporary directory for incremental files
        temp_dir = backup_path / f"incremental_{int(time.time())}"
        temp_dir.mkdir()

        try:
            # Copy modified files to temp directory
            for file_path in modified_files:
                rel_path = os.path.relpath(file_path, source_dir)
                dest_path = temp_dir / rel_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, str(dest_path))

            # Create archive
            archive_name = f"incremental_backup_{int(time.time())}"
            archive_path = self.create_archive(str(temp_dir), str(backup_path / archive_name))

            return archive_path

        finally:
            # Clean up temp directory
            shutil.rmtree(str(temp_dir))

    def extract_with_progress(self, archive_path: str, extract_path: str,
                            progress_callback: Optional[Callable] = None) -> str:
        """Extract archive with progress reporting."""
        archive_path = Path(archive_path)
        extract_path = Path(extract_path)
        extract_path.mkdir(parents=True, exist_ok=True)

        if archive_path.suffix == '.zip':
            import zipfile
            with zipfile.ZipFile(str(archive_path), 'r') as zf:
                members = zf.filelist
                total = len(members)
                for i, member in enumerate(members, 1):
                    zf.extract(member, str(extract_path))
                    if progress_callback:
                        progress_callback(i, total, member.filename)
        else:
            # For tar archives, extract normally
            shutil.unpack_archive(str(archive_path), str(extract_path))
            if progress_callback:
                progress_callback(1, 1, "Archive extracted")

        if self.verbose:
            print(f"Extracted archive to: {extract_path}")

        return str(extract_path)


def demonstrate_basic_archiving():
    """Demonstrate basic archive creation and extraction."""
    print("=== Basic Archiving Demo ===")

    # Create sample directory
    sample_dir = Path("sample_data")
    sample_dir.mkdir(exist_ok=True)

    # Add some files
    (sample_dir / "file1.txt").write_text("Content of file 1")
    (sample_dir / "file2.txt").write_text("Content of file 2")
    (sample_dir / "subdir").mkdir(exist_ok=True)
    (sample_dir / "subdir" / "file3.txt").write_text("Content of file 3")

    manager = ArchiveManager(verbose=True)

    # Create ZIP archive
    zip_archive = manager.create_archive(str(sample_dir), "sample_backup", 'zip')

    # List contents
    contents = manager.list_archive_contents(zip_archive)
    print(f"\nArchive contents ({len(contents)} files):")
    for item in contents:
        print(f"  {item}")

    # Get archive info
    info = manager.get_archive_info(zip_archive)
    print(f"\nArchive info:")
    print(f"  Size: {info['size_mb']:.2f} MB")
    print(f"  Files: {info['file_count']}")
    print(f"  Format: {info['format']}")

    # Extract archive
    extract_dir = "extracted_sample"
    manager.extract_archive(zip_archive, extract_dir)

    # Verify extraction
    extracted_files = list(Path(extract_dir).rglob('*'))
    print(f"\nExtracted {len(extracted_files)} items")


def demonstrate_compressed_archives():
    """Demonstrate different compression formats."""
    print("\n=== Compressed Archives Demo ===")

    sample_dir = "sample_data"
    manager = ArchiveManager(verbose=True)

    formats = ['tar', 'gztar', 'bztar']

    for fmt in formats:
        try:
            archive_path = manager.create_archive(sample_dir, f"sample_{fmt}", fmt)
            size = os.path.getsize(archive_path) / 1024  # KB
            print(f"Created {fmt.upper()}: {archive_path} ({size:.1f} KB)")
        except Exception as e:
            print(f"Failed to create {fmt.upper()}: {e}")


def demonstrate_batch_operations():
    """Demonstrate batch archive operations."""
    print("\n=== Batch Operations Demo ===")

    # Create multiple sample directories
    sources = []
    for i in range(3):
        dir_name = f"project_{i}"
        dir_path = Path(dir_name)
        dir_path.mkdir(exist_ok=True)
        (dir_path / f"data_{i}.txt").write_text(f"Data for project {i}")
        sources.append(dir_name)

    manager = ArchiveManager(verbose=True)

    # Batch create archives
    archives = manager.batch_create_archives(sources, "batch_archives", 'gztar')
    print(f"\nCreated {len(archives)} archives:")
    for archive in archives:
        print(f"  {archive}")

    # Batch extract archives
    extracted = manager.batch_extract_archives(archives, "batch_extracted")
    print(f"\nExtracted to {len(extracted)} directories:")
    for dir_path in extracted:
        print(f"  {dir_path}")


def demonstrate_incremental_backup():
    """Demonstrate incremental backup functionality."""
    print("\n=== Incremental Backup Demo ===")

    # Create source directory
    source_dir = Path("backup_source")
    source_dir.mkdir(exist_ok=True)
    (source_dir / "file1.txt").write_text("Initial content")

    manager = ArchiveManager(verbose=True)

    # First backup
    print("Creating initial backup...")
    backup1 = manager.create_incremental_backup(str(source_dir), "backups")
    print(f"Initial backup: {backup1}")

    # Wait and modify files
    time.sleep(1)
    (source_dir / "file2.txt").write_text("New file")
    (source_dir / "file1.txt").write_text("Modified content")

    # Incremental backup
    print("\nCreating incremental backup...")
    last_backup_time = time.time() - 10  # Approximate
    backup2 = manager.create_incremental_backup(str(source_dir), "backups", last_backup_time)
    if backup2:
        print(f"Incremental backup: {backup2}")
    else:
        print("No changes detected")


def demonstrate_progress_extraction():
    """Demonstrate extraction with progress reporting."""
    print("\n=== Progress Extraction Demo ===")

    manager = ArchiveManager(verbose=False)  # Disable verbose for cleaner output

    def progress_callback(extracted, total, filename):
        percent = (extracted / total) * 100
        print(".1f")

    # Use existing archive
    archive_path = "sample_backup.zip"
    if os.path.exists(archive_path):
        print("Extracting with progress:")
        extract_path = manager.extract_with_progress(archive_path, "progress_extract", progress_callback)
        print(f"Extraction completed to: {extract_path}")
    else:
        print("No archive found for progress demo")


def demonstrate_error_handling():
    """Demonstrate error handling in archive operations."""
    print("\n=== Error Handling Demo ===")

    manager = ArchiveManager(verbose=True)

    # Try to archive non-existent directory
    try:
        manager.create_archive("nonexistent", "error_test")
    except Exception as e:
        print(f"Expected error for non-existent source: {e}")

    # Try to extract non-existent archive
    try:
        manager.extract_archive("nonexistent.zip", "error_extract")
    except Exception as e:
        print(f"Expected error for non-existent archive: {e}")

    # Try to list contents of invalid archive
    try:
        manager.list_archive_contents("invalid.txt")
    except Exception as e:
        print(f"Expected error for invalid archive: {e}")


def cleanup_demo_files():
    """Clean up files created during demonstrations."""
    print("\n=== Cleaning Up Demo Files ===")

    cleanup_items = [
        "sample_data", "extracted_sample", "batch_archives", "batch_extracted",
        "backup_source", "backups", "progress_extract", "error_extract",
        "sample_backup.zip", "sample_tar.tar", "sample_gztar.tar.gz",
        "sample_bztar.tar.bz2", "project_0", "project_1", "project_2"
    ]

    removed_count = 0
    for item in cleanup_items:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.rmtree(item)
            else:
                os.remove(item)
            removed_count += 1

    print(f"Cleaned up {removed_count} items")


def main():
    """Run all demonstrations."""
    print("Shutil Archive Operations Implementations")
    print("=" * 42)

    demonstrate_basic_archiving()
    demonstrate_compressed_archives()
    demonstrate_batch_operations()
    demonstrate_incremental_backup()
    demonstrate_progress_extraction()
    demonstrate_error_handling()

    cleanup_demo_files()

    print("\nAll demonstrations completed!")


if __name__ == "__main__":
    main()
