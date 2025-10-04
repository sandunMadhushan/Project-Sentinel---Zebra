# 🗂️ Folder Browser Feature Guide

## 🆕 New Feature: Visual Folder Browser

You can now **browse and select your data folder visually** without typing paths!

---

## 🚀 How to Use the Folder Browser

### Step 1: Launch Dashboard

```bash
cd LoopCode
python start_dashboard.py
```

### Step 2: Open Data Source Configuration

Click on **"📁 Data Source Configuration"** to expand it.

### Step 3: Select Input Method

Choose **"Browse folders"** from the radio buttons:

- ☐ Select from presets
- ☑ **Browse folders** ← Select this!
- ☐ Enter custom path

---

## 🎮 Using the Folder Browser

### Navigation Controls

**Current Location Bar**

- Shows your current directory path
- Updates as you navigate

**Navigation Buttons:**

| Button                 | Function                                 |
| ---------------------- | ---------------------------------------- |
| ⬆️ **Up**              | Go to parent directory                   |
| 💾 **Drives**          | Show available drives (C:, D:, E:, etc.) |
| ✅ **Use This Folder** | Select current folder as data folder     |

### Browsing Folders

**Folder List:**

- Shows all folders in current location
- ✅ Green checkmark = Valid data folder (has required files)
- 📁 Folder icon = Regular folder
- **→** button = Navigate into folder

**Quick Tips:**

- Click **→** to enter a folder
- Click **⬆️ Up** to go back
- Click **💾 Drives** to switch drives
- Click **✅ Use This Folder** when you find your data

---

## 📝 Example Walkthrough

### Example: Navigate to src/data/input

**Starting Point:** Dashboard opens in project root

1. **See current location:**

   ```
   Current Location: E:\Other Projects\other-clones\Project-Sentinel---Zebra\LoopCode
   ```

2. **Navigate to src folder:**

   - Find "src" in the folder list
   - Click **→** button next to "src"

3. **Navigate to data folder:**

   - Now you see folders inside src
   - Click **→** next to "data"

4. **Navigate to input folder:**

   - Click **→** next to "input"

5. **Verify it's valid:**

   - Should see ✅ next to "input" if it has required files

6. **Select the folder:**

   - Click **✅ Use This Folder** button
   - Success message appears!

7. **Run detection:**
   - Scroll down
   - Click **🚀 Run Event Detection**

---

## 🎯 Quick Navigation Shortcuts

### Navigate to Different Drives

1. Click **💾 Drives** button
2. See available drives: 💾 C:\, 💾 D:\, 💾 E:\, etc.
3. Click on any drive to jump to it
4. Navigate from there

### Start from Project Root

Default starting location is your project root:

```
E:\Other Projects\other-clones\Project-Sentinel---Zebra\LoopCode
```

From here you can navigate to:

- `src/data/input` (3 clicks)
- `tools/generated_test_data` (2 clicks)
- `data/input` (2 clicks)

---

## ✅ Visual Indicators

### Green Checkmark (✅)

Means folder contains all required files:

- ✅ `products_list.csv`
- ✅ `customer_data.csv`
- ✅ At least one `.jsonl` file

**Example:**

```
✅ input         →   ← This folder is ready to use!
📁 output        →
📁 scripts       →
```

### Regular Folder (📁)

Folder exists but doesn't have required data files.

---

## 💡 Tips & Tricks

### Tip 1: Look for Green Checkmarks

When browsing, look for ✅ - these are valid data folders!

### Tip 2: Use Drives Button for Quick Navigation

If your data is on a different drive:

1. Click **💾 Drives**
2. Jump to that drive
3. Navigate from there

### Tip 3: Use "Up" Button to Go Back

Made a wrong turn? Click **⬆️ Up** to go to parent folder.

### Tip 4: Current Location Shows Full Path

Check the "Current Location" field to see exactly where you are.

### Tip 5: Limited to 20 Folders Per View

If you see "Showing 20 of X folders":

- Navigate into folders to narrow down
- This keeps the interface fast

---

## 🆚 Comparison: All Three Methods

### Method 1: Select from Presets

**Pros:**

- ✅ Fastest (one click)
- ✅ Pre-validated folders
- ✅ No navigation needed

**Cons:**

- ❌ Limited to known locations
- ❌ Doesn't show custom data

**Best For:** Quick testing with standard folders

---

### Method 2: Browse Folders (NEW!)

**Pros:**

- ✅ Visual navigation
- ✅ See folder structure
- ✅ Validation indicators (✅)
- ✅ No typing needed
- ✅ Can explore anywhere

**Cons:**

- ⚠️ Slower for deep paths
- ⚠️ Limited to 20 folders per view

