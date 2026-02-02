#!/usr/bin/env python3
"""
Secure File Processing with tempfile

This example demonstrates how to securely process uploaded or untrusted files
using temporary files to prevent security vulnerabilities.
"""

import tempfile
import os
import hashlib
import mimetypes
from pathlib import Path


def secure_file_upload_simulation():
    """Simulate secure processing of uploaded files."""
    print("=== Secure File Upload Processing ===")

    # Simulate uploaded file content (could be malicious)
    uploaded_content = b"""
#!/bin/bash
echo "Malicious script execution!"
rm -rf /important/files
"""

    print("Processing potentially malicious uploaded content...")

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        # Write uploaded content to temporary file
        temp_file.write(uploaded_content)
        temp_path = temp_file.name

    try:
        # Analyze file safely
        file_info = analyze_file_safely(temp_path)
        print(f"File type: {file_info['mime_type']}")
        print(f"File size: {file_info['size']} bytes")
        print(f"SHA256: {file_info['sha256'][:16]}...")

        # Process based on type
        if file_info['mime_type'].startswith('text/'):
            process_text_file(temp_path)
        elif file_info['mime_type'] == 'application/json':
            process_json_file(temp_path)
        else:
            print("Unsupported file type - quarantined")

    finally:
        # Always cleanup
        os.unlink(temp_path)

    print()


def analyze_file_safely(file_path):
    """Safely analyze a file without executing it."""
    info = {}

    # Get file size
    info['size'] = os.path.getsize(file_path)

    # Detect MIME type
    info['mime_type'], _ = mimetypes.guess_type(file_path)

    # Calculate hash for integrity
    with open(file_path, 'rb') as f:
        info['sha256'] = hashlib.sha256(f.read()).hexdigest()

    return info


def process_text_file(file_path):
    """Process text files safely."""
    print("Processing as text file...")

    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # Safe text processing
    lines = content.split('\n')
    print(f"Lines: {len(lines)}")
    print(f"Contains 'echo': {'echo' in content.lower()}")

    # Could apply filters, validation, etc.
    safe_content = sanitize_text_content(content)
    print(f"Sanitized content length: {len(safe_content)}")


def process_json_file(file_path):
    """Process JSON files safely."""
    print("Processing as JSON file...")

    import json

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"JSON keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")

        # Validate JSON structure
        if validate_json_structure(data):
            print("JSON structure is valid")
        else:
            print("JSON structure validation failed")

    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")


def sanitize_text_content(content):
    """Basic text sanitization."""
    # Remove potentially dangerous patterns
    dangerous_patterns = [
        '#!/bin/bash',
        '#!/usr/bin/env',
        'rm -rf',
        'sudo',
        'chmod +x'
    ]

    sanitized = content
    for pattern in dangerous_patterns:
        sanitized = sanitized.replace(pattern, f'[REMOVED: {pattern}]')

    return sanitized


def validate_json_structure(data):
    """Validate JSON has expected structure."""
    if not isinstance(data, dict):
        return False

    required_keys = ['type', 'content']
    return all(key in data for key in required_keys)


def secure_image_processing():
    """Example of processing image files securely."""
    print("=== Secure Image Processing ===")

    # Simulate image data (in real scenario, this would be uploaded)
    image_data = b'\x89PNG\r\n\x1a\n' + b'x' * 1000  # Fake PNG header + data

    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
        temp_file.write(image_data)
        temp_path = temp_file.name

    try:
        # Validate file type by content, not just extension
        if validate_image_file(temp_path):
            print("Image file validated successfully")

            # Safe processing (would use PIL, OpenCV, etc.)
            process_image_safely(temp_path)
        else:
            print("Invalid image file - rejected")

    finally:
        os.unlink(temp_path)

    print()


def validate_image_file(file_path):
    """Validate image file by checking magic bytes."""
    image_signatures = {
        b'\xFF\xD8\xFF': 'JPEG',
        b'\x89PNG\r\n\x1a\n': 'PNG',
        b'GIF87a': 'GIF',
        b'GIF89a': 'GIF'
    }

    try:
        with open(file_path, 'rb') as f:
            header = f.read(10)

        for signature, format_type in image_signatures.items():
            if header.startswith(signature):
                print(f"Detected {format_type} format")
                return True

        return False

    except (OSError, IOError):
        return False


