# Environment Variables

## Overview
Environment variables are key-value pairs that are part of the operating system environment. The `os` module provides functions to access, modify, and manage these variables, which are essential for configuration, system integration, and cross-platform compatibility.

## Core Environment Functions

### `os.environ` - Environment Dictionary
**Purpose**: A dictionary-like object containing all environment variables.

**Access Methods**:
```python
import os

# Get all environment variables
all_vars = dict(os.environ)

# Get specific variable
path_var = os.environ['PATH']

# Get with default
home = os.environ.get('HOME', '/tmp')

# Check if exists
if 'USER' in os.environ:
    username = os.environ['USER']
```

**Characteristics**:
- Dictionary-like interface
- Modifications affect the current process and child processes
- Changes are not persistent across system reboots

### `os.getenv(key, default=None)` - Get Environment Variable
**Purpose**: Gets the value of an environment variable.

**Syntax**:
```python
os.getenv(key, default=None)
```

**Parameters**:
- `key`: Variable name
- `default`: Value to return if variable doesn't exist

**Examples**:
```python
import os

# Get with default
database_url = os.getenv('DATABASE_URL', 'sqlite:///default.db')

# Get without default (returns None if not found)
api_key = os.getenv('API_KEY')

# Safe access
port = int(os.getenv('PORT', '8000'))
```

### `os.putenv(key, value)` - Set Environment Variable
**Purpose**: Sets the value of an environment variable.

**Syntax**:
```python
os.putenv(key, value)
```

**Note**: `os.environ[key] = value` is preferred over `os.putenv()`.

### `os.unsetenv(key)` - Remove Environment Variable
**Purpose**: Removes an environment variable.

**Syntax**:
```python
os.unsetenv(key)
```

**Note**: `del os.environ[key]` is preferred.

## Environment Variable Management

### Setting Variables
```python
import os

# Method 1: Direct assignment (recommended)
os.environ['MY_APP_CONFIG'] = '/etc/myapp/config.json'
os.environ['DEBUG'] = 'true'

# Method 2: Using putenv
os.putenv('TEMP_DIR', '/tmp/myapp')

# Method 3: Using environ.setdefault
os.environ.setdefault('LOG_LEVEL', 'INFO')  # Only sets if not exists
```

### Removing Variables
```python
import os

# Method 1: Direct deletion (recommended)
if 'TEMP_VAR' in os.environ:
    del os.environ['TEMP_VAR']

# Method 2: Using unsetenv
os.unsetenv('TEMP_VAR')
```

### Environment Context Management
```python
import os
from contextlib import contextmanager

@contextmanager
def env_context(**kwargs):
    """Temporarily set environment variables."""
    original = {}
    for key, value in kwargs.items():
        original[key] = os.environ.get(key)
        os.environ[key] = str(value)

    try:
        yield
    finally:
        for key, value in original.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

# Usage
with env_context(DEBUG='true', LOG_LEVEL='DEBUG'):
    # Code that runs with modified environment
    run_application()
# Environment automatically restored
```

## Common Environment Variables

### System Variables
- `PATH`: Executable search paths
- `HOME`/`USERPROFILE`: User's home directory
- `TMP`/`TEMP`: Temporary file directories
- `USER`/`USERNAME`: Current user name
- `PWD`: Current working directory

### Application Variables
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Application secret key
- `DEBUG`: Debug mode flag
- `PORT`: Server port number
- `LOG_LEVEL`: Logging verbosity

## Cross-Platform Considerations

### Platform-Specific Variables
```python
import os

# Home directory (cross-platform)
home_dir = os.environ.get('HOME') or os.environ.get('USERPROFILE')

# Temporary directory
temp_dir = os.environ.get('TMP') or os.environ.get('TEMP') or '/tmp'

# Path separator
path_sep = os.environ.get('PATH', '').split(os.pathsep)
```

### Windows-Specific Variables
- `APPDATA`: Application data directory
- `PROGRAMFILES`: Program files directory
- `SYSTEMROOT`: Windows system directory

### Unix-Specific Variables
- `SHELL`: Default shell
- `LANG`: System language
- `DISPLAY`: X11 display (GUI applications)

## Security Considerations

### Safe Environment Access
```python
import os

def get_secure_env_var(name, default=None, validator=None):
    """Safely get and validate environment variable."""
    value = os.environ.get(name)
    if value is None:
        return default

    if validator and not validator(value):
        raise ValueError(f"Invalid value for {name}")

    return value

# Usage
port = get_secure_env_var('PORT', 8000,
                         lambda x: x.isdigit() and 1000 <= int(x) <= 9999)
```

### Avoiding Environment Injection
```python
import os
import subprocess

# Dangerous: Command injection via environment
user_cmd = os.environ.get('USER_CMD', '')
os.system(user_cmd)  # Vulnerable!

# Safe: Validate and sanitize
allowed_commands = ['ls', 'pwd', 'date']
user_cmd = os.environ.get('USER_CMD', '')
if user_cmd in allowed_commands:
    subprocess.run([user_cmd], check=True)
```

