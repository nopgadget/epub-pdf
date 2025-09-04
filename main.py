#!/usr/bin/env python3
"""
EPUB to PDF Converter
A Python program that converts EPUB, MOBI, and AZW3 files to PDF format.
Based on the epub2pdf library for fixed-layout manga/comic conversion.
"""

import argparse
import os
import sys
from pathlib import Path
import subprocess

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import epub2pdf
        return True
    except ImportError:
        print("Error: epub2pdf package is not installed.")
        print("Please install it using one of the following methods:")
        print("1. pip install epub2pdf")
        print("2. pip install git+https://github.com/mashu3/epub2pdf.git")
        return False

def validate_input_file(input_path):
    """Validate that the input file exists and has a supported format."""
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    supported_formats = ['.epub', '.mobi', '.azw', '.azw3']
    file_extension = Path(input_path).suffix.lower()
    
    if file_extension not in supported_formats:
        raise ValueError(f"Unsupported file format: {file_extension}. Supported formats: {', '.join(supported_formats)}")
    
    return True

def generate_output_path(input_path, output_path=None):
    """Generate output path if not provided."""
    if output_path:
        return output_path
    
    input_file = Path(input_path)
    return str(input_file.with_suffix('.pdf'))

def convert_epub_to_pdf(input_path, output_path=None, page_layout="TwoPageRight", direction="R2L"):
    """
    Convert EPUB/MOBI/AZW file to PDF.
    
    Args:
        input_path (str): Path to the input file
        output_path (str, optional): Path to the output PDF file
        page_layout (str): Page layout option
        direction (str): Reading direction
    """
    try:
        # Validate input
        validate_input_file(input_path)
        
        # Generate output path if not provided
        if not output_path:
            output_path = generate_output_path(input_path)
        
        # Construct the command
        cmd = [
            'python', '-m', 'epub2pdf',
            input_path,
            '-o', output_path,
            '-l', page_layout,
            '-d', direction
        ]
        
        print(f"Converting {input_path} to {output_path}...")
        print(f"Page layout: {page_layout}")
        print(f"Reading direction: {direction}")
        
        # Execute the conversion
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Conversion successful! Output saved to: {output_path}")
        else:
            print(f"❌ Conversion failed!")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error during conversion: {str(e)}")
        return False
    
    return True

def main():
    """Main function to handle command-line interface."""
    parser = argparse.ArgumentParser(
        description="Convert EPUB, MOBI, and AZW3 files to PDF format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py my_manga.epub
  python main.py my_manga.epub -o output.pdf
  python main.py my_comic.epub -l TwoPageLeft -d L2R
  python main.py my_manga.mobi -l SinglePage -d R2L

Page Layout Options:
  SinglePage     - Single page display
  OneColumn      - Enable scrolling
  TwoPageLeft    - Spread view
  TwoColumnLeft  - Spread view with scrolling
  TwoPageRight   - Separate Cover, Spread View (default)
  TwoColumnRight - Separate Cover, Scrolling Spread View

Reading Direction Options:
  L2R - Left Binding
  R2L - Right Binding (default)
        """
    )
    
    parser.add_argument(
        'input_path',
        help='Path to the input EPUB, MOBI, or AZW3 file'
    )
    
    parser.add_argument(
        '-o', '--output',
        dest='output_path',
        help='Path to the output PDF file (optional)'
    )
    
    parser.add_argument(
        '-l', '--page-layout',
        dest='page_layout',
        choices=['SinglePage', 'OneColumn', 'TwoPageLeft', 'TwoColumnLeft', 'TwoPageRight', 'TwoColumnRight'],
        default='TwoPageRight',
        help='Page layout of the PDF file (default: TwoPageRight)'
    )
    
    parser.add_argument(
        '-d', '--direction',
        dest='direction',
        choices=['L2R', 'R2L'],
        default='R2L',
        help='Reading direction of the PDF file (default: R2L)'
    )
    
    parser.add_argument(
        '--check-deps',
        action='store_true',
        help='Check if required dependencies are installed'
    )
    
    args = parser.parse_args()
    
    # Check dependencies if requested
    if args.check_deps:
        if check_dependencies():
            print("✅ All dependencies are installed!")
        else:
            sys.exit(1)
        return
    
    # Check dependencies before conversion
    if not check_dependencies():
        sys.exit(1)
    
    # Perform conversion
    success = convert_epub_to_pdf(
        args.input_path,
        args.output_path,
        args.page_layout,
        args.direction
    )
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
