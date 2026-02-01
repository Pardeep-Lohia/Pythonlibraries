#!/usr/bin/env python3
"""
Automation Script Example

This script demonstrates how to use the `os` module for common automation tasks
like file organization, backup creation, and system maintenance.
"""

import os
import os.path
import shutil
import time
from datetime import datetime, timedelta
import argparse
import json


class FileOrganizer:
    """Automate file organization tasks."""

    def __init__(self, source_dir, dest_dir=None):
        self.source_dir = os.path.abspath(source_dir)
        self.dest_dir = os.path.abspath(dest_dir) if dest_dir else self.source_dir

        if not os.path.exists(self.source_dir):
            raise FileNotFoundError(f"Source directory not found: {self.source_dir}")

    def organize_by_extension(self, create_folders=True):
        """
        Organize files in source directory by their extensions.

        Args:
            create_folders (bool): Whether to create extension folders

        Returns:
            dict: Summary of organization results
        """
        results = {'moved': 0, 'errors': 0, 'folders_created': 0}

        # Get all files in source directory
        files = []
        for item in os.listdir(self.source_dir):
            item_path = os.path.join(self.source_dir, item)
            if os.path.isfile(item_path):
                files.append(item)

        for filename in files:
            filepath = os.path.join(self.source_dir, filename)

            # Get file extension
            _, ext = os.path.splitext(filename)
            ext = ext.lower() if ext else 'no_extension'

            # Create destination folder
            if create_folders:
                ext_folder = os.path.join(self.dest_dir, ext[1:] if ext.startswith('.') else ext)
                if not os.path.exists(ext_folder):
                    os.makedirs(ext_folder, exist_ok=True)
                    results['folders_created'] += 1
                dest_path = os.path.join(ext_folder, filename)
            else:
                dest_path = os.path.join(self.dest_dir, filename)

            # Move file
            try:
                if filepath != dest_path:  # Don't move to same location
                    shutil.move(filepath, dest_path)
                    results['moved'] += 1
                    print(f"Moved: {filename} -> {os.path.basename(os.path.dirname(dest_path))}/")
            except Exception as e:
                print(f"Error moving {filename}: {e}")
                results['errors'] += 1

        return results

    def organize_by_date(self, date_format='%Y-%m-%d'):
        """
        Organize files by their modification date.

        Args:
            date_format (str): Date format for folder names

        Returns:
            dict: Summary of organization results
        """
        results = {'moved': 0, 'errors': 0, 'folders_created': 0}

        for filename in os.listdir(self.source_dir):
            filepath = os.path.join(self.source_dir, filename)

            if not os.path.isfile(filepath):
                continue

            try:
                # Get file modification time
                mod_time = os.path.getmtime(filepath)
                date_str = datetime.fromtimestamp(mod_time).strftime(date_format)

                # Create date folder
                date_folder = os.path.join(self.dest_dir, date_str)
                if not os.path.exists(date_folder):
                    os.makedirs(date_folder, exist_ok=True)
                    results['folders_created'] += 1

                # Move file
                dest_path = os.path.join(date_folder, filename)
                if filepath != dest_path:
                    shutil.move(filepath, dest_path)
                    results['moved'] += 1
                    print(f"Moved: {filename} -> {date_str}/")

            except Exception as e:
                print(f"Error moving {filename}: {e}")
                results['errors'] += 1

        return results

    def remove_duplicates(self, check_content=False):
        """
        Remove duplicate files based on name and optionally content.

        Args:
            check_content (bool): Whether to check file content for duplicates

        Returns:
            dict: Summary of duplicate removal
        """
        from hashlib import md5

        results = {'duplicates_found': 0, 'removed': 0, 'errors': 0}

        # Group files by name
        name_groups = {}
        for filename in os.listdir(self.source_dir):
            filepath = os.path.join(self.source_dir, filename)
            if os.path.isfile(filepath):
                name = filename.lower()
                if name not in name_groups:
                    name_groups[name] = []
                name_groups[name].append(filepath)

        # Process duplicates
        for name, files in name_groups.items():
            if len(files) < 2:
                continue

            results['duplicates_found'] += len(files) - 1

            if check_content:
                # Group by content hash
                content_groups = {}
                for filepath in files:
                    try:
                        with open(filepath, 'rb') as f:
                            content = f.read()
                            content_hash = md5(content).hexdigest()

                        if content_hash not in content_groups:
                            content_groups[content_hash] = []
                        content_groups[content_hash].append(filepath)
                    except Exception:
                        continue

                # Remove duplicates within content groups
                for hash_value, dup_files in content_groups.items():
                    if len(dup_files) > 1:
                        # Keep first file, remove others
                        for dup_file in dup_files[1:]:
                            try:
                                os.remove(dup_file)
                                results['removed'] += 1
                                print(f"Removed duplicate: {os.path.basename(dup_file)}")
                            except Exception as e:
                                print(f"Error removing {dup_file}: {e}")
                                results['errors'] += 1
            else:
                # Remove all but first file with same name
                for dup_file in files[1:]:
                    try:
                        os.remove(dup_file)
                        results['removed'] += 1
                        print(f"Removed duplicate: {os.path.basename(dup_file)}")
                    except Exception as e:
                        print(f"Error removing {dup_file}: {e}")
                        results['errors'] += 1

        return results


