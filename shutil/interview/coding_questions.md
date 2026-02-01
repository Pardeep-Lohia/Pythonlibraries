# Coding Questions for `shutil` Interviews

This document contains common coding problems and challenges related to the `shutil` module that appear in Python developer interviews, along with solutions and explanations.

## Basic File Operations

### 1. Implement a safe file copy function with progress reporting

**Problem:** Write a function that copies a file safely with progress reporting and error handling.

**Solution:**
```python
import shutil
import os
import hashlib

def safe_copy_with_progress(src, dst, buffer_size=1024*1024):
    """
    Safely copy a file with progress reporting and integrity checking.

    Args:
        src: Source file path
        dst: Destination file path
        buffer_size: Copy buffer size in bytes

    Returns:
        bool: True if successful, False otherwise
    """
    if not os.path.exists(src):
        print(f"Source file does not exist: {src}")
        return False

    # Check if destination exists
    if os.path.exists(dst):
        response = input(f"Destination {dst} exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            return False

    # Get source file size for progress
    src_size = os.path.getsize(src)
    copied_size = 0

    # Calculate source hash for integrity check
    src_hash = hashlib.md5()
    with open(src, 'rb') as f:
        while chunk := f.read(buffer_size):
            src_hash.update(chunk)

    try:
        with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
            while True:
                chunk = fsrc.read(buffer_size)
                if not chunk:
                    break

                fdst.write(chunk)
                copied_size += len(chunk)

                # Report progress
                progress = (copied_size / src_size) * 100
                print(f"\rProgress: {progress:.1f}% ({copied_size}/{src_size} bytes)", end='')

        print()  # New line after progress

        # Verify integrity
        dst_hash = hashlib.md5()
        with open(dst, 'rb') as f:
            while chunk := f.read(buffer_size):
                dst_hash.update(chunk)

        if src_hash.hexdigest() == dst_hash.hexdigest():
            print("Integrity check passed")
            return True
        else:
            print("Integrity check failed - removing destination")
            os.remove(dst)
            return False

    except IOError as e:
        print(f"Copy failed: {e}")
        if os.path.exists(dst):
            os.remove(dst)
        return False

# Usage
success = safe_copy_with_progress('large_file.dat', 'backup.dat')
```

### 2. Create a directory backup function

**Problem:** Implement a function that creates a timestamped backup of a directory, excluding certain file types.

**Solution:**
```python
import shutil
import os
from datetime import datetime
from pathlib import Path
import fnmatch

def create_directory_backup(source_dir, backup_dir, exclude_patterns=None):
    """
    Create a timestamped backup of a directory.

    Args:
        source_dir: Directory to backup
        backup_dir: Directory to store backups
        exclude_patterns: List of patterns to exclude (e.g., ['*.tmp', '__pycache__'])

    Returns:
        str: Path to created backup archive
    """
    if exclude_patterns is None:
        exclude_patterns = ['*.tmp', '*.bak', '__pycache__', '.git']

    if not os.path.exists(source_dir):
        raise ValueError(f"Source directory does not exist: {source_dir}")

    # Create backup directory if it doesn't exist
    os.makedirs(backup_dir, exist_ok=True)

    # Generate timestamped backup name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"backup_{os.path.basename(source_dir)}_{timestamp}"

    # Create ignore function
    def ignore_function(directory, contents):
        ignored = []
        for pattern in exclude_patterns:
            ignored.extend(fnmatch.filter(contents, pattern))
        return ignored

    try:
        # Copy directory structure with exclusions
        temp_backup_dir = os.path.join(backup_dir, backup_name)
        shutil.copytree(source_dir, temp_backup_dir, ignore=ignore_function)

        # Create compressed archive
        archive_base = os.path.join(backup_dir, backup_name)
        archive_path = shutil.make_archive(archive_base, 'gztar', temp_backup_dir)

        # Remove temporary directory
        shutil.rmtree(temp_backup_dir)

        print(f"Backup created: {archive_path}")
        return archive_path

    except Exception as e:
        print(f"Backup failed: {e}")
        # Clean up partial backup if it exists
        temp_backup_dir = os.path.join(backup_dir, backup_name)
        if os.path.exists(temp_backup_dir):
            shutil.rmtree(temp_backup_dir)
        raise

# Usage
backup_path = create_directory_backup(
    '/home/user/documents',
    '/home/user/backups',
    exclude_patterns=['*.tmp', '__pycache__', 'node_modules']
)
```

