# Getting Started with Project Sentinel

**LoopCode - Comprehensive Implementation Guide**

---

## Welcome!

This guide will walk you through everything you need to know to use the Project Sentinel solution effectively. Whether you're testing the system or preparing for final submission, this document has you covered.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Understanding the Solution](#understanding-the-solution)
4. [Running Your First Detection](#running-your-first-detection)
5. [Using the Dashboard](#using-the-dashboard)
6. [Working with Data](#working-with-data)
7. [Competition Preparation](#competition-preparation)
8. [Best Practices](#best-practices)

---

## Prerequisites

### System Requirements

**Required:**
- Python 3.9 or higher
- 2GB RAM minimum
- 500MB free disk space
- Internet connection (for dependency installation)

**Recommended:**
- Python 3.10+
- 4GB RAM
- Modern web browser (Chrome, Firefox, Edge)

### Check Your Python Version

```bash
python --version
# Should show: Python 3.9.x or higher
```

If Python is not installed or version is too old, download from [python.org](https://www.python.org/downloads/).

---

## Initial Setup

### Step 1: Navigate to Project Directory

```bash
cd /path/to/Project-Sentinel---Zebra/LoopCode
```

### Step 2: Install Dependencies

Dependencies are automatically installed when you run the detection script, but you can manually install them:

```bash
pip install -r requirements.txt
```

**Required packages:**
- streamlit>=1.28.0
- pandas>=2.0.0
- numpy>=1.24.0
- plotly>=5.14.0

### Step 3: Verify Installation

```bash
python -c "import streamlit, pandas, numpy; print('All dependencies installed!')"
```

---

## Understanding the Solution

### Architecture Overview

Our solution consists of four main components:

**1. Data Models (`src/data_models.py`)**
- Defines data structures for all sensor types
- Handles data parsing and validation
- Provides type-safe interfaces

**2. Event Detector (`src/event_detector.py`)**
- Orchestrates the detection pipeline
- Coordinates all algorithms
- Aggregates and outputs events

**3. Detection Algorithms (`src/algorithms/`)**
- **Fraud Detection:** 4 algorithms
- **Queue Analysis:** 5 algorithms
- **Inventory Monitoring:** 5 algorithms
- **Anomaly Detection:** 5 algorithms

**4. Dashboard (`src/dashboard/dashboard_app.py`)**
- Interactive visualization
- Real-time analytics
- Data exploration tools

### Event Types

The system detects 10 different event types:

| ID | Name | Description |
|----|------|-------------|
| E000 | Success Operation | Normal, validated transaction |
| E001 | Scanner Avoidance | Items detected but not scanned |
| E002 | Barcode Switching | Wrong barcode scanned |
| E003 | Weight Discrepancies | Weight doesn't match expected |
| E004 | System Crashes | Unexpected downtime |
| E005 | Long Queue Length | Excessive queue buildup |
| E006 | Long Wait Time | Customer wait time too long |
| E007 | Inventory Discrepancy | Stock count mismatch |
| E008 | Staffing Needs | Additional staff required |
| E009 | Station Actions | Station open/close needed |

---

## Running Your First Detection

### Method 1: Dashboard (Recommended for Beginners)

**Step 1:** Launch the dashboard
```bash
python start_dashboard.py
```

**Step 2:** Open your browser
- URL: http://localhost:8501
- Dashboard should load automatically

**Step 3:** Configure data source
- Default source is pre-selected: `src/data/input`
- Or click "📂 Open Folder Picker" to choose another folder

**Step 4:** Run detection
- Click "🚀 Run Event Detection"
- Watch progress indicator
- Results appear automatically (1-2 minutes)

**Step 5:** Explore results
- View key metrics at the top
- Scroll through charts and visualizations
- Use filters to drill down
- Export data if needed

### Method 2: Command Line (For Advanced Users)

**Basic command:**
```bash
cd evidence/executables
python run_demo.py --data-dir ../../src/data/input --dataset-type test
```

**What this does:**
1. Loads data from specified directory
2. Runs all 19 detection algorithms
3. Generates `events.jsonl` with results
4. Creates summary report
5. Copies outputs to evidence folders

**View results:**
```bash
# View events file
cat results/events.jsonl

# View summary
cat results/summary_report.txt

# Count events
wc -l results/events.jsonl
```

---

## Using the Dashboard

### Dashboard Layout

**Top Section: Metrics**
- Total Events
- Fraud Events
- Queue Issues
- Stations Monitored

**Middle Section: Visualizations**
- Event Distribution (Bar Chart)
- Event Names (Top 10)
- Timeline Analysis (Line Chart)
- Station Analysis

**Bottom Section: Details**
- Fraud Analysis
- Recent Events Table
- Export Options

### Interactive Features

**Filtering:**
1. Use sidebar to select event types
2. Filter by station ID
3. Apply date/time ranges

**Exploration:**
- Hover over charts for details
- Click legend items to toggle
- Scroll through event tables
- Sort columns in tables

**Exporting:**
- Click "📥 Download as CSV"
- Or "📥 Download as JSON"
- Files download to your browser

### Tips for Dashboard Use

1. **Start with Overview:** Check key metrics first
2. **Use Filters:** Narrow down to specific events
3. **Analyze Patterns:** Look at timeline for trends
4. **Drill Down:** Use table for detailed investigation
5. **Export Data:** Save for further analysis

---

## Working with Data

### Data Structure

Your data folder should contain:

**Required CSV Files:**
- `products_list.csv` - Product catalog
- `customer_data.csv` - Customer profiles

**Required JSONL Files (at least one):**
- `pos_transactions.jsonl` - Point of sale data
- `rfid_readings.jsonl` - RFID sensor data
- `product_recognition.jsonl` - Vision system data
- `queue_monitoring.jsonl` - Queue metrics
- `inventory_snapshots.jsonl` - Stock levels

### CSV Format

**products_list.csv:**
```csv
SKU,product_name,quantity,EPC_range,barcode,weight,price
P001,Product Name,1,EPC001-EPC001,BAR001,100.0,9.99
```

**customer_data.csv:**
```csv
customer_id,name,contact
C001,John Doe,john@example.com
```

### JSONL Format

Each line is a valid JSON object:

```json
{"timestamp":"2025-10-04T12:00:00","station_id":"SCC1","transaction_id":"T001","items":[]}
```

### Data Validation

The system automatically validates:
- File existence
- CSV header format
- JSON syntax
- Required fields
- Data types

If validation fails, you'll see clear error messages indicating the issue.

---

## Competition Preparation

### For Test Dataset

**Step 1:** Receive test dataset from judges

**Step 2:** Run detection
```bash
cd evidence/executables
python run_demo.py --data-dir /path/to/test/data --dataset-type test
```

**Step 3:** Verify output
```bash
# Check events file exists
ls -lh evidence/output/test/events.jsonl

# Validate JSON format
python -c "import json; [json.loads(line) for line in open('evidence/output/test/events.jsonl')]"
```

**Step 4:** Review results in dashboard
```bash
python run_demo.py --dashboard-only
```

**Step 5:** Take screenshots
- Dashboard overview
- Event distribution chart
- Fraud analysis section
- Timeline view
- Save to `evidence/screenshots/`

### For Final Dataset

**Timing:** Run 10 minutes before submission deadline

**Command:**
```bash
cd evidence/executables
python run_demo.py --data-dir /path/to/final/data --dataset-type final
```

**Verify:**
- Output in `evidence/output/final/events.jsonl`
- File is valid JSON
- Results are reasonable
- Summary report looks correct

### Submission Checklist

Before submitting:

**Documentation:**
- [ ] Updated team name in SUBMISSION_GUIDE.md
- [ ] Added team member names
- [ ] Updated contact information
- [ ] Reviewed all documentation

**Testing:**
- [ ] Tested with test dataset
- [ ] Validated output format
- [ ] Verified all algorithms are tagged
- [ ] Tested dashboard functionality

**Evidence:**
- [ ] Added dashboard screenshots
- [ ] Generated both test and final outputs
- [ ] Included summary reports
- [ ] Verified file structure

**Packaging:**
- [ ] Renamed folder to Team##_sentinel
- [ ] Created ZIP archive
- [ ] Tested ZIP extraction
- [ ] Ready for upload

---

## Best Practices

### Development

1. **Test Early and Often:** Don't wait until deadline
2. **Validate Data:** Ensure data format is correct
3. **Check Logs:** Monitor console output
4. **Use Version Control:** Keep track of changes
5. **Document Changes:** Note any modifications

### Performance

1. **Monitor Resources:** Check CPU/memory usage
2. **Optimize Data:** Remove unnecessary files
3. **Batch Processing:** Use appropriate dataset sizes
4. **Cache Results:** Dashboard caches for faster loading

### Troubleshooting

1. **Read Error Messages:** They're usually informative
2. **Check File Paths:** Ensure correct absolute/relative paths
3. **Verify Dependencies:** Make sure all packages are installed
4. **Review Documentation:** Answers are often in the docs
5. **Test Incrementally:** Isolate issues by testing components

---

## Common Workflows

### Scenario 1: First-Time User

```bash
# 1. Navigate to project
cd LoopCode

# 2. Launch dashboard
python start_dashboard.py

# 3. Run detection (using dashboard UI)
# Click "Run Event Detection" button

# 4. Explore results
# Use dashboard filters and charts
```

### Scenario 2: Quick Testing

```bash
# Run detection via command line
cd evidence/executables
python run_demo.py --data-dir ../../src/data/input --dataset-type test

# View results
cat results/summary_report.txt
```

### Scenario 3: Custom Data Analysis

```bash
# 1. Prepare your data folder
# 2. Launch dashboard
python start_dashboard.py

# 3. Use folder picker to select your data
# 4. Run detection
# 5. Export results for further analysis
```

### Scenario 4: Competition Submission

```bash
# 1. Update documentation
# Edit SUBMISSION_GUIDE.md

# 2. Run test dataset
cd evidence/executables
python run_demo.py --data-dir /path/to/test --dataset-type test

# 3. Capture screenshots
python run_demo.py --dashboard-only
# Take screenshots

# 4. Run final dataset (at deadline)
python run_demo.py --data-dir /path/to/final --dataset-type final

# 5. Package and submit
cd ../..
zip -r Team01_sentinel.zip .
```

---

## Next Steps

Now that you understand the system:

1. **Try it out:** Run your first detection
2. **Explore the dashboard:** Get familiar with the interface
3. **Review the code:** Understanding aids debugging
4. **Prepare for competition:** Update documentation
5. **Practice:** Test with different datasets

---

## Additional Resources

- **README.md** - Complete system documentation
- **QUICK_START.md** - 5-minute quick reference
- **SUBMISSION_GUIDE.md** - Detailed submission instructions
- **DOCUMENTATION.md** - Technical implementation details
- **Source code comments** - Inline documentation

---

## Support

If you encounter issues:

1. Check this guide first
2. Review error messages carefully
3. Verify data format and file paths
4. Ensure all dependencies are installed
5. Check Python version compatibility

---

**You're Ready to Start!** 🚀

Begin with: `python start_dashboard.py`

Good luck with the competition! 🏆

---

*LoopCode - Project Sentinel*  
*October 2025*