def process_image_safely(file_path):
    """Safe image processing placeholder."""
    print(f"Would process image: {file_path}")
    # In real implementation:
    # - Use PIL to open and validate image
    # - Check dimensions, format
    # - Apply processing in isolated environment
    # - Save to final location


def secure_code_execution():
    """Example of secure code execution in temporary environment."""
    print("=== Secure Code Execution ===")

    # User-submitted code (potentially malicious)
    user_code = """
import os
print("Current directory:", os.getcwd())
print("Files:", os.listdir("."))
# Dangerous: os.system("rm -rf *")
"""

    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Executing in isolated directory: {temp_dir}")

        # Create code file
        code_path = os.path.join(temp_dir, 'user_code.py')
        with open(code_path, 'w') as f:
            f.write(user_code)

        # Execute in restricted environment
        result = execute_code_safely(code_path, temp_dir)

        print(f"Execution result: {result['success']}")
        if result['output']:
            print(f"Output: {result['output'][:100]}...")

    print()


def execute_code_safely(code_path, working_dir):
    """Execute code in a restricted environment."""
    import subprocess

    try:
        # Run with restricted permissions and timeout
        result = subprocess.run(
            ['python3', code_path],
            cwd=working_dir,
            capture_output=True,
            text=True,
            timeout=5,  # 5 second timeout
            # In real implementation, would use more restrictions
        )

        return {
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr
        }

    except subprocess.TimeoutExpired:
        return {'success': False, 'output': '', 'error': 'Timeout'}
    except Exception as e:
        return {'success': False, 'output': '', 'error': str(e)}


def secure_data_transformation():
    """Secure data transformation pipeline."""
    print("=== Secure Data Transformation ===")

    # Raw input data
    raw_data = "user input; potentially; malicious; data\n" * 100

    # Transformation pipeline using temporary files
    with tempfile.TemporaryDirectory() as workspace:
        print(f"Processing in workspace: {workspace}")

        # Stage 1: Parse and validate
        stage1_path = os.path.join(workspace, 'stage1_validated.csv')
        validated_data = validate_and_parse_csv(raw_data)
        with open(stage1_path, 'w') as f:
            f.write(validated_data)

        # Stage 2: Transform
        stage2_path = os.path.join(workspace, 'stage2_transformed.json')
        transform_data(stage1_path, stage2_path)

        # Stage 3: Finalize
        final_path = os.path.join(workspace, 'final_output.txt')
        finalize_output(stage2_path, final_path)

        # Read final result
        with open(final_path, 'r') as f:
            final_result = f.read()

        print(f"Final output length: {len(final_result)}")
        print(f"Processing completed successfully")

    print()


def validate_and_parse_csv(data):
    """Validate and clean CSV data."""
    lines = data.strip().split('\n')
    validated_lines = []

    for line in lines:
        # Basic validation and sanitization
        if ';' in line and len(line.split(';')) >= 3:
            # Escape semicolons, remove dangerous chars
            safe_line = line.replace('<', '<').replace('>', '>')
            validated_lines.append(safe_line)

    return '\n'.join(validated_lines)


def transform_data(input_path, output_path):
    """Transform validated data to JSON."""
    import json

    with open(input_path, 'r') as f:
        lines = f.readlines()

    # Transform to structured data
    transformed = {
        'records': [line.strip().split(';') for line in lines if line.strip()],
        'metadata': {
            'source': 'validated_csv',
            'record_count': len(lines)
        }
    }

    with open(output_path, 'w') as f:
        json.dump(transformed, f, indent=2)


def finalize_output(input_path, output_path):
    """Create final output."""
    import json

    with open(input_path, 'r') as f:
        data = json.load(f)

    # Create summary
    summary = f"Processed {data['metadata']['record_count']} records\n"
    summary += f"Source: {data['metadata']['source']}\n"
    summary += "Processing completed successfully\n"

    with open(output_path, 'w') as f:
        f.write(summary)


def main():
    """Run all secure processing examples."""
    print("Secure File Processing Examples")
    print("=" * 40)
    print()

    secure_file_upload_simulation()
    secure_image_processing()
    secure_code_execution()
    secure_data_transformation()

    print("All secure processing examples completed!")


if __name__ == "__main__":
    main()
