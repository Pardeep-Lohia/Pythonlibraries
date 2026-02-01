# Disk Usage Management in `shutil`

`shutil` provides utilities for monitoring and managing disk space usage. The `disk_usage()` function offers a cross-platform way to check file system storage statistics.

## `shutil.disk_usage()`

### Purpose
Returns disk usage statistics for a given path, including total, used, and free space.

### Syntax
```python
shutil.disk_usage(path)
```

### Parameters
- `path`: Path to check disk usage for (can be file or directory)

### Returns
Named tuple with three fields:
- `total`: Total disk space in bytes
- `used`: Used disk space in bytes
- `free`: Free disk space in bytes

### Example
```python
import shutil
from pathlib import Path

# Basic disk usage check
usage = shutil.disk_usage('/')
print(f"Total space: {usage.total / (1024**3):.2f} GB")
print(f"Used space: {usage.used / (1024**3):.2f} GB")
print(f"Free space: {usage.free / (1024**3):.2f} GB")
print(f"Usage: {(usage.used / usage.total) * 100:.1f}%")

# Check specific directory
home_usage = shutil.disk_usage(Path.home())
print(f"Home directory usage: {home_usage.used / (1024**2):.0f} MB used")

# Monitor multiple drives (Windows)
if os.name == 'nt':
    drives = ['C:', 'D:', 'E:']
    for drive in drives:
        try:
            usage = shutil.disk_usage(drive)
            percent = (usage.used / usage.total) * 100
            print(f"{drive}: {percent:.1f}% full")
        except OSError:
            print(f"{drive}: not accessible")
```

### Edge Cases
- Works on mounted file systems and network drives
- Requires read access to the path
- Returns 0 for all values if path doesn't exist or is inaccessible
- May not work on some virtual file systems

## Advanced Disk Usage Analysis

### Directory Size Calculation
```python
import os
import shutil
from pathlib import Path

def get_directory_size(path):
    """Calculate total size of a directory recursively"""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except (OSError, FileNotFoundError):
                    # Skip files that can't be accessed
                    pass
    except (OSError, FileNotFoundError):
        return 0
    return total_size

# Compare directory sizes
dirs = ['project1', 'project2', 'archive']
for dir_name in dirs:
    if os.path.exists(dir_name):
        size_mb = get_directory_size(dir_name) / (1024**2)
        print(f"{dir_name}: {size_mb:.2f} MB")
```

### Disk Space Monitoring
```python
import shutil
import time
from pathlib import Path

class DiskMonitor:
    def __init__(self, paths_to_monitor, threshold_percent=90):
        self.paths = paths_to_monitor
        self.threshold = threshold_percent
        self.last_usage = {}

    def check_usage(self):
        """Check disk usage and alert if above threshold"""
        alerts = []
        for path in self.paths:
            try:
                usage = shutil.disk_usage(path)
                percent_used = (usage.used / usage.total) * 100

                # Check for significant changes
                if path in self.last_usage:
                    prev_percent = self.last_usage[path]
                    change = percent_used - prev_percent
                    if abs(change) > 5:  # 5% change threshold
                        alerts.append(f"Usage change for {path}: {change:+.1f}%")

                self.last_usage[path] = percent_used

                if percent_used > self.threshold:
                    alerts.append(f"WARNING: {path} is {percent_used:.1f}% full")

                free_gb = usage.free / (1024**3)
                if free_gb < 1:  # Less than 1GB free
                    alerts.append(f"CRITICAL: {path} has only {free_gb:.2f} GB free")

            except OSError as e:
                alerts.append(f"Error checking {path}: {e}")

        return alerts

    def monitor_continuous(self, interval_seconds=300):
        """Monitor disk usage continuously"""
        print("Starting disk monitoring... (Ctrl+C to stop)")
        try:
            while True:
                alerts = self.check_usage()
                if alerts:
                    print(f"\n{time.strftime('%Y-%m-%d %H:%M:%S')}")
                    for alert in alerts:
                        print(f"  {alert}")
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            print("\nMonitoring stopped.")

# Monitor system drives
monitor = DiskMonitor(['/'], threshold_percent=85)
alerts = monitor.check_usage()
for alert in alerts:
    print(alert)
```

