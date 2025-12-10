#!/usr/bin/env python3
"""
Document Generator using HTML templates and class hierarchy
"""

import os
import argparse
import sys
from pathlib import Path

try:
    from generators.w2.generator import W2Generator
    from generators.paystub.generator import PaystubGenerator
    from generators.other.generator import OtherGenerator
except ImportError:
    # Fallback for direct imports
    from w2_generator import W2Generator
    from paystub_generator import PaystubGenerator
    from other_generator_simple import OtherDocumentGenerator

from config import Config


def setup_output_directories(base_path: str):
    """Create output directory structure."""
    directories = [
        f"{base_path}/w2",
        f"{base_path}/paystub", 
        f"{base_path}/other"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print(f"Created output directories in: {base_path}")


def generate_documents(doc_type: str, count: int, output_dir: str, config: Config):
    """Generate documents of specified type using the new class hierarchy."""
    
    # Create the appropriate generator
    if doc_type == "w2":
        generator = W2Generator(config)
    elif doc_type == "paystub":
        generator = PaystubGenerator(config)
    elif doc_type == "other":
        generator = OtherGenerator(config)
    else:
        print(f"Unknown document type: {doc_type}")
        return
    
    print(f"Generating {count} {doc_type} documents...")
    
    for i in range(count):
        try:
            # Generate filename
            filename = "synthetic_" + doc_type + "_" + str(i+1).zfill(4) + ".jpg"
            output_path = os.path.join(output_dir, doc_type, filename)
            
            # Generate and save document
            generator.generate_and_save(output_path)
            
            if (i + 1) % 10 == 0:
                print("Generated " + str(i + 1) + "/" + str(count) + " " + doc_type + " documents")
                
        except Exception as e:
            print("Error generating " + doc_type + " document " + str(i+1) + ": " + str(e))
            import traceback
            traceback.print_exc()
            continue
    
    print(f"Completed generating {doc_type} documents")


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic documents using HTML templates")
    parser.add_argument("--output_dir", "-o", default="./dataset", 
                       help="Output directory for generated images")
    parser.add_argument("--w2_count", type=int, default=100,
                       help="Number of W-2 documents to generate")
    parser.add_argument("--paystub_count", type=int, default=100,
                       help="Number of paystub documents to generate")
    parser.add_argument("--other_count", type=int, default=100,
                       help="Number of other documents to generate")
    parser.add_argument("--doc_type", choices=["w2", "paystub", "other", "all"],
                       default="all", help="Type of documents to generate")
    
    args = parser.parse_args()
    
    # Load configuration
    config = Config()
    
    # Setup output directories
    setup_output_directories(args.output_dir)
    
    print("Using HTML template-based document generation...")
    
    # Generate documents based on arguments
    if args.doc_type == "all":
        generate_documents("w2", args.w2_count, args.output_dir, config)
        generate_documents("paystub", args.paystub_count, args.output_dir, config)
        generate_documents("other", args.other_count, args.output_dir, config)
    else:
        count_map = {
            "w2": args.w2_count,
            "paystub": args.paystub_count,
            "other": args.other_count
        }
        generate_documents(args.doc_type, count_map[args.doc_type], args.output_dir, config)
    
    print("\nGeneration complete!")
    print(f"Generated documents saved to: {args.output_dir}")


if __name__ == "__main__":
    main()