## Directory Synchronization

### 3. Implement directory synchronization

**Problem:** Write a function that synchronizes two directories, copying new and modified files while removing deleted ones.

**Solution:**
```python
import shutil
import os
from pathlib import Path

def sync_directories(source_dir, dest_dir, dry_run=False):
    """
    Synchronize destination directory with source directory.

    Args:
        source_dir: Source directory
        dest_dir: Destination directory
        dry_run: If True, only show what would be done

    Returns:
        tuple: (files_copied, files_removed, files_skipped)
    """
    source_path = Path(source_dir)
    dest_path = Path(dest_dir)

    if not source_path.exists():
        raise ValueError(f"Source directory does not exist: {source_dir}")

    # Ensure destination exists
    dest_path.mkdir(parents=True, exist_ok=True)

    # Get all files in both directories
    source_files = {}
    for file_path in source_path.rglob('*'):
        if file_path.is_file():
            relative_path = file_path.relative_to(source_path)
            source_files[relative_path] = file_path.stat()

    dest_files = {}
    for file_path in dest_path.rglob('*'):
        if file_path.is_file():
            relative_path = file_path.relative_to(dest_path)
            dest_files[relative_path] = file_path.stat()

    files_copied = 0
    files_removed = 0
    files_skipped = 0

    # Copy new or modified files
    for rel_path, src_stat in source_files.items():
        dest_file = dest_path / rel_path
        src_file = source_path / rel_path

        needs_copy = (
            not dest_file.exists() or
            src_stat.st_mtime > dest_files.get(rel_path, type('obj', (object,), {'st_mtime': 0})).st_mtime or
            src_stat.st_size != dest_files.get(rel_path, type('obj', (object,), {'st_size': 0})).st_size
        )

        if needs_copy:
            if dry_run:
                print(f"Would copy: {rel_path}")
            else:
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_file, dest_file)
                print(f"Copied: {rel_path}")
            files_copied += 1
        else:
            files_skipped += 1

    # Remove files not in source
    for rel_path in dest_files:
        if rel_path not in source_files:
            dest_file = dest_path / rel_path
            if dry_run:
                print(f"Would remove: {rel_path}")
            else:
                dest_file.unlink()
                print(f"Removed: {rel_path}")
            files_removed += 1

    return files_copied, files_removed, files_skipped

# Usage
copied, removed, skipped = sync_directories('/source', '/dest', dry_run=False)
print(f"Sync complete: {copied} copied, {removed} removed, {skipped} skipped")
```

### 4. Implement incremental backup

**Problem:** Create a backup system that only backs up files changed since the last backup.