## Environment Variable Patterns

### Configuration Loading
```python
import os
from typing import Dict, Any

def load_config_from_env(prefix: str = '') -> Dict[str, Any]:
    """Load configuration from environment variables with prefix."""
    config = {}
    prefix_len = len(prefix)

    for key, value in os.environ.items():
        if key.startswith(prefix):
            config_key = key[prefix_len:].lower()
            # Try to convert to appropriate type
            if value.lower() in ('true', 'false'):
                config[config_key] = value.lower() == 'true'
            elif value.isdigit():
                config[config_key] = int(value)
            elif value.replace('.', '').isdigit():
                config[config_key] = float(value)
            else:
                config[config_key] = value

    return config

# Usage
app_config = load_config_from_env('MYAPP_')
# MYAPP_DEBUG=true -> app_config['debug'] = True
# MYAPP_PORT=8000 -> app_config['port'] = 8000
```

### Environment-Based Feature Flags
```python
import os

class FeatureFlags:
    """Feature flags from environment variables."""

    @property
    def enable_new_ui(self):
        return os.environ.get('ENABLE_NEW_UI', 'false').lower() == 'true'

    @property
    def debug_mode(self):
        return os.environ.get('DEBUG', 'false').lower() == 'true'

    @property
    def max_workers(self):
        return int(os.environ.get('MAX_WORKERS', '4'))

# Usage
features = FeatureFlags()
if features.enable_new_ui:
    # Use new UI
    pass
```

## Best Practices

### 1. Use Defaults Liberally
```python
# Good
database_url = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
port = int(os.environ.get('PORT', '8000'))

# Avoid
database_url = os.environ['DATABASE_URL']  # KeyError if missing
```

### 2. Validate Environment Values
```python
import os

def get_port():
    port_str = os.environ.get('PORT', '8000')
    try:
        port = int(port_str)
        if not (1024 <= port <= 65535):
            raise ValueError
        return port
    except (ValueError, TypeError):
        return 8000
```

### 3. Document Required Variables
```python
import os

REQUIRED_ENV_VARS = ['DATABASE_URL', 'SECRET_KEY']

def validate_environment():
    """Validate that all required environment variables are set."""
    missing = []
    for var in REQUIRED_ENV_VARS:
        if var not in os.environ:
            missing.append(var)

    if missing:
        raise EnvironmentError(f"Missing required environment variables: {missing}")

    return True
```

### 4. Use Environment Files for Development
```python
# .env file support
def load_dotenv(filepath='.env'):
    """Load environment variables from .env file."""
    if not os.path.exists(filepath):
        return

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

# Usage
load_dotenv()
```

### 5. Avoid Hardcoding Sensitive Data
```python
# Bad
api_key = 'sk-1234567890abcdef'  # Hardcoded secret

# Good
api_key = os.environ['API_KEY']  # From environment
```

## Common Patterns

### Environment-Aware Logging
```python
import os
import logging

def setup_logging():
    """Set up logging based on environment."""
    log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
    numeric_level = getattr(logging, log_level, logging.INFO)

    logging.basicConfig(
        level=numeric_level,
        format=os.environ.get('LOG_FORMAT', '%(levelname)s: %(message)s')
    )

    # Log to file if specified
    log_file = os.environ.get('LOG_FILE')
    if log_file:
        handler = logging.FileHandler(log_file)
        logging.getLogger().addHandler(handler)
```

### Database Configuration
```python
import os

def get_database_config():
    """Get database configuration from environment."""
    return {
        'url': os.environ.get('DATABASE_URL', 'sqlite:///app.db'),
        'pool_size': int(os.environ.get('DB_POOL_SIZE', '10')),
        'max_overflow': int(os.environ.get('DB_MAX_OVERFLOW', '20')),
        'pool_timeout': int(os.environ.get('DB_POOL_TIMEOUT', '30')),
        'echo': os.environ.get('DB_ECHO', 'false').lower() == 'true'
    }
```

### Application Settings
```python
import os
from dataclasses import dataclass

@dataclass
class AppSettings:
    """Application settings from environment variables."""
    debug: bool = False
    port: int = 8000
    host: str = 'localhost'
    secret_key: str = 'dev-secret-key'
    database_url: str = 'sqlite:///app.db'

    @classmethod
    def from_env(cls):
        """Create settings from environment variables."""
        return cls(
            debug=os.environ.get('DEBUG', 'false').lower() == 'true',
            port=int(os.environ.get('PORT', '8000')),
            host=os.environ.get('HOST', 'localhost'),
            secret_key=os.environ.get('SECRET_KEY', 'dev-secret-key'),
            database_url=os.environ.get('DATABASE_URL', 'sqlite:///app.db')
        )

# Usage
settings = AppSettings.from_env()
```

Environment variables provide a flexible way to configure applications without code changes, making them essential for modern software development.
