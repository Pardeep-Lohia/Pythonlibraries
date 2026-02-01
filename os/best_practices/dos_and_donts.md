# Do's and Don'ts

## Essential Guidelines for Using the `os` Module

### ✅ DO's

#### 1. **Always Use `os.path.join()` for Path Construction**
```python
# ✅ Good
path = os.path.join('home', 'user', 'file.txt')

# ❌ Bad
path = 'home' + '/' + 'user' + '/' + 'file.txt'
```

#### 2. **Check Path Existence Before Operations**
```python
# ✅ Good
if os.path.exists(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

# ❌ Bad - May raise FileNotFoundError
with open(filepath, 'r') as f:
    content = f.read()
```

#### 3. **Use Environment Variables Safely**
```python
# ✅ Good
database_url = os.environ.get('DATABASE_URL', 'sqlite:///default.db')

# ❌ Bad - KeyError if variable doesn't exist
database_url = os.environ['DATABASE_URL']
```

#### 4. **Handle Permissions Appropriately**
```python
# ✅ Good
if os.access(filepath, os.R_OK):
    with open(filepath, 'r') as f:
        content = f.read()

# ❌ Bad - May raise PermissionError
with open(filepath, 'r') as f:
    content = f.read()
```

#### 5. **Use Context Managers for Directory Operations**
```python
# ✅ Good
with os.scandir(directory) as entries:
    for entry in entries:
        if entry.is_file():
            process_file(entry.path)

# ❌ Bad - May leak file descriptors
entries = os.scandir(directory)
for entry in entries:
    if entry.is_file():
        process_file(entry.path)
# Forgot to close entries
```

#### 6. **Validate User Input for Paths**
```python
# ✅ Good
def safe_join(base_dir, user_path):
    full_path = os.path.normpath(os.path.join(base_dir, user_path))
    if not full_path.startswith(os.path.abspath(base_dir)):
        raise ValueError("Path traversal attempt")
    return full_path

# ❌ Bad - Vulnerable to directory traversal
filepath = os.path.join(base_dir, user_input)
```

#### 7. **Prefer `subprocess` Over `os.system` for Complex Commands**
```python
# ✅ Good
import subprocess
result = subprocess.run(['ls', '-la'], capture_output=True, text=True)

# ❌ Bad - Security and functionality issues
os.system('ls -la')
```

#### 8. **Use Absolute Paths for Critical Operations**
```python
# ✅ Good
config_path = os.path.abspath('config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

# ❌ Bad - Relative path may not resolve as expected
with open('config.json', 'r') as f:
    config = json.load(f)
```

#### 9. **Handle OS Differences Explicitly**
```python
# ✅ Good
if os.name == 'nt':
    # Windows-specific code
    executable = 'script.exe'
else:
    # Unix-like systems
    executable = './script'

# ❌ Bad - Assumes Unix behavior
executable = './script'  # Won't work on Windows
```

#### 10. **Clean Up Temporary Files and Directories**
```python
# ✅ Good
import tempfile

with tempfile.TemporaryDirectory() as temp_dir:
    temp_file = os.path.join(temp_dir, 'temp.txt')
    with open(temp_file, 'w') as f:
        f.write('temporary data')
    # Automatically cleaned up

# ❌ Bad - May leave temporary files
temp_file = '/tmp/temp_' + str(os.getpid()) + '.txt'
with open(temp_file, 'w') as f:
    f.write('temporary data')
# Forgot to clean up
```

### ❌ DON'Ts

#### 1. **Don't Hardcode Path Separators**
```python
# ❌ Bad
path = 'home/user/file.txt'  # Unix only
path = 'home\\user\\file.txt'  # Windows only

# ✅ Good
path = os.path.join('home', 'user', 'file.txt')
```

#### 2. **Don't Assume Current Working Directory**
```python
# ❌ Bad
with open('config.json', 'r') as f:  # May not be where you think
    config = json.load(f)

# ✅ Good
config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)
```

#### 3. **Don't Use `os.system()` for User Input**
```python
# ❌ Bad - Command injection vulnerability
filename = input("Enter filename: ")
os.system(f"rm {filename}")  # Dangerous!

# ✅ Good
import subprocess
filename = input("Enter filename: ")
subprocess.run(['rm', filename], check=True)
```

#### 4. **Don't Modify `os.environ` Directly for Temporary Changes**
```python
# ❌ Bad - Affects entire process
old_value = os.environ.get('DEBUG')
os.environ['DEBUG'] = 'true'
# ... do something ...
if old_value:
    os.environ['DEBUG'] = old_value
else:
    del os.environ['DEBUG']

# ✅ Good - Use context manager
import contextlib

@contextlib.contextmanager
def temp_env_var(key, value):
    old_value = os.environ.get(key)
    os.environ[key] = value
    try:
        yield
    finally:
        if old_value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = old_value

with temp_env_var('DEBUG', 'true'):
    # Environment variable is set here
    pass
# Automatically restored
```

#### 5. **Don't Use `os.listdir()` for Large Directories**
```python
# ❌ Bad - Loads all entries into memory
entries = os.listdir('/large/directory')
for entry in entries:
    process_entry(entry)

# ✅ Good - Iterator-based approach
with os.scandir('/large/directory') as entries:
    for entry in entries:
        process_entry(entry)
```

#### 6. **Don't Ignore File Encoding**
```python
# ❌ Bad - May fail with Unicode filenames
files = os.listdir(directory)

# ✅ Good - Handle encoding properly
files = os.listdir(directory)
for filename in files:
    # filename is already properly decoded in Python 3
    filepath = os.path.join(directory, filename)
```

