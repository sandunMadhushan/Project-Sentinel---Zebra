# 🚀 Quick Start Guide# Quick Start Guide# 🚀 Quick Start - Updated Dashboard



**Project Sentinel - LoopCode Solution**



---**Project Sentinel - LoopCode Solution**## ✅ What's Done



## ⚡ 5-Minute Quick Start



### Option 1: Interactive Dashboard (Recommended)---1. **Old data removed:**



```bash   - ❌ `data/input/*` (old competition data)

cd LoopCode

python start_dashboard.py## ⚡ 5-Minute Quick Start   - ❌ `tools/generated_test_data`

```

   - ❌ `tools/input`

**What happens:**

1. Dashboard opens in browser (http://localhost:8501)### Option 1: Interactive Dashboard (Recommended)

2. Data source pre-selected: `src/data/input`

3. Click "🚀 Run Event Detection"2. **Dashboard updated:**

4. View **572 detected events!**

```bash   - ✅ Default preset: `src/data/input` (your new data)

### Option 2: Command Line

cd LoopCode   - ✅ Only 2 input methods: Presets + Folder Picker

```bash

cd evidence/executablespython start_dashboard.py   - ❌ Custom path input removed

python run_demo.py --data-dir ../../src/data/input --dataset-type test

``````



**Output:**3. **CSV parsing fixed:**

- `results/events.jsonl` - Detected events (572 events)

- `results/summary_report.txt` - Analysis summary**What happens:**   - ✅ Handles hidden whitespace in CSV headers



---1. Dashboard opens in browser (http://localhost:8501)   - ✅ Successfully detects 554 events from your data!



## 📊 Dashboard Usage2. Data source pre-selected: `src/data/input`



### Step 1: Launch3. Click "🚀 Run Event Detection"---

```bash

python start_dashboard.py4. View 554 detected events!

```

## 🎯 Start Dashboard Now

### Step 2: Select Data

- **Default:** "New Data (src/data/input)" ✅ Pre-selected### Option 2: Command Line

- **Browse:** Click "📂 Open Folder Picker"

### Option 1: Quick Start (Recommended)

### Step 3: Detect Events

1. Click "🚀 Run Event Detection"```bash```bash

2. Wait ~1-2 minutes

3. Results appear automaticallycd evidence/executablescd /e/Other\ Projects/other-clones/Project-Sentinel---Zebra/LoopCode



### Step 4: Explorepython run_demo.py --data-dir ../../src/data/input --dataset-type testpython start_dashboard.py

- **Metrics:** Total events, fraud counts, queue issues

- **Charts:** Event distribution, timeline analysis``````

- **Filters:** Event type, station, time range

- **Export:** CSV or JSON download



---**Output:**### Option 2: Direct Start



## 📁 Your Data- `results/events.jsonl` - Detected events```bash



**Location:** `src/data/input`- `results/summary_report.txt` - Analysis summarycd /e/Other\ Projects/other-clones/Project-Sentinel---Zebra/LoopCode



**Files:**streamlit run src/dashboard/dashboard_app.py

- products_list.csv (50 products)

- customer_data.csv (60 customers)---```

- pos_transactions.jsonl (252 transactions)

- rfid_readings.jsonl (5,753 readings)

- product_recognition.jsonl (264 recognitions)

- queue_monitoring.jsonl (7,181 measurements)## 📊 Dashboard Usage---

- inventory_snapshots.jsonl (13 snapshots)



**Expected Results:** 572 events

- **E001**: 9 (Scanner Avoidance - Vision-based)### Step 1: Launch## 📊 Using the Dashboard

- **E002**: 228 (Barcode Switching)

- **E003**: 10 (Weight Discrepancies)```bash

- **E005**: 117 (Long Queue Length)

- **E007**: 8 (Inventory Discrepancy)python start_dashboard.py### Step 1: Data Source Selection

- **E008**: 195 (Staffing Needs)

- **E009**: 5 (Station Actions)```When dashboard opens, you'll see:



---- **"New Data (src/data/input)"** - Already selected by default!



## 🎯 Competition Datasets### Step 2: Select Data- Or click **"📂 Open Folder Picker"** to browse



### Test Dataset- **Default:** "New Data (src/data/input)" ✅ Pre-selected

```bash

cd evidence/executables- **Browse:** Click "📂 Open Folder Picker"### Step 2: Run Detection

python run_demo.py --data-dir /path/to/test/data --dataset-type test

```1. Click **"🚀 Run Event Detection"**



### Final Dataset### Step 3: Detect Events2. Wait 1-2 minutes

```bash

python run_demo.py --data-dir /path/to/final/data --dataset-type final1. Click "🚀 Run Event Detection"3. Results load automatically!

```

2. Wait ~1-2 minutes

**Results saved to:**

- Test: `evidence/output/test/events.jsonl`3. Results appear automatically### Step 3: Explore Results

- Final: `evidence/output/final/events.jsonl`

- View 554 detected events

---

### Step 4: Explore- Filter by event type

## 🔧 Command Options

- **Metrics:** Total events, fraud counts, queue issues- See fraud analysis

```bash

python run_demo.py [OPTIONS]- **Charts:** Event distribution, timeline analysis- Export as CSV/JSON

```

- **Filters:** Event type, station, time range

**Options:**

- `--data-dir PATH` - Input data directory- **Export:** CSV or JSON download---

- `--dataset-type TYPE` - `test` or `final`

- `--launch-dashboard` - Open dashboard after detection

- `--dashboard-only` - View existing results only

---## 📁 Your Data

**Examples:**

```bash

# Run detection and open dashboard

python run_demo.py --data-dir ../../src/data/input --launch-dashboard## 📁 Your Data**Location:** `src/data/input`



# View existing results

python run_demo.py --dashboard-only

```**Location:** `src/data/input`**Files:**



---- products_list.csv (50 products)



## ✅ Verification**Files:**- customer_data.csv (60 customers)



### Check Output Format- `products_list.csv` (50 products)- pos_transactions.jsonl (252 transactions)

```bash

# View first event- `customer_data.csv` (60 customers)- rfid_readings.jsonl (5,753 readings)

head -1 results/events.jsonl

- `pos_transactions.jsonl` (252 transactions)- product_recognition.jsonl (264 recognitions)

# Validate JSON format

python -c "import json; [json.loads(line) for line in open('results/events.jsonl')]"- `rfid_readings.jsonl` (5,753 readings)- queue_monitoring.jsonl (7,181 measurements)

```

- `product_recognition.jsonl` (264 recognitions)- inventory_snapshots.jsonl (13 snapshots)

### Expected JSON Structure

```json- `queue_monitoring.jsonl` (7,181 measurements)

{

  "timestamp": "2025-10-04T12:30:00",- `inventory_snapshots.jsonl` (13 snapshots)**Events Detected:** 554 total

  "event_id": "E002",

  "event_data": {- E002: 228 (Barcode Switching)

    "event_name": "Barcode Switching Detected",

    "station_id": "SCC1",**Expected Results:** 554 events- E003: 9 (Weight Discrepancies)

    "customer_id": "C123",

    "details": {}- E002: 228 (Barcode Switching)- E005: 117 (Queue Management)

  }

}- E003: 9 (Weight Discrepancies)- E008: 195 (Anomaly Detection)

```

- E005: 117 (Queue Management)- E009: 5 (System Crashes)

---

- E008: 195 (Anomaly Detection)

## 🚨 Troubleshooting

- E009: 5 (System Crashes)---

### Dashboard Won't Start

```bash

# Install dependencies

pip install -r requirements.txt---## ✨ Ready to Go!



# Try direct start

streamlit run src/dashboard/dashboard_app.py

```## 🎯 Competition DatasetsEverything is configured and tested. Just run:



### No Events Detected

- Verify data files exist in input folder

- Check CSV files for proper formatting (UTF-8 encoding)### Test Dataset```bash

- Review console output for errors

```bashpython start_dashboard.py

### Import Errors

```bashcd evidence/executables```

# Install all dependencies

pip install -r requirements.txtpython run_demo.py --data-dir /path/to/test/data --dataset-type test

```

```Then explore your 554 events! 🎉

---



## 📖 More Information### Final Dataset

```bash

- **[README.md](README.md)** - Complete documentationpython run_demo.py --data-dir /path/to/final/data --dataset-type final

- **[START_HERE.md](START_HERE.md)** - Detailed getting started guide```

- **[SUBMISSION_GUIDE.md](SUBMISSION_GUIDE.md)** - Submission preparation

- **[DOCUMENTATION.md](DOCUMENTATION.md)** - Technical details**Results saved to:**

- **[FINAL_STATUS.md](FINAL_STATUS.md)** - Current project status- Test: `evidence/output/test/events.jsonl`

- Final: `evidence/output/final/events.jsonl`

---

---

## 💡 Tips

## 🔧 Command Options

1. **Use Dashboard:** Easiest way to interact with the system

2. **Check Data:** Ensure files are in correct format (CSV UTF-8, JSONL)```bash

3. **Monitor Progress:** Watch terminal output during detectionpython run_demo.py [OPTIONS]

4. **Explore Results:** Use dashboard filters for detailed analysis```

5. **Export Data:** Save results for further analysis

**Options:**

---- `--data-dir PATH` - Input data directory

- `--dataset-type TYPE` - `test` or `final`

## 🎯 Latest Results (October 2025)- `--launch-dashboard` - Open dashboard after detection

- `--dashboard-only` - View existing results only

**Total Events:** 572  

**Event Types Detected:** 7/10 actively detecting  **Examples:**

**Processing Time:** ~60 seconds  ```bash

**Status:** Production Ready ✅# Run detection and open dashboard

python run_demo.py --data-dir ../../src/data/input --launch-dashboard

**Key Improvements:**

- ✅ Vision-based scanner avoidance (+9 events)# View existing results

- ✅ Optimized weight tolerance 10% (+1 event)python run_demo.py --dashboard-only

- ✅ Enhanced inventory monitoring (+8 events)```

- ✅ Dual-layer fraud detection

- ✅ Industry-standard thresholds---



---## ✅ Verification



**Ready in 5 minutes!** 🚀### Check Output Format

```bash

Run `python start_dashboard.py` and you're all set!# View first event

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
