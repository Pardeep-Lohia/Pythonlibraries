#!/usr/bin/env python3
"""
Log File Cleanup Script

This script demonstrates automated log file management using the os module.
It can find, analyze, compress, and remove old log files based on configurable criteria.
"""

import os
import os.path
import gzip
import shutil
import time
from datetime import datetime, timedelta
import argparse
import re


class LogFileManager:
    """Manage log files in a directory or directory tree."""

    def __init__(self, log_dirs=None, max_age_days=30, compress_after_days=7):
        if log_dirs is None:
            # Default log directories by platform
            if os.name == 'nt':
                log_dirs = [
                    'C:\\Logs',
                    os.path.join(os.environ.get('PROGRAMDATA', 'C:\\ProgramData'), 'Logs'),
                    os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Local', 'Logs')
                ]
            else:
                log_dirs = [
                    '/var/log',
                    '/var/log/apache2',
                    '/var/log/nginx',
                    os.path.join(os.path.expanduser('~'), 'logs')
                ]

        # Filter to existing directories
        self.log_dirs = [d for d in log_dirs if os.path.exists(d)]
        self.max_age_days = max_age_days
        self.compress_after_days = compress_after_days

        # Log file patterns
        self.log_patterns = [
            r'.*\.log$',           # .log files
            r'.*\.log\.\d+$',      # .log.1, .log.2, etc.
            r'.*\.out$',           # .out files
            r'.*\.err$',           # .err files
            r'.*logfile.*',        # files containing 'logfile'
            r'.*error.*\.log$',    # error logs
            r'.*access.*\.log$',   # access logs
        ]

    def is_log_file(self, filename):
        """Check if a file is a log file based on patterns."""
        filename_lower = filename.lower()

        for pattern in self.log_patterns:
            if re.match(pattern, filename_lower, re.IGNORECASE):
                return True

        return False

    def find_log_files(self, directory):
        """Find all log files in a directory tree."""
        log_files = []

        for dirpath, dirnames, filenames in os.walk(directory):
            # Skip certain directories
            dirnames[:] = [d for d in dirnames if d not in ['.git', '__pycache__', 'node_modules']]

            for filename in filenames:
                if self.is_log_file(filename):
                    filepath = os.path.join(dirpath, filename)
                    try:
                        stat_info = os.stat(filepath)
                        log_files.append({
                            'path': filepath,
                            'name': filename,
                            'size': stat_info.st_size,
                            'modified': datetime.fromtimestamp(stat_info.st_mtime),
                            'age_days': (datetime.now() - datetime.fromtimestamp(stat_info.st_mtime)).days
                        })
                    except OSError:
                        continue

        return log_files

    def analyze_log_files(self):
        """Analyze log files in configured directories."""
        all_logs = []

        for log_dir in self.log_dirs:
            logs = self.find_log_files(log_dir)
            all_logs.extend(logs)

        if not all_logs:
            return None

        # Calculate statistics
        total_size = sum(log['size'] for log in all_logs)
        oldest_file = min(all_logs, key=lambda x: x['modified'])
        newest_file = max(all_logs, key=lambda x: x['modified'])

        # Group by age
        stats = {
            'old': [log for log in all_logs if log['age_days'] > self.max_age_days],
            'compress': [log for log in all_logs if self.compress_after_days < log['age_days'] <= self.max_age_days],
            'keep': [log for log in all_logs if log['age_days'] <= self.compress_after_days]
        }

        return {
            'total_files': len(all_logs),
            'total_size': total_size,
            'oldest_file': oldest_file,
            'newest_file': newest_file,
            'stats': stats
        }

    def compress_log_file(self, filepath):
        """Compress a log file using gzip."""
        try:
            # Create compressed file path
            compressed_path = filepath + '.gz'

            # Compress the file
            with open(filepath, 'rb') as f_in:
                with gzip.open(compressed_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

            # Remove original file
            os.remove(filepath)

            # Get compressed file size
            compressed_size = os.path.getsize(compressed_path)
            original_size = os.path.getsize(compressed_path)  # This will fail since we deleted it

            return compressed_path, compressed_size

        except Exception as e:
            print(f"Error compressing {filepath}: {e}")
            return None, 0

    def archive_old_logs(self, dry_run=True):
        """Archive very old log files."""
        archived_count = 0

        for log_dir in self.log_dirs:
            for dirpath, dirnames, filenames in os.walk(log_dir):
                for filename in filenames:
                    if self.is_log_file(filename):
                        filepath = os.path.join(dirpath, filename)

                        try:
                            stat_info = os.stat(filepath)
                            age_days = (time.time() - stat_info.st_mtime) / (24 * 60 * 60)

                            if age_days > self.max_age_days:
                                if dry_run:
                                    print(f"Would archive: {filepath}")
                                else:
                                    # Create archive directory
                                    archive_dir = os.path.join(log_dir, 'archive')
                                    os.makedirs(archive_dir, exist_ok=True)

                                    # Move file to archive
                                    archive_path = os.path.join(archive_dir, filename)
                                    shutil.move(filepath, archive_path)

                                    archived_count += 1
                                    print(f"Archived: {filepath}")

                        except OSError as e:
                            print(f"Error archiving {filepath}: {e}")

        print(f"Archived {archived_count} old log files")
        return archived_count

    def cleanup_logs(self, dry_run=True):
        """Clean up log files based on age criteria."""
        compressed = 0
        deleted = 0

        for log_dir in self.log_dirs:
            logs = self.find_log_files(log_dir)

            for log_info in logs:
                filepath = log_info['path']
                age_days = log_info['age_days']

                try:
                    if age_days > self.max_age_days:
                        # Delete very old logs
                        if dry_run:
                            print(f"Would delete: {filepath}")
                        else:
                            os.remove(filepath)
                            deleted += 1
                            print(f"Deleted: {filepath}")

                    elif age_days > self.compress_after_days:
                        # Compress moderately old logs
                        if dry_run:
                            print(f"Would compress: {filepath}")
                        else:
                            compressed_path, _ = self.compress_log_file(filepath)
                            if compressed_path:
                                compressed += 1
                                print(f"Compressed: {filepath}")

                except OSError as e:
                    print(f"Error processing {filepath}: {e}")

        return compressed, deleted

    def rotate_log_file(self, filepath, max_size_mb=10):
        """Rotate a log file if it exceeds maximum size."""
        if not os.path.exists(filepath):
            print(f"Log file not found: {filepath}")
            return False

        try:
            # Check file size
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            if size_mb <= max_size_mb:
                print(f"Log file {filepath} is {size_mb:.1f} MB, no rotation needed")
                return True

            # Create rotated filename
            base, ext = os.path.splitext(filepath)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            rotated_path = f"{base}_{timestamp}{ext}"

            # Rotate the file
            shutil.move(filepath, rotated_path)

            # Create new empty log file
            with open(filepath, 'w') as f:
                f.write(f"Log rotated at {datetime.now().isoformat()}\n")

            print(f"Rotated {filepath} -> {rotated_path}")
            return True

        except Exception as e:
            print(f"Error rotating log file: {e}")
            return False

    def format_size(self, size_bytes):
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return ".1f"
            size_bytes /= 1024.0
        return ".1f"


def main():
    """Main log cleanup script."""
    parser = argparse.ArgumentParser(description='Log File Cleanup Script')
    parser.add_argument('--analyze', action='store_true', help='Analyze log files only')
    parser.add_argument('--cleanup', action='store_true', help='Perform cleanup operations')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without doing it')
    parser.add_argument('--max-age', type=int, default=30, help='Maximum age in days for log files')
    parser.add_argument('--compress-after', type=int, default=7, help='Compress after this many days')
    parser.add_argument('--log-dir', action='append', help='Log directory to process')
    parser.add_argument('--rotate', help='Rotate a specific log file')
    parser.add_argument('--max-size', type=float, default=10, help='Max size in MB for rotation')

    args = parser.parse_args()

    # Use provided log directories or defaults
    log_dirs = args.log_dir if args.log_dir else None

    manager = LogFileManager(
        log_dirs=log_dirs,
        max_age_days=args.max_age,
        compress_after_days=args.compress_after
    )

    if args.rotate:
        success = manager.rotate_log_file(args.rotate, args.max_size)
        if success:
            print("Log rotation completed")
        else:
            print("Log rotation failed")
        return

    if args.analyze or not args.cleanup:
        print("Analyzing log files...")
        analysis = manager.analyze_log_files()

        if analysis:
            print("Analysis complete:")
            print(f"Total files: {analysis['total_files']}")
            print(f"Total size: {manager.format_size(analysis['total_size'])}")

            for category, stats in analysis['stats'].items():
                print(f"  {category}: {len(stats)} files")

    if args.cleanup:
        print("\nPerforming cleanup...")
        compressed, deleted = manager.cleanup_logs(dry_run=args.dry_run)
        print(f"\nCleanup complete: {compressed} compressed, {deleted} deleted")


if __name__ == "__main__":
    main()