# 🔧 Dashboard Troubleshooting Guide

## ✅ Fix Applied: Path Format Issues

### Problem

When running event detection from the dashboard with custom paths like:

```
E:/Other Projects/other-clones/Project-Sentinel---Zebra/LoopCode/src/data/input
```

You got an error: `chdir: No such file or directory`

### Root Cause

The issue was related to path format inconsistencies between:

- **Git Bash style paths**: `/e/Other Projects/...` (Unix-style)
- **Windows Python paths**: `E:\Other Projects\...` or `E:/Other Projects/...`
- **Subprocess expectations**: Windows-native paths with backslashes

### Solution Applied

Updated `dashboard_app.py` to:

1. ✅ Convert all paths to absolute Windows paths
2. ✅ Replace forward slashes with backslashes for Windows compatibility
3. ✅ Verify folder exists before running detection
4. ✅ Use `shell=False` to avoid shell path interpretation
5. ✅ Better error messages with full command and output

---

## 🚀 How to Use Now

### Step 1: Restart the Dashboard

```bash
# Stop the current dashboard (Ctrl+C in terminal)
# Then restart:
cd LoopCode
python start_dashboard.py
```

### Step 2: Test with Your src/data/input Folder

**Option A: Use Preset (Easiest!)**

1. Open dashboard: http://localhost:8503
2. Click "📁 Data Source Configuration"
3. Select **"Sample Data (src/data/input)"** from dropdown
4. Click "🚀 Run Event Detection"

**Option B: Enter Custom Path**

1. Choose "Enter custom path"
2. Type: `E:\Other Projects\other-clones\Project-Sentinel---Zebra\LoopCode\src\data\input`
   - Or use forward slashes: `E:/Other Projects/other-clones/Project-Sentinel---Zebra/LoopCode/src/data/input`
3. Click "🚀 Run Event Detection"

Both should work now! The dashboard automatically converts paths to the correct format.

---

## 📁 Your src/data/input Folder

I confirmed your folder has all required files:

- ✅ `products_list.csv`
- ✅ `customer_data.csv`
- ✅ `pos_transactions.jsonl`
- ✅ `rfid_readings.jsonl`
- ✅ `product_recognition.jsonl`
- ✅ `queue_monitoring.jsonl`
- ✅ `inventory_snapshots.jsonl`

Perfect! Your data is ready to process.

---

## 🎯 What Changed in the Code

### Before (Problematic)

```python
# Used paths as-is, could be Git Bash style
data_folder_abs = str(Path(data_folder).resolve())

result = subprocess.run(
    cmd,
    cwd=str(executables_dir.resolve())  # Mixed path formats
)
```

### After (Fixed)

```python
# Verify folder exists first
data_folder_path = Path(data_folder).resolve()
if not data_folder_path.exists():
    return False, f"Data folder does not exist: {data_folder_path}", ""

# Convert to Windows-style paths explicitly
data_folder_abs = str(data_folder_path).replace('/', '\\')
executables_dir_abs = str(executables_dir.resolve()).replace('/', '\\')

result = subprocess.run(
    cmd,
    cwd=executables_dir_abs,  # Windows native path
    shell=False  # No shell interpretation
)
```

---

## 🔍 Testing the Fix

### Test 1: Command Line Test (Optional)

```bash
cd LoopCode/evidence/executables
python run_demo.py --data-dir "E:\Other Projects\other-clones\Project-Sentinel---Zebra\LoopCode\src\data\input" --dataset-type test
```

If this works, the dashboard will work too!

### Test 2: Dashboard Test (Main)

1. Launch dashboard: `python start_dashboard.py`
2. Select "Sample Data (src/data/input)" from dropdown
3. Click "Run Event Detection"
4. Should complete successfully! 🎉

---

## 📊 Expected Results

After successful detection with your src/data/input folder:

- **Events File**: `LoopCode/evidence/executables/results/events.jsonl`
- **Expected Events**: Depends on your data size
  - If you copied the sample data: ~1-5 events
  - If you have realistic test data: 50-200+ events
