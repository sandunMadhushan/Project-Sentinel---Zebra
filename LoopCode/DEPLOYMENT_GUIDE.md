# 🚀 Deployment Guide - Project Sentinel Dashboard

This guide covers both **local** and **Streamlit Cloud** deployment options.

---

## 📍 Option 1: Local Deployment (Recommended for Testing)

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Steps

1. **Install Dependencies**
   ```bash
   cd LoopCode
   pip install -r requirements.txt
   ```

2. **Run the Dashboard**
   ```bash
   # Option A: Using the automation script (recommended)
   cd evidence/executables
   python run_demo.py --dashboard-only
   
   # Option B: Run Streamlit directly
   cd src/dashboard
   streamlit run dashboard_app.py
   ```

3. **Access the Dashboard**
   - Open your browser to: `http://localhost:8502`
   - The dashboard will automatically find and load `events.jsonl`

### Local Development Features
- ✅ Hot reload on code changes
- ✅ Full debugging capabilities
- ✅ Works with local data files
- ✅ No upload limits

---

## ☁️ Option 2: Streamlit Cloud Deployment

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))

### Steps

1. **Prepare Your Repository**
   
   Make sure these files are committed to your GitHub repository:
   ```
   LoopCode/
   ├── src/dashboard/dashboard_app.py    ✅ (Main app file)
   ├── requirements.txt                   ✅ (Dependencies)
   ├── .streamlit/config.toml            ✅ (Theme config)
   ├── packages.txt                       ✅ (System packages)
   └── evidence/executables/results/
       └── events.jsonl                   ⚠️  (Your data - see note below)
   ```

2. **Commit Your Events Data** (Important!)
   ```bash
   git add LoopCode/evidence/executables/results/events.jsonl
   git commit -m "Add events data for dashboard"
   git push origin main
   ```

3. **Deploy to Streamlit Cloud**

   a. Go to [share.streamlit.io](https://share.streamlit.io)
   
   b. Click "New app"
   
   c. Fill in the deployment form:
      - **Repository:** `sandunMadhushan/Project-Sentinel---Zebra`
      - **Branch:** `main`
      - **Main file path:** `LoopCode/src/dashboard/dashboard_app.py`
        ⚠️ **Important:** Use forward slashes `/`, not backslashes `\`
   
   d. Click "Deploy!"

4. **Access Your Cloud Dashboard**
   - URL will be: `https://<your-app-name>.streamlit.app`
   - Share this link with anyone!

### Cloud Deployment Features
- ✅ Public URL for sharing
- ✅ Automatic SSL/HTTPS
- ✅ Auto-restart on crashes
- ✅ Free hosting (for public repos)

---

## 📊 Data Considerations

### For Local Deployment
- Dashboard reads from: `LoopCode/evidence/executables/results/events.jsonl`
- You can regenerate test data anytime with: `python tools/generate_test_data.py`

### For Cloud Deployment
⚠️ **Important:** The `events.jsonl` file (40KB, 231 events) needs to be in your Git repository.

**Current Status:** Your events file is NOT yet committed to Git.

**To commit:**
```bash
cd "E:/Other Projects/other-clones/Project-Sentinel---Zebra"
git add LoopCode/evidence/executables/results/events.jsonl
git commit -m "Add detected events for dashboard visualization"
git push origin main
```

---

## 🔧 Troubleshooting

### Common Issues

#### ❌ "This file does not exist" on Streamlit Cloud
- **Cause:** Using backslashes `\` instead of forward slashes `/`
- **Fix:** Use `LoopCode/src/dashboard/dashboard_app.py` (not `LoopCode\src\dashboard\dashboard_app.py`)

#### ❌ Dashboard shows "No events found"
- **Local:** Run `python run_demo.py` to generate events first
- **Cloud:** Make sure `events.jsonl` is committed to Git

#### ❌ Port 8502 already in use
```bash
# Find and kill the process
netstat -ano | findstr :8502
taskkill /PID <process_id> /F
```

#### ❌ Module import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

---

## 🎯 Recommended Workflow

For **Project Sentinel competition submission**:

1. ✅ Use **local deployment** for development and testing
2. ✅ Take screenshots from local dashboard (judges run locally anyway)
3. ⚠️ Use **cloud deployment** only if you need to share a live demo link

**Why?** The judges will run your code locally, so cloud deployment is optional for the competition.

---

## 📸 Taking Screenshots for Submission

1. Run the dashboard locally: `python run_demo.py --dashboard-only`
2. Open `http://localhost:8502` in your browser
3. Capture these views:
   - 📊 Overall metrics (top of page)
   - 📈 Event timeline chart
   - 📋 Events table (showing various event types)
   - 🔍 Detailed view of specific events
4. Save screenshots to `LoopCode/evidence/screenshots/`

---

## 💡 Tips

- **Fast Testing:** Use `--dashboard-only` flag to skip event detection
- **Fresh Data:** Regenerate test data with custom parameters in `generate_test_data.py`
- **Performance:** For large datasets (>1000 events), consider pagination
- **Customization:** Edit `.streamlit/config.toml` for theme changes

---

## 📞 Support

- **Team:** LoopCode
- **Repository:** [Project-Sentinel---Zebra](https://github.com/sandunMadhushan/Project-Sentinel---Zebra)
- **Documentation:** See `DOCUMENTATION.md` for full system details

---

**Last Updated:** October 4, 2025
