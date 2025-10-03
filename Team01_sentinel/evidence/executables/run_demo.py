#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project Sentinel - Automation Script
=====================================

This script automates the complete Project Sentinel analysis workflow.
Judges will run this single command to:
  1. Install dependencies
  2. Run event detection on input data
  3. Generate events.jsonl files
  4. Create visualizations and reports
  5. Launch the dashboard (optional)

Usage:
    # Run full pipeline with data processing
    python3 run_demo.py --data-dir PATH [--launch-dashboard]
    
    # Launch dashboard only (using existing results)
    python3 run_demo.py --dashboard-only

Author: Team 01
Date: October 2025
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path
import time


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(message):
    """Print formatted header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{message.center(70)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")


def print_success(message):
    """Print success message"""
    print(f"{Colors.OKGREEN}[OK] {message}{Colors.ENDC}")


def print_error(message):
    """Print error message"""
    print(f"{Colors.FAIL}[ERROR] {message}{Colors.ENDC}")


def print_info(message):
    """Print info message"""
    print(f"{Colors.OKCYAN}[INFO] {message}{Colors.ENDC}")


def setup_environment():
    """Install required Python packages"""
    print_header("SETTING UP ENVIRONMENT")
    
    print_info("Installing required packages...")
    
    # Requirements
    requirements = [
        'pandas>=2.0.0',
        'streamlit>=1.28.0',
        'plotly>=5.17.0'
    ]
    
    try:
        for req in requirements:
            print(f"  Installing {req}...")
            subprocess.check_call(
                [sys.executable, '-m', 'pip', 'install', '-q', req],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        print_success("All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install dependencies: {e}")
        return False


def run_event_detection(data_dir, output_dir):
    """Run event detection on input data"""
    print_header("RUNNING EVENT DETECTION")
    
    # Get paths - go up two levels from executables to Team01_sentinel root
    script_dir = Path(__file__).parent.parent.parent
    detector_script = script_dir / 'src' / 'event_detector.py'
    
    if not detector_script.exists():
        print_error(f"Event detector script not found: {detector_script}")
        return False
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / 'events.jsonl'
    
    print_info(f"Input data directory: {data_dir}")
    print_info(f"Output file: {output_file}")
    
    try:
        # Run detector
        cmd = [
            sys.executable,
            str(detector_script),
            '--data-dir', str(data_dir),
            '--output', str(output_file)
        ]
        
        print_info("Running detection algorithms...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        # Print output
        if result.stdout:
            print(result.stdout)
        
        if output_file.exists():
            print_success(f"Events generated successfully: {output_file}")
            
            # Count events
            with open(output_file, 'r') as f:
                event_count = sum(1 for line in f if line.strip())
            print_info(f"Total events detected: {event_count}")
            
            return True
        else:
            print_error("Output file was not created")
            return False
            
    except subprocess.CalledProcessError as e:
        print_error(f"Event detection failed: {e}")
        if e.stderr:
            print(e.stderr)
        return False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return False


def copy_to_evidence(output_dir, dataset_type='test'):
    """Copy generated events to evidence folder"""
    print_header(f"COPYING TO EVIDENCE ({dataset_type.upper()})")
    
    script_dir = Path(__file__).parent.parent.parent
    source = output_dir / 'events.jsonl'
    destination = script_dir / 'evidence' / 'output' / dataset_type / 'events.jsonl'
    
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        print_success(f"Events copied to: {destination}")
        return True
    except Exception as e:
        print_error(f"Failed to copy to evidence: {e}")
        return False


def generate_summary_report(output_dir):
    """Generate a summary report of detected events"""
    print_header("GENERATING SUMMARY REPORT")
    
    import json
    from collections import Counter
    
    events_file = output_dir / 'events.jsonl'
    report_file = output_dir / 'summary_report.txt'
    
    try:
        # Load events
        events = []
        with open(events_file, 'r') as f:
            for line in f:
                if line.strip():
                    events.append(json.loads(line))
        
        # Analyze events
        event_counts = Counter(e['event_id'] for e in events)
        event_names = Counter(e['event_data'].get('event_name', 'Unknown') for e in events)
        
        # Station analysis
        stations = set()
        for e in events:
            if 'station_id' in e['event_data']:
                stations.add(e['event_data']['station_id'])
        
        # Generate report
        with open(report_file, 'w') as f:
            f.write("="*70 + "\n")
            f.write("PROJECT SENTINEL - EVENT DETECTION SUMMARY\n")
            f.write("="*70 + "\n\n")
            
            f.write(f"Total Events Detected: {len(events)}\n")
            f.write(f"Unique Stations: {len(stations)}\n\n")
            
            f.write("Event Distribution by ID:\n")
            f.write("-" * 40 + "\n")
            for event_id, count in sorted(event_counts.items()):
                f.write(f"  {event_id}: {count}\n")
            
            f.write("\nEvent Distribution by Name:\n")
            f.write("-" * 40 + "\n")
            for event_name, count in event_names.most_common():
                f.write(f"  {event_name}: {count}\n")
            
            f.write("\n" + "="*70 + "\n")
        
        print_success(f"Summary report generated: {report_file}")
        
        # Print to console
        print("\n" + "="*70)
        print("EVENT SUMMARY")
        print("="*70)
        print(f"Total Events: {len(events)}")
        print(f"Unique Stations: {len(stations)}")
        print("\nEvent Distribution:")
        for event_id, count in sorted(event_counts.items()):
            print(f"  {event_id}: {count}")
        print("="*70 + "\n")
        
        return True
    except Exception as e:
        print_error(f"Failed to generate report: {e}")
        return False


def launch_dashboard(events_file):
    """Launch the Streamlit dashboard"""
    print_header("LAUNCHING DASHBOARD")
    
    script_dir = Path(__file__).parent.parent.parent
    dashboard_script = script_dir / 'src' / 'dashboard' / 'dashboard_app.py'
    
    if not dashboard_script.exists():
        print_error(f"Dashboard script not found: {dashboard_script}")
        return False
    
    try:
        print_info(f"Starting dashboard with events file: {events_file}")
        print_info("Dashboard will open in your browser...")
        print_info("Press Ctrl+C to stop the dashboard")
        
        cmd = [
            sys.executable, '-m', 'streamlit', 'run',
            str(dashboard_script),
            '--',
            '--events-file', str(events_file)
        ]
        
        subprocess.run(cmd)
        return True
    except KeyboardInterrupt:
        print_info("\nDashboard stopped by user")
        return True
    except Exception as e:
        print_error(f"Failed to launch dashboard: {e}")
        return False


def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Project Sentinel - Automated Event Detection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default data directory
  python3 run_demo.py
  
  # Run with custom data directory
  python3 run_demo.py --data-dir /path/to/data
  
  # Run and launch dashboard
  python3 run_demo.py --launch-dashboard
        """
    )
    
    parser.add_argument(
        '--data-dir',
        type=str,
        default='../../data/input',
        help='Directory containing input data (default: ../../data/input)'
    )
    
    parser.add_argument(
        '--launch-dashboard',
        action='store_true',
        help='Launch the dashboard after event detection'
    )
    
    parser.add_argument(
        '--dashboard-only',
        action='store_true',
        help='Launch dashboard only (skip data processing)'
    )
    
    parser.add_argument(
        '--dataset-type',
        type=str,
        choices=['test', 'final'],
        default='test',
        help='Dataset type for evidence folder (default: test)'
    )
    
    args = parser.parse_args()
    
    # Setup paths
    script_dir = Path(__file__).parent
    output_dir = script_dir / 'results'
    
    print_header("PROJECT SENTINEL - AUTOMATED DETECTION")
    print_info(f"Working directory: {script_dir}")
    
    # Dashboard-only mode
    if args.dashboard_only or (args.launch_dashboard and not Path(args.data_dir).resolve().exists()):
        print_info("Dashboard-only mode")
        events_file = output_dir / 'events.jsonl'
        if not events_file.exists():
            print_error(f"Events file not found: {events_file}")
            print_info("Please run event detection first:")
            print_info("  python3 run_demo.py --data-dir /path/to/data")
            sys.exit(1)
        print_success(f"Found events file: {events_file}")
        launch_dashboard(events_file)
        sys.exit(0)
    
    # Normal processing mode
    data_dir = Path(args.data_dir).resolve()
    print_info(f"Data directory: {data_dir}")
    print_info(f"Output directory: {output_dir}")
    
    # Check if data directory exists
    if not data_dir.exists():
        print_error(f"Data directory not found: {data_dir}")
        print_info("Please provide a valid data directory with --data-dir")
        sys.exit(1)
    
    # Step 1: Setup environment
    if not setup_environment():
        print_error("Environment setup failed!")
        sys.exit(1)
    
    # Step 2: Run event detection
    if not run_event_detection(data_dir, output_dir):
        print_error("Event detection failed!")
        sys.exit(1)
    
    # Step 3: Copy to evidence
    if not copy_to_evidence(output_dir, args.dataset_type):
        print_error("Failed to copy to evidence folder!")
        sys.exit(1)
    
    # Step 4: Generate summary report
    if not generate_summary_report(output_dir):
        print_error("Failed to generate summary report!")
    
    # Step 5: Launch dashboard (optional)
    if args.launch_dashboard:
        events_file = output_dir / 'events.jsonl'
        launch_dashboard(events_file)
    else:
        print_info("\nTo launch the dashboard, run:")
        print_info(f"  python3 run_demo.py --dashboard-only")
    
    print_header("AUTOMATION COMPLETE")
    print_success("All tasks completed successfully!")
    print_info(f"Results are in: {output_dir}")
    print_info(f"Evidence files updated in: ../evidence/output/{args.dataset_type}/")


if __name__ == '__main__':
    main()
