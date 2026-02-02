# Python Standard Libraries Comparison

## 1. `os`

**Purpose:** Interact with the operating system.

### Common Uses:

-   File and directory operations (`os.listdir`, `os.remove`,
    `os.mkdir`)
-   Environment variables (`os.environ`)
-   Path utilities (`os.path.join`, `os.path.exists`)
-   Process management (`os.getpid`, `os.system`)

### When to Use:

Use `os` when you need low-level OS interaction or environment handling.

------------------------------------------------------------------------

## 2. `platform`

**Purpose:** Get information about the system/platform.

### Common Uses:

-   OS name (`platform.system()`)
-   OS version (`platform.version()`)
-   Processor info (`platform.processor()`)
-   Architecture (`platform.architecture()`)

### When to Use:

Use `platform` when your program needs to behave differently depending
on the operating system.

------------------------------------------------------------------------

## 3. `shutil`

**Purpose:** High-level file operations (built on top of `os`).

### Common Uses:

-   Copy files (`shutil.copy`)
-   Move files (`shutil.move`)
-   Remove directories (`shutil.rmtree`)
-   Create archives (`shutil.make_archive`)

### When to Use:

Use `shutil` for file copying, moving, and directory management tasks.

------------------------------------------------------------------------

## 4. `subprocess`

**Purpose:** Run external programs and system commands.

### Common Uses:

-   Run shell commands (`subprocess.run`)
-   Capture output
-   Automate CLI tools

### When to Use:

Use `subprocess` when you need to execute external commands or programs
from Python.

------------------------------------------------------------------------

## 5. `sys`

**Purpose:** Access Python interpreter variables and runtime
information.

### Common Uses:

-   Command-line arguments (`sys.argv`)
-   Exit program (`sys.exit()`)
-   Python version (`sys.version`)
-   Modify module search path (`sys.path`)

### When to Use:

Use `sys` for interacting with the Python runtime environment.

------------------------------------------------------------------------

## 6. `pathlib`

**Purpose:** Modern, object-oriented file path handling.

### Common Uses:

-   Create paths (`Path("file.txt")`)
-   Check existence (`path.exists()`)
-   Read/write files (`path.read_text()`)
-   Join paths (`path / "subfolder"`)

### When to Use:

Use `pathlib` instead of `os.path` for cleaner and more readable path
handling.

------------------------------------------------------------------------

## 7. `tempfile`

**Purpose:** Create temporary files and directories securely.

### Common Uses:

-   Temporary files (`tempfile.TemporaryFile`)
-   Temporary directories (`tempfile.TemporaryDirectory`)
-   Named temporary files (`tempfile.NamedTemporaryFile`)

### When to Use:

Use `tempfile` when you need temporary storage that is automatically
cleaned up.

------------------------------------------------------------------------

# Quick Comparison Table

  -----------------------------------------------------------------------------
  Library       Main Purpose                                Level
  ------------- ------------------------------------------- -------------------
  os            OS interaction                              Low-level

  platform      System information                          Informational

  shutil        File operations (copy/move/delete)          High-level

  subprocess    Run external programs                       Process-level

  sys           Python runtime interaction                  Interpreter-level

  pathlib       Modern path handling                        High-level

  tempfile      Temporary file/directory creation           Utility
  -----------------------------------------------------------------------------

------------------------------------------------------------------------

# Recommendation

-   Use `pathlib` for path handling.
-   Use `shutil` for file management.
-   Use `subprocess` for running commands.
-   Use `sys` for runtime interaction.
-   Use `os` for lower-level system tasks.
-   Use `platform` for OS detection.
-   Use `tempfile` for temporary data handling.