class BackupManager:
    """Manage automated backups."""

    def __init__(self, source_dirs, backup_dir):
        self.source_dirs = [os.path.abspath(d) for d in source_dirs]
        self.backup_dir = os.path.abspath(backup_dir)

        # Create backup directory if it doesn't exist
        os.makedirs(self.backup_dir, exist_ok=True)

    def create_backup(self, name=None, compress=True):
        """
        Create a backup of source directories.

        Args:
            name (str): Backup name (uses timestamp if None)
            compress (bool): Whether to compress the backup

        Returns:
            str: Path to created backup
        """
        if name is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            name = f"backup_{timestamp}"

        backup_path = os.path.join(self.backup_dir, name)

        if compress:
            # Create compressed archive
            import tarfile

            backup_file = backup_path + '.tar.gz'
            with tarfile.open(backup_file, 'w:gz') as tar:
                for source_dir in self.source_dirs:
                    if os.path.exists(source_dir):
                        # Add directory to archive
                        arcname = os.path.basename(source_dir)
                        tar.add(source_dir, arcname=arcname)
                        print(f"Added to backup: {arcname}")
                    else:
                        print(f"Warning: Source directory not found: {source_dir}")

            return backup_file
        else:
            # Create directory backup
            os.makedirs(backup_path, exist_ok=True)

            for source_dir in self.source_dirs:
                if os.path.exists(source_dir):
                    dest_dir = os.path.join(backup_path, os.path.basename(source_dir))
                    if os.path.exists(dest_dir):
                        shutil.rmtree(dest_dir)
                    shutil.copytree(source_dir, dest_dir)
                    print(f"Copied: {os.path.basename(source_dir)}")

            return backup_path

    def cleanup_old_backups(self, keep_days=30):
        """
        Remove backups older than specified days.

        Args:
            keep_days (int): Number of days to keep backups

        Returns:
            dict: Cleanup results
        """
        results = {'removed': 0, 'errors': 0, 'total_size_freed': 0}

        cutoff_time = time.time() - (keep_days * 24 * 60 * 60)

        for item in os.listdir(self.backup_dir):
            item_path = os.path.join(self.backup_dir, item)

            # Check if it's a backup file/directory
            if not (item.startswith('backup_') or item.endswith('.tar.gz')):
                continue

            try:
                mod_time = os.path.getmtime(item_path)
                if mod_time < cutoff_time:
                    if os.path.isfile(item_path):
                        size = os.path.getsize(item_path)
                        os.remove(item_path)
                        results['total_size_freed'] += size
                    elif os.path.isdir(item_path):
                        size = sum(os.path.getsize(os.path.join(dirpath, f))
                                 for dirpath, _, files in os.walk(item_path)
                                 for f in files)
                        shutil.rmtree(item_path)
                        results['total_size_freed'] += size

                    results['removed'] += 1
                    print(f"Removed old backup: {item}")

            except Exception as e:
                print(f"Error removing {item}: {e}")
                results['errors'] += 1

        return results

    def list_backups(self):
        """
        List all available backups.

        Returns:
            list: List of backup information
        """
        backups = []

        for item in os.listdir(self.backup_dir):
            item_path = os.path.join(self.backup_dir, item)

            if item.startswith('backup_') or item.endswith('.tar.gz'):
                try:
                    stat_info = os.stat(item_path)
                    backups.append({
                        'name': item,
                        'path': item_path,
                        'size': stat_info.st_size,
                        'created': datetime.fromtimestamp(stat_info.st_mtime),
                        'is_compressed': item.endswith('.tar.gz')
                    })
                except OSError:
                    continue

        # Sort by creation time (newest first)
        backups.sort(key=lambda x: x['created'], reverse=True)
        return backups


