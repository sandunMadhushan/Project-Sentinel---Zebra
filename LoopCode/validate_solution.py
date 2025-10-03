#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validation Script for Project Sentinel Solution
================================================

This script validates that all required components are in place
and properly configured before submission.

Usage:
    python validate_solution.py
"""

import os
from pathlib import Path
import re


class Colors:
    OK = '\033[92m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    INFO = '\033[94m'
    END = '\033[0m'


def print_ok(msg):
    print(f"{Colors.OK}[OK]{Colors.END} {msg}")


def print_warn(msg):
    print(f"{Colors.WARN}[WARN]{Colors.END} {msg}")


def print_fail(msg):
    print(f"{Colors.FAIL}[FAIL]{Colors.END} {msg}")


def print_info(msg):
    print(f"{Colors.INFO}[INFO]{Colors.END} {msg}")


def check_file_exists(file_path, description):
    """Check if a file exists"""
    if file_path.exists():
        print_ok(f"{description}: {file_path.name}")
        return True
    else:
        print_fail(f"{description} missing: {file_path}")
        return False


def check_directory_exists(dir_path, description):
    """Check if a directory exists"""
    if dir_path.exists() and dir_path.is_dir():
        print_ok(f"{description}: {dir_path.name}/")
        return True
    else:
        print_fail(f"{description} missing: {dir_path}")
        return False


def count_algorithm_tags(file_path):
    """Count @algorithm tags in a file"""
    if not file_path.exists():
        return 0
    
    count = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if '# @algorithm' in line:
                count += 1
    return count


def validate_structure():
    """Validate project structure"""
    print("\n" + "="*70)
    print("VALIDATING PROJECT STRUCTURE")
    print("="*70 + "\n")
    
    root = Path(__file__).parent
    all_ok = True
    
    # Check main files
    print("[1] Main Documentation Files:")
    all_ok &= check_file_exists(root / "README.md", "README")
    all_ok &= check_file_exists(root / "SUBMISSION_GUIDE.md", "SUBMISSION_GUIDE")
    all_ok &= check_file_exists(root / "requirements.txt", "requirements.txt")
    
    # Check src directory
    print("\n[2] Source Code Directory:")
    all_ok &= check_directory_exists(root / "src", "src directory")
    all_ok &= check_file_exists(root / "src" / "data_models.py", "data_models.py")
    all_ok &= check_file_exists(root / "src" / "event_detector.py", "event_detector.py")
    
    # Check algorithms
    print("\n[3] Algorithm Files:")
    algo_dir = root / "src" / "algorithms"
    all_ok &= check_directory_exists(algo_dir, "algorithms directory")
    all_ok &= check_file_exists(algo_dir / "fraud_detection.py", "fraud_detection.py")
    all_ok &= check_file_exists(algo_dir / "queue_analyzer.py", "queue_analyzer.py")
    all_ok &= check_file_exists(algo_dir / "inventory_monitor.py", "inventory_monitor.py")
    all_ok &= check_file_exists(algo_dir / "anomaly_detector.py", "anomaly_detector.py")
    
    # Check utils
    print("\n[4] Utilities:")
    utils_dir = root / "src" / "utils"
    all_ok &= check_directory_exists(utils_dir, "utils directory")
    all_ok &= check_file_exists(utils_dir / "helpers.py", "helpers.py")
    
    # Check dashboard
    print("\n[5] Dashboard:")
    dashboard_dir = root / "src" / "dashboard"
    all_ok &= check_directory_exists(dashboard_dir, "dashboard directory")
    all_ok &= check_file_exists(dashboard_dir / "dashboard_app.py", "dashboard_app.py")
    
    # Check evidence structure
    print("\n[6] Evidence Structure:")
    evidence_dir = root / "evidence"
    all_ok &= check_directory_exists(evidence_dir, "evidence directory")
    all_ok &= check_directory_exists(evidence_dir / "screenshots", "screenshots directory")
    all_ok &= check_directory_exists(evidence_dir / "output" / "test", "output/test directory")
    all_ok &= check_directory_exists(evidence_dir / "output" / "final", "output/final directory")
    all_ok &= check_directory_exists(evidence_dir / "executables", "executables directory")
    all_ok &= check_file_exists(evidence_dir / "executables" / "run_demo.py", "run_demo.py")
    
    return all_ok


def validate_algorithms():
    """Validate algorithm tagging"""
    print("\n" + "="*70)
    print("VALIDATING ALGORITHM TAGS")
    print("="*70 + "\n")
    
    root = Path(__file__).parent
    algo_dir = root / "src" / "algorithms"
    
    files = {
        "fraud_detection.py": 4,
        "queue_analyzer.py": 5,
        "inventory_monitor.py": 5,
        "anomaly_detector.py": 5
    }
    
    total_expected = sum(files.values())
    total_found = 0
    all_ok = True
    
    for filename, expected_count in files.items():
        file_path = algo_dir / filename
        count = count_algorithm_tags(file_path)
        total_found += count
        
        if count == expected_count:
            print_ok(f"{filename}: {count}/{expected_count} algorithms tagged")
        elif count > 0:
            print_warn(f"{filename}: {count}/{expected_count} algorithms tagged (mismatch)")
            all_ok = False
        else:
            print_fail(f"{filename}: No algorithm tags found")
            all_ok = False
    
    print(f"\n[INFO] Total algorithms found: {total_found}/{total_expected}")
    
    if total_found >= total_expected:
        print_ok("All algorithms are properly tagged!")
    else:
        print_warn(f"Expected {total_expected} algorithms, found {total_found}")
    
    return all_ok


def validate_submission_guide():
    """Check if SUBMISSION_GUIDE.md has been filled out"""
    print("\n" + "="*70)
    print("VALIDATING SUBMISSION GUIDE")
    print("="*70 + "\n")
    
    root = Path(__file__).parent
    guide_path = root / "SUBMISSION_GUIDE.md"
    
    if not guide_path.exists():
        print_fail("SUBMISSION_GUIDE.md not found")
        return False
    
    with open(guide_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for placeholders
    placeholders = [
        "<ENTER INFO>",
        "[Your Team Members Here]",
        "[Your Email Here]",
        "LoopCode"  # Team name should be filled in
    ]
    
    issues = []
    for placeholder in placeholders:
        if placeholder in content:
            issues.append(placeholder)
    
    if issues:
        print_warn("Found placeholders that need to be replaced:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print_ok("SUBMISSION_GUIDE.md appears to be filled out")
        return True


def validate_screenshots():
    """Check for dashboard screenshots"""
    print("\n" + "="*70)
    print("VALIDATING SCREENSHOTS")
    print("="*70 + "\n")
    
    root = Path(__file__).parent
    screenshots_dir = root / "evidence" / "screenshots"
    
    if not screenshots_dir.exists():
        print_fail("Screenshots directory not found")
        return False
    
    # Check for any image files
    image_files = list(screenshots_dir.glob("*.png")) + list(screenshots_dir.glob("*.jpg"))
    
    if len(image_files) == 0:
        print_warn("No screenshot files found in evidence/screenshots/")
        print_info("Add dashboard screenshots before final submission")
        return False
    else:
        print_ok(f"Found {len(image_files)} screenshot(s)")
        for img in image_files:
            print(f"  - {img.name}")
        return True


def main():
    """Main validation function"""
    print("\n" + "="*70)
    print("PROJECT SENTINEL - SOLUTION VALIDATION")
    print("="*70)
    
    results = {
        "Structure": validate_structure(),
        "Algorithms": validate_algorithms(),
        "Submission Guide": validate_submission_guide(),
        "Screenshots": validate_screenshots()
    }
    
    print("\n" + "="*70)
    print("VALIDATION SUMMARY")
    print("="*70 + "\n")
    
    for check, passed in results.items():
        if passed:
            print_ok(f"{check} validation passed")
        else:
            print_warn(f"{check} validation needs attention")
    
    print("\n" + "="*70)
    
    all_passed = all(results.values())
    
    if all_passed:
        print_ok("ALL VALIDATIONS PASSED - READY FOR SUBMISSION!")
    else:
        print_warn("Some validations need attention before submission")
        print_info("Review the warnings above and address them")
    
    print("="*70 + "\n")
    
    return all_passed


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
