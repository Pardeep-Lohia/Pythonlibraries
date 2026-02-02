#!/usr/bin/env python3
"""
Pipe Communication Examples

This module demonstrates various I/O pipe communication patterns with subprocess,
including stdin/stdout/stderr handling, pipelines, and advanced communication techniques.
"""

import subprocess
import sys
import threading
import time
import platform
import os


def basic_pipe_usage():
    """Demonstrate basic pipe usage with subprocess"""
    print("=== Basic Pipe Usage ===")

    # Capture stdout
    result = subprocess.run(['echo', 'Hello World'],
                           capture_output=True, text=True)
    print(f"Stdout: {result.stdout.strip()}")

    # Capture stderr
    result = subprocess.run(['ls', '/nonexistent'],
                           capture_output=True, text=True)
    print(f"Stderr: {result.stderr.strip()}")
    print(f"Return code: {result.returncode}")


def input_providing_patterns():
    """Demonstrate different ways to provide input to processes"""
    print("\n=== Input Providing Patterns ===")

    # Method 1: Using input parameter
    print("Method 1: input parameter")
    result = subprocess.run(['grep', 'python'],
                           input='Python is great\nJava is good\nPython rocks\n',
                           capture_output=True, text=True)
    print(f"Matches: {result.stdout.strip()}")

    # Method 2: Using stdin with Popen
    print("\nMethod 2: Popen with stdin")
    process = subprocess.Popen(['sort'],
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              text=True)

    input_data = 'zebra\napple\nbanana\n'
    stdout, _ = process.communicate(input_data)
    print(f"Sorted: {stdout.strip()}")

    # Method 3: From file
    print("\nMethod 3: Input from file")
    with open('temp_input.txt', 'w') as f:
        f.write('Line 1\nLine 2\nLine 3\n')

    with open('temp_input.txt', 'r') as f:
        result = subprocess.run(['cat'], stdin=f, capture_output=True, text=True)
    print(f"From file: {result.stdout.strip()}")

    # Cleanup
    os.unlink('temp_input.txt')


