#!/usr/bin/env python
# run_tests.py

import os
import sys
import argparse
import subprocess
from datetime import datetime

def run_tests(test_files=None, verbose=False, coverage=False):
    """
    Run all tests or specific test files.
    
    Args:
        test_files (list): List of test files to run. If None, run all tests.
        verbose (bool): Whether to run tests in verbose mode.
        coverage (bool): Whether to generate coverage report.
    """
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tests_dir = os.path.join(script_dir, "tests")
    
    # If no test files specified, run all tests
    if not test_files:
        test_files = [f for f in os.listdir(tests_dir) if f.startswith("test_") and f.endswith(".py")]
    
    # Build the pytest command
    cmd = ["pytest"]
    
    # Add verbose flag if requested
    if verbose:
        cmd.append("-v")
    
    # Add coverage if requested
    if coverage:
        cmd.extend(["--cov=cosmicembeddings", "--cov-report=term-missing"])
    
    # Add test files
    for test_file in test_files:
        cmd.append(os.path.join(tests_dir, test_file))
    
    # Print the command
    print(f"Running: {' '.join(cmd)}")
    
    # Run the tests
    start_time = datetime.now()
    result = subprocess.run(cmd)
    end_time = datetime.now()
    
    # Print summary
    duration = (end_time - start_time).total_seconds()
    print(f"\nTests completed in {duration:.2f} seconds")
    
    return result.returncode

def main():
    parser = argparse.ArgumentParser(description="Run CosmicEmbeddings SDK tests")
    parser.add_argument("--test", "-t", action="append", help="Specific test file to run (can be specified multiple times)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Run tests in verbose mode")
    parser.add_argument("--coverage", "-c", action="store_true", help="Generate coverage report")
    
    args = parser.parse_args()
    
    # Run the tests
    return run_tests(args.test, args.verbose, args.coverage)

if __name__ == "__main__":
    sys.exit(main()) 