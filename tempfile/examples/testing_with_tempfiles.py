#!/usr/bin/env python3
"""
Example: Using tempfile for testing scenarios.

This script demonstrates how to use the tempfile module effectively
in testing environments, including unit tests, integration tests,
and temporary test data management.
"""

import tempfile
import os
import unittest
import json
import csv
import shutil
import sys
from pathlib import Path


class TempFileTestExamples(unittest.TestCase):
    """
    Unit test examples using tempfile for test isolation.
    """

    def setUp(self):
        """Set up test fixtures using temporary files/directories."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_data = {
            "users": [
                {"id": 1, "name": "Alice", "email": "alice@example.com"},
                {"id": 2, "name": "Bob", "email": "bob@example.com"}
            ]
        }

    def tearDown(self):
        """Clean up temporary resources."""
        self.temp_dir.cleanup()

    def test_file_processing_with_temp_input(self):
        """Test file processing using temporary input file."""
        # Create temporary input file
        input_file = os.path.join(self.temp_dir.name, "input.json")
        with open(input_file, 'w') as f:
            json.dump(self.test_data, f)

        # Test processing function
        result = process_json_file(input_file)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'Alice')

    def test_csv_data_processing(self):
        """Test CSV processing with temporary files."""
        # Create temporary CSV file
        csv_file = os.path.join(self.temp_dir.name, "data.csv")

        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Age', 'City'])
            writer.writerow(['Alice', 30, 'New York'])
            writer.writerow(['Bob', 25, 'London'])

        # Test CSV processing
        result = process_csv_file(csv_file)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['Age'], 30)

    def test_image_processing_simulation(self):
        """Simulate image processing with temporary files."""
        # Create temporary "image" file
        image_file = os.path.join(self.temp_dir.name, "test_image.jpg")
        with open(image_file, 'wb') as f:
            f.write(b"fake image data: " + b"X" * 1000)

        # Test image processing function
        result = process_image_file(image_file)
        self.assertTrue(result['processed'])
        self.assertEqual(result['size'], 1017)  # "fake image data: " + 1000 X's

    def test_directory_operations(self):
        """Test operations requiring temporary directory structures."""
        # Create temporary directory structure
        data_dir = os.path.join(self.temp_dir.name, "data")
        output_dir = os.path.join(self.temp_dir.name, "output")

        os.makedirs(data_dir)
        os.makedirs(output_dir)

        # Create test files
        for i in range(3):
            with open(os.path.join(data_dir, f"file_{i}.txt"), 'w') as f:
                f.write(f"Content {i}")

        # Test directory processing
        result = process_directory(data_dir, output_dir)
        self.assertEqual(result['processed_files'], 3)
        self.assertEqual(result['output_files'], 3)


def process_json_file(file_path):
    """Mock function to process JSON file."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data['users']


def process_csv_file(file_path):
    """Mock function to process CSV file."""
    result = []
    with open(file_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            result.append(row)
    return result


def process_image_file(file_path):
    """Mock function to process image file."""
    with open(file_path, 'rb') as f:
        data = f.read()
    return {
        'processed': True,
        'size': len(data),
        'format': 'simulated'
    }


def process_directory(input_dir, output_dir):
    """Mock function to process directory contents."""
    processed = 0
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f"processed_{filename}")

            with open(input_path, 'r') as f:
                content = f.read()

            with open(output_path, 'w') as f:
                f.write(f"PROCESSED: {content}")

            processed += 1

    return {
        'processed_files': processed,
        'output_files': len(os.listdir(output_dir))
    }


