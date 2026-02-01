#!/usr/bin/env python3
"""
Project Archiver Example

This script demonstrates how to create a comprehensive project archiving system
using shutil. It can archive entire projects with proper exclusion of build artifacts,
temporary files, and version control directories.
"""

import shutil
import os
import time
from pathlib import Path
from typing import List, Set, Optional
import argparse


class ProjectArchiver:
    """A class for archiving software projects with intelligent file selection."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.stats = {'files_processed': 0, 'total_size': 0, 'excluded_count': 0}

    def get_default_exclusions(self) -> Set[str]:
        """Get default patterns for files/directories to exclude from archives."""
        return {
            # Version control
            '.git', '.svn', '.hg', '.bzr',
            # Build artifacts
            'build', 'dist', '__pycache__', '*.pyc', '*.pyo', '*.pyd',
            # IDE files
            '.vscode', '.idea', '*.swp', '*.swo', '*~',
            # OS files
            '.DS_Store', 'Thumbs.db', 'desktop.ini',
            # Temporary files
            '*.tmp', '*.temp', '*.log', '*.cache',
            # Node.js
            'node_modules', 'npm-debug.log*', 'yarn-error.log*',
            # Python
            '.venv', 'venv', 'env', '.env', '*.egg-info',
            # Archives
            '*.zip', '*.tar.gz', '*.tar.bz2', '*.tar.xz',
        }

    def should_exclude(self, path: str, exclusions: Set[str]) -> bool:
        """Check if a path should be excluded from archiving."""
        path_obj = Path(path)

        # Check exact directory/file name matches
        if path_obj.name in exclusions:
            return True

        # Check pattern matches
        import fnmatch
        for pattern in exclusions:
            if '*' in pattern or '?' in pattern:
                if fnmatch.fnmatch(path_obj.name, pattern) or \
                   fnmatch.fnmatch(str(path_obj), pattern):
                    return True

        return False

    def collect_project_files(self, project_path: str, exclusions: Optional[Set[str]] = None) -> List[str]:
        """Collect all files to be included in the archive."""
        if exclusions is None:
            exclusions = self.get_default_exclusions()

        included_files = []

        try:
            for root, dirs, files in os.walk(project_path):
                # Filter directories
                dirs[:] = [d for d in dirs if not self.should_exclude(os.path.join(root, d), exclusions)]

                for file in files:
                    file_path = os.path.join(root, file)
                    if not self.should_exclude(file_path, exclusions):
                        included_files.append(file_path)
                        self.stats['files_processed'] += 1
                        try:
                            self.stats['total_size'] += os.path.getsize(file_path)
                        except OSError:
                            pass
                    else:
                        self.stats['excluded_count'] += 1

        except (OSError, PermissionError) as e:
            if self.verbose:
                print(f"Error accessing {project_path}: {e}")

        return included_files

    def create_project_archive(self, project_path: str, archive_name: Optional[str] = None,
                             format: str = 'zip', exclusions: Optional[Set[str]] = None) -> str:
        """Create an archive of the project with intelligent exclusions."""
        project_path = Path(project_path).resolve()
        if not project_path.exists():
            raise FileNotFoundError(f"Project path does not exist: {project_path}")

        # Generate archive name if not provided
        if archive_name is None:
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            project_name = project_path.name
            archive_name = f"{project_name}_{timestamp}"

        # Determine archive path
        archive_path = f"{archive_name}.{self._get_extension(format)}"

        if self.verbose:
            print(f"Creating {format.upper()} archive: {archive_path}")
            print(f"Scanning project: {project_path}")

        # Collect files to archive
        included_files = self.collect_project_files(str(project_path), exclusions)

        if not included_files:
            raise ValueError("No files found to archive")

        if self.verbose:
            print(f"Files to archive: {len(included_files)}")
            print(f"Excluded: {self.stats['excluded_count']}")
            size_mb = self.stats['total_size'] / (1024 * 1024)
            print(f"Total size: {size_mb:.1f} MB")

        # Create the archive
        try:
            if format == 'zip':
                self._create_zip_archive(archive_path, included_files, project_path)
            elif format in ['tar', 'gztar', 'bztar', 'xztar']:
                self._create_tar_archive(archive_path, included_files, project_path, format)
            else:
                raise ValueError(f"Unsupported archive format: {format}")

            if self.verbose:
                archive_size = os.path.getsize(archive_path) / (1024 * 1024)
                print(f"Archive created: {archive_path} ({archive_size:.1f} MB)")

        except Exception as e:
            # Clean up partial archive on failure
            if os.path.exists(archive_path):
                os.remove(archive_path)
            raise

        return archive_path

    def _create_zip_archive(self, archive_path: str, files: List[str], base_path: Path):
        """Create a ZIP archive."""
        import zipfile

        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in files:
                # Calculate relative path for archive
                rel_path = os.path.relpath(file_path, base_path)
                zf.write(file_path, rel_path)

    def _create_tar_archive(self, archive_path: str, files: List[str], base_path: Path, format: str):
        """Create a TAR archive (possibly compressed)."""
        import tarfile

        mode = {'tar': 'w', 'gztar': 'w:gz', 'bztar': 'w:bz2', 'xztar': 'w:xz'}[format]

        with tarfile.open(archive_path, mode) as tf:
            for file_path in files:
                # Calculate relative path for archive
                rel_path = os.path.relpath(file_path, base_path)
                tf.add(file_path, rel_path)

    def _get_extension(self, format: str) -> str:
        """Get file extension for archive format."""
        extensions = {
            'zip': 'zip',
            'tar': 'tar',
            'gztar': 'tar.gz',
            'bztar': 'tar.bz2',
            'xztar': 'tar.xz'
        }
        return extensions.get(format, 'zip')

    def list_archive_contents(self, archive_path: str) -> List[str]:
        """List contents of an archive."""
        if not os.path.exists(archive_path):
            raise FileNotFoundError(f"Archive not found: {archive_path}")

        contents = []

        if archive_path.endswith('.zip'):
            import zipfile
            with zipfile.ZipFile(archive_path, 'r') as zf:
                contents = zf.namelist()
        elif archive_path.endswith(('.tar', '.tar.gz', '.tar.bz2', '.tar.xz')):
            import tarfile
            with tarfile.open(archive_path, 'r') as tf:
                contents = [member.name for member in tf.getmembers()]

        return sorted(contents)

    def extract_project_archive(self, archive_path: str, extract_path: str) -> str:
        """Extract a project archive."""
        if not os.path.exists(archive_path):
            raise FileNotFoundError(f"Archive not found: {archive_path}")

        os.makedirs(extract_path, exist_ok=True)

        if self.verbose:
            print(f"Extracting {archive_path} to {extract_path}")

        # Use shutil to extract
        shutil.unpack_archive(archive_path, extract_path)

        if self.verbose:
            print("Extraction completed")

        return extract_path

    def get_archive_info(self, archive_path: str) -> dict:
        """Get information about an archive."""
        if not os.path.exists(archive_path):
            raise FileNotFoundError(f"Archive not found: {archive_path}")

        stat = os.stat(archive_path)
        info = {
            'path': archive_path,
            'size': stat.st_size,
            'size_mb': stat.st_size / (1024 * 1024),
            'modified': time.ctime(stat.st_mtime),
            'format': self._detect_format(archive_path)
        }

        # Get contents count
        try:
            contents = self.list_archive_contents(archive_path)
            info['file_count'] = len(contents)
            info['contents_preview'] = contents[:5]  # First 5 files
        except Exception:
            info['file_count'] = 0
            info['contents_preview'] = []

        return info

    def _detect_format(self, archive_path: str) -> str:
        """Detect archive format from file extension."""
        if archive_path.endswith('.zip'):
            return 'zip'
        elif archive_path.endswith('.tar'):
            return 'tar'
        elif archive_path.endswith('.tar.gz'):
            return 'tar.gz'
        elif archive_path.endswith('.tar.bz2'):
            return 'tar.bz2'
        elif archive_path.endswith('.tar.xz'):
            return 'tar.xz'
        else:
            return 'unknown'


def create_sample_project():
    """Create a sample project for demonstration."""
    project_dir = Path("sample_project")
    project_dir.mkdir(exist_ok=True)

    # Create project structure
    (project_dir / "README.md").write_text("# Sample Project\n\nThis is a demo project.")
    (project_dir / "main.py").write_text("print('Hello, World!')")
    (project_dir / "config.py").write_text("DEBUG = True\nSECRET_KEY = 'demo'")

    # Create some modules
    (project_dir / "utils").mkdir(exist_ok=True)
    (project_dir / "utils" / "__init__.py").write_text("")
    (project_dir / "utils" / "helpers.py").write_text("def helper():\n    pass")

    # Create build artifacts to be excluded
    (project_dir / "__pycache__").mkdir(exist_ok=True)
    (project_dir / "__pycache__" / "main.cpython-38.pyc").write_bytes(b"fake pyc")

    (project_dir / ".git").mkdir(exist_ok=True)
    (project_dir / ".git" / "config").write_text("[core]\n\trepositoryformatversion = 0")

    (project_dir / "dist").mkdir(exist_ok=True)
    (project_dir / "dist" / "app.zip").write_bytes(b"fake zip")

    return str(project_dir)


def demonstrate_basic_archiving():
    """Demonstrate basic project archiving."""
    print("=== Basic Project Archiving Demo ===")

    # Create sample project
    project_path = create_sample_project()

    # Create archiver
    archiver = ProjectArchiver(verbose=True)

    # Create ZIP archive
    archive_path = archiver.create_project_archive(project_path, format='zip')

    print(f"\nArchive created: {archive_path}")

    # List contents
    contents = archiver.list_archive_contents(archive_path)
    print(f"\nArchive contents ({len(contents)} files):")
    for item in contents[:10]:  # Show first 10
        print(f"  {item}")
    if len(contents) > 10:
        print(f"  ... and {len(contents) - 10} more files")

    # Get archive info
    info = archiver.get_archive_info(archive_path)
    print(f"\nArchive info:")
    print(f"  Size: {info['size_mb']:.2f} MB")
    print(f"  Files: {info['file_count']}")
    print(f"  Format: {info['format']}")


def demonstrate_format_options():
    """Demonstrate different archive formats."""
    print("\n=== Archive Format Options Demo ===")

    project_path = "sample_project"
    archiver = ProjectArchiver(verbose=True)

    formats = ['zip', 'tar', 'gztar']

    for fmt in formats:
        try:
            archive_path = archiver.create_project_archive(
                project_path,
                archive_name=f"sample_project_{fmt}",
                format=fmt
            )

            size = os.path.getsize(archive_path) / 1024  # KB
            print(f"Created {fmt.upper()}: {archive_path} ({size:.1f} KB)")

        except Exception as e:
            print(f"Failed to create {fmt.upper()}: {e}")


def demonstrate_custom_exclusions():
    """Demonstrate custom exclusion patterns."""
    print("\n=== Custom Exclusions Demo ===")

    project_path = "sample_project"
    archiver = ProjectArchiver(verbose=True)

    # Add custom exclusions
    custom_exclusions = archiver.get_default_exclusions()
    custom_exclusions.update({'*.md', 'config.py'})  # Exclude markdown and config

    archive_path = archiver.create_project_archive(
        project_path,
        archive_name="sample_project_custom",
        exclusions=custom_exclusions
    )

    contents = archiver.list_archive_contents(archive_path)
    print(f"\nArchive with custom exclusions ({len(contents)} files):")
    for item in contents:
        print(f"  {item}")


def demonstrate_extraction():
    """Demonstrate archive extraction."""
    print("\n=== Archive Extraction Demo ===")

    archiver = ProjectArchiver(verbose=True)

    # Extract the ZIP archive
    extract_path = "extracted_project"
    archiver.extract_project_archive("sample_project.zip", extract_path)

    # Verify extraction
    if os.path.exists(extract_path):
        print(f"\nExtracted to: {extract_path}")
        extracted_files = []
        for root, dirs, files in os.walk(extract_path):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), extract_path)
                extracted_files.append(rel_path)

        print(f"Extracted files ({len(extracted_files)}):")
        for file in sorted(extracted_files)[:10]:
            print(f"  {file}")


def demonstrate_error_handling():
    """Demonstrate error handling."""
    print("\n=== Error Handling Demo ===")

    archiver = ProjectArchiver(verbose=True)

    # Try to archive non-existent project
    try:
        archiver.create_project_archive("nonexistent_project")
    except Exception as e:
        print(f"Expected error for non-existent project: {e}")

    # Try to extract non-existent archive
    try:
        archiver.extract_project_archive("nonexistent.zip", "extract_test")
    except Exception as e:
        print(f"Expected error for non-existent archive: {e}")


def cleanup_demo_files():
    """Clean up files created during demonstrations."""
    print("\n=== Cleaning Up Demo Files ===")

    files_to_remove = [
        "sample_project.zip",
        "sample_project.tar",
        "sample_project.tar.gz",
        "sample_project_custom.zip"
    ]

    dirs_to_remove = [
        "sample_project",
        "extracted_project"
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
    """Main demonstration function."""
    parser = argparse.ArgumentParser(description="Project Archiver Demo")
    parser.add_argument('--project', help='Path to project to archive')
    parser.add_argument('--format', choices=['zip', 'tar', 'gztar', 'bztar', 'xztar'],
                       default='zip', help='Archive format')
    parser.add_argument('--output', help='Output archive name')

    args = parser.parse_args()

    if args.project:
        # Archive specified project
        archiver = ProjectArchiver(verbose=True)
        try:
            archive_path = archiver.create_project_archive(
                args.project,
                archive_name=args.output,
                format=args.format
            )
            print(f"Project archived: {archive_path}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        # Run demonstrations
        print("Project Archiver Demonstrations")
        print("=" * 35)

        demonstrate_basic_archiving()
        demonstrate_format_options()
        demonstrate_custom_exclusions()
        demonstrate_extraction()
        demonstrate_error_handling()

        cleanup_demo_files()

        print("\nAll demonstrations completed!")


if __name__ == "__main__":
    main()
