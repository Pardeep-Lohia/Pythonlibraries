# Archiving Utilities in `shutil`

`shutil` provides comprehensive support for creating and extracting archives in multiple formats. These functions make it easy to compress and decompress files and directories for storage, backup, or distribution.

## `shutil.make_archive()`

### Purpose
Create an archive file from a directory, supporting multiple compression formats.

### Syntax
```python
shutil.make_archive(base_name, format, root_dir=None, base_dir=None, verbose=0, dry_run=0, owner=None, group=None, logger=None)
```

### Parameters
- `base_name`: Base name of the archive file (without extension)
- `format`: Archive format ('zip', 'tar', 'gztar', 'bztar', 'xztar')
- `root_dir`: Directory to archive (default: current directory)
- `base_dir`: Directory within root_dir to archive
- `verbose`: Verbosity level (0=quiet, 1=verbose)
- `dry_run`: If True, don't create archive, just show what would be done
- `owner/group`: Set ownership in tar archives (Unix only)
- `logger`: Logger object for output

### Example
```python
import shutil
from pathlib import Path

# Create ZIP archive of current directory
shutil.make_archive('backup', 'zip')

# Create compressed tar archive of specific directory
shutil.make_archive('project_backup', 'gztar', root_dir='/home/user/projects', base_dir='myproject')

# Create archive with custom base name
project_dir = Path('/home/user/myproject')
shutil.make_archive('myproject_v1', 'zip', root_dir=str(project_dir.parent), base_dir=project_dir.name)

# Create archive with verbose output
shutil.make_archive('verbose_backup', 'tar', verbose=1)

# Dry run to see what would be archived
shutil.make_archive('test_backup', 'zip', dry_run=1)
```

### Edge Cases
- Automatically adds appropriate file extension
- Creates parent directories if they don't exist
- Handles large directory trees efficiently
- Preserves file permissions and timestamps
- Can archive across different file systems

## `shutil.unpack_archive()`

### Purpose
Extract an archive file to a directory, automatically detecting the format.

### Syntax
```python
shutil.unpack_archive(filename, extract_dir=None, format=None)
```

### Parameters
- `filename`: Path to archive file
- `extract_dir`: Directory to extract to (default: current directory)
- `format`: Archive format (auto-detected if None)

### Example
```python
import shutil

# Extract ZIP archive
shutil.unpack_archive('backup.zip')

# Extract to specific directory
shutil.unpack_archive('project_backup.tar.gz', extract_dir='/tmp/extracted')

# Extract with explicit format
shutil.unpack_archive('archive.tar', extract_dir='extracted', format='tar')

# Extract multiple archives
archives = ['backup1.zip', 'backup2.tar.gz', 'backup3.tar.bz2']
for archive in archives:
    extract_name = archive.split('.')[0] + '_extracted'
    shutil.unpack_archive(archive, extract_name)
```

### Edge Cases
- Auto-detects format from file extension
- Creates extraction directory if it doesn't exist
- Handles nested directory structures
- Preserves file permissions and timestamps
- Works with relative and absolute paths

## `shutil.get_archive_formats()`

### Purpose
Get a list of supported archive formats for the current system.

### Syntax
```python
shutil.get_archive_formats()
```

### Returns
List of tuples: [(format_name, description), ...]

### Example
```python
import shutil

# Get all supported formats
formats = shutil.get_archive_formats()
print("Supported archive formats:")
for format_name, description in formats:
    print(f"  {format_name}: {description}")

# Check if specific format is supported
supported_formats = [fmt[0] for fmt in shutil.get_archive_formats()]
if 'zip' in supported_formats:
    print("ZIP format is supported")
```

### Common Formats
- `'zip'`: ZIP file format
- `'tar'`: Uncompressed tar file
- `'gztar'`: gzip compressed tar file
- `'bztar'`: bzip2 compressed tar file
- `'xztar'`: xz compressed tar file

## Advanced Archive Operations