**Solution:**
```python
import shutil
import os
import pickle
from pathlib import Path
from datetime import datetime

class IncrementalBackup:
    def __init__(self, source_dir, backup_dir):
        self.source_dir = Path(source_dir)
        self.backup_dir = Path(backup_dir)
        self.manifest_file = self.backup_dir / 'backup_manifest.pkl'

        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.manifest = self._load_manifest()

    def _load_manifest(self):
        """Load backup manifest or create empty one."""
        if self.manifest_file.exists():
            with open(self.manifest_file, 'rb') as f:
                return pickle.load(f)
        return {}

    def _save_manifest(self):
        """Save backup manifest."""
        with open(self.manifest_file, 'wb') as f:
            pickle.dump(self.manifest, f)

    def create_incremental_backup(self):
        """Create an incremental backup."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = self.backup_dir / f"incremental_{timestamp}"

        backup_path.mkdir(exist_ok=True)
        changed_files = []

        # Find changed files
        for file_path in self.source_dir.rglob('*'):
            if file_path.is_file():
                relative_path = file_path.relative_to(self.source_dir)
                current_mtime = file_path.stat().st_mtime

                # Check if file has changed
                if str(relative_path) not in self.manifest or \
                   self.manifest[str(relative_path)] != current_mtime:

                    # Copy file to backup
                    dest_file = backup_path / relative_path
                    dest_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file_path, dest_file)

                    # Update manifest
                    self.manifest[str(relative_path)] = current_mtime
                    changed_files.append(str(relative_path))

        self._save_manifest()

        # Create archive of changed files
        if changed_files:
            archive_name = f"incremental_backup_{timestamp}"
            archive_path = shutil.make_archive(
                str(self.backup_dir / archive_name),
                'gztar',
                str(backup_path)
            )

            # Clean up temporary directory
            shutil.rmtree(backup_path)

            print(f"Incremental backup created: {archive_path}")
            print(f"Files backed up: {len(changed_files)}")
            return archive_path
        else:
            # Clean up empty backup directory
            backup_path.rmdir()
            print("No changes detected - no backup created")
            return None

    def restore_from_incremental(self, backup_archive, restore_dir):
        """Restore from incremental backup."""
        restore_path = Path(restore_dir)
        restore_path.mkdir(parents=True, exist_ok=True)

        # Extract backup
        temp_extract_dir = restore_path / 'temp_extract'
        shutil.unpack_archive(backup_archive, str(temp_extract_dir))

        # Copy files to restore location
        for file_path in temp_extract_dir.rglob('*'):
            if file_path.is_file():
                relative_path = file_path.relative_to(temp_extract_dir)
                dest_file = restore_path / relative_path
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, dest_file)

        # Clean up
        shutil.rmtree(temp_extract_dir)
        print(f"Restored from {backup_archive} to {restore_dir}")

# Usage
backup = IncrementalBackup('/source/project', '/backups')
archive = backup.create_incremental_backup()

# Restore if needed
if archive:
    backup.restore_from_incremental(archive, '/restore/location')
```

## Archive Management

### 5. Implement archive extraction with validation

**Problem:** Write a function that safely extracts archives with format detection and integrity validation.