class IntegrationTestExamples:
    """
    Examples of integration testing with temporary resources.
    """

    @staticmethod
    def test_database_backup_simulation():
        """Simulate database backup using temporary files."""
        print("=== Database Backup Simulation ===")

        with tempfile.TemporaryDirectory() as temp_dir:
            # Simulate database files
            db_files = ['users.db', 'transactions.db', 'config.db']
            for db_file in db_files:
                db_path = os.path.join(temp_dir, db_file)
                with open(db_path, 'wb') as f:
                    f.write(b"fake database content: " + os.urandom(1000))

            # Simulate backup process
            backup_dir = os.path.join(temp_dir, "backup")
            os.makedirs(backup_dir)

            total_size = 0
            for db_file in db_files:
                src = os.path.join(temp_dir, db_file)
                dst = os.path.join(backup_dir, f"backup_{db_file}")
                shutil.copy2(src, dst)
                total_size += os.path.getsize(dst)

            print(f"Backed up {len(db_files)} database files")
            print(f"Total backup size: {total_size} bytes")
            print("Backup simulation completed")

    @staticmethod
    def test_log_rotation_simulation():
        """Simulate log file rotation using temporary files."""
        print("\n=== Log Rotation Simulation ===")

        with tempfile.TemporaryDirectory() as temp_dir:
            log_dir = os.path.join(temp_dir, "logs")
            archive_dir = os.path.join(temp_dir, "archives")
            os.makedirs(log_dir)
            os.makedirs(archive_dir)

            # Create simulated log files
            log_files = []
            for i in range(5):
                log_file = os.path.join(log_dir, f"app_{i}.log")
                with open(log_file, 'w') as f:
                    for j in range(100):
                        f.write(f"2023-01-{i+1} INFO Log entry {j}\n")
                log_files.append(log_file)

            # Simulate rotation
            rotated_count = 0
            for log_file in log_files:
                if os.path.getsize(log_file) > 1000:  # Rotate if > 1KB
                    archive_name = os.path.basename(log_file).replace('.log', f"_{i}.log.gz")
                    archive_path = os.path.join(archive_dir, archive_name)

                    # Simulate compression (just copy for demo)
                    shutil.copy2(log_file, archive_path)

                    # Truncate original log
                    with open(log_file, 'w') as f:
                        f.write("Log rotated\n")

                    rotated_count += 1

            print(f"Rotated {rotated_count} log files")
            print(f"Archives created: {len(os.listdir(archive_dir))}")
            print("Log rotation simulation completed")

    @staticmethod
    def test_cache_simulation():
        """Simulate caching system using temporary files."""
        print("\n=== Cache Simulation ===")

        with tempfile.TemporaryDirectory() as temp_dir:
            cache_dir = os.path.join(temp_dir, "cache")
            os.makedirs(cache_dir)

            # Simulate cache operations
            cache_hits = 0
            cache_misses = 0

            test_keys = ['user_1', 'user_2', 'user_1', 'user_3', 'user_2']

            for key in test_keys:
                cache_file = os.path.join(cache_dir, f"{key}.cache")

                if os.path.exists(cache_file):
                    # Cache hit
                    with open(cache_file, 'r') as f:
                        data = f.read()
                    cache_hits += 1
                    print(f"Cache hit for {key}: {data}")
                else:
                    # Cache miss - fetch and store
                    data = f"Data for {key}: {os.urandom(10).hex()}"
                    with open(cache_file, 'w') as f:
                        f.write(data)
                    cache_misses += 1
                    print(f"Cache miss for {key}, stored: {data}")

            print(f"Cache hits: {cache_hits}, Misses: {cache_misses}")
            print(f"Cache files: {len(os.listdir(cache_dir))}")
            print("Cache simulation completed")


class PerformanceTestExamples:
    """
    Examples of performance testing with temporary files.
    """

    @staticmethod
    def benchmark_file_operations():
        """Benchmark file operations using temporary files."""
        print("=== File Operations Benchmark ===")

        with tempfile.TemporaryDirectory() as temp_dir:
            import time

            # Test data sizes
            sizes = [1024, 1024*1024, 10*1024*1024]  # 1KB, 1MB, 10MB

            for size in sizes:
                # Create test data
                data = b"X" * size

                # Benchmark write
                start_time = time.time()
                with tempfile.NamedTemporaryFile(dir=temp_dir, delete=False) as f:
                    f.write(data)
                    temp_file = f.name
                write_time = time.time() - start_time

                # Benchmark read
                start_time = time.time()
                with open(temp_file, 'rb') as f:
                    read_data = f.read()
                read_time = time.time() - start_time

                # Cleanup
                os.unlink(temp_file)

                print(f"Size: {size} bytes")
                print(".4f")
                print(".4f")
                print()

    @staticmethod
    def memory_vs_disk_performance():
        """Compare memory vs disk temporary file performance."""
        print("=== Memory vs Disk Performance ===")

        import time
        from tempfile import SpooledTemporaryFile

        test_sizes = [1024, 1024*100, 1024*1000]  # Small, medium, large

        for size in test_sizes:
            data = b"X" * size

            # Test SpooledTemporaryFile (memory then disk)
            start_time = time.time()
            with SpooledTemporaryFile(max_size=1024*500) as f:  # 500KB threshold
                f.write(data)
                f.seek(0)
                _ = f.read()
            spooled_time = time.time() - start_time

            # Test NamedTemporaryFile (always disk)
            start_time = time.time()
            with tempfile.NamedTemporaryFile() as f:
                f.write(data)
                f.seek(0)
                _ = f.read()
            named_time = time.time() - start_time

            print(f"Size: {size} bytes")
            print(".4f")
            print(".4f")
            print()


