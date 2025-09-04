# Simple EPUB to PDF Converter

A straightforward Python script for converting EPUB files to PDF format using `ebooklib` and `reportlab`. This approach provides reliable conversion of all pages and is inspired by the [epub_to_pdf_Converter](https://github.com/AlenSarangSatheesh/epub_to_pdf_Converter) repository.

## Why This Approach?

Unlike complex conversion tools that may only convert single pages or require extensive setup, this method:

- ✅ **Processes ALL pages** - Converts the entire EPUB content
- ✅ **Simple dependencies** - Only requires `ebooklib` and `reportlab`
- ✅ **Reliable** - Handles standard EPUB files consistently
- ✅ **Lightweight** - No complex external tools required
- ✅ **Text-based** - Extracts and converts text content properly

## Installation

```bash
# Install the required dependencies
pip install -r requirements.txt

# Or install manually:
pip install ebooklib reportlab Pillow pikepdf
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

## Features

- **Automatic text extraction** from EPUB HTML content
- **Proper formatting** with title, author, and chapter breaks
- **Page breaks** between sections
- **File size and page count** reporting
- **Error handling** for problematic content
- **HTML tag stripping** for clean text output

## How It Works

1. **Reads EPUB file** using `ebooklib`
2. **Extracts text content** from each document section
3. **Strips HTML tags** to get clean text
4. **Creates PDF** using `reportlab` with proper formatting
5. **Adds page breaks** between chapters/sections
6. **Reports statistics** about the conversion

## Example Output

```
Converting book.epub to book.pdf...
📖 Reading EPUB file...
Processing: chapter1.xhtml
Processing: chapter2.xhtml
📄 Building PDF...
✅ Conversion successful!
📄 Output: book.pdf
📊 File size: 245,760 bytes (0.23 MB)
📖 Processed 15 sections
📑 PDF pages: 42
```

## Supported File Formats

- **EPUB** (Electronic Publication) - Primary focus
- **DRM-free files only**

## Requirements

- Python 3.6 or higher
- Core dependencies:
  - `ebooklib` - EPUB file processing
  - `reportlab` - PDF generation
  - `Pillow` - Image handling
  - `pikepdf` - PDF analysis (optional)

## Troubleshooting

### Missing Dependencies
```bash
❌ Missing dependencies: ebooklib, reportlab
Install with: pip install ebooklib reportlab
```

### No Content Found
- Ensure the EPUB file is not corrupted
- Some DRM-protected files may not be readable
- Try with a different EPUB file

### Formatting Issues
- The converter extracts plain text, so complex formatting is simplified
- Images are not currently supported
- For complex layouts, consider using Calibre as an alternative

## Credits

Based on the approach from [AlenSarangSatheesh/epub_to_pdf_Converter](https://github.com/AlenSarangSatheesh/epub_to_pdf_Converter/blob/main/Converter.py).