**Best For:** Finding data folders, exploring structure

---

### Method 3: Enter Custom Path

**Pros:**

- ✅ Direct input
- ✅ Fastest for known paths
- ✅ Copy-paste friendly

**Cons:**

- ❌ Need to type/paste
- ❌ Easy to make typos
- ❌ No visual feedback

**Best For:** When you know exact path

---

## 🎨 UI Layout

```
┌─────────────────────────────────────────────────┐
│ 📁 Data Source Configuration                    │
├─────────────────────────────────────────────────┤
│ Input Method: ○ Presets  ● Browse  ○ Custom    │
│                                                  │
│ 📁 Folder Browser                               │
│ ┌─────────────────────────────────────────────┐ │
│ │ Current Location                             │ │
│ │ E:\...\LoopCode\src\data                    │ │
│ └─────────────────────────────────────────────┘ │
│                                                  │
│ [⬆️ Up]  [💾 Drives]  [✅ Use This Folder]     │
│                                                  │
│ Folders in this location:                       │
│ ✅ input         [→]                            │
│ 📁 output        [→]                            │
│ 📁 cache         [→]                            │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## 🔧 Technical Details

### What Happens When You Browse

1. **Initial Load:**

   - Starts in project root (LoopCode folder)
   - Lists all subfolders

2. **Navigation:**

   - Click → button next to folder name
   - Path updates to that folder
   - New folder list loads

3. **Validation:**

   - Each folder checked for required files
   - ✅ shown if valid
   - Real-time checking

4. **Selection:**
   - Click "Use This Folder"
   - Path saved to session state
   - Validation runs on selected folder

---

## 📊 Expected Behavior

### Valid Data Folder

```
✅ Selected: E:\...\LoopCode\src\data\input
✅ Valid data folder

📂 Folder Contents
CSV Files:        JSONL Files:
✓ products_list   ✓ pos_transactions
✓ customer_data   ✓ rfid_readings
                  ✓ product_recognition
```

### Invalid Folder

```
❌ Missing required files: products_list.csv, customer_data.csv
```

---

## 🐛 Troubleshooting

### Issue: Can't see my folder

**Solution:**

- Make sure you're in the right parent directory
- Use **⬆️ Up** to go back and try again
- Use **💾 Drives** to switch drives

### Issue: Too many folders (shows 20+)

**Solution:**

- Navigate into subfolders to narrow down
- Or use "Enter custom path" if you know exact location

### Issue: No green checkmarks anywhere

**Solution:**

- Your data folders might not have required files
- Check folder needs: `products_list.csv`, `customer_data.csv`, `.jsonl` files
- Or use generated test data: `python tools/generate_test_data.py`

### Issue: Browser doesn't update after clicking

**Solution:**

- Wait a moment for page reload
- If stuck, refresh browser page (F5)

---

## 🎉 Benefits of Folder Browser

### Before (Text Input Only)

- ❌ Had to type/paste full path
- ❌ Easy to make typos
- ❌ No visual feedback
- ❌ Couldn't explore structure

### After (With Browser)

- ✅ Visual navigation
- ✅ Click to navigate
- ✅ See valid folders instantly (✅)
- ✅ Explore folder structure
- ✅ No typing errors

---

## 🚀 Quick Start Examples

### Example 1: Use src/data/input

```
1. Click "Browse folders"
2. Navigate: → src → data → input
3. Click "✅ Use This Folder"
4. Click "🚀 Run Event Detection"
```

### Example 2: Use generated test data

```
1. Click "Browse folders"
2. Navigate: → tools → generated_test_data
3. Click "✅ Use This Folder"
4. Click "🚀 Run Event Detection"
```

### Example 3: Browse D: drive

```
1. Click "Browse folders"
2. Click "💾 Drives"
3. Click "💾 D:\"
4. Navigate to your data folder
5. Click "✅ Use This Folder"
```

---

## 💡 Pro Tips

1. **Look for ✅** - Valid folders show green checkmark
2. **Start from project root** - Common folders are nearby
3. **Use drives for external storage** - Jump to USB/external drives
4. **Current Location = Full Path** - Always shows where you are
5. **Up button = Safe navigation** - Can always go back

---

## 🎯 Summary

### Three Ways to Select Data Folder:

1. **Presets** - Quick (1 click) but limited
2. **Browse** - Visual, easy, exploratory 👈 **New!**
3. **Custom Path** - Fast if you know path

### When to Use Browse Mode:

- ✅ You're not sure where your data is
- ✅ You want to see folder structure
- ✅ You want validation feedback (✅)
- ✅ You don't want to type paths

---

**Now you can find and select your data folders without ever typing a path!** 🎊

---

Last Updated: October 4, 2025
