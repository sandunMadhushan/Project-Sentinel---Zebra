# Quick Start Guide# 🚀 Quick Start - Updated Dashboard



**Project Sentinel - LoopCode Solution**## ✅ What's Done



---1. **Old data removed:**

   - ❌ `data/input/*` (old competition data)

## ⚡ 5-Minute Quick Start   - ❌ `tools/generated_test_data`

   - ❌ `tools/input`

### Option 1: Interactive Dashboard (Recommended)

2. **Dashboard updated:**

```bash   - ✅ Default preset: `src/data/input` (your new data)

cd LoopCode   - ✅ Only 2 input methods: Presets + Folder Picker

python start_dashboard.py   - ❌ Custom path input removed

```

3. **CSV parsing fixed:**

**What happens:**   - ✅ Handles hidden whitespace in CSV headers

1. Dashboard opens in browser (http://localhost:8501)   - ✅ Successfully detects 554 events from your data!

2. Data source pre-selected: `src/data/input`

3. Click "🚀 Run Event Detection"---

4. View 554 detected events!

## 🎯 Start Dashboard Now

### Option 2: Command Line

### Option 1: Quick Start (Recommended)

```bash```bash

cd evidence/executablescd /e/Other\ Projects/other-clones/Project-Sentinel---Zebra/LoopCode

python run_demo.py --data-dir ../../src/data/input --dataset-type testpython start_dashboard.py

``````



**Output:**### Option 2: Direct Start

- `results/events.jsonl` - Detected events```bash

- `results/summary_report.txt` - Analysis summarycd /e/Other\ Projects/other-clones/Project-Sentinel---Zebra/LoopCode

streamlit run src/dashboard/dashboard_app.py

---```



## 📊 Dashboard Usage---



### Step 1: Launch## 📊 Using the Dashboard

```bash

python start_dashboard.py### Step 1: Data Source Selection

```When dashboard opens, you'll see:

- **"New Data (src/data/input)"** - Already selected by default!

### Step 2: Select Data- Or click **"📂 Open Folder Picker"** to browse

- **Default:** "New Data (src/data/input)" ✅ Pre-selected

- **Browse:** Click "📂 Open Folder Picker"### Step 2: Run Detection

1. Click **"🚀 Run Event Detection"**

### Step 3: Detect Events2. Wait 1-2 minutes

1. Click "🚀 Run Event Detection"3. Results load automatically!

2. Wait ~1-2 minutes

3. Results appear automatically### Step 3: Explore Results

- View 554 detected events

### Step 4: Explore- Filter by event type

- **Metrics:** Total events, fraud counts, queue issues- See fraud analysis

- **Charts:** Event distribution, timeline analysis- Export as CSV/JSON

- **Filters:** Event type, station, time range

- **Export:** CSV or JSON download---



---## 📁 Your Data



## 📁 Your Data**Location:** `src/data/input`



**Location:** `src/data/input`**Files:**

- products_list.csv (50 products)

**Files:**- customer_data.csv (60 customers)

- `products_list.csv` (50 products)- pos_transactions.jsonl (252 transactions)

- `customer_data.csv` (60 customers)- rfid_readings.jsonl (5,753 readings)

- `pos_transactions.jsonl` (252 transactions)- product_recognition.jsonl (264 recognitions)

- `rfid_readings.jsonl` (5,753 readings)- queue_monitoring.jsonl (7,181 measurements)

- `product_recognition.jsonl` (264 recognitions)- inventory_snapshots.jsonl (13 snapshots)

- `queue_monitoring.jsonl` (7,181 measurements)

- `inventory_snapshots.jsonl` (13 snapshots)**Events Detected:** 554 total

- E002: 228 (Barcode Switching)

**Expected Results:** 554 events- E003: 9 (Weight Discrepancies)

- E002: 228 (Barcode Switching)- E005: 117 (Queue Management)

- E003: 9 (Weight Discrepancies)- E008: 195 (Anomaly Detection)

- E005: 117 (Queue Management)- E009: 5 (System Crashes)

- E008: 195 (Anomaly Detection)

- E009: 5 (System Crashes)---



---## ✨ Ready to Go!



## 🎯 Competition DatasetsEverything is configured and tested. Just run:



### Test Dataset```bash

```bashpython start_dashboard.py

cd evidence/executables```

python run_demo.py --data-dir /path/to/test/data --dataset-type test

```Then explore your 554 events! 🎉


### Final Dataset
```bash
python run_demo.py --data-dir /path/to/final/data --dataset-type final
```

**Results saved to:**
- Test: `evidence/output/test/events.jsonl`
- Final: `evidence/output/final/events.jsonl`

---

## 🔧 Command Options

```bash
python run_demo.py [OPTIONS]
```

**Options:**
- `--data-dir PATH` - Input data directory
- `--dataset-type TYPE` - `test` or `final`
- `--launch-dashboard` - Open dashboard after detection
- `--dashboard-only` - View existing results only

**Examples:**
```bash
# Run detection and open dashboard
python run_demo.py --data-dir ../../src/data/input --launch-dashboard

# View existing results
python run_demo.py --dashboard-only
```

---

## ✅ Verification

### Check Output Format
```bash
# View first event
head -1 results/events.jsonl

# Validate JSON format
python -c "import json; [json.loads(line) for line in open('results/events.jsonl')]"
```

### Expected JSON Structure
```json
{
  "timestamp": "2025-10-04T12:30:00",
  "event_id": "E002",
  "event_data": {
    "event_name": "Barcode Switching Detected",
    "station_id": "SCC1",
    "customer_id": "C123",
    "details": {}
  }
}
```

---

## 🚨 Troubleshooting

### Dashboard Won't Start
```bash
# Install Streamlit
pip install streamlit

# Try direct start
streamlit run src/dashboard/dashboard_app.py
```

### No Events Detected
- Verify data files exist in input folder
- Check CSV files for proper formatting
- Review console output for errors

### Import Errors
```bash
# Install dependencies
pip install -r requirements.txt
```

---

## 📖 More Information

- **README.md** - Complete documentation
- **START_HERE.md** - Detailed getting started guide
- **SUBMISSION_GUIDE.md** - Submission preparation
- **DOCUMENTATION.md** - Technical details

---

## 💡 Tips

1. **Use Dashboard:** Easiest way to interact with the system
2. **Check Data:** Ensure files are in correct format
3. **Monitor Progress:** Watch terminal output during detection
4. **Explore Results:** Use dashboard filters for analysis
5. **Export Data:** Save results for further analysis

---

**Ready in 5 minutes!** 🚀

Run `python start_dashboard.py` and you're all set!