def output_redirection_patterns():
    """Demonstrate output redirection patterns"""
    print("\n=== Output Redirection Patterns ===")

    # Method 1: To file
    print("Method 1: Redirect to file")
    with open('temp_output.txt', 'w') as f:
        subprocess.run(['echo', 'Hello File'], stdout=f)

    with open('temp_output.txt', 'r') as f:
        content = f.read().strip()
    print(f"File content: {content}")

    # Method 2: Merge stderr to stdout
    print("\nMethod 2: Merge stderr to stdout")
    result = subprocess.run(['python3', '-c', 'import sys; print("out"); sys.stderr.write("err\\n")'],
                           capture_output=True, text=True)
    print(f"Stdout: '{result.stdout.strip()}'")

    result = subprocess.run(['python3', '-c', 'import sys; print("out"); sys.stderr.write("err\\n")'],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    print(f"Merged: '{result.stdout.strip()}'")

    # Method 3: Discard output
    print("\nMethod 3: Discard output")
    result = subprocess.run(['echo', 'This will be discarded'],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
    print(f"Return code: {result.returncode} (output discarded)")

    # Cleanup
    os.unlink('temp_output.txt')


def process_pipelines():
    """Demonstrate creating pipelines between processes"""
    print("\n=== Process Pipelines ===")

    # Simple pipeline: ls | grep .py
    if platform.system() == 'Windows':
        # Windows version
        p1 = subprocess.Popen(['dir', '/b'], stdout=subprocess.PIPE, text=True)
        p2 = subprocess.Popen(['findstr', '.py'], stdin=p1.stdout,
                             stdout=subprocess.PIPE, text=True)
        p1.stdout.close()
    else:
        # Unix version
        p1 = subprocess.Popen(['ls', '-la'], stdout=subprocess.PIPE, text=True)
        p2 = subprocess.Popen(['grep', '.py'], stdin=p1.stdout,
                             stdout=subprocess.PIPE, text=True)
        p1.stdout.close()

    output, _ = p2.communicate()
    p2.wait()

    print(f"Python files: {len(output.strip().split('\\n'))} found")

    # Complex pipeline: ls | grep .py | wc -l
    print("\nComplex pipeline:")
    if platform.system() == 'Windows':
        p1 = subprocess.Popen(['dir', '/b'], stdout=subprocess.PIPE, text=True)
        p2 = subprocess.Popen(['findstr', '.py'], stdin=p1.stdout,
                             stdout=subprocess.PIPE, text=True)
        p1.stdout.close()
        p3 = subprocess.Popen(['find', '/c', '""'], stdin=p2.stdout,
                             stdout=subprocess.PIPE, text=True)
        p2.stdout.close()
    else:
        p1 = subprocess.Popen(['ls', '-la'], stdout=subprocess.PIPE, text=True)
        p2 = subprocess.Popen(['grep', '.py'], stdin=p1.stdout,
                             stdout=subprocess.PIPE, text=True)
        p1.stdout.close()
        p3 = subprocess.Popen(['wc', '-l'], stdin=p2.stdout,
                             stdout=subprocess.PIPE, text=True)
        p2.stdout.close()

    final_output, _ = p3.communicate()
    p3.wait()

    print(f"Total Python files: {final_output.strip()}")


def real_time_io():
    """Demonstrate real-time I/O with pipes"""
    print("\n=== Real-Time I/O ===")

    # Start a process that produces output over time
    if platform.system() == 'Windows':
        cmd = ['ping', '-n', '3', '127.0.0.1']
    else:
        cmd = ['ping', '-c', '3', '127.0.0.1']

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, text=True)

    print("Reading output in real-time:")
    while True:
        line = process.stdout.readline()
        if line == '' and process.poll() is not None:
            break
        if line:
            print(f"  {line.strip()}")

    print(f"Process completed with return code: {process.returncode}")


def bidirectional_communication():
    """Demonstrate bidirectional communication with a subprocess"""
    print("\n=== Bidirectional Communication ===")

    # Start an interactive Python process
    process = subprocess.Popen([sys.executable, '-c', '''
import sys
print("Interactive Python subprocess")
sys.stdout.flush()

while True:
    try:
        line = input(">>> ")
        if line.lower() == 'quit':
            print("Goodbye!")
            break
        result = eval(line)
        print(f"Result: {result}")
        sys.stdout.flush()
    except (EOFError, KeyboardInterrupt):
        break
    except Exception as e:
        print(f"Error: {e}")
        sys.stdout.flush()
'''],
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              text=True)

    # Interact with the process
    interactions = [
        ('2 + 3', '5'),
        ('len("hello")', '5'),
        ('quit', 'Goodbye!')
    ]

    for input_line, expected in interactions:
        print(f"Sending: {input_line}")

        # Send input
        process.stdin.write(input_line + '\n')
        process.stdin.flush()

        # Read prompt
        prompt = process.stdout.readline().strip()
        print(f"Prompt: {prompt}")

        # Read result
        result = process.stdout.readline().strip()
        print(f"Result: {result}")

        time.sleep(0.1)  # Allow subprocess to process

    # Close stdin and get remaining output
    process.stdin.close()
    remaining, errors = process.communicate()

    if remaining:
        print(f"Remaining output: {remaining.strip()}")

    print(f"Subprocess return code: {process.returncode}")


def non_blocking_io():
    """Demonstrate non-blocking I/O operations"""
    print("\n=== Non-Blocking I/O ===")

    try:
        import fcntl
        import select

        # Start a process
        process = subprocess.Popen(['python3', '-c', '''
import time
for i in range(5):
    print(f"Line {i+1}")
    time.sleep(0.5)
'''],
                                  stdout=subprocess.PIPE,
                                  text=True)

        # Make stdout non-blocking
        fd = process.stdout.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

        print("Reading non-blocking output:")
        output_lines = []

        while process.poll() is None or output_lines:
            # Check if data is available
            ready, _, _ = select.select([process.stdout], [], [], 0.1)

            if ready:
                try:
                    line = process.stdout.readline()
                    if line:
                        output_lines.append(line.strip())
                        print(f"  Read: {line.strip()}")
                except OSError:
                    # No data available
                    pass

            # Process completed
            if process.poll() is not None and not ready:
                break

        # Read any remaining output
        remaining, _ = process.communicate()
        if remaining:
            for line in remaining.strip().split('\n'):
                if line:
                    output_lines.append(line)
                    print(f"  Remaining: {line}")

        print(f"Total lines read: {len(output_lines)}")

    except ImportError:
        print("Non-blocking I/O not available on this platform")


def pipe_buffering_techniques():
    """Demonstrate pipe buffering techniques"""
    print("\n=== Pipe Buffering Techniques ===")

    # Line-buffered output
    print("Line-buffered output:")
    process = subprocess.Popen(['python3', '-c', '''
import sys
import time
for i in range(3):
    print(f"Line {i+1}", flush=True)
    time.sleep(0.2)
'''],
                              stdout=subprocess.PIPE,
                              text=True,
                              bufsize=1)  # Line buffered

    for line in process.stdout:
        print(f"  Received: {line.strip()}")

    # Unbuffered output
    print("\nUnbuffered output:")
    process = subprocess.Popen(['python3', '-c', '''
import sys
import time
import os
# Make stdout unbuffered
os.environ['PYTHONUNBUFFERED'] = '1'

for i in range(3):
    sys.stdout.write(f"Chunk {i+1}\\n")
    sys.stdout.flush()
    time.sleep(0.2)
'''],
                              stdout=subprocess.PIPE,
                              text=True)

    while True:
        chunk = process.stdout.read(10)  # Read in small chunks
        if not chunk and process.poll() is not None:
            break
        if chunk:
            print(f"  Chunk: {chunk.strip()}")


def error_handling_in_pipes():
    """Demonstrate error handling in pipe operations"""
    print("\n=== Error Handling in Pipes ===")

    # Handle broken pipes
    print("Testing broken pipe handling:")
    process = subprocess.Popen(['yes'], stdout=subprocess.PIPE, text=True)

    try:
        # Read a few lines then close the pipe
        for i in range(3):
            line = process.stdout.readline()
            print(f"  Read: {line.strip()}")

        # Close the pipe early (simulates broken pipe)
        process.stdout.close()

        # Try to read more (should handle gracefully)
        try:
            line = process.stdout.readline()
            if line:
                print(f"  Unexpected read: {line.strip()}")
        except:
            print("  Pipe closed as expected")

    except Exception as e:
        print(f"  Error: {e}")
    finally:
        # Clean up
        if process.poll() is None:
            process.terminate()
            process.wait()

    # Handle subprocess errors
    print("\nTesting subprocess error handling:")
    try:
        result = subprocess.run(['false'], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"  Subprocess error: return code {e.returncode}")
        if e.stderr:
            print(f"  Error output: {e.stderr.strip()}")

    # Handle timeouts
    print("\nTesting timeout handling:")
    try:
        result = subprocess.run(['sleep', '5'], timeout=2, capture_output=True, text=True)
    except subprocess.TimeoutExpired as e:
        print(f"  Timeout: {e.timeout} seconds exceeded")
        print(f"  Command: {' '.join(e.cmd)}")


def advanced_pipeline_patterns():
    """Demonstrate advanced pipeline patterns"""
    print("\n=== Advanced Pipeline Patterns ===")

    # Pipeline with error handling
    def safe_pipeline(commands):
        """Execute a pipeline with error handling"""
        processes = []
        prev_stdout = None

        try:
            for i, cmd in enumerate(commands):
                stdin = prev_stdout
                stdout = subprocess.PIPE if i < len(commands) - 1 else None

                process = subprocess.Popen(cmd, stdin=stdin, stdout=stdout,
                                         stderr=subprocess.PIPE, text=True)
                processes.append(process)
                prev_stdout = process.stdout

            # Close the first stdout to allow SIGPIPE
            if processes:
                processes[0].stdout.close()

            # Wait for all processes
            results = []
            for process in processes:
                stdout, stderr = process.communicate()
                results.append({
                    'returncode': process.returncode,
                    'stdout': stdout,
                    'stderr': stderr
                })

            return results

        except Exception as e:
            # Clean up on error
            for process in processes:
                if process.poll() is None:
                    process.terminate()
            raise

    # Test the pipeline
    if platform.system() != 'Windows':
        pipeline_commands = [
            ['echo', 'hello world'],
            ['tr', 'a-z', 'A-Z'],
            ['rev']
        ]

        try:
            results = safe_pipeline(pipeline_commands)
            for i, result in enumerate(results):
                print(f"  Stage {i+1}: return code {result['returncode']}")
                if result['stdout']:
                    print(f"    Output: {result['stdout'].strip()}")
                if result['stderr']:
                    print(f"    Errors: {result['stderr'].strip()}")

        except Exception as e:
            print(f"  Pipeline error: {e}")


def memory_efficient_streaming():
    """Demonstrate memory-efficient streaming with pipes"""
    print("\n=== Memory-Efficient Streaming ===")

    # Generate a large amount of output
    process = subprocess.Popen(['python3', '-c', '''
import sys
# Generate 1000 lines
for i in range(1000):
    print(f"Line {i+1:04d}: {'x' * 50}")
'''],
                              stdout=subprocess.PIPE,
                              text=True)

    print("Streaming output (first 10 lines):")
    line_count = 0
    chunk_size = 0

    while line_count < 10:
        line = process.stdout.readline()
        if not line and process.poll() is not None:
            break

        if line:
            line_count += 1
            chunk_size += len(line)
            print(f"  {line.strip()}")

    # Skip remaining lines efficiently
    remaining_data = process.stdout.read()  # Read all remaining at once
    remaining_lines = remaining_data.count('\n')

    process.wait()

    print(f"Total lines: {line_count + remaining_lines}")
    print(f"Memory used for streaming: ~{chunk_size} bytes")
    print(f"Process return code: {process.returncode}")


def main():
    """Run all pipe communication examples"""
    print("Pipe Communication Examples")
    print("=" * 40)

    examples = [
        basic_pipe_usage,
        input_providing_patterns,
        output_redirection_patterns,
        process_pipelines,
        real_time_io,
        bidirectional_communication,
        non_blocking_io,
        pipe_buffering_techniques,
        error_handling_in_pipes,
        advanced_pipeline_patterns,
        memory_efficient_streaming,
    ]

    for example in examples:
        try:
            example()
        except KeyboardInterrupt:
            print("\nInterrupted by user")
            break
        except Exception as e:
            print(f"Error in {example.__name__}: {e}")

    print("\n" + "=" * 40)
    print("All pipe communication examples completed!")


if __name__ == '__main__':
    main()
