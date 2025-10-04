# Submission Guide

## Team details

- Team name: LoopCode
- Members: D.T.P.D.Wickramasinghe, K.L.L.S.Liyanage, Sandun Madhushan, T.H.M.Thilakarathna
- Primary contact email: tharindapamindu@gmail.com

## Judge run command

Judges will `cd evidence/executables/` and run **one command** on Ubuntu 24.04:

```
python3 run_demo.py --data-dir /path/to/data
```

Adapt `run_demo.py` to set up dependencies, start any services, ingest data, and write all artefacts into `./results/` (relative to `evidence/executables/`). No additional scripts or manual steps are allowed.

### What the script does

The `run_demo.py` script automates the entire workflow:

1. Installs dependencies (pandas, streamlit, plotly)
2. Loads input data from specified directory
3. Runs all 20 detection algorithms
4. Generates `results/events.jsonl` with detected events
5. Creates `results/summary_report.txt` with statistics
6. Copies output to `evidence/output/` folder

### Results with provided dataset

**Total Events Detected:** 572  
**Unique Stations:** 5  
**Event Types:** 7 (E001, E002, E003, E005, E007, E008, E009)

Event breakdown:

- E002 (Barcode Switching): 228 events
- E008 (Staffing Needs): 195 events
- E005 (Long Queue Length): 117 events
- E003 (Weight Discrepancies): 10 events
- E001 (Scanner Avoidance): 9 events
- E007 (Inventory Discrepancy): 8 events
- E009 (Checkout Station Action): 5 events

## Checklist before zipping and submitting

- Algorithms tagged with `# @algorithm Name | Purpose` comments: **Yes, 20 algorithms tagged**

  - fraud_detection.py: 5 algorithms
  - queue_analyzer.py: 5 algorithms
  - inventory_monitor.py: 5 algorithms
  - anomaly_detector.py: 5 algorithms

- Evidence artefacts present in `evidence/`: **Yes, all present**

  - executables/run_demo.py (automation script)
  - executables/results/ (will be generated when judges run)
  - output/test/events.jsonl (test results)
  - output/final/events.jsonl (final results)

- Source code complete under `src/`: **Yes, all files present**
  - data_models.py (data structures)
  - event_detector.py (main detection orchestrator)
  - algorithms/fraud_detection.py
  - algorithms/queue_analyzer.py
  - algorithms/inventory_monitor.py
  - algorithms/anomaly_detector.py
  - utils/helpers.py
  - dashboard/dashboard_app.py

## Contact

For questions or issues, please contact: tharindapamindu@gmail.com

---

**LoopCode - Team 14 - Project Sentinel** | October 2025