### Creating Archives with Filtering
```python
import shutil
import os
from pathlib import Path

def create_filtered_archive(source_dir, archive_name, exclude_patterns=None):
    """Create archive excluding certain files/patterns."""
    if exclude_patterns is None:
        exclude_patterns = ['*.pyc', '__pycache__', '.git']

    # Create temporary directory with filtered content
    temp_dir = Path(f"temp_{archive_name}")
    temp_dir.mkdir()

    try:
        for root, dirs, files in os.walk(source_dir):
            # Filter directories
            dirs[:] = [d for d in dirs if not any(d.endswith(pat.lstrip('*')) or pat in d for pat in exclude_patterns)]

            # Create relative path in temp dir
            rel_path = os.path.relpath(root, source_dir)
            if rel_path != '.':
                (temp_dir / rel_path).mkdir(parents=True, exist_ok=True)

            # Copy files
            for file in files:
                if not any(file.endswith(pat.lstrip('*')) for pat in exclude_patterns):
                    src_file = os.path.join(root, file)
                    if rel_path == '.':
                        dst_file = temp_dir / file
                    else:
                        dst_file = temp_dir / rel_path / file
                    shutil.copy2(src_file, dst_file)

        # Create archive from temp directory
        shutil.make_archive(archive_name, 'zip', root_dir=str(temp_dir))

    finally:
        # Clean up temp directory
        shutil.rmtree(temp_dir)

# Usage
create_filtered_archive('/home/user/project', 'clean_backup')
```

### Incremental Archives
```python
import shutil
import os
import time
from pathlib import Path

def create_incremental_archive(source_dir, archive_name, last_backup_time=None):
    """Create archive of files modified since last backup."""
    source_path = Path(source_dir)
    modified_files = []

    # Find modified files
    for file_path in source_path.rglob('*'):
        if file_path.is_file():
            if last_backup_time is None or file_path.stat().st_mtime > last_backup_time:
                modified_files.append(file_path)

    if not modified_files:
        print("No files modified since last backup")
        return None

    # Create temporary structure
    temp_dir = Path(f"temp_incremental_{int(time.time())}")
    temp_dir.mkdir()

    try:
        for file_path in modified_files:
            # Create relative path
            rel_path = file_path.relative_to(source_path)
            temp_file = temp_dir / rel_path
            temp_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(file_path), str(temp_file))

        # Create archive
        archive_path = shutil.make_archive(archive_name, 'zip', root_dir=str(temp_dir))
        return archive_path

    finally:
        shutil.rmtree(temp_dir)

# Usage
last_backup = time.time() - (7 * 24 * 60 * 60)  # 7 days ago
create_incremental_archive('/home/user/data', 'weekly_incremental', last_backup)
```

### Archive Verification
```python
import shutil
import os
import hashlib

def verify_archive_integrity(archive_path):
    """Verify archive integrity by checking file sizes and counts."""
    archive_path = Path(archive_path)

    if not archive_path.exists():
        return False, "Archive file not found"

    try:
        # Extract to temporary directory
        temp_dir = Path(f"verify_temp_{int(time.time())}")
        temp_dir.mkdir()

        shutil.unpack_archive(str(archive_path), str(temp_dir))

        # Count files and total size
        total_files = 0
        total_size = 0

        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                total_files += 1
                total_size += os.path.getsize(file_path)

        # Clean up
        shutil.rmtree(temp_dir)

        return True, {
            'file_count': total_files,
            'total_size': total_size,
            'total_size_mb': total_size / (1024 * 1024)
        }

    except Exception as e:
        return False, str(e)

# Usage
success, info = verify_archive_integrity('backup.zip')
if success:
    print(f"Archive OK: {info['file_count']} files, {info['total_size_mb']:.1f} MB")
else:
    print(f"Archive corrupted: {info}")
```

