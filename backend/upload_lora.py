#!/usr/bin/env python3
"""
Separate script for uploading LoRA files to fal.
Usage: python upload_lora.py <path_to_lora_file>
"""

import sys
import os
from dotenv import load_dotenv
import fal_client

# Load environment variables
load_dotenv()


def upload_lora_file(file_path):
    """
    Upload a LoRA file to fal and return the public URL.

    Args:
        file_path (str): Path to the local LoRA file

    Returns:
        str: Public URL of the uploaded file
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    if not file_path.endswith(".safetensors"):
        raise ValueError("File must be a .safetensors file")

    print(f"Uploading {file_path}...")

    try:
        # Upload the file and get the public URL
        lora_url = fal_client.upload_file(file_path)
        print(f"Successfully uploaded! URL: {lora_url}")
        return lora_url
    except Exception as e:
        print(f"Error uploading file: {e}")
        raise


def main():
    if len(sys.argv) != 2:
        print("Usage: python upload_lora.py <path_to_lora_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        url = upload_lora_file(file_path)
        print(f"\nUpload successful!")
        print(f"File URL: {url}")
        print(f"\nYou can now use this URL in your inference calls.")
    except Exception as e:
        print(f"Upload failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
