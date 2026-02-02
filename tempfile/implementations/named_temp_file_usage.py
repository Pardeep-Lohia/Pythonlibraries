#!/usr/bin/env python3
"""
Implementation examples for NamedTemporaryFile usage in the tempfile module.

This script demonstrates various ways to use NamedTemporaryFile for temporary
files with accessible filenames.
"""

import tempfile
import os
import sys
import shutil


def basic_named_temporary_file():
    """
    Basic usage of NamedTemporaryFile - creates a named temporary file.
    """
    print("=== Basic NamedTemporaryFile Usage ===")

    # Create a named temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        print(f"Named temporary file created: {temp_file.name}")

        # Write some data
        data = b"Hello, this is named temporary data!"
        temp_file.write(data)
        print(f"Wrote {len(data)} bytes to named temporary file")

        # Read the data back
        temp_file.seek(0)  # Go back to beginning
        read_data = temp_file.read()
        print(f"Read back: {read_data.decode()}")

        # File path is accessible
        print(f"File exists at: {temp_file.name}")
        print(f"File size on disk: {os.path.getsize(temp_file.name)} bytes")

    # File is automatically deleted when exiting the context
    print(f"File still exists after context exit: {os.path.exists(temp_file.name)}")


def named_temporary_file_custom_prefix_suffix():
    """
    Demonstrate custom prefix and suffix with NamedTemporaryFile.
    """
    print("\n=== Custom Prefix and Suffix ===")

    with tempfile.NamedTemporaryFile(
        prefix="myapp_temp_",
        suffix=".log",
        delete=False
    ) as f:
        print(f"Custom named file: {f.name}")
        f.write(b"Log entry: Application started")

    print(f"File deleted: {not os.path.exists(f.name)}")


def named_temporary_file_modes():
    """
    Demonstrate different file modes with NamedTemporaryFile.
    """
    print("\n=== NamedTemporaryFile with Different Modes ===")

    # Binary mode
    print("Binary mode:")
    with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as f:
        print(f"  File: {f.name}")
        f.write(b"Binary data")
        f.seek(0)
        print(f"  Read: {f.read()}")

    # Text mode
    print("Text mode:")
    with tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8', delete=False) as f:
        print(f"  File: {f.name}")
        f.write("Text data: Hello 世界")
        f.seek(0)
        print(f"  Read: {f.read()}")


def named_temporary_file_persistence():
    """
    Show how to keep NamedTemporaryFile after context exit.
    """
    print("\n=== File Persistence Control ===")

    # Automatic deletion
    with tempfile.NamedTemporaryFile() as auto_delete:
        print(f"Auto-delete file: {auto_delete.name}")
        auto_delete.write(b"This will be deleted")
    print(f"Auto-delete file exists: {os.path.exists(auto_delete.name)}")

    # Manual deletion control
    manual_file = tempfile.NamedTemporaryFile(delete=False)
    manual_file.write(b"This persists after close")
    manual_file.close()
    print(f"Manual file exists after close: {os.path.exists(manual_file.name)}")

    # Manual cleanup
    os.unlink(manual_file.name)
    print(f"Manual file exists after unlink: {os.path.exists(manual_file.name)}")


def named_temporary_file_external_access():
    """
    Demonstrate accessing NamedTemporaryFile from external programs.
    """
    print("\n=== External Program Access ===")

    with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as f:
        # Write data that can be accessed externally
        f.write("This file can be opened by other programs\n")
        f.write(f"File path: {f.name}\n")
        f.flush()  # Ensure data is written to disk

        print(f"File created for external access: {f.name}")

        # Simulate external program access
        with open(f.name, 'r') as external_f:
            content = external_f.read()
            print("Content read by external access:")
            print(content)

    print(f"File cleaned up: {not os.path.exists(f.name)}")


def named_temporary_file_with_custom_dir():
    """
    Use NamedTemporaryFile with custom directory.
    """
    print("\n=== Custom Directory ===")

    # Create a custom temp directory
    custom_temp_dir = tempfile.mkdtemp(prefix="my_custom_temp_")
    print(f"Using custom temp directory: {custom_temp_dir}")

    try:
        with tempfile.NamedTemporaryFile(dir=custom_temp_dir, delete=False) as f:
            f.write(b"Data in custom directory")
            print(f"File in custom dir: {f.name}")
            print(f"Directory contents: {os.listdir(custom_temp_dir)}")
    finally:
        # Clean up
        if os.path.exists(f.name):
            os.unlink(f.name)
        os.rmdir(custom_temp_dir)
        print("Custom temp directory and file cleaned up")