### Multi-part Archives
```python
import shutil
import os
from pathlib import Path

def create_multi_part_archive(source_dir, base_name, max_size_mb=100):
    """Create multi-part archive if source exceeds max size."""
    source_path = Path(source_dir)

    # Calculate source size
    total_size = sum(f.stat().st_size for f in source_path.rglob('*') if f.is_file())
    total_size_mb = total_size / (1024 * 1024)

    if total_size_mb <= max_size_mb:
        # Single archive
        return [shutil.make_archive(base_name, 'zip', root_dir=str(source_path))]

    # Multi-part archive
    archives = []
    part_num = 1
    current_size = 0
    temp_dir = Path(f"temp_multipart_{int(time.time())}")
    temp_dir.mkdir()

    try:
        for file_path in source_path.rglob('*'):
            if file_path.is_file():
                file_size = file_path.stat().st_size
                rel_path = file_path.relative_to(source_path)

                # Check if adding this file would exceed limit
                if current_size + file_size > max_size_mb * 1024 * 1024 and current_size > 0:
                    # Create archive for current part
                    part_name = f"{base_name}_part{part_num}"
                    archives.append(shutil.make_archive(part_name, 'zip', root_dir=str(temp_dir)))
                    part_num += 1
                    current_size = 0

                    # Clear temp directory
                    shutil.rmtree(temp_dir)
                    temp_dir.mkdir()

                # Add file to current part
                temp_file = temp_dir / rel_path
                temp_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(str(file_path), str(temp_file))
                current_size += file_size

        # Create final part
        if current_size > 0:
            part_name = f"{base_name}_part{part_num}"
            archives.append(shutil.make_archive(part_name, 'zip', root_dir=str(temp_dir)))

        return archives

    finally:
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

# Usage
archives = create_multi_part_archive('/large/dataset', 'dataset_backup', max_size_mb=50)
print(f"Created {len(archives)} archive parts:")
for archive in archives:
    print(f"  {archive}")
```

## Cross-Platform Considerations

### Path Separators
- Archive paths always use forward slashes (/) internally
- Automatic conversion on extraction for platform compatibility

### Permissions
- Unix permissions preserved in tar formats
- Windows attributes handled appropriately
- Execute permissions maintained where supported

### Character Encoding
- UTF-8 encoding for filenames in archives
- Automatic handling of special characters
- Platform-specific encoding considerations

## Performance Tips

### Large Archives
- Use appropriate compression format (gzip for speed, xz for size)
- Consider archive splitting for very large datasets
- Use incremental backups to reduce archive size

### Memory Usage
- Archives are created on disk, not in memory
- Large directory trees processed iteratively
- Temporary space needed for compression

### Speed Optimization
- ZIP format often fastest for small files
- Tar+gzip good balance for most use cases
- Bzip2/xz better compression but slower

## Error Handling

Archive operations can raise several exceptions:

```python
import shutil

def safe_archive_operation(source, archive_name, format='zip'):
    """Safe archive creation with comprehensive error handling."""
    try:
        archive_path = shutil.make_archive(archive_name, format, root_dir=source)
        return True, archive_path
    except shutil.Error as e:
        return False, f"Archive error: {e}"
    except OSError as e:
        return False, f"OS error: {e}"
    except ValueError as e:
        return False, f"Invalid format: {e}"

def safe_extract_operation(archive_path, extract_dir):
    """Safe archive extraction with error handling."""
    try:
        shutil.unpack_archive(archive_path, extract_dir)
        return True, extract_dir
    except shutil.ReadError as e:
        return False, f"Read error: {e}"
    except OSError as e:
        return False, f"OS error: {e}"
    except ValueError as e:
        return False, f"Invalid format: {e}"
```

## Common Use Cases

### Backup Scripts
```python
# Daily backup with timestamp
timestamp = time.strftime('%Y%m%d_%H%M%S')
backup_name = f"daily_backup_{timestamp}"
shutil.make_archive(backup_name, 'gztar', root_dir='/home/user/data')
```

### Software Distribution
```python
# Create release archive
shutil.make_archive('myapp_v1.0', 'zip', root_dir='dist', base_dir='myapp')
```

### Log Rotation
```python
# Archive old logs
log_archive = f"logs_{time.strftime('%Y%m')}"
shutil.make_archive(log_archive, 'gztar', root_dir='/var/log', base_dir='old_logs')
```

### Data Migration
```python
# Archive data before migration
shutil.make_archive('migration_backup', 'tar', root_dir='/data')
# ... perform migration ...
# Extract if rollback needed
shutil.unpack_archive('migration_backup.tar', '/rollback/data')
```

Archiving utilities in `shutil` provide a robust, cross-platform way to compress, store, and distribute files and directories, making them essential for backup systems, software distribution, and data management workflows.