**Solution:**
```python
import shutil
import os
import hashlib
import zipfile
import tarfile
from pathlib import Path

def safe_extract_archive(archive_path, extract_dir, validate_integrity=True):
    """
    Safely extract an archive with validation.

    Args:
        archive_path: Path to archive file
        extract_dir: Directory to extract to
        validate_integrity: Whether to validate archive integrity

    Returns:
        bool: True if successful
    """
    if not os.path.exists(archive_path):
        print(f"Archive does not exist: {archive_path}")
        return False

    # Create extraction directory
    os.makedirs(extract_dir, exist_ok=True)

    # Validate archive integrity if requested
    if validate_integrity:
        if not _validate_archive_integrity(archive_path):
            print("Archive integrity check failed")
            return False

    try:
        # Extract archive
        shutil.unpack_archive(archive_path, extract_dir)

        # Get extracted files
        extracted_files = []
        for root, dirs, files in os.walk(extract_dir):
            for file in files:
                extracted_files.append(os.path.join(root, file))

        print(f"Successfully extracted {len(extracted_files)} files to {extract_dir}")
        return True

    except shutil.ReadError as e:
        print(f"Archive read error: {e}")
        return False
    except OSError as e:
        print(f"Extraction failed: {e}")
        return False

def _validate_archive_integrity(archive_path):
    """Validate archive integrity."""
    try:
        if archive_path.endswith('.zip'):
            with zipfile.ZipFile(archive_path, 'r') as zf:
                # Test archive integrity
                bad_files = zf.testzip()
                return bad_files is None

        elif archive_path.endswith(('.tar.gz', '.tar.bz2', '.tar.xz', '.tar')):
            with tarfile.open(archive_path, 'r:*') as tf:
                # Extract to memory to test
                import io
                for member in tf.getmembers():
                    if member.isfile():
                        try:
                            tf.extractfile(member).read(1024)  # Read first 1KB
                        except:
                            return False
                return True

        else:
            print(f"Unsupported archive format: {archive_path}")
            return False

    except Exception as e:
        print(f"Integrity check failed: {e}")
        return False

def extract_with_progress(archive_path, extract_dir):
    """Extract archive with progress reporting."""
    # For simple progress, we can show file count
    print(f"Extracting {archive_path}...")

    # Get archive info
    if archive_path.endswith('.zip'):
        with zipfile.ZipFile(archive_path, 'r') as zf:
            total_files = len(zf.filelist)
            print(f"Archive contains {total_files} files")

    elif archive_path.endswith(('.tar.gz', '.tar.bz2', '.tar.xz', '.tar')):
        with tarfile.open(archive_path, 'r:*') as tf:
            total_files = len([m for m in tf.getmembers() if m.isfile()])
            print(f"Archive contains {total_files} files")

    # Extract
    success = safe_extract_archive(archive_path, extract_dir, validate_integrity=False)

    if success:
        # Count extracted files
        extracted_count = sum(1 for _, _, files in os.walk(extract_dir) for _ in files)
        print(f"Extracted {extracted_count} files")

    return success

# Usage
success = safe_extract_archive('project_backup.tar.gz', '/tmp/extracted')
if success:
    print("Archive extracted successfully")
```

## Disk Usage Analysis

### 6. Implement disk usage analyzer

**Problem:** Create a tool that analyzes disk usage and identifies large files and directories.

**Solution:**
```python
import shutil
import os
from pathlib import Path
from collections import defaultdict

class DiskUsageAnalyzer:
    def __init__(self, root_path):
        self.root_path = Path(root_path)

    def analyze_usage(self, max_depth=3):
        """Analyze disk usage by directory and file type."""
        usage_by_dir = {}
        usage_by_type = defaultdict(int)
        large_files = []

        for root, dirs, files in os.walk(self.root_path):
            # Limit depth
            depth = len(Path(root).relative_to(self.root_path).parts)
            if depth > max_depth:
                dirs[:] = []  # Don't recurse deeper
                continue

            dir_size = 0

            for file in files:
                file_path = os.path.join(root, file)
                try:
                    size = os.path.getsize(file_path)
                    dir_size += size

                    # Track by file type
                    _, ext = os.path.splitext(file)
                    usage_by_type[ext.lower()] += size

                    # Track large files
                    if size > 100 * 1024 * 1024:  # 100MB
                        large_files.append((file_path, size))

                except OSError:
                    pass

            usage_by_dir[root] = dir_size

        return {
            'by_directory': usage_by_dir,
            'by_type': dict(usage_by_type),
            'large_files': large_files
        }

    def print_report(self, analysis):
        """Print formatted usage report."""
        print("=== Disk Usage Analysis ===")
        print(f"Root: {self.root_path}")
        print()

        # Directory usage
        print("Top Directories by Size:")
        sorted_dirs = sorted(analysis['by_directory'].items(),
                           key=lambda x: x[1], reverse=True)[:10]

        for dir_path, size in sorted_dirs:
            size_mb = size / (1024 * 1024)
            print(".1f")

        print()

        # File type usage
        print("Usage by File Type:")
        sorted_types = sorted(analysis['by_type'].items(),
                            key=lambda x: x[1], reverse=True)[:10]

        for ext, size in sorted_types:
            size_mb = size / (1024 * 1024)
            print(".1f")

        print()

        # Large files
        if analysis['large_files']:
            print("Large Files (>100MB):")
            for file_path, size in sorted(analysis['large_files'],
                                        key=lambda x: x[1], reverse=True)[:10]:
                size_gb = size / (1024 ** 3)
                print(".2f")
        else:
            print("No large files found")

    def find_duplicates(self):
        """Find duplicate files based on size and hash."""
        file_hashes = defaultdict(list)

        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    size = os.path.getsize(file_path)
                    if size > 0:  # Skip empty files
                        # Quick hash of first 1KB
                        with open(file_path, 'rb') as f:
                            data = f.read(1024)
                        hash_key = (size, hash(data))

                        file_hashes[hash_key].append(file_path)
                except OSError:
                    pass

        # Find duplicates
        duplicates = []
        for hash_key, files in file_hashes.items():
            if len(files) > 1:
                duplicates.append((hash_key[0], files))

        return duplicates

# Usage
analyzer = DiskUsageAnalyzer('/home/user')
analysis = analyzer.analyze_usage()
analyzer.print_report(analysis)

duplicates = analyzer.find_duplicates()
if duplicates:
    print(f"\nFound {len(duplicates)} sets of duplicate files")
    for size, files in duplicates[:5]:  # Show first 5
        print(f"Size: {size} bytes, Files: {files}")
```

