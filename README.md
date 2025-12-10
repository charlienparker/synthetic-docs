# Synthetic Document Generator

Python tool for generating synthetic documents for machine learning training datasets. Supports W-2 tax forms, paystubs, driver's licenses, receipts, and other document types with realistic data generation and document augmentation effects.

## Features

- **Multiple Document Types**: W-2 tax forms, paystubs, driver's licenses, store receipts, personal letters, book pages, medical summaries, and report cards
- **Template-based Generation**: HTML templates with accurate dimensions and styling
- **Synthetic Data**: Faker library integration with document-specific data generation logic
- **Document Augmentation**: Augraphy pipeline for paper texture, folding, shadows, perspective warping, and camera effects
- **High-resolution Output**: 1654×2339 pixel images for computer vision training
- **Modular Structure**: Extensible generator system with separate document type modules
- **Batch Processing**: Generate large quantities of documents efficiently
- **Configurable**: Adjustable image quality and augmentation parameters

## Quick Start

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Test Your Setup**:
```bash
python test_setup.py
```

3. **Generate Documents**:
```bash
# Generate a mixed dataset (default: 50 of each type)
python generate_synthetic_docs.py

# Generate specific quantities
python generate_synthetic_docs.py --w2_count 100 --paystub_count 100 --other_count 50
```

## Installation

### System Requirements

- **Python 3.8 or higher**
- **4GB+ RAM** (for large batch processing)
- **2GB+ disk space** (for fonts, caches, and output)

### Dependencies

This project uses several specialized libraries:

- **Augraphy** (8.2.6+): Advanced document augmentation pipeline
- **WeasyPrint** (67.0+): HTML to PDF conversion with precise rendering
- **PyMuPDF** (1.26.0+): High-quality PDF to image conversion
- **OpenCV** (cv2): Image processing and computer vision
- **Faker**: Realistic synthetic data generation
- **Jinja2**: Template engine for dynamic document generation

### Step-by-Step Installation

1. **Clone the Repository**:
```bash
git clone https://github.com/yourusername/synthetic-docs.git
cd synthetic-docs
```

2. **Create Virtual Environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Requirements**:
```bash
pip install -r requirements.txt
```

4. **Verify Installation**:
```bash
python test_setup.py
```

## Usage

### Basic Generation

Generate a mixed dataset with default quantities:
```bash
python generate_synthetic_docs.py
```

### Custom Quantities

Specify the number of each document type:
```bash
python generate_synthetic_docs.py --w2_count 200 --paystub_count 150 --other_count 100
```

### Generate Only Specific Document Types

Generate only W-2 documents:
```bash
python generate_synthetic_docs.py --doc_type w2 --w2_count 200
```

Generate only paystubs:
```bash
python generate_synthetic_docs.py --doc_type paystub --paystub_count 150
```

Generate only diverse documents:
```bash
python generate_synthetic_docs.py --doc_type other --other_count 100
```

### Custom Output Directory

Specify a custom output directory:
```bash
python generate_synthetic_docs.py --output_dir /path/to/your/dataset
```

### Help

See all available options:
```bash
python generate_synthetic_docs.py --help
```

## Output Structure

Generated documents are organized in a clean directory structure:

```
outputs/
├── w2/
│   ├── synthetic_w2_0001.jpg
│   ├── synthetic_w2_0002.jpg
│   └── ...
├── paystub/
│   ├── synthetic_paystub_0001.jpg
│   ├── synthetic_paystub_0002.jpg
│   └── ...
└── other/
    ├── synthetic_other_0001.jpg
    ├── synthetic_other_0002.jpg
    └── ...
```

## Document Types

### W-2 Tax Forms
- **IRS format compliance**: 8.5" × 5.5" dimensions matching official layout
- **Variable tax years**: Random selection from 2000-present
- **Calculated withholdings**: Federal/state taxes, Social Security, Medicare based on generated wages
- **Generated employer data**: Company names, addresses, and EIN numbers using Faker
- **Employee information**: Names, addresses, SSNs with format validation

### Paystubs
- **Template variety**: Standard, ADP-style, QuickBooks, PayChex, Government, Traditional formats
- **Color variations**: 8 different color schemes (currently applied to QuickBooks template)
- **Tax calculations**: Federal/state taxes, Social Security, Medicare, insurance, retirement deductions
- **Pay period support**: Bi-weekly, monthly, and semi-monthly with date calculations
- **Data fields**: Employee information, earnings, deductions, year-to-date totals

### Other Documents
- **Driver's Licenses**: State-specific formats with generated personal information
- **Store Receipts**: Thermal printer styling with itemized purchases and tax calculations
- **Personal Letters**: Correspondence format with generated text content
- **Book Pages**: Literature excerpts with typography and pagination
- **Medical Summaries**: Medical document formats with generated medical terminology
- **Report Cards**: Academic transcript format with grades and school information

