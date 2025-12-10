"""
Utility functions for the document generator.
"""

import os
import cv2
import numpy as np
from typing import Tuple, List
import json
from pathlib import Path


def create_directory_structure(base_path: str, subdirs: List[str]) -> dict:
    """
    Create directory structure for organizing generated documents.
    
    Args:
        base_path: Base directory path
        subdirs: List of subdirectories to create
    
    Returns:
        Dictionary mapping subdir names to their full paths
    """
    directories = {}
    for subdir in subdirs:
        dir_path = os.path.join(base_path, subdir)
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        directories[subdir] = dir_path
    
    return directories


def save_generation_metadata(output_dir: str, metadata: dict):
    """
    Save metadata about the generation process.
    
    Args:
        output_dir: Output directory
        metadata: Metadata dictionary to save
    """
    metadata_path = os.path.join(output_dir, "generation_metadata.json")
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2, default=str)


def load_generation_metadata(output_dir: str) -> dict:
    """
    Load generation metadata if it exists.
    
    Args:
        output_dir: Output directory
    
    Returns:
        Metadata dictionary or empty dict if not found
    """
    metadata_path = os.path.join(output_dir, "generation_metadata.json")
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            return json.load(f)
    return {}


def draw_text_box(img: np.ndarray, text: str, position: Tuple[int, int], 
                  box_size: Tuple[int, int], font_scale: float = 0.6,
                  text_color: Tuple[int, int, int] = (0, 0, 0),
                  border_color: Tuple[int, int, int] = (0, 0, 0),
                  padding: int = 5) -> np.ndarray:
    """
    Draw a text box with border on an image.
    
    Args:
        img: Input image
        text: Text to draw
        position: (x, y) position of top-left corner
        box_size: (width, height) of the box
        font_scale: Font scale
        text_color: RGB color for text
        border_color: RGB color for border
        padding: Internal padding
    
    Returns:
        Modified image
    """
    x, y = position
    width, height = box_size
    
    # Draw border
    cv2.rectangle(img, (x, y), (x + width, y + height), border_color, 1)
    
    # Draw text
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, text, (x + padding, y + height - padding), 
                font, font_scale, text_color, 1)
    
    return img


def draw_multi_line_text(img: np.ndarray, lines: List[str], 
                        start_pos: Tuple[int, int], line_height: int = 25,
                        font_scale: float = 0.6, 
                        text_color: Tuple[int, int, int] = (0, 0, 0)) -> np.ndarray:
    """
    Draw multiple lines of text on an image.
    
    Args:
        img: Input image
        lines: List of text lines
        start_pos: (x, y) starting position
        line_height: Height between lines
        font_scale: Font scale
        text_color: RGB color for text
    
    Returns:
        Modified image
    """
    x, y = start_pos
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    for i, line in enumerate(lines):
        current_y = y + (i * line_height)
        cv2.putText(img, line, (x, current_y), font, font_scale, text_color, 1)
    
    return img


def add_form_header(img: np.ndarray, title: str, subtitle: str = "",
                   title_pos: Tuple[int, int] = (50, 50)) -> np.ndarray:
    """
    Add a standard form header to an image.
    
    Args:
        img: Input image
        title: Main title text
        subtitle: Optional subtitle text
        title_pos: Position for the title
    
    Returns:
        Modified image
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    x, y = title_pos
    
    # Main title
    cv2.putText(img, title, (x, y), font, 1.2, (0, 0, 0), 2)
    
    # Subtitle if provided
    if subtitle:
        cv2.putText(img, subtitle, (x, y + 40), font, 0.8, (0, 0, 0), 1)
    
    return img


def calculate_text_size(text: str, font_scale: float = 0.6) -> Tuple[int, int]:
    """
    Calculate the size of text when rendered.
    
    Args:
        text: Text to measure
        font_scale: Font scale
    
    Returns:
        (width, height) of the text
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    thickness = 1
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    return text_width, text_height + baseline


