"""
Configuration settings for the document generator.
"""

import os
from pathlib import Path


class Config:
    """Configuration class for document generation settings."""
    
    # Image settings
    IMAGE_WIDTH = 850
    IMAGE_HEIGHT = 1100
    IMAGE_DPI = 300
    IMAGE_FORMAT = "jpg"
    IMAGE_QUALITY = 85
    
    # Document canvas settings
    CANVAS_COLOR = (255, 255, 255)  # White background
    TEXT_COLOR = (0, 0, 0)  # Black text
    BORDER_COLOR = (0, 0, 0)  # Black borders
    
    # Font settings
    FONT_SCALE_TITLE = 1.2
    FONT_SCALE_HEADER = 0.8
    FONT_SCALE_NORMAL = 0.6
    FONT_SCALE_SMALL = 0.4
    FONT_THICKNESS_BOLD = 2
    FONT_THICKNESS_NORMAL = 1
    
    # Layout settings
    MARGIN_LEFT = 50
    MARGIN_TOP = 50
    MARGIN_RIGHT = 50
    MARGIN_BOTTOM = 50
    
    BOX_HEIGHT = 60
    BOX_WIDTH = 350
    LINE_SPACING = 30
    SECTION_SPACING = 40
    
    # Augmentation settings
    AUGMENTATION_ENABLED = True
    
    # Folding settings
    FOLD_COUNT_RANGE = (1, 3)
    FOLD_NOISE = 0.1
    FOLD_ANGLE_RANGE = (-5, 5)
    
    # Noise settings
    NOISE_SIGMA_RANGE = (3, 10)
    NOISE_TURBULENCE_RANGE = (2, 5)
    
    # Lighting settings
    LIGHTING_MAX_BRIGHTNESS = 255
    LIGHTING_MIN_BRIGHTNESS = 160
    
    # Geometric transformation settings
    GEOMETRIC_SCALE_RANGE = (0.8, 1.2)
    GEOMETRIC_ROTATION_RANGE = (-5, 5)
    
    # Blur settings
    BLUR_RADIUS_RANGE = (1, 3)
    
    # JPEG compression settings
    JPEG_QUALITY_RANGE = (70, 95)
    
    # Data generation settings
    SALARY_RANGE = (30000, 150000)
    TAX_WITHHOLDING_RATE = 0.22
    STATE_TAX_RATE = 0.05
    SOCIAL_SECURITY_RATE = 0.062
    MEDICARE_RATE = 0.0145
    
    HOURLY_RATE_RANGE = (15, 45)
    HOURS_RANGE = (70, 80)
    OVERTIME_MULTIPLIER = 1.5
    
    # Output settings
    DEFAULT_OUTPUT_DIR = "./dataset"
    DEFAULT_COUNTS = {
        "w2": 100,
        "paystub": 100,
        "other": 100
    }
    
    @classmethod
    def get_output_directories(cls, base_path=None):
        """Get the output directory structure."""
        if base_path is None:
            base_path = cls.DEFAULT_OUTPUT_DIR
        
        return {
            "w2": os.path.join(base_path, "w2"),
            "paystub": os.path.join(base_path, "paystub"),
            "other": os.path.join(base_path, "other")
        }
    
    @classmethod
    def ensure_output_dirs(cls, base_path=None):
        """Ensure output directories exist."""
        directories = cls.get_output_directories(base_path)
        for directory in directories.values():
            Path(directory).mkdir(parents=True, exist_ok=True)
        return directories