# 🎯 Interactive Dashboard Guide

## 🆕 New Feature: In-Dashboard Data Selection & Detection

You can now **select data folders and run event detection directly from the dashboard UI** - no more terminal commands needed!

---

## 🚀 Quick Start

### Option 1: Simple Start (Recommended)

```bash
cd LoopCode
python start_dashboard.py
```

### Option 2: Direct Launch

```bash
cd LoopCode/src/dashboard
streamlit run dashboard_app.py
```

The dashboard will open at: **http://localhost:8502**

---

## 🎮 How to Use the New Features

### Step 1: Launch the Dashboard

```bash
python start_dashboard.py
```

### Step 2: Configure Data Source

1. Click on **"📁 Data Source Configuration"** (expanded by default on first run)
2. Choose your input method:
   - **Select from presets**: Choose from detected data folders (fastest)
   - **Browse folders**: Visual folder browser with navigation (NEW! 🆕)
   - **Enter custom path**: Type your own folder path

### Step 3: Select Data Folder

**Method A: Select from Presets** (Easiest!)

- Dropdown menu with auto-detected folders
- One-click selection

**Method B: Browse Folders** (NEW! Visual & Easy! 🆕)

- Navigate through folders visually
- Click folders to enter them
- ✅ Green checkmark shows valid data folders
- Click "Use This Folder" when ready
- **Full guide:** See [FOLDER_BROWSER_GUIDE.md](FOLDER_BROWSER_GUIDE.md)

**Method C: Enter Custom Path**

- Text box for direct path input
- Copy-paste friendly

### Step 4: Validate Folder

The dashboard will automatically check if your folder contains:

- ✅ `products_list.csv`
- ✅ `customer_data.csv`
- ✅ At least one `.jsonl` file (pos_transactions, rfid_readings, etc.)

### Step 5: Run Detection

1. Select dataset type: **test** or **final**
2. Click **"🚀 Run Event Detection"**
3. Wait for processing (progress shown with spinner)
4. Results load automatically when complete! 🎉

### Step 6: Analyze Results

Once detection completes:

- View key metrics (total events, fraud counts, etc.)
- Filter by event type or station
- Explore interactive charts
- Export data as needed

---

## 📋 Features Overview

### 🎯 Interactive Data Selection

- **Preset Folders**: Auto-detects common data locations
- **Custom Paths**: Enter any folder path
- **Validation**: Real-time folder content checking
- **Preview**: See files before running detection

### 🚀 One-Click Event Detection

- **In-Dashboard Processing**: No terminal needed!
- **Progress Tracking**: Real-time status updates
- **Auto-Reload**: Results load automatically
- **Error Handling**: Clear error messages

### 📊 Smart Result Management

- **Session State**: Remembers your selections
- **Existing Results**: Option to load previous runs
- **Quick Reset**: Clear and restart anytime

### 🔄 Backward Compatibility

Still works with command-line arguments:

```bash
streamlit run dashboard_app.py -- --events-file path/to/events.jsonl
```

---

## 🗂️ Folder Structure Requirements

Your data folder must contain:

```
your-data-folder/
├── products_list.csv          # Required
├── customer_data.csv          # Required
├── pos_transactions.jsonl     # At least one .jsonl required
├── rfid_readings.jsonl        # Optional
├── product_recognition.jsonl  # Optional
├── queue_monitoring.jsonl     # Optional
└── inventory_snapshots.jsonl  # Optional
```

---

## 💡 Usage Examples

### Example 1: Use Generated Test Data

```bash
# 1. Generate test data first (if not already done)
cd tools
python generate_test_data.py

# 2. Launch dashboard
cd ..
python start_dashboard.py

# 3. In the dashboard:
#    - Select "Generated Test Data" from presets
#    - Click "Run Event Detection"
#    - View results (should show ~231 events)
```

### Example 2: Use Competition Data

```bash
# 1. Launch dashboard
python start_dashboard.py

# 2. In the dashboard:
#    - Select "Competition Data (data/input)" from presets
#    - Choose dataset type: "test" or "final"
#    - Click "Run Event Detection"
```

### Example 3: Use Custom Folder

```bash
# 1. Launch dashboard
python start_dashboard.py

# 2. In the dashboard:
#    - Choose "Enter custom path"
#    - Type: /path/to/your/data/folder
#    - Click "Run Event Detection"
```

---

## 🎨 Dashboard Sections

### 1. Data Source Configuration (New! 🆕)

- Select input folder
- Validate data files
- Run event detection
- Load existing results