def wrap_text(text: str, max_width: int, font_scale: float = 0.6) -> List[str]:
    """
    Wrap text to fit within a maximum width.
    
    Args:
        text: Text to wrap
        max_width: Maximum width in pixels
        font_scale: Font scale
    
    Returns:
        List of wrapped text lines
    """
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        text_width, _ = calculate_text_size(test_line, font_scale)
        
        if text_width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    return lines


def add_watermark(img: np.ndarray, watermark_text: str = "SYNTHETIC",
                 opacity: float = 0.1) -> np.ndarray:
    """
    Add a subtle watermark to indicate synthetic data.
    
    Args:
        img: Input image
        watermark_text: Watermark text
        opacity: Opacity of the watermark (0.0 to 1.0)
    
    Returns:
        Modified image
    """
    overlay = img.copy()
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 2.0
    thickness = 3
    
    # Get text size
    text_width, text_height = calculate_text_size(watermark_text, font_scale)
    
    # Position watermark in center
    x = (img.shape[1] - text_width) // 2
    y = (img.shape[0] + text_height) // 2
    
    # Draw watermark
    cv2.putText(overlay, watermark_text, (x, y), font, font_scale, (128, 128, 128), thickness)
    
    # Blend with original image
    cv2.addWeighted(overlay, opacity, img, 1 - opacity, 0, img)
    
    return img


def validate_image_quality(img: np.ndarray, min_size: Tuple[int, int] = (400, 400)) -> bool:
    """
    Validate that generated image meets minimum quality standards.
    
    Args:
        img: Input image
        min_size: Minimum (width, height) dimensions
    
    Returns:
        True if image passes validation
    """
    if img is None:
        return False
    
    height, width = img.shape[:2]
    min_width, min_height = min_size
    
    # Check minimum dimensions
    if width < min_width or height < min_height:
        return False
    
    # Check if image is not completely blank
    if np.all(img == img[0, 0]):
        return False
    
    # Check if image has reasonable contrast
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    contrast = np.std(gray)
    
    if contrast < 10:  # Very low contrast threshold
        return False
    
    return True


def create_dataset_split(total_count: int, train_ratio: float = 0.8, 
                        val_ratio: float = 0.1, test_ratio: float = 0.1) -> dict:
    """
    Create dataset split information.
    
    Args:
        total_count: Total number of samples
        train_ratio: Training set ratio
        val_ratio: Validation set ratio
        test_ratio: Test set ratio
    
    Returns:
        Dictionary with split counts
    """
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 0.001, "Ratios must sum to 1.0"
    
    train_count = int(total_count * train_ratio)
    val_count = int(total_count * val_ratio)
    test_count = total_count - train_count - val_count
    
    return {
        "total": total_count,
        "train": train_count,
        "validation": val_count,
        "test": test_count
    }


def print_generation_summary(metadata: dict):
    """
    Print a summary of the generation process.
    
    Args:
        metadata: Generation metadata
    """
    print("\n" + "="*60)
    print("DOCUMENT GENERATION SUMMARY")
    print("="*60)
    
    if "counts" in metadata:
        print("\nGenerated Documents:")
        for doc_type, count in metadata["counts"].items():
            print(f"  {doc_type.upper()}: {count} documents")
        
        total = sum(metadata["counts"].values())
        print(f"  TOTAL: {total} documents")
    
    if "output_directory" in metadata:
        print(f"\nOutput Directory: {metadata['output_directory']}")
    
    if "generation_time" in metadata:
        print(f"Generation Time: {metadata['generation_time']:.2f} seconds")
    
    if "split_info" in metadata:
        split = metadata["split_info"]
        print(f"\nDataset Split:")
        print(f"  Training: {split['train']} ({split['train']/split['total']*100:.1f}%)")
        print(f"  Validation: {split['validation']} ({split['validation']/split['total']*100:.1f}%)")
        print(f"  Test: {split['test']} ({split['test']/split['total']*100:.1f}%)")
    
    print("\n" + "="*60)