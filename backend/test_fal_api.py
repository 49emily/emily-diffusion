#!/usr/bin/env python3
"""
Test script to verify fal-client API methods.
"""

import fal_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_fal_methods():
    """Test which methods are available in fal_client."""
    print("Available methods in fal_client:")
    methods = [method for method in dir(fal_client) if not method.startswith("_")]
    for method in sorted(methods):
        print(f"  - {method}")

    print(f"\nfal_client version: {getattr(fal_client, '__version__', 'unknown')}")


def test_simple_call():
    """Test a simple fal call."""
    try:
        # Try the submit method first (from documentation)
        print("\nTesting fal_client.submit()...")
        handler = fal_client.submit(
            "fal-ai/flux-lora", arguments={"prompt": "a simple test image"}
        )
        print(f"Submit successful! Request ID: {handler.request_id}")

        # Get the result
        print("Getting result...")
        result = handler.get()
        print(f"Result: {result}")

    except Exception as e:
        print(f"Submit method failed: {e}")

        # Try the subscribe method
        try:
            print("\nTesting fal_client.subscribe()...")
            result = fal_client.subscribe(
                "fal-ai/flux-lora",
                arguments={"prompt": "a simple test image"},
                with_logs=True,
            )
            print(f"Subscribe successful! Result: {result}")

        except Exception as e2:
            print(f"Subscribe method failed: {e2}")


if __name__ == "__main__":
    test_fal_methods()
    test_simple_call()
