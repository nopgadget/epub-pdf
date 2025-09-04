# EPUB to PDF Converter

A Python program that converts EPUB, MOBI, and AZW3 files to PDF format, specifically designed for fixed-layout manga and comic files.

## Features

- Convert EPUB, MOBI, and AZW3 files to PDF
- Multiple page layout options for different reading preferences
- Support for both left-to-right and right-to-left reading directions
- Command-line interface with comprehensive options
- Input validation and error handling
- Dependency checking

## Installation

### Option 1: Install dependencies directly

```bash
pip install -r requirements.txt
```

### Option 2: Install epub2pdf manually

```bash
# From PyPI
pip install epub2pdf

# Or from GitHub (latest version)
pip install git+https://github.com/mashu3/epub2pdf.git
```

## Usage

### Basic Usage

```bash
# Convert with default settings (TwoPageRight layout, R2L direction)
python main.py my_manga.epub

# Specify output file
python main.py my_manga.epub -o output.pdf
```

### Advanced Usage

```bash
# Convert with custom page layout and reading direction
python main.py my_comic.epub -l TwoPageLeft -d L2R

# Single page layout for mobile reading
python main.py my_manga.epub -l SinglePage -d R2L
```

### Check Dependencies

```bash
python main.py --check-deps
```

## Page Layout Options

- **SinglePage**: Single page display
- **OneColumn**: Enable scrolling
- **TwoPageLeft**: Spread view
- **TwoColumnLeft**: Spread view with scrolling
- **TwoPageRight**: Separate Cover, Spread View (default)
- **TwoColumnRight**: Separate Cover, Scrolling Spread View

## Reading Direction Options

- **L2R**: Left Binding (for Western comics)
- **R2L**: Right Binding (for Japanese manga, default)

## Examples

```bash
# Japanese manga (default settings)
python main.py my_manga.epub

# Western comic with left-to-right reading
python main.py my_comic.epub -l TwoPageLeft -d L2R

# Mobile-friendly single page view
python main.py my_manga.epub -l SinglePage
```

## Supported File Formats

- EPUB (Electronic Publication)
- MOBI (Mobipocket)
- AZW3 (Amazon Kindle Format 8)

**Note**: This tool only supports DRM-free files with fixed-layout formats, particularly suited for manga and comics.

## Requirements

- Python 3.6 or higher
- epub2pdf package and its dependencies:
  - img2pdf
  - pikepdf
  - lxml
  - mobi

## Credits

This program is built upon the [epub2pdf](https://pypi.org/project/epub2pdf/) package by mashu3, which provides the core conversion functionality.

## License

This wrapper program follows the same GPLv3 license as the underlying epub2pdf library.
