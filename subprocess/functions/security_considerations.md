# Security Considerations with Subprocess

## Overview

Security is paramount when using `subprocess` due to the potential for command injection attacks and system compromise. This document covers security best practices, vulnerability prevention, and safe coding patterns.

## Shell Injection Vulnerabilities

### The Danger of shell=True

**Vulnerable Code:**
```python
# DANGEROUS - Shell injection vulnerability
import subprocess

filename = input("Enter filename: ")
subprocess.run(f'cat {filename}', shell=True)  # Attacker can execute: "; rm -rf /"
```

**Why it's dangerous:**
- Shell interprets special characters (`;`, `|`, `&`, etc.)
- User input becomes shell commands
- Can execute arbitrary system commands

**Safe Code:**
```python
# SAFE - No shell interpretation
filename = input("Enter filename: ")
subprocess.run(['cat', filename])  # Arguments passed directly to exec
```

### Command Injection Examples

```python
# Vulnerable patterns
user_input = "; rm -rf /"  # Malicious input

# These are all vulnerable:
subprocess.run(f'ls {user_input}', shell=True)
subprocess.run('ls ' + user_input, shell=True)
subprocess.run(f'grep "{user_input}" file.txt', shell=True)
```

### When shell=True is Acceptable

Shell is only safe when:
- No user input is involved
- Command is hardcoded
- Input is strictly validated

```python
# Acceptable uses of shell=True
subprocess.run('ls | head -5', shell=True)  # Hardcoded pipeline
subprocess.run('echo "Hello World"', shell=True)  # No variables
```

## Input Validation and Sanitization

### Input Validation Strategies

```python
import os
import re

def validate_filename(filename):
    """Validate filename input"""
    # Check for dangerous characters
    if any(char in filename for char in [';', '|', '&', '`', '$', '(', ')']):
        raise ValueError("Invalid characters in filename")

    # Check for path traversal
    if '..' in filename or filename.startswith('/'):
        raise ValueError("Invalid path")

    # Check length
    if len(filename) > 255:
        raise ValueError("Filename too long")

    return filename

def safe_cat_file(filename):
    """Safely display file contents"""
    safe_filename = validate_filename(filename)

    # Additional check: file exists and is readable
    if not os.path.isfile(safe_filename):
        raise FileNotFoundError("File not found")

    if not os.access(safe_filename, os.R_OK):
        raise PermissionError("File not readable")

    return subprocess.run(['cat', safe_filename], capture_output=True, text=True)
```

### Input Sanitization

```python
import shlex

def sanitize_shell_input(user_input):
    """Sanitize input for shell usage (not recommended)"""
    # Remove dangerous characters
    sanitized = re.sub(r'[;&|`$()<>]', '', user_input)

    # Quote the input
    quoted = shlex.quote(sanitized)

    return quoted

# Even with sanitization, prefer argument lists
def safe_grep(pattern, filename):
    """Safe grep implementation"""
    # Validate inputs
    if not pattern or not filename:
        raise ValueError("Pattern and filename required")

    # Use argument list - completely safe
    return subprocess.run(['grep', pattern, filename],
                         capture_output=True, text=True)
```

## Environment Variable Security

### Environment Variable Injection

```python
# Dangerous: User can control environment
user_env = {'PATH': '/malicious/path'}
subprocess.run(['ls'], env=user_env)  # PATH injection
```

### Safe Environment Handling

```python
def run_with_safe_environment(command, extra_env=None):
    """Run command with sanitized environment"""
    # Start with clean environment
    safe_env = {}

    # Copy only safe variables
    safe_vars = {'PATH', 'HOME', 'USER', 'SHELL', 'LANG', 'LC_ALL'}

    for var in safe_vars:
        value = os.environ.get(var)
        if value:
            safe_env[var] = value

    # Set secure PATH
    safe_env['PATH'] = '/usr/local/bin:/usr/bin:/bin'

    # Add extra environment variables (validated)
    if extra_env:
        for key, value in extra_env.items():
            if isinstance(key, str) and isinstance(value, str):
                safe_env[key] = value

    return subprocess.run(command, env=safe_env)
