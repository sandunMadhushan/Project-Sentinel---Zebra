#!/usr/bin/env python3
"""
Test script to verify event detection works with custom paths
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from dashboard.dashboard_app import run_event_detection

# Test with the src/data/input folder
data_folder = Path(__file__).parent / "src" / "data" / "input"

print(f"Testing event detection with folder: {data_folder}")
print(f"Folder exists: {data_folder.exists()}")
print(f"Absolute path: {data_folder.resolve()}")
print("\nRunning detection...\n")

success, message, events_file = run_event_detection(str(data_folder), "test")

print(f"\nSuccess: {success}")
print(f"Message: {message}")
print(f"Events file: {events_file}")

if success:
    print("\n✅ Detection completed successfully!")
    print(f"Events saved to: {events_file}")
else:
    print("\n❌ Detection failed!")
    print("Check the error message above for details.")