class SystemMonitor:
    """Monitor system resources and perform maintenance."""

    def __init__(self):
        self.start_time = time.time()

    def get_disk_usage(self, path='/'):
        """
        Get disk usage information.

        Args:
            path (str): Path to check disk usage for

        Returns:
            dict: Disk usage information
        """
        try:
            stat = os.statvfs(path)
            total = stat.f_blocks * stat.f_frsize
            free = stat.f_available * stat.f_frsize
            used = total - free

            return {
                'total': total,
                'used': used,
                'free': free,
                'used_percent': (used / total) * 100 if total > 0 else 0
            }
        except AttributeError:
            return {'error': 'statvfs not available on this platform'}

    def check_temp_space(self, threshold_mb=100):
        """
        Check if temporary space is running low.

        Args:
            threshold_mb (int): Threshold in MB

        Returns:
            dict: Temp space status
        """
        temp_dir = os.environ.get('TMP', os.environ.get('TEMP', '/tmp'))
        temp_dir = os.path.expanduser(temp_dir)

        if not os.path.exists(temp_dir):
            return {'error': f'Temp directory not found: {temp_dir}'}

        usage = self.get_disk_usage(temp_dir)
        if 'error' in usage:
            return usage

        threshold_bytes = threshold_mb * 1024 * 1024
        low_space = usage['free'] < threshold_bytes

        return {
            'temp_dir': temp_dir,
            'free_mb': usage['free'] / (1024 * 1024),
            'low_space': low_space,
            'threshold_mb': threshold_mb
        }

    def cleanup_temp_files(self, pattern='*', older_than_hours=24):
        """
        Clean up temporary files.

        Args:
            pattern (str): File pattern to match
            older_than_hours (int): Remove files older than this

        Returns:
            dict: Cleanup results
        """
        import glob

        results = {'removed': 0, 'errors': 0, 'total_size_freed': 0}

        temp_dir = os.environ.get('TMP', os.environ.get('TEMP', '/tmp'))
        temp_dir = os.path.expanduser(temp_dir)

        if not os.path.exists(temp_dir):
            return {'error': f'Temp directory not found: {temp_dir}'}

        cutoff_time = time.time() - (older_than_hours * 60 * 60)

        # Find matching files
        pattern_path = os.path.join(temp_dir, pattern)
        temp_files = glob.glob(pattern_path)

        for temp_file in temp_files:
            if not os.path.isfile(temp_file):
                continue

            try:
                mod_time = os.path.getmtime(temp_file)
                if mod_time < cutoff_time:
                    size = os.path.getsize(temp_file)
                    os.remove(temp_file)
                    results['removed'] += 1
                    results['total_size_freed'] += size
                    print(f"Removed temp file: {os.path.basename(temp_file)}")

            except Exception as e:
                print(f"Error removing {temp_file}: {e}")
                results['errors'] += 1

        return results


def main():
    """Main automation script."""
    parser = argparse.ArgumentParser(description='File Organization and Backup Automation')
    parser.add_argument('--organize', nargs='*', help='Organize files by extension in specified directories')
    parser.add_argument('--organize-by-date', nargs='*', help='Organize files by date in specified directories')
    parser.add_argument('--backup', nargs='+', help='Create backup of specified directories')
    parser.add_argument('--backup-dir', default='./backups', help='Backup directory')
    parser.add_argument('--cleanup-backups', type=int, help='Remove backups older than N days')
    parser.add_argument('--remove-duplicates', help='Remove duplicate files in directory')
    parser.add_argument('--monitor-system', action='store_true', help='Monitor system resources')
    parser.add_argument('--cleanup-temp', action='store_true', help='Clean up temporary files')

    args = parser.parse_args()

    if args.organize:
        for source_dir in args.organize:
            if os.path.exists(source_dir):
                print(f"\nOrganizing files in: {source_dir}")
                organizer = FileOrganizer(source_dir)
                results = organizer.organize_by_extension()
                print(f"Results: {results}")
            else:
                print(f"Directory not found: {source_dir}")

    if args.organize_by_date:
        for source_dir in args.organize_by_date:
            if os.path.exists(source_dir):
                print(f"\nOrganizing files by date in: {source_dir}")
                organizer = FileOrganizer(source_dir)
                results = organizer.organize_by_date()
                print(f"Results: {results}")
            else:
                print(f"Directory not found: {source_dir}")

    if args.backup:
        print(f"\nCreating backup of: {args.backup}")
        backup_mgr = BackupManager(args.backup, args.backup_dir)
        backup_path = backup_mgr.create_backup()
        print(f"Backup created: {backup_path}")

    if args.cleanup_backups:
        print(f"\nCleaning up backups older than {args.cleanup_backups} days")
        backup_mgr = BackupManager([], args.backup_dir)  # Empty source list for cleanup
        results = backup_mgr.cleanup_old_backups(args.cleanup_backups)
        print(f"Cleanup results: {results}")

    if args.remove_duplicates:
        if os.path.exists(args.remove_duplicates):
            print(f"\nRemoving duplicates in: {args.remove_duplicates}")
            organizer = FileOrganizer(args.remove_duplicates)
            results = organizer.remove_duplicates(check_content=True)
            print(f"Results: {results}")
        else:
            print(f"Directory not found: {args.remove_duplicates}")

    if args.monitor_system:
        print("\nSystem Monitoring:")
        monitor = SystemMonitor()

        # Check disk usage
        disk_usage = monitor.get_disk_usage()
        if 'error' not in disk_usage:
            print(f"Disk Usage: {disk_usage['used_percent']:.1f}% used, "
                  f"{disk_usage['free']/(1024**3):.1f} GB free")
        else:
            print(f"Disk usage: {disk_usage['error']}")

        # Check temp space
        temp_status = monitor.check_temp_space()
        if 'error' not in temp_status:
            status = "LOW" if temp_status['low_space'] else "OK"
            print(f"Temp Space: {temp_status['free_mb']:.1f} MB free ({status})")
        else:
            print(f"Temp space: {temp_status['error']}")

    if args.cleanup_temp:
        print("\nCleaning up temporary files...")
        monitor = SystemMonitor()
        results = monitor.cleanup_temp_files()
        print(f"Cleanup results: {results}")


if __name__ == "__main__":
    main()