### Storage Cleanup Utilities
```python
import shutil
import os
import time
from pathlib import Path

def find_large_files(directory, min_size_mb=100):
    """Find files larger than specified size"""
    min_size_bytes = min_size_mb * 1024 * 1024
    large_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                size = os.path.getsize(file_path)
                if size > min_size_bytes:
                    large_files.append((file_path, size))
            except OSError:
                pass

    # Sort by size (largest first)
    large_files.sort(key=lambda x: x[1], reverse=True)
    return large_files

def cleanup_old_files(directory, days_old=30):
    """Remove files older than specified days"""
    cutoff_time = time.time() - (days_old * 24 * 60 * 60)
    removed_files = []
    total_space_freed = 0

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if os.path.getmtime(file_path) < cutoff_time:
                    size = os.path.getsize(file_path)
                    os.remove(file_path)
                    removed_files.append(file_path)
                    total_space_freed += size
            except OSError:
                pass

    return removed_files, total_space_freed

def analyze_storage_usage(root_path):
    """Analyze storage usage by file types"""
    usage_by_type = {}
    total_size = 0

    for root, dirs, files in os.walk(root_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                size = os.path.getsize(file_path)
                total_size += size

                # Get file extension
                _, ext = os.path.splitext(file)
                ext = ext.lower() or 'no_extension'

                if ext not in usage_by_type:
                    usage_by_type[ext] = {'count': 0, 'size': 0}
                usage_by_type[ext]['count'] += 1
                usage_by_type[ext]['size'] += size

            except OSError:
                pass

    # Print analysis
    print(f"Total files analyzed: {sum(stats['count'] for stats in usage_by_type.values())}")
    print(f"Total size: {total_size / (1024**3):.2f} GB")
    print("\nUsage by file type:")
    for ext, stats in sorted(usage_by_type.items(), key=lambda x: x[1]['size'], reverse=True):
        size_gb = stats['size'] / (1024**3)
        print(f"  {ext}: {stats['count']} files, {size_gb:.2f} GB")

    return usage_by_type

# Example usage
if __name__ == "__main__":
    # Find large files
    large_files = find_large_files('/home/user', min_size_mb=500)
    print("Large files (>500MB):")
    for file_path, size in large_files[:10]:  # Top 10
        print(f"  {file_path}: {size / (1024**3):.2f} GB")

    # Cleanup old files
    removed, space_freed = cleanup_old_files('/tmp', days_old=7)
    print(f"\nCleaned up {len(removed)} old files, freed {space_freed / (1024**2):.2f} MB")

    # Analyze storage
    analyze_storage_usage('/home/user/Documents')
```

### Quota Management
```python
import shutil
import os
from pathlib import Path

class StorageQuota:
    def __init__(self, base_path, max_size_gb):
        self.base_path = Path(base_path)
        self.max_size_bytes = max_size_gb * 1024**3
        self.current_size = self._calculate_size()

    def _calculate_size(self):
        """Calculate current directory size"""
        total = 0
        try:
            for file_path in self.base_path.rglob('*'):
                if file_path.is_file():
                    total += file_path.stat().st_size
        except (OSError, PermissionError):
            pass
        return total

    def check_quota(self):
        """Check if quota is exceeded"""
        usage_percent = (self.current_size / self.max_size_bytes) * 100
        return {
            'current_size_gb': self.current_size / (1024**3),
            'max_size_gb': self.max_size_bytes / (1024**3),
            'usage_percent': usage_percent,
            'exceeded': self.current_size > self.max_size_bytes
        }

    def enforce_quota(self, strategy='oldest'):
        """Enforce quota by removing files"""
        if not self.check_quota()['exceeded']:
            return []

        removed_files = []
        files = []

        # Get all files with modification times
        for file_path in self.base_path.rglob('*'):
            if file_path.is_file():
                try:
                    stat = file_path.stat()
                    files.append((file_path, stat.st_mtime, stat.st_size))
                except OSError:
                    pass

        # Sort by strategy
        if strategy == 'oldest':
            files.sort(key=lambda x: x[1])  # Sort by modification time
        elif strategy == 'largest':
            files.sort(key=lambda x: x[2], reverse=True)  # Sort by size

        # Remove files until under quota
        for file_path, _, size in files:
            if self.current_size <= self.max_size_bytes:
                break
            try:
                file_path.unlink()
                self.current_size -= size
                removed_files.append(str(file_path))
            except OSError:
                pass

        return removed_files

# Example usage
quota = StorageQuota('/home/user/cache', max_size_gb=5)
status = quota.check_quota()
print(f"Cache usage: {status['usage_percent']:.1f}%")

if status['exceeded']:
    removed = quota.enforce_quota(strategy='oldest')
    print(f"Removed {len(removed)} old files to free space")
```

