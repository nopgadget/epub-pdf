# EPUB to PDF Converter

A Python script for converting EPUB files to PDF format while preserving images, formatting, and text sizes. This tool creates professional-quality, AI-readable PDFs and is inspired by the [epub_to_pdf_Converter](https://github.com/AlenSarangSatheesh/epub_to_pdf_Converter) repository.

## Features

- ✅ **Preserves ALL content** - Converts the entire EPUB with all pages
- ✅ **Maintains formatting** - Keeps original text sizes, fonts, and layout
- ✅ **Embeds images** - Automatically includes images from EPUB files
- ✅ **AI-readable output** - Creates searchable PDFs that work with AI tools
- ✅ **Professional quality** - Uses HTML/CSS rendering for high-quality output

## Installation

```bash
# Install the required dependencies
pip install -r requirements.txt

# Or install manually:
pip install ebooklib reportlab Pillow beautifulsoup4 weasyprint pikepdf
```

## Usage

### Basic Usage

```bash
# Convert EPUB to PDF (output will be same name with .pdf extension)
python main.py book.epub

# Specify output file
python main.py book.epub -o my_book.pdf

# Verbose output to see processing details
python main.py book.epub -v
```

### Check Dependencies

```bash
python main.py --check-deps
```

## How It Works

1. **Reads EPUB file** using `ebooklib`
2. **Extracts images** and saves them temporarily
3. **Processes HTML content** preserving original formatting
4. **Converts to PDF** using `weasyprint` for professional quality
5. **Embeds images** and maintains CSS styling
6. **Reports statistics** including page count and file size

## Example Output

```
Converting book.epub to book.pdf...
📖 Reading EPUB file...
📁 Using temp directory: /tmp/tmp4ny3606r
Processing: chapter1.xhtml
Processing: chapter2.xhtml
📄 Converting HTML to PDF...
✅ Conversion successful!
📄 Output: book.pdf
📊 File size: 1,403,164 bytes (1.34 MB)
📷 Images preserved: 5
📑 PDF pages: 385
```

## Supported File Formats

- **EPUB** (Electronic Publication) - Primary focus
- **DRM-free files only**

## Requirements

- Python 3.6 or higher
- Core dependencies:
  - `ebooklib` - EPUB file processing
  - `weasyprint` - HTML to PDF conversion
  - `beautifulsoup4` - HTML parsing
  - `Pillow` - Image handling
  - `pikepdf` - PDF analysis (optional)

## Troubleshooting

### Missing Dependencies
```bash
❌ Conversion failed - missing dependencies: No module named 'weasyprint'
Please install missing dependencies with:
pip install beautifulsoup4 weasyprint
```

### No Content Found
- Ensure the EPUB file is not corrupted
- Some DRM-protected files may not be readable
- Try with a different EPUB file

### Large File Sizes
- The converter preserves formatting and images, resulting in larger PDFs
- This is normal and indicates quality preservation
- Use compression tools if smaller files are needed

## Credits

Based on the approach from [AlenSarangSatheesh/epub_to_pdf_Converter](https://github.com/AlenSarangSatheesh/epub_to_pdf_Converter/blob/main/Converter.py).