#### 7. **Don't Use `os.popen()` - Use `subprocess`**
```python
# ❌ Bad - Deprecated
pipe = os.popen('ls -la', 'r')
output = pipe.read()
pipe.close()

# ✅ Good
import subprocess
result = subprocess.run(['ls', '-la'], capture_output=True, text=True)
output = result.stdout
```

#### 8. **Don't Assume File Permissions Work the Same Everywhere**
```python
# ❌ Bad - Windows doesn't have the same permission model
os.chmod('file.txt', 0o755)  # May not work as expected on Windows

# ✅ Good - Check platform and handle appropriately
if os.name == 'posix':
    os.chmod('file.txt', 0o755)
else:
    # Windows-specific permission handling
    pass
```

#### 9. **Don't Use Relative Paths in Libraries**
```python
# ❌ Bad - Library code shouldn't assume CWD
config_file = 'config/settings.json'  # Relative to what?

# ✅ Good - Use __file__ to get module directory
module_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(module_dir, 'config', 'settings.json')
```

#### 10. **Don't Forget to Handle Symlinks**
```python
# ❌ Bad - May not handle symlinks correctly
if os.path.isfile(filepath):
    # This might be a symlink to a directory

# ✅ Good - Be explicit about what you want
if os.path.islink(filepath):
    # Handle symlink
    pass
elif os.path.isfile(filepath):
    # Handle regular file
    pass
elif os.path.isdir(filepath):
    # Handle directory
    pass
```

## Performance Best Practices

### 1. **Cache `os.stat()` Results**
```python
# ✅ Good - Cache stat results
file_stats = {}
for filename in os.listdir(directory):
    filepath = os.path.join(directory, filename)
    file_stats[filepath] = os.stat(filepath)

# Now use cached results
for filepath, stat_info in file_stats.items():
    if stat_info.st_size > 1024 * 1024:  # 1MB
        print(f"Large file: {filepath}")
```

### 2. **Use `os.scandir()` Instead of `os.listdir()` + `os.stat()`**
```python
# ✅ Good - More efficient
with os.scandir(directory) as entries:
    for entry in entries:
        if entry.is_file() and entry.stat().st_size > 0:
            process_file(entry.path)

# ❌ Bad - Less efficient
for filename in os.listdir(directory):
    filepath = os.path.join(directory, filename)
    if os.path.isfile(filepath) and os.path.getsize(filepath) > 0:
        process_file(filepath)
```

### 3. **Batch File Operations**
```python
# ✅ Good - Batch operations for better performance
files_to_process = []
with os.scandir(directory) as entries:
    for entry in entries:
        if entry.is_file():
            files_to_process.append(entry.path)

# Process in batches
batch_size = 100
for i in range(0, len(files_to_process), batch_size):
    batch = files_to_process[i:i + batch_size]
    process_batch(batch)
```

## Security Best Practices

### 1. **Validate All User-Supplied Paths**
```python
def secure_path_join(base_dir, user_path):
    """Safely join paths without directory traversal."""
    # Normalize the path
    full_path = os.path.normpath(os.path.join(base_dir, user_path))

    # Ensure it stays within base directory
    base_abs = os.path.abspath(base_dir)
    full_abs = os.path.abspath(full_path)

    if not full_abs.startswith(base_abs):
        raise ValueError("Path traversal detected")

    return full_path
```

### 2. **Use Temporary Files Securely**
```python
import tempfile

# ✅ Good - Secure temporary file creation
with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.tmp') as f:
    temp_path = f.name
    f.write('temporary data')

try:
    # Use temp file
    process_file(temp_path)
finally:
    # Ensure cleanup
    os.unlink(temp_path)
```

### 3. **Check Permissions Before Sensitive Operations**
```python
def safe_file_operation(filepath, operation):
    """Perform file operation only if permissions allow."""
    if operation == 'read' and not os.access(filepath, os.R_OK):
        raise PermissionError(f"Cannot read {filepath}")
    elif operation == 'write' and not os.access(filepath, os.W_OK):
        raise PermissionError(f"Cannot write {filepath}")

    # Perform operation
    if operation == 'read':
        with open(filepath, 'r') as f:
            return f.read()
    # ... other operations
```

## Cross-Platform Best Practices

### 1. **Handle Path Separators Correctly**
```python
# ✅ Good - Platform-independent
config_dir = os.path.join('app', 'config')
log_file = os.path.join(config_dir, 'app.log')

# ❌ Bad - Platform-specific
config_dir = 'app/config'  # Unix only
log_file = 'app/config/app.log'
```

### 2. **Use Environment Variables Appropriately**
```python
# ✅ Good - Cross-platform environment handling
home_dir = os.environ.get('HOME') or os.environ.get('USERPROFILE')
temp_dir = os.environ.get('TMP') or os.environ.get('TEMP') or '/tmp'

# ❌ Bad - Platform assumptions
home_dir = os.environ['HOME']  # Doesn't exist on Windows
temp_dir = '/tmp'  # May not be appropriate on Windows
```

### 3. **Test on Target Platforms**
```python
# ✅ Good - Platform-aware code
def get_app_data_dir():
    """Get application data directory for current platform."""
    if os.name == 'nt':  # Windows
        base_dir = os.environ.get('APPDATA', '~/AppData/Roaming')
    else:  # Unix-like
        base_dir = os.environ.get('XDG_DATA_HOME', '~/.local/share')

    app_dir = os.path.join(base_dir, 'myapp')
    os.makedirs(app_dir, exist_ok=True)
    return app_dir
```

Following these do's and don'ts will help you write robust, secure, and maintainable code when working with the `os` module.
