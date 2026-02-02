# pathlib vs os.path: When to Use Which

## Introduction

Python offers two primary ways to handle filesystem paths: the modern `pathlib` module (introduced in Python 3.4) and the traditional `os.path` module. Understanding when to use each is crucial for writing clean, maintainable, and cross-platform code.

## Core Differences

### Design Philosophy

**os.path:**
- Procedural approach with functions
- String-based path manipulation
- Requires manual platform handling

**pathlib:**
- Object-oriented approach with classes
- Path objects encapsulate path logic
- Automatic cross-platform compatibility

### Basic Usage Comparison

```python
import os
from pathlib import Path

# Joining paths
# os.path approach
full_path = os.path.join('home', 'user', 'file.txt')

# pathlib approach
full_path = Path('home') / 'user' / 'file.txt'

# Getting file extension
# os.path approach
ext = os.path.splitext('file.txt')[1]

# pathlib approach
ext = Path('file.txt').suffix
```

## When to Use pathlib

### ✅ New Code and Modern Python Projects

**Use pathlib when:**
- Starting a new project
- Working with Python 3.4+
- Cross-platform compatibility is required
- Code readability and maintainability are priorities

**Example:**
```python
# Modern application configuration
from pathlib import Path

class AppConfig:
    def __init__(self):
        self.config_dir = Path.home() / '.myapp'
        self.config_file = self.config_dir / 'config.ini'
        self.data_dir = self.config_dir / 'data'

    def ensure_directories(self):
        """Create necessary directories."""
        self.config_dir.mkdir(exist_ok=True)
        self.data_dir.mkdir(exist_ok=True)

    def get_log_path(self, log_name: str) -> Path:
        """Get path for a log file."""
        return self.config_dir / 'logs' / f"{log_name}.log"
```

### ✅ Complex Path Manipulations

**Use pathlib when:**
- Building complex path hierarchies
- Performing multiple path operations
- Needing to modify path components

**Example:**
```python
def process_dataset(dataset_path: Path):
    """Process a dataset with multiple output files."""
    # Create output directory
    output_dir = dataset_path.parent / f"{dataset_path.stem}_processed"
    output_dir.mkdir(exist_ok=True)

    # Generate related file paths
    summary_file = output_dir / 'summary.txt'
    data_file = output_dir / 'data.csv'
    config_file = output_dir / 'config.json'

    # Process files...
```

### ✅ File System Traversals

**Use pathlib when:**
- Walking directory trees
- Finding files with patterns
- Performing batch file operations

**Example:**
```python
def find_python_files(project_root: Path) -> list[Path]:
    """Find all Python files in a project."""
    return list(project_root.rglob('*.py'))

def organize_by_extension(source_dir: Path, dest_dir: Path):
    """Organize files by extension."""
    for file_path in source_dir.rglob('*'):
        if file_path.is_file():
            ext_dir = dest_dir / file_path.suffix[1:]
            ext_dir.mkdir(exist_ok=True)
            # Move file to extension directory
            file_path.rename(ext_dir / file_path.name)
```

### ✅ Type Safety and IDE Support

**Use pathlib when:**
- Using static type checkers (mypy, pyright)
- Wanting better IDE autocomplete and error detection
- Needing self-documenting code

**Example:**
```python
from pathlib import Path
from typing import List

def backup_files(files: List[Path], backup_dir: Path) -> List[Path]:
    """Create backups of files."""
    backups = []
    for file_path in files:
        backup_path = backup_dir / f"{file_path.name}.bak"
        backup_path.write_bytes(file_path.read_bytes())
        backups.append(backup_path)
    return backups
```

## When to Use os.path

### ✅ Legacy Code Maintenance

**Use os.path when:**
- Maintaining existing codebases
- Working with libraries that expect string paths
- Minimal changes are desired

**Migration Example:**
```python
# Before (os.path)
import os

def get_config_path():
    return os.path.join(os.path.expanduser('~'), '.config', 'app.ini')

# After (pathlib)
from pathlib import Path

def get_config_path():
    return Path.home() / '.config' / 'app.ini'
```

### ✅ Simple Path Operations

**Use os.path when:**
- Only basic path operations are needed
- Working with very performance-critical code
- The operations are simple string manipulations

**Example:**
```python
import os

# Simple existence check
if os.path.exists('file.txt'):
    print("File exists")

# Simple path splitting
path = '/home/user/file.txt'
dirname = os.path.dirname(path)  # '/home/user'
basename = os.path.basename(path)  # 'file.txt'
```

### ✅ Integration with Legacy APIs

**Use os.path when:**
- Interfacing with C extensions
- Working with older libraries that don't support Path objects
- System-level operations

**Example:**
```python
import os
from pathlib import Path

def legacy_function_that_expects_string(path_string: str):
    """Some legacy function that expects a string path."""
    pass

# Convert Path to string for legacy functions
path = Path.home() / 'file.txt'
legacy_function_that_expects_string(str(path))
```

## Performance Considerations

### When pathlib Might Be Slower

**os.path advantages:**
- Minimal object creation overhead
- Faster for simple operations
- Lower memory usage for basic string operations

