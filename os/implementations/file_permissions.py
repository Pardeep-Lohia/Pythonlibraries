"""
File Permissions Implementation

This module demonstrates file permission management using the os module,
including setting permissions, checking access, and handling security.
"""

import os
import os.path
import stat
from typing import Optional, List, Dict, Any


class PermissionManager:
    """
    A class for managing file and directory permissions.
    """

    def __init__(self):
        """Initialize the permission manager."""
        self.platform = os.name

    def get_permissions(self, path: str) -> Optional[str]:
        """
        Get the current permissions of a file or directory.

        Args:
            path (str): Path to check

        Returns:
            str or None: Permission string (e.g., 'rw-r--r--') or None if error
        """
        try:
            stat_info = os.stat(path)
            mode = stat_info.st_mode

            # Convert to permission string
            return self._mode_to_string(mode)
        except OSError:
            return None

    def set_permissions(self, path: str, permissions: str) -> bool:
        """
        Set permissions for a file or directory.

        Args:
            path (str): Path to modify
            permissions (str): Permission string (e.g., '755', 'rwxr-xr-x')

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if permissions.isdigit():
                # Octal notation
                mode = int(permissions, 8)
            else:
                # Symbolic notation
                mode = self._string_to_mode(permissions)

            os.chmod(path, mode)
            return True
        except (OSError, ValueError):
            return False

    def make_executable(self, path: str) -> bool:
        """
        Make a file executable.

        Args:
            path (str): Path to the file

        Returns:
            bool: True if successful
        """
        try:
            current_mode = os.stat(path).st_mode
            # Add execute permission for owner
            new_mode = current_mode | stat.S_IXUSR
            os.chmod(path, new_mode)
            return True
        except OSError:
            return False

    def make_readonly(self, path: str) -> bool:
        """
        Make a file read-only.

        Args:
            path (str): Path to the file

        Returns:
            bool: True if successful
        """
        try:
            current_mode = os.stat(path).st_mode
            # Remove write permissions for owner, group, and others
            new_mode = current_mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)
            os.chmod(path, new_mode)
            return True
        except OSError:
            return False

    def check_access(self, path: str, access_type: str) -> bool:
        """
        Check if the current user has specific access to a path.

        Args:
            path (str): Path to check
            access_type (str): Type of access ('read', 'write', 'execute')

        Returns:
            bool: True if access is allowed
        """
        access_map = {
            'read': os.R_OK,
            'write': os.W_OK,
            'execute': os.X_OK
        }

        if access_type not in access_map:
            return False

        return os.access(path, access_map[access_type])

    def get_ownership(self, path: str) -> Optional[Dict[str, Any]]:
        """
        Get ownership information for a file or directory.

        Args:
            path (str): Path to check

        Returns:
            dict or None: Ownership information or None if error
        """
        try:
            stat_info = os.stat(path)
            return {
                'uid': stat_info.st_uid,
                'gid': stat_info.st_gid,
                'owner_name': self._get_username(stat_info.st_uid),
                'group_name': self._get_groupname(stat_info.st_gid)
            }
        except OSError:
            return None

    def set_ownership(self, path: str, uid: Optional[int] = None,
                     gid: Optional[int] = None) -> bool:
        """
        Set ownership of a file or directory.

        Args:
            path (str): Path to modify
            uid (int): User ID (-1 to leave unchanged)
            gid (int): Group ID (-1 to leave unchanged)

        Returns:
            bool: True if successful
        """
        try:
            if uid is None:
                uid = -1
            if gid is None:
                gid = -1

            os.chown(path, uid, gid)
            return True
        except OSError:
            return False

    def _mode_to_string(self, mode: int) -> str:
        """Convert a mode integer to a permission string."""
        perms = []
        for who in ['USR', 'GRP', 'OTH']:
            perm = ''
            for what in [('R', getattr(stat, f'S_IR{who}')),
                        ('W', getattr(stat, f'S_IW{who}')),
                        ('X', getattr(stat, f'S_IX{who}'))]:
                perm += what[0] if mode & what[1] else '-'
            perms.append(perm)
        return ''.join(perms)

    def _string_to_mode(self, perm_string: str) -> int:
        """Convert a permission string to mode integer."""
        if len(perm_string) != 9:
            raise ValueError("Permission string must be 9 characters")

        mode = 0
        for i, char in enumerate(perm_string):
            if char not in '-rwx':
                raise ValueError("Invalid character in permission string")

            if char != '-':
                # Calculate which permission bit this is
                who_index = i // 3  # 0=user, 1=group, 2=others
                perm_index = i % 3  # 0=read, 1=write, 2=execute

                who_map = ['USR', 'GRP', 'OTH']
                perm_map = ['R', 'W', 'X']

                stat_const = getattr(stat, f'S_I{perm_map[perm_index]}{who_map[who_index]}')
                mode |= stat_const

        return mode

    def _get_username(self, uid: int) -> str:
        """Get username from UID."""
        try:
            import pwd
            return pwd.getpwuid(uid).pw_name
        except (ImportError, KeyError):
            return str(uid)

    def _get_groupname(self, gid: int) -> str:
        """Get group name from GID."""
        try:
            import grp
            return grp.getgrgid(gid).gr_name
        except (ImportError, KeyError):
            return str(gid)


def analyze_permissions_recursive(directory: str) -> Dict[str, Any]:
    """
    Analyze permissions recursively in a directory.

    Args:
        directory (str): Directory to analyze

    Returns:
        dict: Permission analysis results
    """
    analysis = {
        'total_files': 0,
        'readable_files': 0,
        'writable_files': 0,
        'executable_files': 0,
        'permission_issues': [],
        'ownership_variations': set()
    }

    pm = PermissionManager()

    for root, dirs, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            analysis['total_files'] += 1

            # Check permissions
            if pm.check_access(filepath, 'read'):
                analysis['readable_files'] += 1
            if pm.check_access(filepath, 'write'):
                analysis['writable_files'] += 1
            if pm.check_access(filepath, 'execute'):
                analysis['executable_files'] += 1

            # Check ownership
            ownership = pm.get_ownership(filepath)
            if ownership:
                owner_key = f"{ownership['owner_name']}:{ownership['group_name']}"
                analysis['ownership_variations'].add(owner_key)

            # Check for permission issues
            perms = pm.get_permissions(filepath)
            if perms:
                # Check for world-writable files
                if perms[7] in ['w', 'x']:  # Others can write or execute
                    analysis['permission_issues'].append({
                        'path': filepath,
                        'issue': 'world_writable',
                        'permissions': perms
                    })

    analysis['ownership_variations'] = list(analysis['ownership_variations'])
    return analysis


def fix_common_permission_issues(directory: str, dry_run: bool = True) -> List[str]:
    """
    Fix common permission issues in a directory.

    Args:
        directory (str): Directory to fix
        dry_run (bool): If True, only report what would be changed

    Returns:
        list: List of actions taken or that would be taken
    """
    actions = []
    pm = PermissionManager()

    for root, dirs, files in os.walk(directory):
        # Fix directory permissions (should be 755)
        for dirname in dirs:
            dirpath = os.path.join(root, dirname)
            current_perms = pm.get_permissions(dirpath)
            if current_perms and current_perms != 'rwxr-xr-x':
                if dry_run:
                    actions.append(f"Would change {dirpath} permissions to 755 (current: {current_perms})")
                else:
                    if pm.set_permissions(dirpath, '755'):
                        actions.append(f"Changed {dirpath} permissions to 755")
                    else:
                        actions.append(f"Failed to change {dirpath} permissions")

        # Fix file permissions (should be 644 for regular files)
        for filename in files:
            filepath = os.path.join(root, filename)
            current_perms = pm.get_permissions(filepath)

            if current_perms:
                # Check if it's a script (has shebang or .sh/.py extension)
                is_script = False
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        first_line = f.readline()
                        if first_line.startswith('#!'):
                            is_script = True
                except:
                    pass

                if filename.endswith(('.sh', '.py', '.pl', '.rb')):
                    is_script = True

                if is_script and not current_perms[3] == 'x':  # Owner execute
                    if dry_run:
                        actions.append(f"Would make {filepath} executable (current: {current_perms})")
                    else:
                        if pm.make_executable(filepath):
                            actions.append(f"Made {filepath} executable")
                        else:
                            actions.append(f"Failed to make {filepath} executable")
                elif not is_script and current_perms != 'rw-r--r--':
                    if dry_run:
                        actions.append(f"Would change {filepath} permissions to 644 (current: {current_perms})")
                    else:
                        if pm.set_permissions(filepath, '644'):
                            actions.append(f"Changed {filepath} permissions to 644")
                        else:
                            actions.append(f"Failed to change {filepath} permissions")

    return actions


def create_secure_file(filepath: str, content: str = "", permissions: str = "600") -> bool:
    """
    Create a file with secure permissions.

    Args:
        filepath (str): Path to create
        content (str): File content
        permissions (str): Permission string

    Returns:
        bool: True if successful
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Create file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        # Set secure permissions
        pm = PermissionManager()
        return pm.set_permissions(filepath, permissions)

    except Exception:
        return False


