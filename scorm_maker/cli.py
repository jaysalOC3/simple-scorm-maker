#!/usr/bin/env python3
"""
Command-line interface for SCORM-Maker.

This module handles command-line arguments and serves as the entry point
for the SCORM-Maker tool.
"""

import argparse
import os
import sys
from pathlib import Path

from . import __version__
from .config import load_config
from .content_processor import process_content
from .scorm_generator import generate_scorm_package


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="SCORM-Maker: Generate SCORM-compliant e-learning packages"
    )
    
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to the directory containing content files"
    )
    
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Path to the output directory for the SCORM package"
    )
    
    parser.add_argument(
        "--config", "-c",
        default="scorm_config.yaml",
        help="Path to the configuration file (default: scorm_config.yaml)"
    )
    
    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"SCORM-Maker {__version__}"
    )
    
    return parser.parse_args()


def main():
    """Main entry point for the SCORM-Maker CLI."""
    args = parse_args()
    
    # Validate input directory
    input_dir = Path(args.input)
    if not input_dir.exists() or not input_dir.is_dir():
        print(f"Error: Input directory '{args.input}' does not exist or is not a directory")
        sys.exit(1)
    
    # Validate output directory
    output_dir = Path(args.output)
    if output_dir.exists() and not output_dir.is_dir():
        print(f"Error: Output path '{args.output}' exists but is not a directory")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Validate config file
    config_file = Path(args.config)
    if not config_file.exists() or not config_file.is_file():
        print(f"Error: Configuration file '{args.config}' does not exist or is not a file")
        sys.exit(1)
    
    try:
        # Load configuration
        config = load_config(config_file)
        
        # Process content
        processed_content = process_content(input_dir, config)
        
        # Generate SCORM package
        package_path = generate_scorm_package(
            processed_content,
            output_dir,
            config
        )
        
        print(f"SCORM package successfully generated at: {package_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
