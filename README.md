# Dive Color Corrector

A Python application for correcting underwater images, making them more vibrant and true to life.

## Features

- Color correction for underwater images and videos
- User-friendly GUI interface
- Support for multiple image formats
- Real-time preview of corrections
- Batch processing capabilities

## Installation

### From PyPI (Coming Sometime...)

```bash
pip install dive-color-corrector
```

### From Source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/dive-color-corrector.git
cd dive-color-corrector
```

2. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install the package:
```bash
uv pip install -e ".[gui]"
```

## Usage

### GUI Application

Launch the application:
```bash
python -m dive_color_corrector
```

### Command Line Interface

For images:
```bash
python -m dive_color_corrector image /path/to/raw.png /path/to/corrected.png
```

For videos:
```bash
python -m dive_color_corrector video /path/to/raw.mp4 /path/to/corrected.mp4
```

## Examples

### Sample Images
![Example](./examples/example.jpg)

### Sample Video
[![Video](https://img.youtube.com/vi/NEpl41-LMBs/0.jpg)](https://www.youtube.com/watch?v=NEpl41-LMBs)

## Development

### Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) for dependency management
- Git

### Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/dive-color-corrector.git
cd dive-color-corrector
```

2. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install development dependencies:
```bash
uv pip install -e ".[gui]"
```

### Building Executables

The project uses PyInstaller to create standalone executables. To build locally:

```bash
uv pip install pyinstaller pillow
pyinstaller --name "Dive Color Corrector" \
            --windowed \
            --icon "logo/logo.png" \
            --add-data "src/dive_color_corrector/gui/assets:dive_color_corrector/gui/assets" \
            --clean \
            --noconfirm \
            src/dive_color_corrector/__main__.py
```

The executable will be created in the `dist` directory.

## Project Structure

```
dive-color-corrector/
├── src/
│   └── dive_color_corrector/
│       ├── core/           # Core color correction logic
│       ├── gui/            # GUI components
│       │   └── assets/     # GUI assets (images, icons)
│       ├── __init__.py
│       └── __main__.py     # Application entry point
├── tests/                  # Test suite
├── examples/               # Example images
├── logo/                   # Application logo
├── pyproject.toml         # Project configuration
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to all contributors who have helped shape this project especially [bornfree](https://github.com/bornfree)
- Special thanks to the open-source community for the tools and libraries used in this project
- Inspired by the algorithm at [nikolajbech/underwater-image-color-correction](https://github.com/nikolajbech/underwater-image-color-correction)

## Share

If this project was useful, please consider [sharing the word](https://twitter.com/intent/tweet?url=https://github.com/bornfree/dive-color-correction&text=Correct%20your%20dive%20footage%20with%20Python%20#scuba%20#gopro%20#python%20#opencv) on Twitter.
