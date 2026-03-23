#!/usr/bin/env python3
"""
mir_to_json.py - Convert Rust MIR dump files to JSON

Usage: python3 mir_to_json.py /path/to/mir_dump
"""

import os
import sys
import glob
import json
import re
from pathlib import Path

# Regex to extract function name from filename.
re_fname = re.compile(r"\w*\.(.*)\.[0-9-]+\.[A-Za-z\.\-]+\.mir");

def extract_funcname(filename):
    """Extract function name from MIR filename"""
    base = os.path.basename(filename)
    name = re_fname.match(base)
    return name.group(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 mir_to_json.py <mir_folder>")
        sys.exit(1)

    mir_dir = sys.argv[1]

    if not os.path.exists(mir_dir):
        print(f"Error: Directory '{mir_dir}' does not exist")
        sys.exit(1)

    # Generate JSON files at different stages of the optimisation pipeline.
    mir_to_json(mir_dir, "built")
    mir_to_json(mir_dir, "runtime-optimized")

def mir_to_json(mir_dir, opt):

    # Find all MIR files at the given opt stage
    pattern = os.path.join(mir_dir, "**", f"*.{opt}.after.mir")
    mir_files = glob.glob(pattern, recursive=True)

    if not mir_files:
        print(f"No files found for opt stage {opt}")
        return

    mir_data = {}

    for filepath in mir_files:
        funcname = extract_funcname(filepath)

        # Read MIR content as raw text
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        mir_data[funcname] = content

    # Write the JSON file.
    fout = f"{mir_dir}/{opt}.json"
    with open(fout, 'w', encoding='utf-8') as f:
        json.dump(mir_data, f, indent=2, ensure_ascii=False)

    print(f"Json written to {fout}")

if __name__ == "__main__":
    main()