**Performance-critical scenarios:**
```python
import os
import time
from pathlib import Path

# For millions of simple operations, os.path might be faster
paths = ['file1.txt', 'file2.txt', 'file3.txt'] * 1000000

# os.path approach
start = time.time()
for p in paths:
    dirname = os.path.dirname(p)
os_path_time = time.time() - start

# pathlib approach
start = time.time()
for p in paths:
    dirname = Path(p).parent
pathlib_time = time.time() - start

print(f"os.path: {os_path_time:.3f}s")
print(f"pathlib: {pathlib_time:.3f}s")
```

### When pathlib Performance Doesn't Matter

In most applications, the performance difference is negligible:
- File I/O operations dominate execution time
- Path operations are rarely the bottleneck
- Code maintainability is more important than micro-optimizations

## Migration Strategies

### Gradual Migration

**Step 1: Import pathlib**
```python
import os
from pathlib import Path
```

**Step 2: Convert simple operations**
```python
# Before
config_path = os.path.join(os.path.expanduser('~'), '.config', 'app')

# After
config_path = Path.home() / '.config' / 'app'
```

**Step 3: Handle return values**
```python
# Before
def get_files(directory):
    return os.listdir(directory)

# After
def get_files(directory: str) -> List[Path]:
    return list(Path(directory).iterdir())
```

### Complete Migration

**Convert entire functions:**
```python
# Before
def process_files(src_dir, dst_dir):
    for filename in os.listdir(src_dir):
        src_path = os.path.join(src_dir, filename)
        dst_path = os.path.join(dst_dir, filename)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)

# After
def process_files(src_dir: Path, dst_dir: Path):
    for src_path in src_dir.iterdir():
        if src_path.is_file():
            dst_path = dst_dir / src_path.name
            shutil.copy(src_path, dst_path)
```

## Compatibility and Interoperability

### Using Both Together

**Safe interoperability:**
```python
import os
from pathlib import Path

# Convert between types as needed
def hybrid_function(path_input):
    """Function that accepts both strings and Paths."""
    if isinstance(path_input, str):
        path = Path(path_input)
    else:
        path = path_input

    # Use pathlib operations
    if path.exists():
        return str(path.resolve())  # Return string if needed

    return None
```

### Libraries That Expect Strings

**Handle legacy libraries:**
```python
import configparser
from pathlib import Path

# configparser expects strings
config = configparser.ConfigParser()
config_path = Path.home() / '.config' / 'app.ini'

# Convert to string for libraries that need it
with open(str(config_path), 'r') as f:
    config.read_file(f)
```

## Decision Framework

### Choose pathlib if:
- ✅ Python 3.4+ is your minimum version
- ✅ Cross-platform compatibility is important
- ✅ Code readability matters
- ✅ You're doing complex path operations
- ✅ Type safety is desired
- ✅ You're starting a new project

### Choose os.path if:
- ✅ Maintaining legacy Python 2/3.3 code
- ✅ Working with performance-critical code
- ✅ Only simple path operations are needed
- ✅ Integrating with libraries that don't support Path objects
- ✅ Minimal code changes are required

### Migration Timeline

**Immediate (Python 3.4+ projects):**
- Use pathlib for all new code
- Convert simple os.path operations

**Gradual (existing projects):**
- Introduce pathlib alongside os.path
- Convert functions incrementally
- Update type hints

**Long-term:**
- Complete migration to pathlib
- Remove os.path imports
- Update documentation

## Best Practices

### Consistent Usage

**Within a codebase:**
```python
# Good: Consistent pathlib usage
from pathlib import Path

def create_project_structure(base_dir: Path):
    src_dir = base_dir / 'src'
    tests_dir = base_dir / 'tests'
    docs_dir = base_dir / 'docs'

    for directory in [src_dir, tests_dir, docs_dir]:
        directory.mkdir(parents=True, exist_ok=True)

# Bad: Mixing approaches
def mixed_approach(base_dir):
    src_dir = os.path.join(base_dir, 'src')  # os.path
    tests_dir = Path(base_dir) / 'tests'     # pathlib
    docs_dir = base_dir + '/docs'            # string concat
```

### Documentation and Type Hints

**Clear interfaces:**
```python
from pathlib import Path
from typing import Union, List

def process_files(files: Union[str, Path, List[Union[str, Path]]]) -> List[Path]:
    """
    Process files, accepting various input types.

    Args:
        files: Single file path or list of file paths

    Returns:
        List of processed file paths
    """
    if isinstance(files, (str, Path)):
        files = [files]

    processed = []
    for file_input in files:
        file_path = Path(file_input)
        if file_path.exists():
            processed.append(file_path)

    return processed
```

## Conclusion

**pathlib** is the modern, recommended approach for path handling in Python:
- More readable and maintainable code
- Automatic cross-platform compatibility
- Rich object-oriented API
- Better integration with type checkers

**os.path** remains relevant for:
- Legacy code maintenance
- Simple operations in performance-critical code
- Integration with string-expecting APIs

**Migration strategy:** Use pathlib for all new Python projects and gradually migrate existing codebases. The benefits of pathlib far outweigh the minimal migration effort required.
