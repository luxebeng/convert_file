#!/usr/bin/env python3
"""
Preprocessing script for nvshmemi_h_to_d_coll_defs.cuh
Generates host and device versions of the file with appropriate function bodies.
"""

import re
import sys
import os
from pathlib import Path

def process_cuda_arch_blocks(content, is_device=True):
    """
    Process __CUDA_ARCH__ blocks in the content.

    Args:
        content: Source file content
        is_device: True for device version, False for host version

    Returns:
        Processed content
    """
    # Pattern to match #ifdef __CUDA_ARCH__ blocks
    pattern = r'#ifdef __CUDA_ARCH__\s*\n(.*?)#endif'

    def replace_block(match):
        cuda_block = match.group(1)
        if is_device:
            # For device version, keep the CUDA_ARCH block content
            return cuda_block
        else:
            # For host version, replace with empty body
            return "\n"

    # Replace all __CUDA_ARCH__ blocks
    processed_content = re.sub(pattern, replace_block, content, flags=re.DOTALL)

    return processed_content

def generate_host_version(input_file, output_file):
    """Generate host version with empty function bodies."""
    with open(input_file, 'r') as f:
        content = f.read()

    # Process __CUDA_ARCH__ blocks for host version
    processed_content = process_cuda_arch_blocks(content, is_device=False)

    with open(output_file, 'w') as f:
        f.write(processed_content)

    print(f"Generated host version: {output_file}")

def generate_device_version(input_file, output_file):
    """Generate device version with full function bodies."""
    with open(input_file, 'r') as f:
        content = f.read()

    # Process __CUDA_ARCH__ blocks for device version
    processed_content = process_cuda_arch_blocks(content, is_device=True)

    with open(output_file, 'w') as f:
        f.write(processed_content)

    print(f"Generated device version: {output_file}")

def main():
    """Main function to process the file."""
    if len(sys.argv) != 2:
        print("Usage: python preprocess_coll_defs.py <input_file>")
        print("Example: python preprocess_coll_defs.py src/include/internal/non_abi/nvshmemi_h_to_d_coll_defs.cuh")
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} does not exist")
        sys.exit(1)

    # Generate output file paths
    input_path = Path(input_file)
    base_name = input_path.stem
    output_dir = input_path.parent

    host_output = output_dir / f"{base_name}_host.cuh"
    device_output = output_dir / f"{base_name}_device.cuh"

    print(f"Processing {input_file}...")
    print(f"Generating host version: {host_output}")
    print(f"Generating device version: {device_output}")

    # Generate both versions
    generate_host_version(input_file, host_output)
    generate_device_version(input_file, device_output)

    print("Preprocessing completed successfully!")

if __name__ == "__main__":
    main()
