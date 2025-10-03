#!/usr/bin/env python3
"""
Quick Deployment Helper for Project Sentinel Dashboard
========================================================

This script helps you quickly deploy the dashboard locally or prepare for cloud deployment.

Usage:
    python deploy.py --local          # Run dashboard locally
    python deploy.py --prepare-cloud  # Prepare files for Streamlit Cloud
    python deploy.py --check          # Check deployment status
"""

import argparse
import subprocess
import sys
from pathlib import Path
import json


def check_requirements():
    """Check if all required packages are installed."""
    print("🔍 Checking requirements...")
    try:
        import pandas
        import streamlit
        import plotly
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e.name}")
        print("\n📦 Installing requirements...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return False


def check_events_file():
    """Check if events.jsonl exists and has data."""
    print("\n🔍 Checking for events data...")
    events_file = Path("evidence/executables/results/events.jsonl")
    
    if not events_file.exists():
        print("❌ Events file not found!")
        print(f"   Expected: {events_file.absolute()}")
        print("\n💡 Generate events first:")
        print("   cd evidence/executables")
        print("   python run_demo.py --data-dir ../../tools/generated_test_data --dataset-type test")
        return False
    
    # Count events
    event_count = 0
    with open(events_file, 'r') as f:
        for line in f:
            if line.strip():
                event_count += 1
    
    print(f"✅ Events file found: {event_count} events")
    return True


def check_git_status():
    """Check if events file is committed to Git."""
    print("\n🔍 Checking Git status...")
    try:
        result = subprocess.run(
            ["git", "ls-files", "--error-unmatch", "LoopCode/evidence/executables/results/events.jsonl"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Events file is committed to Git")
            return True
        else:
            print("⚠️  Events file is NOT committed to Git")
            print("\n💡 To commit:")
            print("   git add LoopCode/evidence/executables/results/events.jsonl")
            print("   git commit -m 'Add events data for dashboard'")
            print("   git push origin main")
            return False
    except FileNotFoundError:
        print("⚠️  Git not found (not critical for local deployment)")
        return False


def run_local():
    """Run dashboard locally."""
    print("\n🚀 Starting local dashboard...\n")
    
    # Check requirements first
    check_requirements()
    
    # Check events file
    if not check_events_file():
        return
    
    # Run Streamlit
    dashboard_path = Path("src/dashboard/dashboard_app.py")
    if not dashboard_path.exists():
        print(f"❌ Dashboard file not found: {dashboard_path.absolute()}")
        return
    
    print(f"\n📊 Dashboard URL: http://localhost:8502")
    print("Press Ctrl+C to stop\n")
    
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(dashboard_path)])


def prepare_cloud():
    """Prepare for Streamlit Cloud deployment."""
    print("\n☁️  Preparing for Streamlit Cloud deployment...\n")
    
    all_good = True
    
    # Check requirements.txt
    if Path("requirements.txt").exists():
        print("✅ requirements.txt found")
    else:
        print("❌ requirements.txt missing")
        all_good = False
    
    # Check .streamlit/config.toml
    if Path(".streamlit/config.toml").exists():
        print("✅ .streamlit/config.toml found")
    else:
        print("⚠️  .streamlit/config.toml missing (optional)")
    
    # Check dashboard file
    if Path("src/dashboard/dashboard_app.py").exists():
        print("✅ src/dashboard/dashboard_app.py found")
    else:
        print("❌ src/dashboard/dashboard_app.py missing")
        all_good = False
    
    # Check events file
    check_events_file()
    
    # Check Git status
    events_committed = check_git_status()
    
    print("\n" + "="*60)
    if all_good and events_committed:
        print("✅ Ready for Streamlit Cloud deployment!")
        print("\n📋 Deployment Instructions:")
        print("   1. Go to: https://share.streamlit.io")
        print("   2. Click 'New app'")
        print("   3. Fill in:")
        print("      - Repository: sandunMadhushan/Project-Sentinel---Zebra")
        print("      - Branch: main")
        print("      - Main file: LoopCode/src/dashboard/dashboard_app.py")
        print("   4. Click 'Deploy!'")
    else:
        print("⚠️  Some issues need to be resolved before cloud deployment")
        if not events_committed:
            print("\n⚠️  Important: Commit events.jsonl to Git first!")


def check_status():
    """Check overall deployment status."""
    print("📊 Project Sentinel - Deployment Status\n")
    print("="*60)
    
    check_requirements()
    check_events_file()
    check_git_status()
    
    print("\n" + "="*60)
    print("\n💡 Available Commands:")
    print("   python deploy.py --local          # Run locally")
    print("   python deploy.py --prepare-cloud  # Prepare for cloud")
    print("   python deploy.py --check          # Check status (this)")


def main():
    parser = argparse.ArgumentParser(description="Project Sentinel Dashboard Deployment Helper")
    parser.add_argument("--local", action="store_true", help="Run dashboard locally")
    parser.add_argument("--prepare-cloud", action="store_true", help="Prepare for cloud deployment")
    parser.add_argument("--check", action="store_true", help="Check deployment status")
    
    args = parser.parse_args()
    
    # Change to LoopCode directory
    script_dir = Path(__file__).parent
    try:
        import os
        os.chdir(script_dir)
    except:
        pass
    
    if args.local:
        run_local()
    elif args.prepare_cloud:
        prepare_cloud()
    elif args.check:
        check_status()
    else:
        # Default: show help
        check_status()


if __name__ == "__main__":
    main()