def demonstrate_file_permissions():
    """Demonstrate file permission operations."""

    print("=== File Permissions Demo ===\n")

    # Create a test file
    test_file = 'test_permissions.txt'
    with open(test_file, 'w') as f:
        f.write('This is a test file for permissions demo.')

    pm = PermissionManager()

    print("1. Current Permissions:")
    current_perms = pm.get_permissions(test_file)
    print(f"   {test_file}: {current_perms}")
    print()

    print("2. Permission Checks:")
    print(f"   Readable: {pm.check_access(test_file, 'read')}")
    print(f"   Writable: {pm.check_access(test_file, 'write')}")
    print(f"   Executable: {pm.check_access(test_file, 'execute')}")
    print()

    print("3. Changing Permissions:")
    # Make it executable
    if pm.make_executable(test_file):
        print("   Made file executable")
        new_perms = pm.get_permissions(test_file)
        print(f"   New permissions: {new_perms}")
    else:
        print("   Failed to make file executable")
    print()

    print("4. Ownership Information:")
    ownership = pm.get_ownership(test_file)
    if ownership:
        print(f"   Owner: {ownership['owner_name']} (UID: {ownership['uid']})")
        print(f"   Group: {ownership['group_name']} (GID: {ownership['gid']})")
    else:
        print("   Could not get ownership information")
    print()

    print("5. Creating Secure File:")
    secure_file = 'secure_file.txt'
    if create_secure_file(secure_file, 'Secret content', '600'):
        print(f"   Created secure file: {secure_file}")
        secure_perms = pm.get_permissions(secure_file)
        print(f"   Permissions: {secure_perms}")
    else:
        print("   Failed to create secure file")
    print()

    print("6. Permission Analysis:")
    # Analyze current directory
    analysis = analyze_permissions_recursive('.')
    print(f"   Total files analyzed: {analysis['total_files']}")
    print(f"   Readable files: {analysis['readable_files']}")
    print(f"   Writable files: {analysis['writable_files']}")
    print(f"   Executable files: {analysis['executable_files']}")
    print(f"   Unique ownership combinations: {len(analysis['ownership_variations'])}")
    if analysis['permission_issues']:
        print(f"   Permission issues found: {len(analysis['permission_issues'])}")
    print()

    print("7. Permission Fixes (Dry Run):")
    fixes = fix_common_permission_issues('.', dry_run=True)
    if fixes:
        print("   Suggested fixes:")
        for fix in fixes[:5]:  # Show first 5
            print(f"     {fix}")
        if len(fixes) > 5:
            print(f"     ... and {len(fixes) - 5} more")
    else:
        print("   No permission fixes needed")
    print()

    # Cleanup
    print("8. Cleanup:")
    try:
        os.remove(test_file)
        print(f"   Removed {test_file}")
    except OSError:
        print(f"   Could not remove {test_file}")

    try:
        os.remove(secure_file)
        print(f"   Removed {secure_file}")
    except OSError:
        print(f"   Could not remove {secure_file}")
    print()

    print("Demo completed!")


if __name__ == "__main__":
    demonstrate_file_permissions()
