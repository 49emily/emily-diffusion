#!/usr/bin/env python3
"""
Test client for the fal inference Flask server.
Demonstrates how to use the API endpoints.
"""

import requests
import json

BASE_URL = "http://localhost:8000"


def test_health_check():
    """Test the health check endpoint."""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()


def test_upload_lora(file_path):
    """Test uploading a LoRA file."""
    print(f"Testing LoRA upload with file: {file_path}")

    try:
        with open(file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(f"{BASE_URL}/upload-lora", files=files)

        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")

        if response.status_code == 200:
            return response.json().get("lora_url")

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error: {e}")

    print()
    return None


def test_generate_simple(prompt, lora_url=None, lora_scale=0.8):
    """Test the simple generate endpoint."""
    print(f"Testing simple generation with prompt: '{prompt}'")

    payload = {"prompt": prompt}

    if lora_url:
        payload["lora_url"] = lora_url
        payload["lora_scale"] = lora_scale

    response = requests.post(
        f"{BASE_URL}/generate-simple",
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload),
    )

    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()


def test_generate_full(prompt, loras=None):
    """Test the full generate endpoint."""
    print(f"Testing full generation with prompt: '{prompt}'")

    payload = {"prompt": prompt, "sync_mode": True}

    if loras:
        payload["loras"] = loras

    response = requests.post(
        f"{BASE_URL}/generate",
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload),
    )

    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()


def main():
    """Run all tests."""
    print("=== Fal Inference Server Test Client ===\n")

    # Test health check
    test_health_check()

    # Test simple generation without LoRA
    test_generate_simple("a beautiful landscape painting")

    # Example with LoRA (you would need to upload a file first)
    # Uncomment and modify these lines if you have a LoRA file to test:

    # lora_url = test_upload_lora("path/to/your/lora.safetensors")
    # if lora_url:
    #     test_generate_simple("portrait photo in my custom style", lora_url, 0.8)
    #
    #     # Test full endpoint with LoRA
    #     loras = [{"path": lora_url, "scale": 0.8}]
    #     test_generate_full("portrait photo in my custom style", loras)


if __name__ == "__main__":
    main()
