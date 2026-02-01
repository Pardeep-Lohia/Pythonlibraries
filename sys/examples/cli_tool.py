#!/usr/bin/env python3
"""
CLI Tool Example

A practical command-line interface tool that demonstrates real-world usage
of the sys module for argument parsing, input/output handling, and system
interaction.
"""

import sys
import os
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional


class FileProcessor:
    """A command-line file processing tool using sys module extensively"""

    def __init__(self):
        self.script_name = sys.argv[0]
        self.args = sys.argv[1:]

    def parse_arguments(self) -> Dict[str, Any]:
        """Parse command line arguments using sys.argv"""
        if len(self.args) == 0:
            self.show_help()
            sys.exit(0)

        config = {
            'command': None,
            'input_files': [],
            'output_file': None,
            'options': {}
        }

        # Simple argument parsing without external libraries
        i = 0
        while i < len(self.args):
            arg = self.args[i]

            if arg in ['-h', '--help']:
                self.show_help()
                sys.exit(0)
            elif arg in ['-v', '--version']:
                self.show_version()
                sys.exit(0)
            elif arg == '--verbose':
                config['options']['verbose'] = True
            elif arg == '--quiet':
                config['options']['quiet'] = True
            elif arg.startswith('--output='):
                config['output_file'] = arg.split('=', 1)[1]
            elif arg == '-o' and i + 1 < len(self.args):
                config['output_file'] = self.args[i + 1]
                i += 1
            elif arg.startswith('--format='):
                config['options']['format'] = arg.split('=', 1)[1]
            elif arg.startswith('-'):
                self.error(f"Unknown option: {arg}")
            elif config['command'] is None:
                config['command'] = arg
            else:
                config['input_files'].append(arg)

            i += 1

        if config['command'] is None:
            self.error("No command specified")

        return config

    def show_help(self):
        """Display help information"""
        help_text = f"""
{self.script_name} - File Processing CLI Tool

USAGE:
    {self.script_name} <command> [options] [files...]

COMMANDS:
    count       Count lines, words, and characters in files
    merge       Merge multiple files into one
    split       Split a file into multiple parts
    analyze     Analyze file contents and statistics
    convert     Convert file formats (txt to json, etc.)

OPTIONS:
    -h, --help          Show this help message
    -v, --version       Show version information
    -o <file>           Output file
    --output=<file>     Output file (alternative syntax)
    --verbose           Verbose output
    --quiet             Suppress output
    --format=<fmt>      Output format (json, text)

EXAMPLES:
    {self.script_name} count file1.txt file2.txt
    {self.script_name} merge file1.txt file2.txt -o combined.txt
    {self.script_name} analyze --verbose large_file.txt
    {self.script_name} convert data.txt --format=json -o data.json

VERSION: 1.0.0
Python: {sys.version.split()[0]}
Platform: {sys.platform}
"""
        sys.stdout.write(help_text)

    def show_version(self):
        """Show version and system information"""
        version_info = f"""
File Processor CLI Tool v1.0.0

Python Version: {sys.version}
Platform: {sys.platform}
Executable: {sys.executable}
"""
        sys.stdout.write(version_info)

    def error(self, message: str, exit_code: int = 1):
        """Display error message and exit"""
        sys.stderr.write(f"Error: {message}\n")
        sys.stderr.write(f"Use '{self.script_name} --help' for usage information.\n")
        sys.exit(exit_code)

    def validate_files(self, files: List[str]) -> List[Path]:
        """Validate that input files exist and are readable"""
        valid_files = []
        for file_path in files:
            path = Path(file_path)
            if not path.exists():
                self.error(f"File not found: {file_path}")
            if not path.is_file():
                self.error(f"Not a regular file: {file_path}")
            if not os.access(path, os.R_OK):
                self.error(f"File not readable: {file_path}")
            valid_files.append(path)
        return valid_files

    def count_command(self, config: Dict[str, Any]):
        """Count lines, words, and characters in files"""
        files = self.validate_files(config['input_files'])
        verbose = config['options'].get('verbose', False)
        quiet = config['options'].get('quiet', False)

        total_stats = {'lines': 0, 'words': 0, 'chars': 0, 'files': 0}

        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                lines = len(content.splitlines())
                words = len(content.split())
                chars = len(content)

                if not quiet:
                    if verbose:
                        sys.stdout.write(f"{file_path}:\n")
                        sys.stdout.write(f"  Lines: {lines}\n")
                        sys.stdout.write(f"  Words: {words}\n")
                        sys.stdout.write(f"  Characters: {chars}\n")
                        sys.stdout.write(f"  Size: {file_path.stat().st_size} bytes\n")
                    else:
                        sys.stdout.write(f"{lines:8} {words:8} {chars:8} {file_path}\n")

                total_stats['lines'] += lines
                total_stats['words'] += words
                total_stats['chars'] += chars
                total_stats['files'] += 1

            except Exception as e:
                sys.stderr.write(f"Error processing {file_path}: {e}\n")

        if len(files) > 1 and not quiet:
            if verbose:
                sys.stdout.write("TOTALS:\n")
                sys.stdout.write(f"  Files: {total_stats['files']}\n")
                sys.stdout.write(f"  Lines: {total_stats['lines']}\n")
                sys.stdout.write(f"  Words: {total_stats['words']}\n")
                sys.stdout.write(f"  Characters: {total_stats['chars']}\n")
            else:
                sys.stdout.write(f"{total_stats['lines']:8} {total_stats['words']:8} {total_stats['chars']:8} total\n")

    def merge_command(self, config: Dict[str, Any]):
        """Merge multiple files into one output file"""
        files = self.validate_files(config['input_files'])
        output_file = config['output_file']
        verbose = config['options'].get('verbose', False)

        if not output_file:
            self.error("Output file required for merge command (use -o option)")

        try:
            with open(output_file, 'w', encoding='utf-8') as outfile:
                for file_path in files:
                    if verbose:
                        sys.stdout.write(f"Merging {file_path}...\n")

                    with open(file_path, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                        outfile.write(content)
                        outfile.write('\n')  # Add separator between files

            if not config['options'].get('quiet', False):
                sys.stdout.write(f"Successfully merged {len(files)} files into {output_file}\n")

        except Exception as e:
            self.error(f"Error during merge: {e}")

    def analyze_command(self, config: Dict[str, Any]):
        """Analyze file contents and provide statistics"""
        files = self.validate_files(config['input_files'])
        verbose = config['options'].get('verbose', False)
        output_format = config['options'].get('format', 'text')

        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Basic statistics
                stats = {
                    'filename': str(file_path),
                    'size_bytes': file_path.stat().st_size,
                    'lines': len(content.splitlines()),
                    'words': len(content.split()),
                    'characters': len(content),
                    'characters_no_spaces': len(content.replace(' ', '').replace('\n', '').replace('\t', '')),
                }

                # Content analysis
                lines = content.splitlines()
                if lines:
                    stats['avg_line_length'] = sum(len(line) for line in lines) / len(lines)
                    stats['max_line_length'] = max(len(line) for line in lines)
                    stats['min_line_length'] = min(len(line) for line in lines)
                    stats['empty_lines'] = sum(1 for line in lines if not line.strip())

                # Character frequency (basic)
                char_freq = {}
                for char in content:
                    char_freq[char] = char_freq.get(char, 0) + 1
                stats['unique_characters'] = len(char_freq)
                stats['most_common_char'] = max(char_freq.items(), key=lambda x: x[1]) if char_freq else None

                # Output based on format
                if output_format == 'json':
                    json_output = json.dumps(stats, indent=2, default=str)
                    if config['output_file']:
                        with open(config['output_file'], 'w') as f:
                            f.write(json_output)
                    else:
                        sys.stdout.write(json_output)
                else:
                    # Text format
                    if verbose:
                        sys.stdout.write(f"Analysis of {file_path}:\n")
                        sys.stdout.write("-" * 40 + "\n")
                        for key, value in stats.items():
                            sys.stdout.write(f"{key}: {value}\n")
                        sys.stdout.write("\n")
                    else:
                        sys.stdout.write(f"{file_path}: {stats['lines']} lines, {stats['words']} words, {stats['size_bytes']} bytes\n")

            except Exception as e:
                sys.stderr.write(f"Error analyzing {file_path}: {e}\n")

    def convert_command(self, config: Dict[str, Any]):
        """Convert file formats"""
        files = self.validate_files(config['input_files'])
        output_format = config['options'].get('format', 'json')
        output_file = config['output_file']

        if not output_file and len(files) > 1:
            self.error("Output file required when converting multiple files")

        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Simple conversion: text to JSON
                if output_format == 'json':
                    lines = content.splitlines()
                    data = {
                        'filename': str(file_path),
                        'content': lines,
                        'metadata': {
                            'lines': len(lines),
                            'total_chars': len(content)
                        }
                    }

                    json_content = json.dumps(data, indent=2)

                    out_path = output_file or str(file_path.with_suffix('.json'))
                    with open(out_path, 'w', encoding='utf-8') as f:
                        f.write(json_content)

                    if not config['options'].get('quiet', False):
                        sys.stdout.write(f"Converted {file_path} to {out_path}\n")

                else:
                    self.error(f"Unsupported output format: {output_format}")

            except Exception as e:
                sys.stderr.write(f"Error converting {file_path}: {e}\n")

    def run(self):
        """Main execution method"""
        try:
            config = self.parse_arguments()
            command = config['command']

            # Route to appropriate command handler
            if command == 'count':
                self.count_command(config)
            elif command == 'merge':
                self.merge_command(config)
            elif command == 'analyze':
                self.analyze_command(config)
            elif command == 'convert':
                self.convert_command(config)
            else:
                self.error(f"Unknown command: {command}")

        except KeyboardInterrupt:
            sys.stderr.write("\nOperation cancelled by user.\n")
            sys.exit(130)
        except Exception as e:
            sys.stderr.write(f"Unexpected error: {e}\n")
            if config.get('options', {}).get('verbose'):
                import traceback
                traceback.print_exc()
            sys.exit(1)


def main():
    """Entry point"""
    tool = FileProcessor()
    tool.run()


if __name__ == "__main__":
    main()
