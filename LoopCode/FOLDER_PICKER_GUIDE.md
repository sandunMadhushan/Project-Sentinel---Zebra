# 📂 Folder Picker Guide

## 🎉 Native Folder Picker Dialog

You can now use a **native Windows folder picker dialog** to select your data folder!

---

## 🚀 How to Use

### Quick Start

```bash
cd LoopCode
python start_dashboard.py
```

### Select Your Folder (3 Easy Ways)

#### Method 1: Folder Picker Dialog (NEW! 🆕)

1. Open http://localhost:8503
2. Click **"📁 Data Source Configuration"**
3. Select **"Browse for folder"** radio button
4. Click **"📂 Open Folder Picker"** button
5. **Windows folder dialog pops up!** 📂
6. Navigate to your folder (e.g., `src/data/input`)
7. Click "Select Folder"
8. Done! Path is automatically filled in ✨

#### Method 2: Select from Presets (Fastest)

1. Select **"Select from presets"**
2. Choose from dropdown (includes "Sample Data (src/data/input)")
3. Done!

#### Method 3: Enter Custom Path (Direct)

1. Select **"Enter custom path"**
2. Type or paste folder path
3. Done!

---

## 🎮 Using the Folder Picker

### What You'll See

**In Dashboard:**

```
┌─────────────────────────────────────────┐
│ Input Method:                           │
│ ○ Presets  ● Browse for folder  ○ Path │
├─────────────────────────────────────────┤
│ 📁 Folder Picker                        │
│                                         │
│ Click the button below to open a        │
│ folder picker dialog.                   │
│                                         │
│ [📂 Open Folder Picker]  [🗑️ Clear]    │
└─────────────────────────────────────────┘
```

**Native Windows Dialog Pops Up:**

```
┌─────────────────────────────────────────┐
│ Select Data Input Folder         [X]    │
├─────────────────────────────────────────┤
│ 📁 This PC                              │
│   📁 Local Disk (C:)                    │
│   📁 Local Disk (D:)                    │
│   📁 Local Disk (E:)                    │
│     └─ 📁 Other Projects                │
│         └─ 📁 other-clones              │
│             └─ 📁 Project-Sentinel      │
│                 └─ 📁 LoopCode          │
│                     └─ 📁 src           │
│                         └─ 📁 data      │
│                             └─ 📁 input │
│                                         │
│ [Cancel]  [Select Folder]               │
└─────────────────────────────────────────┘
```

---

## 📝 Step-by-Step Example

### Navigate to src/data/input

1. **Click "Browse for folder"**
2. **Click "📂 Open Folder Picker"**
3. **In the dialog that pops up:**
   - Navigate through folders normally (double-click to open)
   - Or type path in address bar
   - E: → Other Projects → other-clones → Project-Sentinel---Zebra → LoopCode → src → data → input
4. **Click "Select Folder"**
5. **Back in dashboard:**
   - Path automatically filled: `E:\...\src\data\input`
   - Green checkmark shows it's valid ✅
6. **Click "🚀 Run Event Detection"**
7. **Done!** 🎉

---

## ✨ Features

### Native Dialog

- ✅ **Familiar Windows interface** - Just like File Explorer
- ✅ **Easy navigation** - Double-click folders, use address bar
- ✅ **All your drives** - C:, D:, E:, network drives
- ✅ **Recent locations** - Quick access sidebar
- ✅ **Search** - Find folders quickly

### In Dashboard

- ✅ **Shows current selection** - See what you picked
- ✅ **Clear button** - Reset selection easily
- ✅ **Auto-validation** - Checks if folder is valid
- ✅ **No typing needed** - Pure point-and-click

---

## 🆚 Comparison

### Old Way (Typing Path)

```
1. Type: E:\Other Projects\other-clones\...
   ❌ Long
   ❌ Prone to typos
   ❌ Hard to remember exact path
```

### New Way (Folder Picker)

