#!/usr/bin/env python3
"""
Command Line Arguments Implementation

This module demonstrates various ways to handle command-line arguments
using sys.argv, including parsing, validation, and common patterns.
"""

import sys
import os
from typing import List, Optional, Callable, Any


class ArgumentParser:
    """Simple command-line argument parser using sys.argv"""

    def __init__(self):
        self.script_name = sys.argv[0]
        self.args = sys.argv[1:]

    def get_positional(self, index: int, default=None) -> Optional[str]:
        """Get positional argument by index"""
        if 0 <= index < len(self.args):
            return self.args[index]
        return default

    def has_flag(self, flag: str) -> bool:
        """Check if a flag is present"""
        return flag in self.args

    def get_flag_value(self, flag: str, default=None) -> Optional[str]:
        """Get value for a flag (e.g., --flag value)"""
        try:
            idx = self.args.index(flag)
            if idx + 1 < len(self.args):
                return self.args[idx + 1]
        except ValueError:
            pass
        return default

    def get_all_positional(self) -> List[str]:
        """Get all positional arguments (excluding flags starting with -)"""
        return [arg for arg in self.args if not arg.startswith('-')]

    def get_flags_and_values(self) -> dict:
        """Parse flags and their values into a dictionary"""
        result = {}
        i = 0
        while i < len(self.args):
            arg = self.args[i]
            if arg.startswith('--'):
                # Long flag
                flag_name = arg[2:]
                if i + 1 < len(self.args) and not self.args[i + 1].startswith('-'):
                    result[flag_name] = self.args[i + 1]
                    i += 2
                else:
                    result[flag_name] = True
                    i += 1
            elif arg.startswith('-') and len(arg) > 1:
                # Short flag
                flag_name = arg[1:]
                if i + 1 < len(self.args) and not self.args[i + 1].startswith('-'):
                    result[flag_name] = self.args[i + 1]
                    i += 2
                else:
                    result[flag_name] = True
                    i += 1
            else:
                # Positional argument
                i += 1
        return result


def simple_cli_example():
    """Simple command-line interface example"""
    print("Simple CLI Tool")
    print("=" * 15)

    if len(sys.argv) < 2:
        print("Usage: python argv_handling.py <command> [args...]")
        print("Commands: greet, calc, info")
        return

    command = sys.argv[1].lower()

    if command == 'greet':
        # Get name from arguments
        name = sys.argv[2] if len(sys.argv) > 2 else "World"
        print(f"Hello, {name}!")

    elif command == 'calc':
        # Simple calculator
        if len(sys.argv) < 5:
            print("Usage: python argv_handling.py calc <num1> <op> <num2>")
            return

        try:
            num1 = float(sys.argv[2])
            op = sys.argv[3]
            num2 = float(sys.argv[4])

            if op == '+':
                result = num1 + num2
            elif op == '-':
                result = num1 - num2
            elif op == '*':
                result = num1 * num2
            elif op == '/':
                if num2 == 0:
                    print("Error: Division by zero")
                    return
                result = num1 / num2
            else:
                print(f"Unknown operator: {op}")
                return

            print(f"{num1} {op} {num2} = {result}")

        except ValueError:
            print("Error: Invalid numbers")

    elif command == 'info':
        # Show script information
        print(f"Script: {sys.argv[0]}")
        print(f"Arguments: {len(sys.argv) - 1}")
        print("All arguments:")
        for i, arg in enumerate(sys.argv[1:], 1):
            print(f"  {i}: {arg}")

    else:
        print(f"Unknown command: {command}")


def advanced_parsing_example():
    """Advanced argument parsing example"""
    print("Advanced Argument Parsing")
    print("=" * 26)

    parser = ArgumentParser()

    # Example: file processor
    input_file = parser.get_positional(0)
    output_file = parser.get_positional(1)

    if not input_file:
        print("Error: Input file required")
        print("Usage: python argv_handling.py <input_file> [output_file] [--verbose] [--encoding utf8]")
        return

    # Check flags
    verbose = parser.has_flag('--verbose') or parser.has_flag('-v')
    encoding = parser.get_flag_value('--encoding') or 'utf-8'

    if verbose:
        print(f"Input file: {input_file}")
        print(f"Output file: {output_file or 'stdout'}")
        print(f"Encoding: {encoding}")

    # Simulate file processing
    try:
        with open(input_file, 'r', encoding=encoding) as f:
            content = f.read()

        if verbose:
            print(f"Read {len(content)} characters")

        if output_file:
            with open(output_file, 'w', encoding=encoding) as f:
                f.write(content.upper())
            print(f"Processed content written to {output_file}")
        else:
            print(content.upper())

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
    except Exception as e:
        print(f"Error: {e}")