## Error Handling and Robust Operations

### 7. Implement robust file operations with retry logic

**Problem:** Create file operations that handle temporary failures and network issues gracefully.

**Solution:**
```python
import shutil
import os
import time
import errno
from functools import wraps

def retry_on_failure(max_retries=3, delay=1, backoff=2):
    """Decorator for retrying operations on failure."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            current_delay = delay

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except (OSError, IOError) as e:
                    last_exception = e

                    # Don't retry on certain errors
                    if e.errno in (errno.ENOENT, errno.EACCES, errno.EPERM):
                        raise

                    if attempt < max_retries:
                        print(f"Attempt {attempt + 1} failed: {e}. Retrying in {current_delay}s...")
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        print(f"All {max_retries + 1} attempts failed")

            raise last_exception
        return wrapper
    return decorator

class RobustFileOperations:
    def __init__(self, max_retries=3):
        self.max_retries = max_retries

    @retry_on_failure(max_retries=3)
    def robust_copy(self, src, dst):
        """Robust file copy with retry logic."""
        shutil.copy2(src, dst)
        print(f"Successfully copied {src} -> {dst}")

    @retry_on_failure(max_retries=3)
    def robust_move(self, src, dst):
        """Robust file move with retry logic."""
        shutil.move(src, dst)
        print(f"Successfully moved {src} -> {dst}")

    def robust_copytree(self, src, dst):
        """Robust directory copy with error collection."""
        errors = []

        def error_handler(func, path, excinfo):
            errors.append((func, path, excinfo))
            print(f"Error in {func.__name__}({path}): {excinfo[1]}")

        try:
            shutil.copytree(src, dst, onerror=error_handler)
            if errors:
                print(f"Copy completed with {len(errors)} errors")
            else:
                print(f"Successfully copied directory {src} -> {dst}")
            return len(errors) == 0
        except Exception as e:
            print(f"Copy failed: {e}")
            return False

    def safe_rmtree(self, path, confirm=False):
        """Safely remove directory tree with confirmation."""
        if not os.path.exists(path):
            print(f"Path does not exist: {path}")
            return True

        if confirm:
            # Calculate size for confirmation
            total_size = 0
            file_count = 0
            for root, dirs, files in os.walk(path):
                for file in files:
                    try:
                        total_size += os.path.getsize(os.path.join(root, file))
                        file_count += 1
                    except OSError:
                        pass

            size_mb = total_size / (1024 * 1024)
            response = input(f"Delete {path} ({file_count} files, {size_mb:.1f} MB)? (y/N): ")
            if response.lower() != 'y':
                return False

        def error_handler(func, path, excinfo):
            print(f"Error removing {path}: {excinfo[1]}")

        try:
            shutil.rmtree(path, onerror=error_handler)
            print(f"Successfully removed {path}")
            return True
        except Exception as e:
            print(f"Removal failed: {e}")
            return False

# Usage
ops = RobustFileOperations()

# Robust copy
try:
    ops.robust_copy('source.txt', 'dest.txt')
except Exception as e:
    print(f"Copy failed after retries: {e}")

# Robust directory operations
success = ops.robust_copytree('/source/dir', '/dest/dir')
if success:
    print("Directory copy completed")
```