- **Processing Time**: 10-60 seconds depending on data size

---

## 🐛 Other Common Issues & Solutions

### Issue 1: "Folder does not exist"

**Symptoms:** Red error message saying folder doesn't exist

**Solutions:**

- Use absolute path: `E:\full\path\to\folder`
- Don't use relative paths like `../data/input`
- Check for typos in the path
- Verify folder exists in File Explorer

### Issue 2: "Missing required files"

**Symptoms:** Validation fails, lists missing files

**Solutions:**

- Ensure folder has `products_list.csv`
- Ensure folder has `customer_data.csv`
- Ensure at least one `.jsonl` file exists
- Check file names match exactly (case-sensitive!)

### Issue 3: Detection runs but no events created

**Symptoms:** Green success but 0 events

**Possible Causes:**

- Data files are empty
- Data format is incorrect
- No transactions to analyze

**Solutions:**

- Check your data files have content
- Verify CSV/JSONL format is correct
- Try with generated test data first: `python tools/generate_test_data.py`

### Issue 4: Long processing time

**Symptoms:** Spinner shows for >5 minutes

**Normal If:**

- Large dataset (500+ transactions)
- Complex data (many products/customers)
- First run (installing dependencies)

**Check:**

- Look at terminal/console for progress
- Don't close browser during processing
- Wait patiently for large datasets

### Issue 5: Port already in use

**Symptoms:** Dashboard won't start, port 8503 busy

**Solution:**

```bash
# Windows - Kill process on port 8503
netstat -ano | findstr :8503
taskkill /PID <process_id> /F

# Then restart dashboard
python start_dashboard.py
```

---

## 📝 Path Format Examples

### ✅ Correct Formats (All Work Now!)

```
E:\Other Projects\other-clones\Project-Sentinel---Zebra\LoopCode\src\data\input
E:/Other Projects/other-clones/Project-Sentinel---Zebra/LoopCode/src/data/input
E:\Other Projects\other-clones\Project-Sentinel---Zebra\tools\generated_test_data
C:\Users\YourName\Documents\project-data
```

### ❌ Avoid These Formats

```
../data/input                    # Relative paths (use absolute!)
/e/Other Projects/...           # Git Bash paths (let dashboard convert)
data/input                      # Relative without ../
~\Documents\data                # Home directory shortcut
```

---

## 🎉 Summary

### What Was Fixed

1. ✅ Path normalization to Windows format
2. ✅ Folder existence validation before running
3. ✅ Better error messages with full details
4. ✅ Added "Sample Data (src/data/input)" to presets
5. ✅ Improved subprocess execution

### What You Need to Do

1. **Restart dashboard** if it's still running
2. **Select your data folder** (preset or custom)
3. **Click "Run Event Detection"**
4. **Wait for results** (should work now!)

### Next Steps

1. ✅ Test with src/data/input folder
2. ✅ Verify events are detected
3. ✅ Explore results in dashboard
4. ✅ Try with other folders (generated test data)

---

## 💡 Pro Tips

1. **Use Presets First**: They're pre-validated and faster to select
2. **Check Folder Contents**: Use the preview before running
3. **Watch Terminal**: Console shows detailed progress
4. **Be Patient**: Large datasets take time
5. **Test Small First**: Start with small data to verify everything works

---

## 📞 Still Having Issues?

If you still get errors after the fix:

1. **Check the error message** - Now includes full command and output
2. **Verify your data** - Make sure files are properly formatted
3. **Try generated test data** - Known-good data for testing:
   ```bash
   cd tools
   python generate_test_data.py
   ```
4. **Check terminal output** - Look for Python errors or stack traces
5. **Restart fresh** - Close dashboard, restart, try again

---

**Your dashboard should now work with any valid data folder path!** 🎊

Test it with your src/data/input folder and let me know the results! 🚀

---

Last Updated: October 4, 2025