def flag_parsing_example():
    """Example of parsing various flag formats"""
    print("Flag Parsing Examples")
    print("=" * 21)

    parser = ArgumentParser()

    print("Arguments:", parser.args)
    print()

    # Check different flag formats
    flags_to_check = ['-v', '--verbose', '-h', '--help', '-o', '--output']
    for flag in flags_to_check:
        present = parser.has_flag(flag)
        print(f"Flag {flag}: {'present' if present else 'not present'}")

    print()

    # Get flag values
    values_to_get = ['-o', '--output', '-e', '--encoding', '-c', '--count']
    for flag in values_to_get:
        value = parser.get_flag_value(flag, 'not set')
        print(f"Flag {flag}: {value}")

    print()

    # Get all flags and values
    all_flags = parser.get_flags_and_values()
    print("All flags and values:")
    for flag, value in all_flags.items():
        print(f"  {flag}: {value}")


def validation_example():
    """Example of argument validation"""
    print("Argument Validation")
    print("=" * 19)

    def validate_file_exists(filepath: str) -> bool:
        """Validate that a file exists"""
        if not os.path.exists(filepath):
            print(f"Error: File '{filepath}' does not exist")
            return False
        return True

    def validate_positive_number(value: str) -> Optional[float]:
        """Validate and convert to positive number"""
        try:
            num = float(value)
            if num <= 0:
                print(f"Error: Number must be positive, got {num}")
                return None
            return num
        except ValueError:
            print(f"Error: '{value}' is not a valid number")
            return None

    parser = ArgumentParser()

    # Validate input file
    input_file = parser.get_positional(0)
    if not input_file:
        print("Error: Input file required")
        return

    if not validate_file_exists(input_file):
        return

    # Validate count parameter
    count_str = parser.get_flag_value('-c') or parser.get_flag_value('--count')
    if count_str:
        count = validate_positive_number(count_str)
        if count is None:
            return
    else:
        count = 1

    print(f"Processing file: {input_file}")
    print(f"Count: {count}")

    # Simulate processing
    try:
        with open(input_file, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines[:int(count)]):
                print(f"Line {i+1}: {line.strip()}")
    except Exception as e:
        print(f"Error processing file: {e}")


def safe_argument_access():
    """Demonstrate safe ways to access command line arguments"""
    print("Safe Argument Access")
    print("=" * 20)

    # Method 1: Check length first
    print("Method 1: Length checking")
    if len(sys.argv) > 1:
        first_arg = sys.argv[1]
        print(f"First argument: {first_arg}")
    else:
        print("No arguments provided")

    # Method 2: Use try-except
    print("\nMethod 2: Try-except")
    try:
        second_arg = sys.argv[2]
        print(f"Second argument: {second_arg}")
    except IndexError:
        print("No second argument provided")

    # Method 3: Default values
    print("\nMethod 3: Default values")
    third_arg = sys.argv[3] if len(sys.argv) > 3 else "default"
    print(f"Third argument: {third_arg}")

    # Method 4: Helper function
    print("\nMethod 4: Helper function")
    def safe_get_arg(index: int, default=None):
        return sys.argv[index] if index < len(sys.argv) else default

    for i in range(5):
        arg = safe_get_arg(i, f"arg{i}_default")
        print(f"Argument {i}: {arg}")


def type_conversion_example():
    """Example of converting arguments to different types"""
    print("Type Conversion Examples")
    print("=" * 24)

    def convert_arg(index: int, converter: Callable, default=None):
        """Convert argument at index using converter function"""
        if index >= len(sys.argv):
            return default
        try:
            return converter(sys.argv[index])
        except (ValueError, TypeError):
            print(f"Error converting argument {index} ('{sys.argv[index]}')")
            return default

    # Examples of different conversions
    conversions = [
        (1, int, "integer argument"),
        (2, float, "float argument"),
        (3, str, "string argument"),
        (4, lambda x: x.lower() == 'true', "boolean argument"),
    ]

    for index, converter, description in conversions:
        value = convert_arg(index, converter, "conversion_failed")
        print(f"{description}: {value} (type: {type(value).__name__})")


def main():
    """Main function demonstrating different argument handling techniques"""

    examples = {
        'simple': simple_cli_example,
        'advanced': advanced_parsing_example,
        'flags': flag_parsing_example,
        'validation': validation_example,
        'safe': safe_argument_access,
        'types': type_conversion_example,
    }

    if len(sys.argv) < 2:
        print("Command Line Arguments Examples")
        print("===============================")
        print()
        print("Available examples:")
        for name in examples.keys():
            print(f"  {name}")
        print()
        print("Usage: python argv_handling.py <example_name> [args...]")
        print("Example: python argv_handling.py simple greet Alice")
        return

    example_name = sys.argv[1].lower()

    if example_name in examples:
        try:
            examples[example_name]()
        except KeyboardInterrupt:
            print("\nExample interrupted by user")
        except Exception as e:
            print(f"\nExample failed: {e}")
            import traceback
            traceback.print_exc()
    else:
        sys.stderr.write(f"Unknown example: {example_name}\n")
        sys.stderr.write(f"Available examples: {', '.join(examples.keys())}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