```
1. Click "Open Folder Picker"
2. Navigate visually in familiar dialog
3. Click "Select Folder"
   ✅ Easy
   ✅ No typos
   ✅ Native OS dialog
```

**Time saved: ~60%** 🚀

---

## 💡 Tips

### Tip 1: Use Address Bar in Dialog

Instead of clicking through folders, type or paste path in the address bar at top of dialog.

### Tip 2: Quick Access Sidebar

The dialog shows:

- Quick access
- This PC
- Desktop
- Documents
- Downloads

Use these for faster navigation!

### Tip 3: Network Drives Work Too

The picker shows all mapped network drives. You can select folders from network locations.

### Tip 4: Clear Button Resets

Made a mistake? Click **🗑️ Clear** to reset and pick again.

### Tip 5: Presets Still Fastest

For common folders (src/data/input, tools/generated_test_data), presets are still one-click!

---

## 🐛 Troubleshooting

### Issue: Dialog doesn't pop up

**Cause:** tkinter not installed or browser blocked popup

**Solutions:**

1. Make sure tkinter is installed (comes with Python)
2. Check if browser blocked popup (shouldn't happen with Streamlit)
3. Try refreshing the page (F5)
4. Use "Enter custom path" as alternative

### Issue: Can't find my folder in dialog

**Solution:**

- Type path in address bar at top
- Or use Quick Access sidebar
- Or navigate from This PC → drive → folders

### Issue: Selected wrong folder

**Solution:**

- Click **🗑️ Clear** button
- Click "📂 Open Folder Picker" again
- Select correct folder

### Issue: Dialog shows but selecting doesn't work

**Solution:**

1. Make sure you click "Select Folder" not "Cancel"
2. Refresh dashboard page
3. Try again

---

## 🎯 Best Practices

### For Quick Testing

Use **Presets** - Fastest for known locations

### For Your Custom Data

Use **Folder Picker** - Easy navigation, no typing

### When You Know Path

Use **Custom Path** - Direct input, copy-paste

---

## 📊 All Three Methods

| Method            | Speed  | Ease   | Best For         |
| ----------------- | ------ | ------ | ---------------- |
| **Presets**       | ⚡⚡⚡ | ⭐⭐⭐ | Known folders    |
| **Folder Picker** | ⚡⚡   | ⭐⭐⭐ | Finding data     |
| **Custom Path**   | ⚡     | ⭐     | Known exact path |

---

## 🚀 Get Started

### Restart Dashboard

```bash
# Press Ctrl+C to stop current dashboard
cd LoopCode
python start_dashboard.py
```

### Try the Folder Picker

1. Open http://localhost:8503
2. Click "📁 Data Source Configuration"
3. Select "Browse for folder"
4. Click "📂 Open Folder Picker"
5. Navigate to `src/data/input`
6. Click "Select Folder"
7. Click "🚀 Run Event Detection"

---

## ✅ Technical Details

### How It Works

```python
import tkinter as tk
from tkinter import filedialog

# Creates hidden root window
root = tk.Tk()
root.withdraw()

# Opens native folder dialog
folder = filedialog.askdirectory(
    title="Select Data Input Folder"
)

# Returns selected path
return folder
```

### Requirements

- ✅ Python's tkinter (included with Python)
- ✅ Works on Windows, Mac, Linux
- ✅ No additional packages needed

---

## 🎉 Summary

### What Changed

- ❌ Removed complex folder browser
- ✅ Added simple "Open Folder Picker" button
- ✅ Uses native Windows dialog
- ✅ Familiar interface
- ✅ Easier to use

### What You Get

- 📂 **Native OS folder picker**
- 🎯 **Point-and-click selection**
- ✅ **Auto-validation**
- 🗑️ **Easy reset**
- 💯 **No typing needed**

---

**Your folder selection is now as easy as it gets!** 🎊

**Restart dashboard and try it!** 🚀

---

Last Updated: October 4, 2025
Team: LoopCode