class MockFileSystemExamples:
    """
    Examples of creating mock file systems for testing.
    """

    @staticmethod
    def create_mock_project_structure():
        """Create a mock project structure for testing."""
        print("=== Mock Project Structure ===")

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create directory structure
            dirs = [
                "src",
                "src/utils",
                "tests",
                "docs",
                "data",
                "data/input",
                "data/output"
            ]

            for dir_path in dirs:
                os.makedirs(os.path.join(temp_dir, dir_path))

            # Create mock files
            files = {
                "src/main.py": "print('Hello, World!')",
                "src/utils/helpers.py": "def helper(): pass",
                "tests/test_main.py": "import unittest\n\nclass TestMain(unittest.TestCase):\n    pass",
                "docs/README.md": "# Project Documentation",
                "data/input/sample.csv": "name,age\nAlice,30\nBob,25",
                "requirements.txt": "pytest\nrequests",
                ".gitignore": "*.pyc\n__pycache__/"
            }

            for file_path, content in files.items():
                full_path = os.path.join(temp_dir, file_path)
                with open(full_path, 'w') as f:
                    f.write(content)

            # Show structure
            print("Created mock project structure:")
            for root, dirs, files in os.walk(temp_dir):
                level = root.replace(temp_dir, '').count(os.sep)
                indent = '  ' * level
                print(f"{indent}{os.path.basename(root)}/")
                subindent = '  ' * (level + 1)
                for file in files:
                    print(f"{subindent}{file}")

            print(f"Total directories: {sum(len(dirs) for _, dirs, _ in os.walk(temp_dir))}")
            print(f"Total files: {sum(len(files) for _, _, files in os.walk(temp_dir))}")

    @staticmethod
    def simulate_file_upload_scenario():
        """Simulate file upload processing."""
        print("\n=== File Upload Simulation ===")

        with tempfile.TemporaryDirectory() as temp_dir:
            upload_dir = os.path.join(temp_dir, "uploads")
            processed_dir = os.path.join(temp_dir, "processed")
            os.makedirs(upload_dir)
            os.makedirs(processed_dir)

            # Simulate uploaded files
            uploaded_files = [
                ("document.pdf", b"PDF content " + os.urandom(1000)),
                ("image.jpg", b"JPG content " + os.urandom(2000)),
                ("text.txt", b"TXT content: Hello, World!"),
                ("spreadsheet.xlsx", b"XLSX content " + os.urandom(1500))
            ]

            processed_count = 0

            for filename, content in uploaded_files:
                # Save uploaded file
                upload_path = os.path.join(upload_dir, filename)
                with open(upload_path, 'wb') as f:
                    f.write(content)

                # Simulate processing
                processed_path = os.path.join(processed_dir, f"processed_{filename}")
                with open(processed_path, 'wb') as f:
                    f.write(b"PROCESSED: " + content)

                processed_count += 1
                print(f"Processed {filename} ({len(content)} bytes)")

            print(f"Total files processed: {processed_count}")
            print(f"Upload directory: {len(os.listdir(upload_dir))} files")
            print(f"Processed directory: {len(os.listdir(processed_dir))} files")


def main():
    """Run all testing examples."""
    print("Tempfile Testing Examples")
    print("=" * 50)

    # Run unit tests
    print("\nRunning Unit Tests...")
    unittest.main(argv=[''], exit=False, verbosity=2)

    # Run integration test examples
    print("\nRunning Integration Test Examples...")
    IntegrationTestExamples.test_database_backup_simulation()
    IntegrationTestExamples.test_log_rotation_simulation()
    IntegrationTestExamples.test_cache_simulation()

    # Run performance test examples
    print("\nRunning Performance Test Examples...")
    PerformanceTestExamples.benchmark_file_operations()
    PerformanceTestExamples.memory_vs_disk_performance()

    # Run mock filesystem examples
    print("\nRunning Mock File System Examples...")
    MockFileSystemExamples.create_mock_project_structure()
    MockFileSystemExamples.simulate_file_upload_scenario()

    print("\n" + "=" * 50)
    print("All testing examples completed successfully!")


if __name__ == "__main__":
    main()