## Advanced Challenges

### 8. Implement a file system diff tool

**Problem:** Create a tool that shows differences between two directory trees.

**Solution:**
```python
import shutil
import os
from pathlib import Path
from typing import Dict, List, Tuple

class DirectoryDiff:
    def __init__(self, dir1: str, dir2: str):
        self.dir1 = Path(dir1)
        self.dir2 = Path(dir2)

    def get_file_info(self, directory: Path) -> Dict[str, os.stat_result]:
        """Get file information for all files in directory."""
        file_info = {}
        try:
            for file_path in directory.rglob('*'):
                if file_path.is_file():
                    relative_path = file_path.relative_to(directory)
                    file_info[str(relative_path)] = file_path.stat()
        except PermissionError:
            pass
        return file_info

    def compare_directories(self) -> Dict[str, List]:
        """Compare two directories and return differences."""
        files1 = self.get_file_info(self.dir1)
        files2 = self.get_file_info(self.dir2)

        only_in_dir1 = []
        only_in_dir2 = []
        modified = []
        same = []

        # Files only in dir1
        for path in files1:
            if path not in files2:
                only_in_dir1.append(path)

        # Files only in dir2
        for path in files2:
            if path not in files1:
                only_in_dir2.append(path)

        # Files in both - check if modified
        for path in files1:
            if path in files2:
                stat1 = files1[path]
                stat2 = files2[path]

                if (stat1.st_size != stat2.st_size or
                    stat1.st_mtime != stat2.st_mtime):
                    modified.append(path)
                else:
                    same.append(path)

        return {
            'only_in_left': only_in_dir1,
            'only_in_right': only_in_dir2,
            'modified': modified,
            'same': same
        }

    def print_diff(self, diff_result: Dict[str, List]):
        """Print formatted diff results."""
        print(f"Directory comparison: {self.dir1} vs {self.dir2}")
        print("=" * 60)

        print(f"Files only in {self.dir1}:")
        for file in sorted(diff_result['only_in_left']):
            print(f"  + {file}")

        print(f"\nFiles only in {self.dir2}:")
        for file in sorted(diff_result['only_in_right']):
            print(f"  + {file}")

        print(f"\nModified files:")
        for file in sorted(diff_result['modified']):
            print(f"  ~ {file}")

        print(f"\nUnchanged files: {len(diff_result['same'])}")

    def sync_from_left_to_right(self, diff_result: Dict[str, List]):
        """Sync files from left directory to right based on diff."""
        synced = 0

        # Copy new files
        for file in diff_result['only_in_left']:
            src = self.dir1 / file
            dst = self.dir2 / file
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            synced += 1

        # Copy modified files
        for file in diff_result['modified']:
            src = self.dir1 / file
            dst = self.dir2 / file
            shutil.copy2(src, dst)
            synced += 1

        # Remove files only in right
        for file in diff_result['only_in_right']:
            dst = self.dir2 / file
            dst.unlink()
            synced += 1

        print(f"Synced {synced} files")
        return synced

# Usage
diff = DirectoryDiff('/dir1', '/dir2')
result = diff.compare_directories()
diff.print_diff(result)

# Optional: sync directories
sync_count = diff.sync_from_left_to_right(result)
```

These coding challenges cover the most common `shutil` use cases and help demonstrate practical understanding of the module's capabilities and proper error handling techniques.
