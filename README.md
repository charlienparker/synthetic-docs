# Synthetic Document Generator

A Python-based synthetic data generator for creating realistic W-2s, paystubs, and other documents for training document classifiers.

## Features

- **Multiple Document Types**: Generates W-2 tax forms, paystubs, bank statements, invoices, receipts, and tax documents
- **Realistic Data**: Uses Faker library to generate realistic personal and financial information
- **Document Augmentation**: Applies realistic distortions using Augraphy to simulate phone camera uploads
- **Customizable Pipeline**: Configurable augmentation settings for different use cases
- **Organized Output**: Automatically creates organized directory structure for training data

## Installation

1. **Clone or download the project files**

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Test the setup:**
   ```bash
   python test_setup.py
   ```

## Usage

### Basic Usage

Generate 100 documents of each type:
```bash
python main.py
```

### Custom Counts

Generate specific numbers of each document type:
```bash
python main.py --w2_count 50 --paystub_count 75 --other_count 25
```

### Generate Only Specific Document Types

Generate only W-2 documents:
```bash
python main.py --doc_type w2 --w2_count 200
```

Generate only paystubs:
```bash
python main.py --doc_type paystub --paystub_count 150
```

### Custom Output Directory

Specify a custom output directory:
```bash
python main.py --output_dir /path/to/your/dataset
```

### Help

See all available options:
```bash
python main.py --help
```

## Output Structure

The generated documents will be organized in the following structure:

```
dataset/
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
- Standard W-2 layout with boxes a-f and wage information
- Realistic SSN, EIN, and employer information
- Random but plausible wage and withholding amounts

### Paystubs
- Standard payroll format with earnings and deductions
- Employee information and pay period details
- Calculated tax withholdings and net pay

### Other Documents
- **Bank Statements**: Account information and transaction history
- **Invoices**: Business invoices with itemized charges
- **Receipts**: Retail receipts with multiple items
- **Tax Documents**: Various 1099 forms and tax-related documents

## Augmentation Pipeline

The system applies realistic augmentations to simulate real-world document capture:

- **Paper Phase**:
  - Folding lines (documents come in envelopes)
  - Paper texture and noise
  - Subtle stains and aging effects

- **Post Phase**:
  - Lighting gradients (shadows from camera/hand)
  - Geometric perspective warping (phone held at angle)
  - Camera blur
  - JPEG compression artifacts

## Configuration

You can modify `config.py` to customize:

- Image dimensions and quality settings
- Font sizes and colors
- Layout parameters (margins, spacing)
- Augmentation intensity ranges
- Data generation parameters (salary ranges, tax rates)

## File Structure

- `main.py`: Main entry point for document generation
- `document_generator.py`: Core document generation logic
- `config.py`: Configuration settings
- `utils.py`: Utility functions for text rendering and file management
- `test_setup.py`: Setup verification script
- `requirements.txt`: Python dependencies

## Example Usage for ML Training

```python
from document_generator import DocumentGenerator
import cv2

# Generate a single document
generator = DocumentGenerator()
w2_image = generator.generate_clean_w2()
augmented_image = generator.apply_augmentation(w2_image)

# Save for training
cv2.imwrite('training_sample.jpg', augmented_image)
```

## Requirements

- Python 3.7+
- OpenCV (cv2)
- NumPy
- Faker
- Augraphy
- Pillow

## Tips for Best Results

1. **Generate Large Datasets**: For ML training, generate thousands of samples per class
2. **Validate Quality**: Check generated images to ensure they meet your quality standards
3. **Customize Augmentation**: Adjust augmentation settings in `config.py` to match your target domain
4. **Balance Classes**: Ensure roughly equal numbers of each document type for classification
5. **Test Pipeline**: Always run `test_setup.py` after installation or configuration changes

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`
2. **Permission Errors**: Ensure you have write permissions to the output directory
3. **Memory Issues**: For large batch generations, consider generating in smaller batches

### Augraphy Installation Issues

If Augraphy fails to install:
```bash
# Try installing from conda-forge
conda install -c conda-forge augraphy

# Or install development version
pip install git+https://github.com/sparkfish/augraphy.git
```

## Contributing

Feel free to extend this generator by:
- Adding new document types
- Improving existing templates
- Adding more realistic data generation
- Enhancing the augmentation pipeline

## License

This project is provided as-is for educational and research purposes.