```

### PATH Security

```python
def secure_path_command(command_name, *args):
    """Run command with secure PATH resolution"""
    # Use absolute paths when possible
    secure_commands = {
        'ls': '/bin/ls',
        'cat': '/bin/cat',
        'grep': '/bin/grep',
    }

    if command_name in secure_commands:
        full_command = [secure_commands[command_name]] + list(args)
        return subprocess.run(full_command, capture_output=True, text=True)
    else:
        raise ValueError(f"Command not allowed: {command_name}")
```

## Privilege Management

### Running with Different Privileges

```python
def run_as_limited_user(command, username=None):
    """Run command as different user (Unix only)"""
    import pwd
    import grp

    if username:
        try:
            user_info = pwd.getpwnam(username)
            group_info = grp.getgrgid(user_info.pw_gid)

            def preexec():
                os.setgid(user_info.pw_gid)
                os.setuid(user_info.pw_uid)

            return subprocess.Popen(command, preexec_fn=preexec)

        except KeyError:
            raise ValueError(f"User {username} not found")
        except PermissionError:
            raise PermissionError("Insufficient privileges to change user")

    # Run with current privileges but drop capabilities
    return subprocess.run(command)
```

### Dropping Privileges

```python
def drop_privileges():
    """Drop root privileges to regular user"""
    if os.getuid() == 0:  # Running as root
        # Set UID and GID to nobody or specific user
        nobody_uid = pwd.getpwnam('nobody').pw_uid
        nobody_gid = grp.getgrnam('nogroup').gr_gid

        os.setgid(nobody_gid)
        os.setuid(nobody_uid)

def run_dropped_privileges(command):
    """Run command with dropped privileges"""
    def preexec():
        drop_privileges()

    return subprocess.Popen(command, preexec_fn=preexec)
```

## Resource Limitations

### Preventing Resource Exhaustion

```python
import resource

def run_with_resource_limits(command, cpu_limit=60, mem_limit=50*1024*1024):
    """Run command with resource constraints"""

    def preexec():
        # CPU time limit (seconds)
        resource.setrlimit(resource.RLIMIT_CPU, (cpu_limit, cpu_limit))

        # Memory limit (bytes)
        resource.setrlimit(resource.RLIMIT_AS, (mem_limit, mem_limit))

        # File size limit
        resource.setrlimit(resource.RLIMIT_FSIZE, (100*1024*1024, 100*1024*1024))

        # Number of processes
        resource.setrlimit(resource.RLIMIT_NPROC, (10, 10))

    return subprocess.Popen(command, preexec_fn=preexec)
```

### Timeout Protection

```python
def run_with_timeout_protection(command, timeout=30):
    """Run command with timeout to prevent hanging"""
    try:
        return subprocess.run(command, timeout=timeout,
                             capture_output=True, text=True)
    except subprocess.TimeoutExpired:
        print(f"Command timed out after {timeout} seconds")
        return None
```

## File System Security

### Path Traversal Prevention

```python
def secure_file_access(filename, base_directory='/tmp'):
    """Securely access files within a base directory"""
    # Resolve to absolute path
    abs_path = os.path.abspath(filename)

    # Check if path is within base directory
    base_abs = os.path.abspath(base_directory)
    if not abs_path.startswith(base_abs):
        raise ValueError("Access denied: path outside base directory")

    # Additional checks
    if not os.path.exists(abs_path):
        raise FileNotFoundError("File not found")

    if not os.path.isfile(abs_path):
        raise ValueError("Not a regular file")

    return abs_path

def safe_read_file(filename):
    """Safely read a file"""
    secure_path = secure_file_access(filename)

    return subprocess.run(['cat', secure_path],
                         capture_output=True, text=True)
```

### Permission Validation

```python
def validate_file_permissions(filepath, required_permissions=os.R_OK):
    """Validate file permissions before access"""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    if not os.access(filepath, required_permissions):
        raise PermissionError(f"Insufficient permissions: {filepath}")

    # Check if file is a symlink (potential security risk)
    if os.path.islink(filepath):
        raise ValueError("Symlinks not allowed")

    return filepath
