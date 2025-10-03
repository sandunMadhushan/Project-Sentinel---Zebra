# Team 01 - Project Sentinel Submission

## Team Details
- **Team name:** Team 01
- **Members:** [Your Team Members Here]
- **Primary contact email:** [Your Email Here]

## Judge Run Command

Judges will `cd evidence/executables/` and run **one command** on Ubuntu 24.04:

```bash
python3 run_demo.py --data-dir /path/to/test/data --dataset-type test
```

For the final dataset:

```bash
python3 run_demo.py --data-dir /path/to/final/data --dataset-type final
```

### What the Script Does

The `run_demo.py` script automates the entire analysis workflow:

1. **Installs dependencies** - Automatically installs pandas, streamlit, plotly
2. **Loads input data** - Reads all JSONL and CSV files from the data directory
3. **Runs detection algorithms** - Executes all 10+ detection algorithms
4. **Generates events.jsonl** - Creates output in the correct format
5. **Copies to evidence/** - Automatically places files in evidence/output/test or evidence/output/final
6. **Creates summary report** - Generates detailed statistics

### Optional: Launch Dashboard

To view the interactive dashboard after detection:

```bash
python3 run_demo.py --data-dir /path/to/data --launch-dashboard
```

## System Requirements

- **Python:** 3.9 or higher
- **RAM:** 2GB minimum
- **Disk:** 500MB for dependencies and output
- **Internet:** Required for initial dependency installation only

## Output Structure

After running, the script creates:

```
evidence/executables/results/
├── events.jsonl              # Main output file
└── summary_report.txt        # Statistical summary

evidence/output/
├── test/
│   └── events.jsonl         # Test dataset results
└── final/
    └── events.jsonl         # Final dataset results
```

## Checklist Before Zipping and Submitting

- [x] **Algorithms tagged** with `# @algorithm Name | Purpose` comments (10+ algorithms)
- [x] **Evidence artifacts** present in `evidence/`:
  - [x] executables/run_demo.py - Automation script
  - [ ] screenshots/ - Dashboard screenshots (add before submission)
  - [x] output/test/events.jsonl - Will be generated
  - [x] output/final/events.jsonl - Will be generated
- [x] **Source code complete** under `src/`:
  - [x] data_models.py - Data structures
  - [x] event_detector.py - Main detection logic
  - [x] algorithms/ - All detection algorithms
    - [x] fraud_detection.py - 4 algorithms
    - [x] queue_analyzer.py - 5 algorithms
    - [x] inventory_monitor.py - 5 algorithms
    - [x] anomaly_detector.py - 5 algorithms
  - [x] utils/helpers.py - Helper functions
  - [x] dashboard/dashboard_app.py - Interactive dashboard

## Algorithm Summary

Our solution implements **19 algorithms** across 4 categories:

### Fraud Detection (4 algorithms)
1. Scanner Avoidance Detection - Compare RFID vs POS scans
2. Barcode Switching Detection - Vision system vs actual scans
3. Weight Verification - Detect weight discrepancies
4. Success Operation Detection - Identify normal transactions

### Queue Analysis (5 algorithms)
5. Queue Threshold Analysis - Monitor queue length
6. Wait Time Threshold Analysis - Monitor customer wait times
7. Staffing Requirements Prediction - Predict staffing needs
8. Station Status Management - Recommend opening/closing stations
9. Queue Trend Analysis - Analyze patterns over time

### Inventory Monitoring (5 algorithms)
10. Inventory Reconciliation - Compare expected vs actual stock
11. Stock Level Monitoring - Low stock alerts
12. Inventory Velocity Analysis - Calculate turnover rates
13. Shrinkage Detection - Detect unexplained losses
14. Reorder Point Calculation - Optimal reorder timing

### Anomaly Detection (5 algorithms)
15. System Downtime Detection - Detect crashes and gaps
16. Statistical Anomaly Detection - Z-score based outliers
17. Pattern-based Anomaly Detection - Deviation from expected patterns
18. Behavioral Anomaly Detection - Unusual customer behavior
19. Correlation Analysis - Multi-metric anomaly detection

## Architecture Overview

```
Input Data (JSONL/CSV)
         ↓
    Data Models (data_models.py)
         ↓
    Event Detector (event_detector.py)
         ↓
    ┌────────────┬─────────────┬────────────────┬──────────────┐
    │  Fraud     │   Queue     │   Inventory    │   Anomaly    │
    │ Detection  │  Analysis   │   Monitoring   │  Detection   │
    └────────────┴─────────────┴────────────────┴──────────────┘
         ↓
    Detected Events
         ↓
    events.jsonl + Dashboard
```

## Key Features

✅ **Comprehensive Detection** - 19 algorithms covering all event types
✅ **Automated Pipeline** - Single command execution
✅ **Interactive Dashboard** - Real-time visualization with Streamlit
✅ **Modular Design** - Easy to extend and maintain
✅ **Well Documented** - Clear comments and documentation
✅ **Robust Error Handling** - Graceful failure management

## Detected Event Types

| Event ID | Event Name | Description |
|----------|------------|-------------|
| E000 | Success Operation | Normal checkout completed |
| E001 | Scanner Avoidance | Item not scanned |
| E002 | Barcode Switching | Wrong barcode scanned |
| E003 | Weight Discrepancies | Weight mismatch |
| E004 | Unexpected Systems Crash | System downtime |
| E005 | Long Queue Length | Too many customers |
| E006 | Long Wait Time | Excessive wait time |
| E007 | Inventory Discrepancy | Stock count mismatch |
| E008 | Staffing Needs | Additional staff required |
| E009 | Checkout Station Action | Open/close station |

## Testing Instructions

To test the solution locally:

```bash
# 1. Navigate to executables
cd evidence/executables

# 2. Run with sample data
python3 run_demo.py --data-dir ../../data/input

# 3. Check output
ls -l results/events.jsonl

# 4. Launch dashboard
python3 run_demo.py --data-dir ../../data/input --launch-dashboard
```

## Dashboard Screenshots

Dashboard screenshots will be added to `evidence/screenshots/` showing:
- Event distribution charts
- Timeline analysis
- Station performance
- Fraud detection metrics
- Real-time monitoring interface

## Notes for Judges

- The solution is entirely self-contained and requires no manual configuration
- All dependencies are installed automatically
- Output files are placed in the correct evidence folders automatically
- The dashboard provides interactive exploration of detected events
- All algorithms are properly tagged for automated scoring
- Code follows Python best practices and PEP 8 style guide

## Contact

For questions or issues, please contact: [Your Email]

---

**Team 01 - Project Sentinel** | October 2025
