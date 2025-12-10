"""
Base document generator class that handles fake data population and augmentation.
"""

import numpy as np
import cv2
import os
from faker import Faker
from augraphy import (
    AugraphyPipeline,
    InkBleed, ColorPaper, Folding, NoiseTexturize, 
    DirtyRollers, SubtleNoise, LightingGradient,
    Geometric, Jpeg, default_augraphy_pipeline
)
import random
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import Config
from abc import ABC, abstractmethod
import tempfile
import weasyprint
from jinja2 import Template
import fitz  # PyMuPDF


class BaseDocumentGenerator(ABC):
    """Base class for all document generators."""
    
    def __init__(self, config=None):
        self.fake = Faker()
        self.config = config or Config()
        self.pipeline = self._create_augmentation_pipeline()
    
    def _create_augmentation_pipeline(self):
        """Create the document augmentation pipeline using Augraphy."""
        return AugraphyPipeline(
            ink_phase=[
                # Simulate ink bleeding/smudging  
                InkBleed(intensity_range=(0.1, 0.3), kernel_size=(5, 7))
            ],
            paper_phase=[
                # Simulate folding lines (documents come in envelopes!)
                Folding(fold_count=2, fold_noise=0.1, fold_angle_range=(-5, 5)),
                # Add paper texture/noise
                NoiseTexturize(sigma_range=(3, 10), turbulence_range=(2, 5))
            ],
            post_phase=[
                # Simulate lighting gradient (shadow from camera/hand)
                LightingGradient(
                    light_position=None, 
                    direction=None, 
                    max_brightness=255, 
                    min_brightness=160
                ),
                # Simulate geometric perspective warp (phone held at angle)
                Geometric(
                    scale=(0.8, 1.2), 
                    translation=(0, 0), 
                    fliplr=0, 
                    flipud=0, 
                    rotate_range=(-5, 5)
                ),
                # Add JPEG compression artifacts
                Jpeg(quality_range=(70, 95))
            ]
        )
    
    @abstractmethod
    def get_html_template_path(self):
        """Return the path to the HTML template for this document type."""
        pass
    
    @abstractmethod
    def generate_fake_data(self):
        """Generate fake data specific to this document type."""
        pass
    
    def render_html_to_image(self, template_path, data, width=850, height=1100):
        """Render HTML template with data to an image."""
        # Read the HTML template
        with open(template_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Render the template with data using Jinja2
        template = Template(html_content)
        rendered_html = template.render(**data)
        
        # Use WeasyPrint to convert HTML to PDF, then to image
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as pdf_file:
            weasyprint.HTML(string=rendered_html).write_pdf(pdf_file.name)
            pdf_path = pdf_file.name
        
        try:
            # Convert PDF to image using OpenCV (via intermediate conversion)
            import fitz  # PyMuPDF
            pdf_doc = fitz.open(pdf_path)
            page = pdf_doc[0]
            
            # Render page to image
            mat = fitz.Matrix(2.0, 2.0)  # High resolution
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("ppm")
            
            # Convert to OpenCV format
            img_array = np.frombuffer(img_data, dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            
            # Resize to target dimensions
            img = cv2.resize(img, (width, height))
            
            pdf_doc.close()
            return img
            
        finally:
            # Clean up temporary PDF file
            os.unlink(pdf_path)
    
    def generate_clean_document(self):
        """Generate a clean document image."""
        template_path = self.get_html_template_path()
        data = self.generate_fake_data()
        return self.render_html_to_image(template_path, data)
    
    def apply_augmentation(self, image):
        """Apply the augmentation pipeline to make the document look realistic."""
        return self.pipeline(image)
    
    def generate_document(self):
        """Generate a complete document with augmentation."""
        clean_img = self.generate_clean_document()
        return self.apply_augmentation(clean_img)
    
    def save_image(self, image, filepath):
        """Save the image to the specified filepath."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        cv2.imwrite(filepath, image)
    
    def generate_and_save(self, filepath):
        """Generate a document and save it to the specified path."""
        document = self.generate_document()
        self.save_image(document, filepath)
        return document