```

## Network Security

### Safe Network Commands

```python
def safe_curl(url, output_file=None):
    """Safely download file with curl"""
    # Validate URL
    from urllib.parse import urlparse
    parsed = urlparse(url)

    if parsed.scheme not in ['http', 'https']:
        raise ValueError("Only HTTP/HTTPS URLs allowed")

    if not parsed.netloc:
        raise ValueError("Invalid URL")

    command = ['curl', '--silent', '--show-error', '--fail']

    if output_file:
        # Validate output file path
        output_file = secure_file_access(output_file)
        command.extend(['-o', output_file])

    command.append(url)

    return subprocess.run(command, capture_output=True, text=True)
```

### SSH Security

```python
def safe_ssh_command(host, command, key_file=None, user=None):
    """Execute command over SSH securely"""
    # Validate inputs
    if not host or not command:
        raise ValueError("Host and command required")

    # Build SSH command
    ssh_cmd = ['ssh']

    if user:
        # Validate username
        if not re.match(r'^[a-zA-Z0-9_-]+$', user):
            raise ValueError("Invalid username")
        ssh_cmd.extend(['-l', user])

    if key_file:
        # Validate key file
        if not os.path.isfile(key_file):
            raise FileNotFoundError("SSH key file not found")
        ssh_cmd.extend(['-i', key_file])

    # Strict host key checking
    ssh_cmd.extend(['-o', 'StrictHostKeyChecking=yes'])
    ssh_cmd.extend(['-o', 'UserKnownHostsFile=/dev/null'])  # For security

    ssh_cmd.append(host)
    ssh_cmd.append(command)

    return subprocess.run(ssh_cmd, capture_output=True, text=True)
```

## Secure Coding Patterns

### Command Builder Pattern

```python
class SecureCommandBuilder:
    """Secure command builder with validation"""

    def __init__(self, base_command):
        self.allowed_commands = {
            'ls', 'cat', 'grep', 'head', 'tail', 'wc', 'sort', 'uniq'
        }

        if base_command not in self.allowed_commands:
            raise ValueError(f"Command not allowed: {base_command}")

        self.command = [base_command]

    def add_safe_argument(self, arg):
        """Add argument with validation"""
        if not isinstance(arg, str):
            raise TypeError("Argument must be string")

        # Prevent dangerous characters
        if any(char in arg for char in [';', '|', '&', '`', '$']):
            raise ValueError("Dangerous characters in argument")

        self.command.append(arg)
        return self

    def add_flag(self, flag):
        """Add flag with validation"""
        if not flag.startswith('-'):
            raise ValueError("Invalid flag format")

        self.command.append(flag)
        return self

    def run(self, **kwargs):
        """Execute the built command"""
        defaults = {
            'capture_output': True,
            'text': True,
            'timeout': 30
        }
        defaults.update(kwargs)
        return subprocess.run(self.command, **defaults)

# Usage
cmd = SecureCommandBuilder('grep')
result = cmd.add_flag('-i').add_safe_argument('pattern').run()
```

### Input Sanitization Decorator

```python
def sanitize_subprocess_inputs(func):
    """Decorator to sanitize subprocess inputs"""
    def wrapper(*args, **kwargs):
        # Sanitize positional arguments
        sanitized_args = []
        for arg in args:
            if isinstance(arg, str):
                # Remove dangerous characters
                sanitized = re.sub(r'[;&|`$()<>]', '', arg)
                sanitized_args.append(sanitized)
            else:
                sanitized_args.append(arg)

        # Sanitize keyword arguments
        sanitized_kwargs = {}
        for key, value in kwargs.items():
            if isinstance(value, str):
                sanitized = re.sub(r'[;&|`$()<>]', '', value)
                sanitized_kwargs[key] = sanitized
            else:
                sanitized_kwargs[key] = value

        return func(*sanitized_args, **sanitized_kwargs)
    return wrapper