## Example Output

*This section will be populated with sample images of generated documents.*

<!-- TODO: Add example images showing:
- W-2 with augmentation effects demonstrating realistic camera capture
- Paystub samples showing different template styles and color schemes
- Driver's license examples from different states
- Store receipt with thermal printer styling
- Medical document with professional formatting
- Before/after augmentation comparison showing paper effects
- Side-by-side comparison with real documents (redacted)
-->

## Augmentation Pipeline

The system uses Augraphy to apply document augmentation effects:

### Paper Phase Effects
- **Document folding**: Realistic creases from mailing, storage, and handling
- **Paper texture**: Subtle grain, fiber patterns, and surface irregularities  
- **Natural aging**: Yellowing, wear patterns, and subtle discoloration
- **Realistic stains**: Coffee rings, ink spots, water marks, and handling residue
- **Edge wear**: Natural document edge degradation from use

### Camera Capture Simulation
- **Lighting gradients**: Natural shadows, reflections, and illumination variations
- **Geometric distortion**: Perspective warping from hand-held camera angles
- **Focus effects**: Realistic depth-of-field blur and motion blur
- **Digital artifacts**: JPEG compression, noise, and sensor limitations
- **Color variations**: White balance adjustments and exposure differences

## Project Structure

```
synthetic-docs/
├── generate_synthetic_docs.py    # Main entry point script
├── config.py                    # Global configuration settings
├── utils.py                     # Shared utility functions
├── generators/                  # Modular document generation system
│   ├── __init__.py
│   ├── base_generator.py        # Abstract base class with common functionality
│   ├── w2/                      # W-2 tax form generation
│   │   ├── generator.py         # W2Generator class with tax calculations
│   │   └── templates/
│   │       └── w2_template.html # Pixel-perfect IRS W-2 recreation
│   ├── paystub/                # Paystub generation
│   │   ├── generator.py        # PaystubGenerator with multiple formats
│   │   └── templates/
│   │       ├── paystub_standard.html
│   │       ├── paystub_adp_style.html
│   │       ├── paystub_quickbooks.html
│   │       ├── paystub_government.html
│   │       ├── paystub_paychex_legacy.html
│   │       └── paystub_basic_traditional.html
│   └── other/                  # Diverse document types
│       ├── generator.py        # OtherGenerator with template-specific logic
│       └── templates/
│           ├── drivers_license.html  # State-specific license formats
│           ├── store_receipt.html    # Thermal printer styling
│           ├── personal_letter.html  # Handwritten correspondence
│           ├── book_page.html        # Literature with typography
│           ├── medical_summary.html  # HIPAA-compliant medical docs
│           └── report_card.html      # Academic transcripts
├── outputs/                    # Generated document images organized by type
├── fonts/                      # Professional fonts for authentic rendering
├── augraphy_cache/            # Caching for augmentation pipeline performance
└── requirements.txt           # Python package dependencies
```

## Configuration

Customize all aspects of document generation in `config.py`:

### Image Quality Settings
```python
IMAGE_WIDTH = 1654          # Output image width (pixels)
IMAGE_HEIGHT = 2339         # Output image height (pixels)  
DPI = 150                   # Rendering resolution for sharp text
JPEG_QUALITY = 95           # Output image compression quality
```

### Augmentation Controls
```python
AUGMENTATION_INTENSITY = 0.7    # Overall effect strength (0.0-1.0)
ENABLE_FOLDING = True           # Paper folding and crease effects
LIGHTING_VARIATION = 0.5        # Shadow and illumination intensity
PERSPECTIVE_WARP = 0.3          # Camera angle distortion amount
```

### Document Generation Parameters
```python
SALARY_RANGE = (30000, 120000)  # Annual salary range for paystubs/W-2s
TAX_YEAR_RANGE = (2000, 2024)   # Available tax years for W-2 generation  
DEFAULT_BATCH_SIZE = 50         # Documents per type in default generation
```

## Advanced Usage

### Programmatic Generation

```python
from generators.w2.generator import W2Generator
from generators.paystub.generator import PaystubGenerator
from generators.other.generator import OtherGenerator
import cv2

# Initialize generators
w2_gen = W2Generator()
paystub_gen = PaystubGenerator()
other_gen = OtherGenerator()

# Generate specific documents
w2_image = w2_gen.generate()
paystub_image = paystub_gen.generate()
license_image = other_gen.generate()  # Automatically selects random template

# Save with custom names
cv2.imwrite('custom_w2.jpg', w2_image)
cv2.imwrite('custom_paystub.jpg', paystub_image)
cv2.imwrite('custom_document.jpg', license_image)
```

