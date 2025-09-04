#!/usr/bin/env python3
"""
Simple EPUB to PDF Converter
Based on the approach from: https://github.com/AlenSarangSatheesh/epub_to_pdf_Converter

Uses ebooklib and reportlab for reliable conversion of all pages.
"""

import argparse
import os
import sys
from pathlib import Path
import io
from html.parser import HTMLParser
import base64
import tempfile

def check_dependencies():
    """Check if required dependencies are installed."""
    missing = []
    
    try:
        import ebooklib
        print("✅ ebooklib is available")
    except ImportError:
        missing.append("ebooklib")
    
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        print("✅ reportlab is available")
    except ImportError:
        missing.append("reportlab")
    
    try:
        from PIL import Image
        print("✅ Pillow is available")
    except ImportError:
        missing.append("Pillow")
    
    try:
        import weasyprint
        print("✅ WeasyPrint is available")
    except ImportError:
        print("⚠️  WeasyPrint not available - will use basic HTML parsing")
    
    try:
        from bs4 import BeautifulSoup
        print("✅ BeautifulSoup is available")
    except ImportError:
        missing.append("beautifulsoup4")
    
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print("Install with: pip install " + " ".join(missing))
        return False
    
    return True

class HTMLStripper(HTMLParser):
    """Simple HTML tag stripper to extract text content."""
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = io.StringIO()

    def handle_data(self, data):
        self.text.write(data)

    def get_data(self):
        return self.text.getvalue()

def strip_html_tags(html_content):
    """Remove HTML tags and return plain text."""
    stripper = HTMLStripper()
    stripper.feed(html_content)
    return stripper.get_data()

def validate_input_file(input_path):
    """Validate that the input file exists and is an EPUB."""
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    if not input_path.lower().endswith('.epub'):
        raise ValueError(f"File must be an EPUB file: {input_path}")
    
    return True

def generate_output_path(input_path, output_path=None):
    """Generate output path if not provided."""
    if output_path:
        return output_path
    
    input_file = Path(input_path)
    return str(input_file.with_suffix('.pdf'))

def extract_images_from_epub(book, temp_dir, verbose=False):
    """Extract images from EPUB and save to temporary directory."""
    import ebooklib
    image_map = {}
    
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_IMAGE:
            if verbose:
                print(f"Extracting image: {item.get_name()}")
            
            # Save image to temp directory
            image_path = os.path.join(temp_dir, os.path.basename(item.get_name()))
            with open(image_path, 'wb') as img_file:
                img_file.write(item.get_content())
            
            # Map the original path to the temp path
            image_map[item.get_name()] = image_path
    
    return image_map

def convert_html_to_pdf_content(html_content, image_map, temp_dir, verbose=False):
    """Convert HTML content to PDF-friendly format with images."""
    try:
        from bs4 import BeautifulSoup
        
        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Update image sources to point to extracted files
        for img in soup.find_all('img'):
            src = img.get('src')
            if src and src in image_map:
                img['src'] = image_map[src]
                if verbose:
                    print(f"Updated image src: {src} -> {image_map[src]}")
        
        return str(soup)
        
    except ImportError:
        if verbose:
            print("BeautifulSoup not available, falling back to basic parsing")
        return html_content