## Cross-Platform Disk Usage

### Windows-Specific Considerations
```python
import shutil
import os

def get_windows_drive_info():
    """Get information about all drives on Windows"""
    if os.name != 'nt':
        return []

    drives = []
    for drive_letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        drive = f"{drive_letter}:"
        try:
            usage = shutil.disk_usage(drive)
            drives.append({
                'drive': drive,
                'total_gb': usage.total / (1024**3),
                'used_gb': usage.used / (1024**3),
                'free_gb': usage.free / (1024**3),
                'usage_percent': (usage.used / usage.total) * 100
            })
        except OSError:
            # Drive not accessible or doesn't exist
            pass
    return drives

# Display drive information
for drive_info in get_windows_drive_info():
    print(f"{drive_info['drive']}: {drive_info['usage_percent']:.1f}% full "
          f"({drive_info['free_gb']:.1f} GB free)")
```

### Unix/Linux-Specific Features
```python
import shutil
import os
from pathlib import Path

def get_mount_points():
    """Get all mount points and their usage"""
    mounts = []
    try:
        with open('/proc/mounts', 'r') as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 2:
                    mount_point = parts[1]
                    try:
                        usage = shutil.disk_usage(mount_point)
                        mounts.append({
                            'mount_point': mount_point,
                            'device': parts[0],
                            'total_gb': usage.total / (1024**3),
                            'used_gb': usage.used / (1024**3),
                            'free_gb': usage.free / (1024**3)
                        })
                    except OSError:
                        pass
    except FileNotFoundError:
        # Not on Linux, try alternative method
        pass
    return mounts

def check_inode_usage(path):
    """Check inode usage (Unix/Linux)"""
    try:
        stat = os.statvfs(path)
        total_inodes = stat.f_files
        used_inodes = stat.f_files - stat.f_favail
        inode_usage = (used_inodes / total_inodes) * 100 if total_inodes > 0 else 0
        return {
            'total_inodes': total_inodes,
            'used_inodes': used_inodes,
            'free_inodes': stat.f_favail,
            'usage_percent': inode_usage
        }
    except AttributeError:
        # statvfs not available
        return None

# Check mount points
for mount in get_mount_points():
    print(f"{mount['mount_point']}: {mount['used_gb']:.1f}/{mount['total_gb']:.1f} GB")

# Check inode usage
inode_info = check_inode_usage('/')
if inode_info:
    print(f"Inode usage: {inode_info['usage_percent']:.1f}%")
```

## Error Handling

Disk usage operations can fail for various reasons:

```python
import shutil

def safe_disk_usage_check(path):
    """Check disk usage with comprehensive error handling"""
    try:
        usage = shutil.disk_usage(path)
        return {
            'success': True,
            'total': usage.total,
            'used': usage.used,
            'free': usage.free
        }
    except FileNotFoundError:
        return {'success': False, 'error': 'Path not found'}
    except PermissionError:
        return {'success': False, 'error': 'Permission denied'}
    except OSError as e:
        return {'success': False, 'error': f'OS error: {e}'}

# Safe usage checking
result = safe_disk_usage_check('/some/path')
if result['success']:
    print(f"Free space: {result['free'] / (1024**3):.2f} GB")
else:
    print(f"Error: {result['error']}")
```

## Performance Considerations

- `disk_usage()` is efficient and fast
- Directory size calculation can be slow for large trees
- Consider caching results for monitoring applications
- Use appropriate sampling intervals to avoid overhead
- For very large file systems, consider parallel processing

## Best Practices

- Always check available space before large operations
- Monitor disk usage in long-running applications
- Implement cleanup strategies for temporary directories
- Use appropriate thresholds for different storage types
- Consider both space and inode usage on Unix systems
- Handle network drives and removable media gracefully