### Creating Custom Templates

Extend the system with new document types:

1. **Create HTML Template**: Add to appropriate `templates/` directory using Jinja2 syntax
2. **Add Data Generation**: Implement template-specific data logic in generator class
3. **Register Template**: Add to generator's template list for random selection
4. **Test Generation**: Verify output quality and data accuracy

Example template structure:
```html
<!DOCTYPE html>
<html>
<head>
    <style>
        /* CSS for exact document dimensions and styling */
        body { width: 8.5in; height: 11in; margin: 0; }
        .header { font-family: Arial; font-size: 12pt; }
    </style>
</head>
<body>
    <div class="header">{{ document_title }}</div>
    <div class="content">{{ generated_data }}</div>
</body>
</html>
```

## Performance & Best Practices

### Optimization Tips
1. **Batch Processing**: Generate large quantities in single runs for better efficiency
2. **Memory Management**: Monitor RAM usage during large batch operations  
3. **Disk Space**: Clear `augraphy_cache/` periodically to manage storage
4. **Parallel Generation**: Run multiple instances for different document types
5. **Performance Tuning**: Adjust augmentation intensity based on speed requirements

### Usage Recommendations
- **Dataset Size**: Generate 1000+ samples per document type for ML training
- **Quality Control**: Inspect sample outputs for quality and accuracy
- **Data Distribution**: Balance representation across document types
- **Augmentation Testing**: Verify effects match target capture conditions

## Requirements

### System Requirements
- **Python 3.8+** (Python 3.9+ recommended for best performance)
- **Operating System**: macOS, Linux, or Windows (cross-platform compatible)
- **Memory**: 4GB+ RAM (8GB+ recommended for large batches)
- **Storage**: 2GB+ available disk space

### Key Python Dependencies
- `augraphy>=8.2.6` - Advanced document augmentation effects
- `weasyprint>=67.0` - High-quality HTML to PDF conversion
- `PyMuPDF>=1.26.0` - Professional PDF to image processing  
- `opencv-python>=4.5.0` - Computer vision and image manipulation
- `faker>=20.0.0` - Realistic synthetic data generation
- `jinja2>=3.1.0` - Powerful template rendering engine
- `numpy>=1.21.0` - Numerical computing foundation

## Troubleshooting

### Installation Issues

**Dependency Installation Problems**:
```bash
# Upgrade pip and try again
pip install --upgrade pip
pip install -r requirements.txt --upgrade
```

**Augraphy Installation Failure**:
```bash
# Try conda installation (often more reliable)
conda install -c conda-forge augraphy

# Or install development version from source
pip install git+https://github.com/sparkfish/augraphy.git
```

**WeasyPrint Installation Issues**:
```bash
# macOS: Install system dependencies
brew install pango gdk-pixbuf libffi

# Linux: Install system packages
sudo apt-get install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0
```

### Runtime Issues

**Memory Errors**:
```bash
# Generate smaller batches
python generate_synthetic_docs.py --w2_count 25 --paystub_count 25
```

**Permission Errors**:
```bash
# Ensure output directory is writable
mkdir -p outputs && chmod 755 outputs
```

**Font Rendering Problems**:
```bash
# Install additional system fonts or check fonts/ directory
fc-cache -f -v  # Linux/macOS font cache refresh
```

### Quality Issues

- **Blurry Text**: Increase `DPI` setting in `config.py` (try 200-300)
- **Unrealistic Colors**: Adjust color variation ranges in generator classes
- **Poor Augmentation**: Modify `AUGMENTATION_INTENSITY` in configuration
- **Template Errors**: Check HTML syntax and Jinja2 template variables

## Contributing

Priority areas for enhancement:

### New Features
- **Additional Document Types**: Insurance cards, bank statements, utility bills, tax forms (1099, 1040)
- **Enhanced Templates**: More authentic styling, regional variations, historical formats
- **Improved Data Generation**: More sophisticated financial calculations and realistic correlations
- **Advanced Augmentation**: Additional camera effects, environmental conditions, age variations

### Code Improvements  
- **Performance Optimization**: Faster rendering, parallel processing, memory efficiency
- **Template System**: Better inheritance, shared components, style libraries
- **Testing Coverage**: Unit tests, integration tests, quality validation
- **Documentation**: Code comments, API documentation, tutorial content

### Getting Started with Contributions
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-document-type`)
3. Make your changes and test thoroughly  
4. Submit a pull request with detailed description

## License

This project is provided for educational and research purposes. Generated documents are synthetic and should not be used fraudulently. Ensure compliance with local regulations and ethical guidelines when using synthetic documents for machine learning training.