def convert_epub_to_pdf_enhanced(input_path, output_path=None, verbose=False):
    """
    Enhanced EPUB to PDF conversion preserving images and formatting.
    """
    try:
        import weasyprint
        import ebooklib
        from ebooklib import epub
        
        # Validate input
        validate_input_file(input_path)
        
        # Generate output path if not provided
        if not output_path:
            output_path = generate_output_path(input_path)
        
        print(f"Converting {input_path} to {output_path} (Enhanced mode)...")
        
        # Read the EPUB file
        if verbose:
            print("📖 Reading EPUB file...")
        book = epub.read_epub(input_path)
        
        # Create temporary directory for images
        with tempfile.TemporaryDirectory() as temp_dir:
            if verbose:
                print(f"📁 Using temp directory: {temp_dir}")
            
            # Extract images
            image_map = extract_images_from_epub(book, temp_dir, verbose)
            if verbose and image_map:
                print(f"📷 Extracted {len(image_map)} images")
            
            # Collect all HTML content
            html_parts = []
            
            # Add CSS for better formatting
            html_parts.append("""
            <html>
            <head>
                <style>
                    body { 
                        font-family: serif; 
                        line-height: 1.6; 
                        margin: 40px;
                        font-size: 12pt;
                    }
                    h1 { font-size: 18pt; margin-top: 30px; }
                    h2 { font-size: 16pt; margin-top: 25px; }
                    h3 { font-size: 14pt; margin-top: 20px; }
                    p { margin-bottom: 12px; text-align: justify; }
                    img { max-width: 100%; height: auto; display: block; margin: 10px auto; }
                    .page-break { page-break-before: always; }
                </style>
            </head>
            <body>
            """)
            
            # Process each document in the EPUB
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    if verbose:
                        print(f"Processing: {item.get_name()}")
                    
                    # Get content and decode
                    content = item.get_content().decode('utf-8')
                    
                    # Process HTML to update image paths
                    processed_content = convert_html_to_pdf_content(content, image_map, temp_dir, verbose)
                    
                    # Extract body content or use as-is
                    try:
                        from bs4 import BeautifulSoup
                        soup = BeautifulSoup(processed_content, 'html.parser')
                        body = soup.find('body')
                        if body:
                            # Add page break before each new section
                            html_parts.append('<div class="page-break"></div>')
                            html_parts.append(str(body))
                        else:
                            html_parts.append(processed_content)
                    except ImportError:
                        html_parts.append(processed_content)
            
            html_parts.append("</body></html>")
            
            # Combine all HTML
            full_html = '\n'.join(html_parts)
            
            # Convert to PDF using WeasyPrint
            if verbose:
                print("📄 Converting HTML to PDF...")
            
            weasyprint.HTML(string=full_html, base_url=temp_dir).write_pdf(output_path)
            
            # Analyze the result
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                print(f"✅ Enhanced conversion successful!")
                print(f"📄 Output: {output_path}")
                print(f"📊 File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
                print(f"📷 Images preserved: {len(image_map)}")
                
                # Try to get actual page count
                try:
                    import pikepdf
                    pdf = pikepdf.open(output_path)
                    actual_pages = len(pdf.pages)
                    print(f"📑 PDF pages: {actual_pages}")
                    pdf.close()
                except ImportError:
                    if verbose:
                        print("ℹ️  Install pikepdf to get actual page count")
                except Exception as e:
                    if verbose:
                        print(f"⚠️  Could not analyze PDF: {str(e)}")
            
            return True
            
    except ImportError as e:
        if verbose:
            print(f"Enhanced mode not available: {str(e)}")
        print("🔄 Falling back to basic conversion...")
        return convert_epub_to_pdf_basic(input_path, output_path, verbose)
    except Exception as e:
        print(f"❌ Error during enhanced conversion: {str(e)}")
        if verbose:
            import traceback
            traceback.print_exc()
        print("🔄 Trying basic conversion...")
        return convert_epub_to_pdf_basic(input_path, output_path, verbose)

def convert_epub_to_pdf_basic(input_path, output_path=None, verbose=False):
    """
    Convert EPUB to PDF using ebooklib and reportlab.
    
    Args:
        input_path (str): Path to the input EPUB file
        output_path (str, optional): Path to the output PDF file
        verbose (bool): Enable verbose output
    """
    try:
        import ebooklib
        from ebooklib import epub
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.units import inch
        
        # Validate input
        validate_input_file(input_path)
        
        # Generate output path if not provided
        if not output_path:
            output_path = generate_output_path(input_path)
        
        print(f"Converting {input_path} to {output_path}...")
        
        # Read the EPUB file
        if verbose:
            print("📖 Reading EPUB file...")
        book = epub.read_epub(input_path)
        
        # Create PDF document
        doc = SimpleDocTemplate(output_path, pagesize=letter,
                              rightMargin=0.75*inch, leftMargin=0.75*inch,
                              topMargin=1*inch, bottomMargin=1*inch)
        
        # Get styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
        )
        normal_style = styles['Normal']
        
        # Story to hold all content
        story = []
        
        # Add title if available
        title = book.get_metadata('DC', 'title')
        if title:
            story.append(Paragraph(title[0][0], title_style))
            story.append(Spacer(1, 20))
        
        # Add author if available
        author = book.get_metadata('DC', 'creator')
        if author:
            story.append(Paragraph(f"By: {author[0][0]}", normal_style))
            story.append(Spacer(1, 20))
        
        page_count = 0
        
        # Process each item in the EPUB
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                if verbose:
                    print(f"Processing: {item.get_name()}")
                
                # Get content and decode
                content = item.get_content().decode('utf-8')
                
                # Strip HTML tags to get plain text
                text_content = strip_html_tags(content)
                
                # Clean up the text
                text_content = text_content.strip()
                
                if text_content:  # Only add non-empty content
                    # Split into paragraphs
                    paragraphs = text_content.split('\n')
                    
                    for para in paragraphs:
                        para = para.strip()
                        if para:  # Skip empty paragraphs
                            try:
                                story.append(Paragraph(para, normal_style))
                                story.append(Spacer(1, 12))
                            except Exception as e:
                                if verbose:
                                    print(f"⚠️  Skipping problematic paragraph: {str(e)}")
                                # Add as plain text if Paragraph fails
                                story.append(Spacer(1, 12))
                    
                    # Add page break between chapters/sections
                    story.append(PageBreak())
                    page_count += 1
        
        if not story or page_count == 0:
            raise Exception("No readable content found in the EPUB file")
        
        # Build the PDF
        if verbose:
            print("📄 Building PDF...")
        doc.build(story)
        
        # Analyze the result
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✅ Conversion successful!")
            print(f"📄 Output: {output_path}")
            print(f"📊 File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
            print(f"📖 Processed {page_count} sections")
            
            # Try to get actual page count if pikepdf is available
            try:
                import pikepdf
                pdf = pikepdf.open(output_path)
                actual_pages = len(pdf.pages)
                print(f"📑 PDF pages: {actual_pages}")
                pdf.close()
            except ImportError:
                if verbose:
                    print("ℹ️  Install pikepdf to get actual page count")
            except Exception as e:
                if verbose:
                    print(f"⚠️  Could not analyze PDF: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during conversion: {str(e)}")
        if verbose:
            import traceback
            traceback.print_exc()
        return False

def convert_epub_to_pdf(input_path, output_path=None, verbose=False):
    """
    Main conversion function - tries enhanced mode first, falls back to basic.
    """
    # Try enhanced conversion first (with images and formatting)
    return convert_epub_to_pdf_enhanced(input_path, output_path, verbose)

def main():
    """Main function to handle command-line interface."""
    parser = argparse.ArgumentParser(
        description="Simple EPUB to PDF converter using ebooklib and reportlab",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python simple_converter.py book.epub
  python simple_converter.py book.epub -o output.pdf
  python simple_converter.py book.epub -v

Based on: https://github.com/AlenSarangSatheesh/epub_to_pdf_Converter
        """
    )
    
    parser.add_argument(
        'input_path',
        help='Path to the input EPUB file'
    )
    
    parser.add_argument(
        '-o', '--output',
        dest='output_path',
        help='Path to the output PDF file (optional)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
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
            print("✅ All dependencies are available!")
        else:
            sys.exit(1)
        return
    
    # Check dependencies before conversion
    if not check_dependencies():
        print("\nInstall missing dependencies with:")
        print("pip install ebooklib reportlab Pillow")
        sys.exit(1)
    
    # Perform conversion
    success = convert_epub_to_pdf(
        args.input_path,
        args.output_path,
        args.verbose
    )
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
