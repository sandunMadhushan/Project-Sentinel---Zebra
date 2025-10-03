#!/usr/bin/env python3
"""
Quick Start Script for Project Sentinel Dashboard
==================================================

This script launches the dashboard in interactive mode where you can:
- Select data input folders from the UI
- Run event detection directly
- View results in real-time

Usage:
    python start_dashboard.py
"""

import subprocess
import sys
from pathlib import Path


def main():
    """Launch the dashboard."""
    dashboard_path = Path(__file__).parent / "src" / "dashboard" / "dashboard_app.py"
    
    if not dashboard_path.exists():
        print(f"❌ Error: Dashboard not found at {dashboard_path}")
        return 1
    
    print("🚀 Starting Project Sentinel Dashboard...")
    print("📊 The dashboard will open in your browser shortly.")
    print("🔧 You can select data folders and run detection from the UI!")
    print("\n✨ Features:")
    print("   - Interactive data folder selection")
    print("   - Run event detection with one click")
    print("   - Real-time visualization")
    print("   - Export capabilities")
    print("\n⏹️  Press Ctrl+C to stop\n")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            str(dashboard_path),
            "--server.headless", "true"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard stopped. Thanks for using Project Sentinel!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