@sanitize_subprocess_inputs
def safe_run_command(command, *args):
    """Run command with sanitized inputs"""
    full_command = [command] + list(args)
    return subprocess.run(full_command, capture_output=True, text=True)
```

## Cross-Platform Security

### Platform-Specific Security

```python
def secure_command_execution(command, **kwargs):
    """Execute command with platform-specific security"""
    system = platform.system()

    if system == 'Windows':
        # Windows-specific security
        # Use full paths to prevent DLL hijacking
        secure_env = os.environ.copy()
        secure_env['PATH'] = r'C:\Windows\System32'

        return subprocess.run(command, env=secure_env, **kwargs)

    elif system == 'Linux':
        # Linux-specific security
        def preexec():
            # Drop capabilities
            try:
                import prctl
                prctl.capbset(prctl.CAP_SYS_ADMIN, prctl.CAPBSET_DROP)
            except ImportError:
                pass  # prctl not available

        return subprocess.Popen(command, preexec_fn=preexec, **kwargs)

    else:
        # Default security
        return subprocess.run(command, **kwargs)
```

### Path Security Across Platforms

```python
def secure_path_join(*parts):
    """Securely join path components"""
    # Normalize path
    path = os.path.join(*parts)
    path = os.path.abspath(path)

    # Platform-specific validation
    if platform.system() == 'Windows':
        # Prevent UNC path attacks
        if path.startswith('\\\\'):
            raise ValueError("UNC paths not allowed")
    else:
        # Prevent absolute path traversal
        if path.startswith('/'):
            # Allow only specific directories
            allowed_prefixes = ['/tmp', '/var/tmp', '/home']
            if not any(path.startswith(prefix) for prefix in allowed_prefixes):
                raise ValueError("Path not in allowed directories")

    return path
```

## Logging and Auditing

### Security Event Logging

```python
import logging

class SecurityLogger:
    """Logger for security-related subprocess events"""

    def __init__(self):
        self.logger = logging.getLogger('subprocess_security')
        self.logger.setLevel(logging.WARNING)

        handler = logging.FileHandler('/var/log/subprocess_security.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_command_execution(self, command, user=None, success=True):
        """Log command execution for audit trail"""
        cmd_str = ' '.join(command) if isinstance(command, list) else command
        status = "SUCCESS" if success else "FAILED"

        message = f"User: {user or 'unknown'} | Command: {cmd_str} | Status: {status}"
        self.logger.warning(message)

    def log_security_violation(self, violation_type, details):
        """Log security violations"""
        message = f"SECURITY VIOLATION: {violation_type} - {details}"
        self.logger.error(message)

# Usage
security_logger = SecurityLogger()

def audited_run(command, user=None):
    """Run command with security auditing"""
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        success = result.returncode == 0
        security_logger.log_command_execution(command, user, success)
        return result
    except Exception as e:
        security_logger.log_security_violation("COMMAND_EXECUTION_ERROR", str(e))
        raise
```

## Testing Security

### Security Test Cases

```python
def test_subprocess_security():
    """Test subprocess security measures"""

    # Test cases for injection attempts
    injection_tests = [
        ("; rm -rf /", "semicolon injection"),
        ("| cat /etc/passwd", "pipe injection"),
        ("`whoami`", "command substitution"),
        ("$(rm -rf /)", "command substitution 2"),
        ("&& evil_command", "logical and injection"),
        ("|| evil_command", "logical or injection"),
    ]

    for injection, description in injection_tests:
        print(f"Testing {description}: {injection}")

        # This should fail safely
        try:
            # Dangerous - don't actually run this!
            # subprocess.run(f'echo {injection}', shell=True)
            print("  Would be vulnerable with shell=True")
        except:
            pass

        # Safe version
        try:
            result = subprocess.run(['echo', injection])
            print(f"  Safe version output: {result.stdout.decode().strip()}")
        except Exception as e:
            print(f"  Safe version error: {e}")

if __name__ == '__main__':
    test_subprocess_security()
```

This comprehensive guide covers all critical security aspects of using `subprocess`, with practical examples of secure coding patterns and vulnerability prevention techniques.