### 2. Key Metrics

- Total Events
- Fraud Events
- Queue Issues
- Inventory Discrepancies

### 3. Event Distribution

- Bar chart of event types
- Color-coded by category

### 4. Timeline Analysis

- Events over time
- Hourly patterns
- Date filtering

### 5. Station Analysis

- Performance by station
- Station-specific metrics

### 6. Fraud Detection

- Detailed fraud analytics
- Top customers/products

### 7. Detailed Event Table

- Sortable, filterable table
- All event details
- Export options

---

## 🔧 Troubleshooting

### Issue: "Missing required files"

**Solution:** Ensure your folder has:

- `products_list.csv`
- `customer_data.csv`
- At least one `.jsonl` file

### Issue: Detection takes too long

**Solution:**

- Large datasets (500+ transactions) may take 2-5 minutes
- Check terminal/console for progress
- Don't close the browser during processing

### Issue: "Detection failed"

**Solution:**

- Check that data files are properly formatted
- Ensure CSV files have required columns
- Look at error message for specific issue

### Issue: Dashboard not loading results

**Solution:**

- Click "🔄 Clear and Restart" button
- Reselect data folder
- Run detection again

### Issue: Can't find my data folder

**Solution:**

- Use absolute path (full path from drive root)
- Example: `E:/Projects/data` not `../data`
- Check folder actually exists and has correct files

---

## 🆚 Old Way vs New Way

### Old Way (Terminal-Based) ❌

```bash
# Step 1: Run detection in terminal
cd evidence/executables
python run_demo.py --data-dir /path/to/data --dataset-type test

# Step 2: Launch dashboard separately
python run_demo.py --dashboard-only

# Step 3: View results
# Open browser to localhost:8502
```

### New Way (All-in-One Dashboard) ✅

```bash
# Step 1: Launch dashboard
python start_dashboard.py

# Step 2-4: Everything in the UI!
# - Select folder from dropdown
# - Click "Run Event Detection"
# - Results load automatically
```

**Time Saved:** ~75% less clicking and typing! 🚀

---

## 📊 Expected Results

### With Generated Test Data (100 transactions)

- **Processing Time:** ~30 seconds
- **Events Detected:** ~231
- **Event Types:** 7 (E000, E002, E003, E004, E007, E008, E009)
- **Stations:** 4 (SCC1, SCC2, SCC3, SCC4)

### With Sample Data (minimal)

- **Processing Time:** ~5 seconds
- **Events Detected:** 1-5
- **Event Types:** 1-2
- **Stations:** 1

---

## 🎓 Tips & Best Practices

### 1. Start with Test Data

Use generated test data first to verify everything works:

```bash
cd tools && python generate_test_data.py
```

### 2. Use Presets When Possible

Presets are auto-validated and faster to select.

### 3. Check Folder Contents

Use the "📂 Folder Contents" expander to verify files before running.

### 4. Monitor Progress

Keep an eye on the spinner - it shows detection is running.

### 5. Save Your Results

Use the export buttons to save:

- CSV format (for Excel)
- JSON format (for processing)

### 6. Experiment with Filters

Try different event types and stations to explore data.

---

## 🔗 Related Files

- **Dashboard:** `LoopCode/src/dashboard/dashboard_app.py`
- **Quick Start:** `LoopCode/start_dashboard.py`
- **Detection Script:** `LoopCode/evidence/executables/run_demo.py`
- **Test Data Generator:** `LoopCode/tools/generate_test_data.py`

---

## 📞 Need Help?

### Can't find data folders?

- Check `data/input/` exists
- Run test data generator: `python tools/generate_test_data.py`

### Detection not starting?

- Ensure no other detection is running
- Check terminal for error messages
- Try restarting the dashboard

### Results look wrong?

- Verify data file formats (CSV/JSONL)
- Check for empty or corrupted files
- Generate fresh test data

---

## 🎉 What's New in v2.0

- ✅ Interactive folder selection
- ✅ In-dashboard event detection
- ✅ Real-time progress tracking
- ✅ Automatic result loading
- ✅ Preset folder detection
- ✅ Folder content preview
- ✅ Smart validation
- ✅ Session state management
- ✅ Quick restart option
- ✅ Backward compatibility

---

## 🚀 Next Steps

1. **Launch the dashboard:**

   ```bash
   python start_dashboard.py
   ```

2. **Select your data folder** from the UI

3. **Click "Run Event Detection"**

4. **Explore your results!** 🎊

---

**Team LoopCode**  
_Making event detection interactive and intuitive!_

October 2025