def named_temporary_file_large_data():
    """
    Handle large data with NamedTemporaryFile.
    """
    print("\n=== Large Data Handling ===")

    # Create 5MB test data
    large_data = b"X" * (5 * 1024 * 1024)

    with tempfile.NamedTemporaryFile(delete=False) as f:
        print(f"Writing {len(large_data)} bytes...")
        f.write(large_data)
        f.flush()

        # Check file size on disk
        disk_size = os.path.getsize(f.name)
        print(f"File size on disk: {disk_size} bytes")

        # Verify data integrity
        f.seek(0)
        read_data = f.read()
        if len(read_data) == len(large_data):
            print("Data size verified")
        else:
            print("Data size mismatch!")

    # Manual cleanup for large file
    os.unlink(f.name)
    print("Large temporary file cleaned up")


def named_temporary_file_multiple_files():
    """
    Create and manage multiple NamedTemporaryFile instances.
    """
    print("\n=== Multiple Named Temporary Files ===")

    files = []
    try:
        # Create multiple files
        for i in range(3):
            f = tempfile.NamedTemporaryFile(
                prefix=f"multi_{i}_",
                suffix=".dat",
                delete=False
            )
            f.write(f"Data for file {i}".encode())
            f.close()
            files.append(f.name)
            print(f"Created file {i}: {f.name}")

        # List all files
        print(f"Total files created: {len(files)}")
        for name in files:
            print(f"  {name} (exists: {os.path.exists(name)})")

    finally:
        # Clean up all files
        for name in files:
            if os.path.exists(name):
                os.unlink(name)
                print(f"Cleaned up: {name}")


def named_temporary_file_with_contextlib():
    """
    Use NamedTemporaryFile with contextlib for advanced resource management.
    """
    print("\n=== Advanced Resource Management ===")

    from contextlib import ExitStack

    with ExitStack() as stack:
        # Create multiple temporary files
        temp_files = []
        for i in range(3):
            f = stack.enter_context(
                tempfile.NamedTemporaryFile(
                    prefix=f"context_{i}_",
                    delete=False
                )
            )
            f.write(f"Context-managed file {i}".encode())
            temp_files.append(f)

        print("Created files in context:")
        for f in temp_files:
            print(f"  {f.name}")

        # Files are automatically cleaned up when exiting context
    print("All context-managed files cleaned up")


def named_temporary_file_error_handling():
    """
    Demonstrate error handling with NamedTemporaryFile.
    """
    print("\n=== Error Handling ===")

    try:
        with tempfile.NamedTemporaryFile() as f:
            # Try to perform invalid operation
            f.write("String data to binary file")
    except TypeError as e:
        print(f"Caught expected type error: {e}")

    # Proper usage
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        f.write("Proper text data")
        f.seek(0)
        print(f"Successfully wrote: {f.read()}")


def named_temporary_file_system_integration():
    """
    Show integration with other system modules.
    """
    print("\n=== System Integration ===")

    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp_f:
        # Write test data
        temp_f.write(b"Integration test data\n")
        temp_f.write(b"Line 2\n")
        temp_f.flush()

        # Use shutil to copy the file
        with tempfile.NamedTemporaryFile(suffix='.bak', delete=False) as backup_f:
            shutil.copy2(temp_f.name, backup_f.name)
            print(f"Copied {temp_f.name} to {backup_f.name}")

            # Verify copy
            with open(backup_f.name, 'rb') as verify_f:
                copied_data = verify_f.read()
                print(f"Backup contains: {len(copied_data)} bytes")

        # Clean up backup
        os.unlink(backup_f.name)

    # Original file cleaned up by context manager


def main():
    """
    Run all NamedTemporaryFile implementation examples.
    """
    print("NamedTemporaryFile Implementation Examples")
    print("=" * 50)

    basic_named_temporary_file()
    named_temporary_file_custom_prefix_suffix()
    named_temporary_file_modes()
    named_temporary_file_persistence()
    named_temporary_file_external_access()
    named_temporary_file_with_custom_dir()
    named_temporary_file_large_data()
    named_temporary_file_multiple_files()
    named_temporary_file_with_contextlib()
    named_temporary_file_error_handling()
    named_temporary_file_system_integration()

    print("\n" + "=" * 50)
    print("All examples completed successfully!")


if __name__ == "__main__":
    main()
