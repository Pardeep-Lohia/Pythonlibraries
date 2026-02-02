#!/usr/bin/env python3
"""
Git Automation Example

A comprehensive example demonstrating how to automate Git operations using subprocess
in a safe and cross-platform manner.
"""

import subprocess
import sys
import os
import platform
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple


class GitAutomation:
    """A class for automating Git operations safely"""

    def __init__(self, repo_path: str = ".", verbose: bool = False):
        self.repo_path = Path(repo_path).resolve()
        self.verbose = verbose
        self.logger = self._setup_logging()

        # Verify git is available
        self._check_git_available()

    def _setup_logging(self) -> logging.Logger:
        """Set up logging for Git operations"""
        logger = logging.getLogger('GitAutomation')
        logger.setLevel(logging.DEBUG if self.verbose else logging.INFO)

        # Remove any existing handlers
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        # Console handler
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(levelname)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

    def _check_git_available(self) -> None:
        """Check if Git is available on the system"""
        try:
            result = subprocess.run(['git', '--version'],
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                version = result.stdout.strip()
                self.logger.debug(f"Git available: {version}")
            else:
                raise RuntimeError("Git command failed")
        except (FileNotFoundError, subprocess.TimeoutExpired):
            raise RuntimeError("Git is not available on this system")

    def _run_git_command(self, args: List[str], **kwargs) -> subprocess.CompletedProcess:
        """Run a Git command safely"""
        command = ['git'] + args

        # Set default kwargs
        defaults = {
            'cwd': self.repo_path,
            'capture_output': True,
            'text': True,
            'timeout': 60
        }
        defaults.update(kwargs)

        self.logger.debug(f"Running: {' '.join(command)}")

        try:
            result = subprocess.run(command, **defaults)

            if result.returncode != 0 and 'check' not in kwargs:
                self.logger.warning(f"Git command failed: {' '.join(args)}")
                if result.stderr:
                    self.logger.warning(f"Error: {result.stderr.strip()}")

            return result

        except subprocess.TimeoutExpired:
            self.logger.error(f"Git command timed out: {' '.join(args)}")
            raise
        except Exception as e:
            self.logger.error(f"Git command error: {e}")
            raise

    def is_git_repository(self) -> bool:
        """Check if the current directory is a Git repository"""
        try:
            result = self._run_git_command(['rev-parse', '--git-dir'])
            return result.returncode == 0
        except:
            return False

    def init_repository(self, initial_commit: bool = True) -> bool:
        """Initialize a new Git repository"""
        if self.is_git_repository():
            self.logger.info("Repository already initialized")
            return True

        self.logger.info("Initializing Git repository...")

        # Initialize repository
        result = self._run_git_command(['init'])
        if result.returncode != 0:
            return False

        # Create initial .gitignore if it doesn't exist
        gitignore_path = self.repo_path / '.gitignore'
        if not gitignore_path.exists():
            try:
                with open(gitignore_path, 'w') as f:
                    f.write("# Python\n__pycache__/\n*.pyc\n*.pyo\n*.pyd\n.Python\n")
                    f.write("env/\nvenv/\n.venv/\n")
                    f.write("# IDE\n.vscode/\n.idea/\n*.swp\n*.swo\n")
                    f.write("# OS\n.DS_Store\nThumbs.db\n")
                self.logger.info("Created default .gitignore")
            except Exception as e:
                self.logger.warning(f"Could not create .gitignore: {e}")

        # Initial commit
        if initial_commit:
            return self.initial_commit()
        else:
            return True

    def initial_commit(self) -> bool:
        """Create an initial commit with all files"""
        try:
            # Add all files
            self._run_git_command(['add', '.'])

            # Check if there are files to commit
            status_result = self._run_git_command(['status', '--porcelain'])
            if not status_result.stdout.strip():
                self.logger.info("No files to commit")
                return True

            # Commit
            result = self._run_git_command(['commit', '-m', 'Initial commit'])
            if result.returncode == 0:
                self.logger.info("Initial commit created")
                return True
            else:
                return False

        except Exception as e:
            self.logger.error(f"Failed to create initial commit: {e}")
            return False

    def get_status(self) -> Dict[str, List[str]]:
        """Get repository status"""
        result = self._run_git_command(['status', '--porcelain'])

        status = {
            'staged': [],
            'modified': [],
            'untracked': [],
            'deleted': []
        }

        for line in result.stdout.splitlines():
            status_code = line[:2]
            filename = line[3:]

            if status_code[0] in 'MAD':
                status['staged'].append(filename)
            if status_code[1] in 'MAD':
                status['modified'].append(filename)

            if status_code == '??':
                status['untracked'].append(filename)
            elif status_code[1] == 'D':
                status['deleted'].append(filename)

        return status

    def add_files(self, files: List[str] = None) -> bool:
        """Add files to staging area"""
        if files is None:
            # Add all files
            result = self._run_git_command(['add', '.'])
        else:
            # Validate files exist
            valid_files = []
            for file in files:
                file_path = self.repo_path / file
                if file_path.exists():
                    valid_files.append(file)
                else:
                    self.logger.warning(f"File not found: {file}")

            if not valid_files:
                self.logger.warning("No valid files to add")
                return False

            result = self._run_git_command(['add'] + valid_files)

        return result.returncode == 0

    def commit(self, message: str, amend: bool = False) -> bool:
        """Create a commit"""
        if not message.strip():
            self.logger.error("Commit message cannot be empty")
            return False

        args = ['commit', '-m', message]
        if amend:
            args.append('--amend')

        result = self._run_git_command(args)
        if result.returncode == 0:
            self.logger.info("Commit created successfully")
            return True
        else:
            return False

    def push(self, remote: str = 'origin', branch: str = None) -> bool:
        """Push commits to remote repository"""
        if branch is None:
            # Get current branch
            branch_result = self._run_git_command(['branch', '--show-current'])
            if branch_result.returncode != 0:
                self.logger.error("Could not determine current branch")
                return False
            branch = branch_result.stdout.strip()

        self.logger.info(f"Pushing to {remote}/{branch}...")
        result = self._run_git_command(['push', remote, branch])

        if result.returncode == 0:
            self.logger.info("Push successful")
            return True
        else:
            return False

    def pull(self, remote: str = 'origin', branch: str = None) -> bool:
        """Pull changes from remote repository"""
        args = ['pull']
        if remote:
            args.append(remote)
        if branch:
            args.append(branch)

        result = self._run_git_command(args)
        return result.returncode == 0

    def clone_repository(self, url: str, target_path: str = None) -> bool:
        """Clone a repository"""
        if target_path is None:
            # Extract repo name from URL
            repo_name = url.split('/')[-1]
            if repo_name.endswith('.git'):
                repo_name = repo_name[:-4]
            target_path = repo_name

        self.logger.info(f"Cloning {url} to {target_path}...")

        # Clone to parent directory
        clone_path = self.repo_path.parent / target_path

        result = subprocess.run(['git', 'clone', url, str(clone_path)],
                              capture_output=True, text=True, timeout=300)

        if result.returncode == 0:
            self.logger.info("Repository cloned successfully")
            return True
        else:
            self.logger.error(f"Clone failed: {result.stderr.strip()}")
            return False

    def create_branch(self, branch_name: str, checkout: bool = True) -> bool:
        """Create a new branch"""
        if not branch_name.strip():
            self.logger.error("Branch name cannot be empty")
            return False

        args = ['checkout', '-b', branch_name] if checkout else ['branch', branch_name]

        result = self._run_git_command(args)
        if result.returncode == 0:
            action = "created and checked out" if checkout else "created"
            self.logger.info(f"Branch '{branch_name}' {action}")
            return True
        else:
            return False

    def switch_branch(self, branch_name: str) -> bool:
        """Switch to a different branch"""
        result = self._run_git_command(['checkout', branch_name])
        if result.returncode == 0:
            self.logger.info(f"Switched to branch '{branch_name}'")
            return True
        else:
            return False

    def get_branches(self) -> Tuple[str, List[str]]:
        """Get current branch and list of all branches"""
        # Get current branch
        current_result = self._run_git_command(['branch', '--show-current'])
        current_branch = current_result.stdout.strip() if current_result.returncode == 0 else None

        # Get all branches
        branches_result = self._run_git_command(['branch', '--all'])
        branches = []
        if branches_result.returncode == 0:
            for line in branches_result.stdout.splitlines():
                branch = line.strip().lstrip('* ')
                if branch:
                    branches.append(branch)

        return current_branch, branches

    def add_remote(self, name: str, url: str) -> bool:
        """Add a remote repository"""
        result = self._run_git_command(['remote', 'add', name, url])
        if result.returncode == 0:
            self.logger.info(f"Remote '{name}' added: {url}")
            return True
        else:
            return False

    def get_remotes(self) -> Dict[str, str]:
        """Get remote repositories"""
        result = self._run_git_command(['remote', '-v'])
        remotes = {}

        if result.returncode == 0:
            for line in result.stdout.splitlines():
                parts = line.split()
                if len(parts) >= 2:
                    name, url = parts[0], parts[1]
                    remotes[name] = url

        return remotes

    def get_log(self, count: int = 10, oneline: bool = True) -> List[str]:
        """Get commit log"""
        args = ['log']
        if oneline:
            args.append('--oneline')
        args.extend(['-n', str(count)])

        result = self._run_git_command(args)
        if result.returncode == 0:
            return result.stdout.splitlines()
        else:
            return []

    def batch_operations(self, operations: List[Dict]) -> Dict[str, bool]:
        """Perform multiple Git operations in batch"""
        results = {}

        for op in operations:
            op_type = op.get('type')
            op_name = op.get('name', op_type)

            try:
                if op_type == 'add':
                    success = self.add_files(op.get('files'))
                elif op_type == 'commit':
                    success = self.commit(op.get('message'), op.get('amend', False))
                elif op_type == 'push':
                    success = self.push(op.get('remote', 'origin'), op.get('branch'))
                elif op_type == 'pull':
                    success = self.pull(op.get('remote', 'origin'), op.get('branch'))
                elif op_type == 'create_branch':
                    success = self.create_branch(op['branch_name'], op.get('checkout', True))
                elif op_type == 'switch_branch':
                    success = self.switch_branch(op['branch_name'])
                else:
                    self.logger.error(f"Unknown operation type: {op_type}")
                    success = False

                results[op_name] = success

            except Exception as e:
                self.logger.error(f"Operation '{op_name}' failed: {e}")
                results[op_name] = False

        return results

    def sync_repository(self, remote: str = 'origin', branch: str = None) -> bool:
        """Sync repository with remote (fetch + merge/rebase)"""
        self.logger.info("Syncing repository...")

        # Fetch latest changes
        fetch_result = self._run_git_command(['fetch', remote])
        if fetch_result.returncode != 0:
            return False

        # Get current branch if not specified
        if branch is None:
            current_result = self._run_git_command(['branch', '--show-current'])
            if current_result.returncode != 0:
                return False
            branch = current_result.stdout.strip()

        # Try to rebase first (cleaner history), fall back to merge
        rebase_result = self._run_git_command(['rebase', f'{remote}/{branch}'])

        if rebase_result.returncode == 0:
            self.logger.info("Repository synced with rebase")
            return True
        else:
            # Abort rebase if it failed
            self._run_git_command(['rebase', '--abort'])

            # Fall back to merge
            merge_result = self._run_git_command(['merge', f'{remote}/{branch}'])
            if merge_result.returncode == 0:
                self.logger.info("Repository synced with merge")
                return True
            else:
                self.logger.error("Failed to sync repository")
                return False


def main():
    """Main function demonstrating Git automation"""
    import argparse

    parser = argparse.ArgumentParser(description="Git Automation Tool")
    parser.add_argument('--repo', default='.', help='Repository path')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--init', action='store_true', help='Initialize repository')
    parser.add_argument('--status', action='store_true', help='Show repository status')
    parser.add_argument('--add', nargs='*', help='Add files to staging')
    parser.add_argument('--commit', help='Commit with message')
    parser.add_argument('--push', action='store_true', help='Push to remote')
    parser.add_argument('--pull', action='store_true', help='Pull from remote')
    parser.add_argument('--clone', help='Clone repository from URL')
    parser.add_argument('--branch', help='Branch name for operations')
    parser.add_argument('--create-branch', help='Create new branch')

    args = parser.parse_args()

    try:
        git = GitAutomation(args.repo, args.verbose)

        if args.init:
            success = git.init_repository()
            print(f"Repository initialization: {'✓' if success else '✗'}")

        elif args.status:
            if not git.is_git_repository():
                print("Not a Git repository")
                return 1

            status = git.get_status()
            current_branch, branches = git.get_branches()

            print(f"Current branch: {current_branch}")
            print(f"All branches: {', '.join(branches)}")

            print("\nStatus:")
            for category, files in status.items():
                if files:
                    print(f"  {category.capitalize()}: {', '.join(files)}")

        elif args.add is not None:
            success = git.add_files(args.add if args.add else None)
            print(f"Add operation: {'✓' if success else '✗'}")

        elif args.commit:
            success = git.commit(args.commit)
            print(f"Commit operation: {'✓' if success else '✗'}")

        elif args.push:
            success = git.push(branch=args.branch)
            print(f"Push operation: {'✓' if success else '✗'}")

        elif args.pull:
            success = git.pull(branch=args.branch)
            print(f"Pull operation: {'✓' if success else '✗'}")

        elif args.clone:
            success = git.clone_repository(args.clone)
            print(f"Clone operation: {'✓' if success else '✗'}")

        elif args.create_branch:
            success = git.create_branch(args.create_branch)
            print(f"Create branch operation: {'✓' if success else '✗'}")

        else:
            parser.print_help()

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
