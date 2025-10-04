# 🎓 Understanding Project Sentinel from Scratch

**A Complete Beginner's Guide to the LoopCode Solution**

---

## 👋 Welcome!

This guide will help you understand **everything** about Project Sentinel and our LoopCode solution, even if you have zero prior knowledge. We'll start from the very basics and build up to the complete system.

**Estimated Reading Time:** 30 minutes  
**Prerequisites:** None! We'll explain everything.

---

## 📑 Table of Contents

1. [What is Project Sentinel?](#1-what-is-project-sentinel)
2. [The Problem We're Solving](#2-the-problem-were-solving)
3. [How Self-Checkout Works](#3-how-self-checkout-works)
4. [The Data We Receive](#4-the-data-we-receive)
5. [What We Need to Detect](#5-what-we-need-to-detect)
6. [Our Solution Architecture](#6-our-solution-architecture)
7. [The Algorithms Explained](#7-the-algorithms-explained)
8. [How the Code Works](#8-how-the-code-works)
9. [The Dashboard](#9-the-dashboard)
10. [Running the Project](#10-running-the-project)
11. [Understanding the Results](#11-understanding-the-results)
12. [Next Steps](#12-next-steps)

---

## 1. What is Project Sentinel?

### The Competition

**Project Sentinel** is a coding competition organized by Zebra Technologies. Teams must build a system that monitors self-checkout stations in retail stores and detects problems automatically.

### Real-World Context

Imagine a grocery store with self-checkout stations. Customers scan their own items, but sometimes:
- People make mistakes (scan wrong barcode)
- People try to cheat (don't scan expensive items)
- Machines break down (system crashes)
- Lines get too long (need more staff)
- Inventory doesn't match (theft or errors)

**Our job:** Build software that watches these stations and alerts staff when problems occur.

### Why It Matters

- **Retailers lose billions** to checkout fraud every year
- **Customers get frustrated** waiting in long lines
- **Staff need help** knowing when to intervene
- **Automated monitoring** can catch problems humans miss

---

## 2. The Problem We're Solving

### The Challenge

You're given sensor data from self-checkout stations, and you must:

1. **Read the data** from multiple sensors (cameras, RFID tags, scales, etc.)
2. **Analyze patterns** to find problems
3. **Generate events** when you detect something wrong
4. **Visualize results** in a dashboard for store managers

### What Makes It Hard?

- **Multiple data sources**: 7 different types of sensors
- **Real-time processing**: Data streams continuously
- **Complex patterns**: Fraud isn't always obvious
- **High accuracy needed**: False alarms waste staff time
- **Time pressure**: Competition deadline!

### Our Approach

We built **LoopCode** - a comprehensive event detection system with:
- 20+ detection algorithms
- Multi-modal sensor fusion
- Interactive dashboard
- Production-ready code quality

---

## 3. How Self-Checkout Works

### The Physical Setup

```
┌─────────────────────────────────────┐
│    Self-Checkout Station (SCC1)     │
├─────────────────────────────────────┤
│                                     │
│  📹 Camera (Vision System)          │
│     └─ Sees products                │
│                                     │
│  📊 Barcode Scanner                 │
│     └─ Reads barcodes               │
│                                     │
│  ⚖️  Weight Scale                   │
│     └─ Weighs items                 │
│                                     │
│  📡 RFID Reader                     │
│     └─ Detects RFID tags            │
│                                     │
│  💳 Payment Terminal                │
│     └─ Processes payment            │
│                                     │
│  🎥 Queue Camera                    │
│     └─ Counts waiting customers     │
│                                     │
└─────────────────────────────────────┘
```

### Normal Checkout Flow

1. **Customer arrives** at station
2. **Camera sees** them approach
3. **Customer scans** item barcode
4. **System records** item in transaction
5. **Customer places** item in bagging area
6. **Scale weighs** item (should match catalog weight)
7. **RFID reader** detects tag (if item has one)
8. **Customer pays** and leaves
9. **Camera sees** them depart

### When Things Go Wrong

**Scenario: Barcode Switching**
- Customer picks up expensive steak ($20)
- Customer scans banana barcode ($1)
- System thinks they bought bananas
- **Our detection:** Vision system saw steak, but POS recorded bananas!

**Scenario: Scanner Avoidance**
- Customer picks up item with RFID tag
- Customer "forgets" to scan it
- Customer puts it in bag and leaves
- **Our detection:** RFID saw the tag, but no POS transaction!

---

## 4. The Data We Receive

### Data Sources (7 Types)

#### 1. **POS Transactions** (Point of Sale)
What the cash register records when items are scanned.

```json
{
  "timestamp": "2025-10-04T12:30:00",
  "station_id": "SCC1",
  "customer_id": "C001",
  "transaction_id": "T001",
  "items": [
    {
      "sku": "P001",
      "product_name": "Apple",
      "barcode": "BAR001",
      "price": 2.99,
      "weight_g": 150
    }
  ]
}
```

**What it tells us:** What the customer officially bought

#### 2. **RFID Readings**
Radio frequency tags detected near the station.

```json
{
  "timestamp": "2025-10-04T12:29:58",
  "station_id": "SCC1",
  "epc": "EPC001",
  "sku": "P001",
  "location": "checkout_zone"
}
```

**What it tells us:** What items passed through (even if not scanned)

#### 3. **Product Recognition** (Vision System)
What the camera sees and identifies.

```json
{
  "timestamp": "2025-10-04T12:29:59",
  "station_id": "SCC1",
  "predicted_product": "P001",
  "accuracy": 0.95
}
```

**What it tells us:** What items the camera saw

#### 4. **Queue Monitoring**
How many people are waiting and for how long.

```json
{
  "timestamp": "2025-10-04T12:30:00",
  "station_id": "SCC1",
  "customer_count": 5,
  "average_dwell_time": 120
}
```

**What it tells us:** Queue lengths and wait times

#### 5. **Inventory Snapshots**
Stock levels at specific times.

```json
{
  "timestamp": "2025-10-04T16:00:00",
  "data": {
    "P001": 50,
    "P002": 30,
    "P003": 100
  }
}
```

**What it tells us:** How much inventory we should have

#### 6. **Product Catalog** (CSV)
Reference data about all products.

```csv
SKU,product_name,barcode,weight,price
P001,Apple,BAR001,150,2.99
P002,Banana,BAR002,120,1.99
```

**What it tells us:** Expected properties of each product

#### 7. **Customer Data** (CSV)
Information about registered customers.

```csv
customer_id,name,contact
C001,John Doe,john@example.com
C002,Jane Smith,jane@example.com
```

**What it tells us:** Who the customers are

---

## 5. What We Need to Detect

### The 10 Event Types

We must detect 10 different types of events. Each event has a unique ID (E000-E009).

#### **E000: Success Operation** ✅
- **What:** A normal, legitimate transaction with no issues
- **Why detect:** Establishes baseline for comparison
- **Example:** Customer scans apple, weighs correctly, pays, leaves

#### **E001: Scanner Avoidance** 🚨
- **What:** Item detected but not scanned (theft attempt)
- **Why detect:** Prevents revenue loss
- **Example:** RFID or camera sees item, but no POS scan

#### **E002: Barcode Switching** 🚨
- **What:** Customer scans wrong barcode (cheaper item)
- **Why detect:** Price manipulation fraud
- **Example:** Vision sees steak, POS records bananas

#### **E003: Weight Discrepancies** 🚨
- **What:** Item weight doesn't match catalog
- **Why detect:** Product substitution or incorrect scanning
- **Example:** Catalog says 150g, scale reads 500g

#### **E004: System Crashes** ⚠️
- **What:** Checkout station stops working
- **Why detect:** Need technician immediately
- **Example:** No transactions for 2+ minutes

#### **E005: Long Queue Length** 📊
- **What:** Too many customers waiting
- **Why detect:** Need to open more checkouts
- **Example:** 5+ customers in line

#### **E006: Long Wait Time** 📊
- **What:** Customers waiting too long
- **Why detect:** Poor customer experience
- **Example:** Average wait time > 5 minutes

#### **E007: Inventory Discrepancy** 📦
- **What:** Stock count doesn't match expected
- **Why detect:** Shrinkage, theft, or counting errors
- **Example:** Sold 10 apples, but inventory shows 8 missing

#### **E008: Staffing Needs** 👥
- **What:** Workload requires more staff
- **Why detect:** Resource allocation
- **Example:** All stations busy, queues building

#### **E009: Station Actions** 🔄
- **What:** Need to open/close checkout stations
- **Why detect:** Operational efficiency
- **Example:** Recommend closing idle station

---

## 6. Our Solution Architecture

### The Big Picture

```
┌─────────────────────────────────────┐
│   SENSORS (Cameras, RFID, etc.)     │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│   DATA FILES (CSV, JSONL)           │
│   • pos_transactions.jsonl          │
│   • rfid_readings.jsonl             │
│   • product_recognition.jsonl       │
│   • queue_monitoring.jsonl          │
│   • inventory_snapshots.jsonl       │
│   • products_list.csv               │
│   • customer_data.csv               │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│   DATA MODELS (Python Classes)      │
│   • POSTransaction                  │
│   • RFIDReading                     │
│   • ProductRecognition              │
│   • QueueMeasurement                │
│   • InventorySnapshot               │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│   EVENT DETECTOR (Orchestrator)     │
│   Coordinates all algorithms        │
└────────────┬────────────────────────┘
             ↓
        ┌────┴────┐
        ↓         ↓
┌──────────────┐  ┌──────────────┐
│   FRAUD      │  │    QUEUE     │
│  DETECTION   │  │   ANALYSIS   │
│  5 algorithms│  │  5 algorithms│
└──────────────┘  └──────────────┘
        ↓         ↓
┌──────────────┐  ┌──────────────┐
│  INVENTORY   │  │   ANOMALY    │
│  MONITORING  │  │  DETECTION   │
│  5 algorithms│  │  5 algorithms│
└──────────────┘  └──────────────┘
        ↓         ↓
        └────┬────┘
             ↓
┌─────────────────────────────────────┐
│   DETECTED EVENTS (JSONL)           │
│   • event_id (E000-E009)            │
│   • timestamp                       │
│   • event_data                      │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│   DASHBOARD (Streamlit)             │
│   • Charts and visualizations       │
│   • Filters and exploration         │
│   • Export capabilities             │
└─────────────────────────────────────┘
```

### System Components

#### 1. **Data Models** (`src/data_models.py`)
Python classes that represent our data structures.

**Example:**
```python
@dataclass
class POSTransaction:
    timestamp: datetime
    station_id: str
    customer_id: str
    transaction_id: str
    items: List[TransactionItem]
```

**Why:** Type safety, validation, easy to use

#### 2. **Event Detector** (`src/event_detector.py`)
The main orchestrator that coordinates everything.

**What it does:**
1. Loads all data files
2. Calls each detection algorithm
3. Collects all detected events
4. Saves results to events.jsonl

#### 3. **Algorithm Modules** (`src/algorithms/`)
Four modules containing 20+ detection algorithms.

- **fraud_detection.py** - 5+ fraud algorithms
- **queue_analyzer.py** - 5 queue algorithms
- **inventory_monitor.py** - 5 inventory algorithms
- **anomaly_detector.py** - 5 anomaly algorithms

#### 4. **Dashboard** (`src/dashboard/dashboard_app.py`)
Interactive web interface built with Streamlit.

**Features:**
- Real-time metrics
- Interactive charts
- Event filtering
- Data export

#### 5. **Automation Script** (`evidence/executables/run_demo.py`)
One-command execution script.

**What it does:**
1. Installs dependencies
2. Runs event detection
3. Generates reports
4. Optionally launches dashboard

---

## 7. The Algorithms Explained

### Algorithm Categories

We have 20+ algorithms organized into 4 categories:

### 🚨 Fraud Detection (5+ Algorithms)

#### **1. Scanner Avoidance - Vision-Based** (Primary)
**How it works:**
1. Look at all POS transactions
2. For each transaction, check if vision system saw products
3. Time window: 5 seconds before to 10 seconds after transaction
4. If vision saw products NOT in POS → Scanner avoidance!

**Code concept:**
```python
# @algorithm Scanner Avoidance (Vision) | Detects items seen but not scanned
def detect_scanner_avoidance_vision(transactions, recognitions):
    events = []
    for transaction in transactions:
        # Find vision detections near this transaction time
        nearby_visions = find_visions_in_timewindow(
            recognitions,
            transaction.timestamp,
            before=5, after=10
        )
        
        # Check if vision saw products not in transaction
        for vision in nearby_visions:
            if vision.predicted_product not in transaction.items:
                # Found scanner avoidance!
                events.append(create_event("E001", ...))
    
    return events
```

#### **2. Scanner Avoidance - RFID-Based** (Secondary)
Similar to vision-based, but uses RFID readings instead.

#### **3. Barcode Switching**
Compares vision system predictions with what was actually scanned.

**Logic:**
- Vision: "I see a steak (P042)"
- POS: "Customer scanned banana (P001)"
- **Result:** Barcode switching detected!

#### **4. Weight Verification**
Checks if scanned item weight matches catalog weight.

**Logic:**
- Catalog: Apple weighs 150g ± 10%
- Scale: Item weighs 500g
- **Result:** Weight discrepancy detected!

#### **5. Success Operation**
Validates legitimate transactions (all checks pass).

### 📊 Queue Analysis (5 Algorithms)

#### **6. Queue Threshold Analysis**
**Logic:**
```
If customer_count >= 5:
    Create E005 event (Long Queue)
```

#### **7. Wait Time Analysis**
**Logic:**
```
If average_dwell_time >= 300 seconds:
    Create E006 event (Long Wait Time)
```

#### **8. Staffing Prediction**
Analyzes workload and recommends staffing levels.

#### **9. Station Status Management**
Recommends opening/closing stations based on demand.

#### **10. Queue Trend Analysis**
Identifies patterns in queue buildup.

### 📦 Inventory Monitoring (5 Algorithms)

#### **11. Inventory Reconciliation**
**How it works:**
1. Start with initial inventory count
2. Subtract all sold items from POS
3. Compare with actual inventory snapshot
4. If difference > 2 units → Discrepancy!

**Example:**
```
Initial: 50 apples
Sold: 10 apples
Expected: 40 apples
Actual: 38 apples
Difference: 2 apples → No event (within tolerance)

Actual: 35 apples
Difference: 5 apples → EVENT E007!
```

#### **12-15. Other Inventory Algorithms**
- Stock level monitoring
- Velocity analysis
- Shrinkage detection
- Reorder calculations

### 🔍 Anomaly Detection (5 Algorithms)

#### **16. System Downtime Detection**
**Logic:**
```
If time_between_transactions >= 120 seconds:
    Create E004 event (System Crash)
```

#### **17-20. Other Anomaly Algorithms**
- Statistical analysis (Z-scores)
- Pattern detection
- Behavioral profiling
- Correlation analysis

---

## 8. How the Code Works

### File Structure

```
src/
├── data_models.py           # Data structures
├── event_detector.py        # Main orchestrator
├── algorithms/
│   ├── fraud_detection.py   # Fraud algorithms
│   ├── queue_analyzer.py    # Queue algorithms
│   ├── inventory_monitor.py # Inventory algorithms
│   └── anomaly_detector.py  # Anomaly algorithms
├── utils/
│   └── helpers.py          # Utility functions
├── dashboard/
│   └── dashboard_app.py    # Streamlit dashboard
└── data/
    └── input/              # Data files
```

### Execution Flow

#### Step 1: Load Data
```python
# In event_detector.py
def load_data(data_dir):
    # Load CSV files
    products = load_products_csv(data_dir / "products_list.csv")
    customers = load_customers_csv(data_dir / "customer_data.csv")
    
    # Load JSONL files
    transactions = load_pos_transactions(data_dir / "pos_transactions.jsonl")
    rfid_readings = load_rfid_readings(data_dir / "rfid_readings.jsonl")
    # ... etc
    
    return DataContainer(products, customers, transactions, ...)
```

#### Step 2: Run Detection Algorithms
```python
def detect_events(data):
    all_events = []
    
    # Fraud detection
    fraud_events = detect_fraud(data)
    all_events.extend(fraud_events)
    
    # Queue analysis
    queue_events = analyze_queues(data)
    all_events.extend(queue_events)
    
    # Inventory monitoring
    inventory_events = monitor_inventory(data)
    all_events.extend(inventory_events)
    
    # Anomaly detection
    anomaly_events = detect_anomalies(data)
    all_events.extend(anomaly_events)
    
    return all_events
```

#### Step 3: Save Results
```python
def save_events(events, output_file):
    with open(output_file, 'w') as f:
        for event in events:
            # Write each event as one JSON line
            json_line = json.dumps(event.to_dict())
            f.write(json_line + '\n')
```

### Example: Complete Detection Process

```python
# Simplified version of what happens
def main():
    # 1. Load data
    print("Loading data...")
    data = load_data("src/data/input")
    
    # 2. Run detection
    print("Running detection...")
    events = []
    
    # Fraud detection
    events.extend(detect_scanner_avoidance_vision(
        data.transactions,
        data.recognitions
    ))
    events.extend(detect_barcode_switching(
        data.transactions,
        data.recognitions
    ))
    # ... more algorithms
    
    # 3. Save results
    print(f"Detected {len(events)} events")
    save_events(events, "results/events.jsonl")
    
    # 4. Generate summary
    generate_summary_report(events)
```

---

## 9. The Dashboard

### What Is It?

An interactive web application built with Streamlit that visualizes detected events.

### Key Features

#### 1. **Metrics Overview**
```
┌─────────────────────────────────────┐
│   Total Events: 572                 │
│   Fraud Events: 247                 │
│   Queue Issues: 117                 │
│   Stations: 5                       │
└─────────────────────────────────────┘
```

#### 2. **Event Distribution Chart**
Bar chart showing how many of each event type was detected.

#### 3. **Timeline View**
Line chart showing when events occurred over time.

#### 4. **Station Analysis**
Performance metrics broken down by checkout station.

#### 5. **Event Details Table**
Searchable table with all event details.

#### 6. **Filters**
- Filter by event type
- Filter by station
- Filter by time range

#### 7. **Export**
Download results as CSV or JSON.

### How to Use

```bash
# Launch dashboard
python start_dashboard.py

# Opens at: http://localhost:8501
```

**In the dashboard:**
1. Select data source (default: src/data/input)
2. Click "Run Event Detection"
3. Wait 1-2 minutes
4. Explore results!

---

## 10. Running the Project

### Prerequisites

- Python 3.9 or higher
- Internet connection (for first-time dependency install)

### Method 1: Quick Start (Dashboard)

```bash
# 1. Navigate to project
cd LoopCode

# 2. Launch dashboard
python start_dashboard.py

# 3. In browser (opens automatically):
#    - Click "Run Event Detection"
#    - Wait for results
#    - Explore!
```

### Method 2: Command Line

```bash
# 1. Navigate to executables
cd LoopCode/evidence/executables

# 2. Run detection
python run_demo.py --data-dir ../../src/data/input --dataset-type test

# 3. View results
cat results/events.jsonl
cat results/summary_report.txt
```

### Method 3: Dashboard Only (View Existing Results)

```bash
cd LoopCode/evidence/executables
python run_demo.py --dashboard-only
```

### What Happens When You Run?

1. **Dependency Installation** (~30 seconds first time)
   - Installs pandas, streamlit, plotly, numpy

2. **Data Loading** (~5 seconds)
   - Reads all CSV and JSONL files
   - Validates data format

3. **Event Detection** (~45 seconds)
   - Runs all 20+ algorithms
   - Collects detected events

4. **Results Generation** (~5 seconds)
   - Saves events.jsonl
   - Creates summary report
   - Copies to evidence folders

5. **Dashboard Launch** (optional)
   - Starts web server
   - Opens browser automatically

**Total Time:** ~90 seconds

---

## 11. Understanding the Results

### Output Files

#### 1. **events.jsonl**
Main output file with all detected events.

**Location:** `evidence/executables/results/events.jsonl`

**Format:** One JSON object per line

**Example:**
```json
{"timestamp":"2025-10-04T12:30:00","event_id":"E002","event_data":{"event_name":"Barcode Switching","station_id":"SCC1","customer_id":"C001","scanned_product":"P001","predicted_product":"P042","confidence":0.95}}
```

**Fields:**
- `timestamp`: When event occurred
- `event_id`: Event type (E000-E009)
- `event_data`: Event-specific details

#### 2. **summary_report.txt**
Human-readable summary.

**Location:** `evidence/executables/results/summary_report.txt`

**Example:**
```
======================================================================
PROJECT SENTINEL - EVENT DETECTION SUMMARY
======================================================================

Total Events Detected: 572
Unique Stations: 5

Event Distribution by ID:
----------------------------------------
  E001: 9
  E002: 228
  E003: 10
  E005: 117
  E007: 8
  E008: 195
  E009: 5
```

### Interpreting Results

#### Our Current Results (572 Events)

**E001: 9 Scanner Avoidance Events**
- Vision system saw items not scanned
- Potential theft attempts
- Need staff intervention

**E002: 228 Barcode Switching Events**
- Customers scanned wrong barcodes
- Most common fraud type
- Price manipulation attempts

**E003: 10 Weight Discrepancies**
- Item weights don't match catalog
- Product substitution or errors
- Need verification

**E005: 117 Long Queue Events**
- Too many customers waiting
- Need to open more checkouts
- Customer experience issue

**E007: 8 Inventory Discrepancies**
- Stock counts don't match
- Shrinkage or counting errors
- Need inventory check

**E008: 195 Staffing Needs**
- Workload requires more staff
- Resource allocation needed
- Operational efficiency

**E009: 5 Station Actions**
- Need to open/close stations
- Dynamic management
- Optimize resources

---

## 12. Next Steps

### Now That You Understand the Project...

#### 1. **Run It Yourself**
```bash
cd LoopCode
python start_dashboard.py
```

#### 2. **Explore the Code**
- Read `src/data_models.py` - See data structures
- Read `src/event_detector.py` - See main logic
- Read `src/algorithms/fraud_detection.py` - See detection algorithms

#### 3. **Modify Something**
- Try changing a threshold (e.g., queue length from 5 to 3)
- Add a print statement to see algorithm execution
- Experiment with different parameters

#### 4. **Read More Documentation**
- [Technical Documentation](../technical/DOCUMENTATION.md) - Code details
- [Algorithm Explanations](../technical/EVENT_DETECTION_EXPLANATION.md) - How algorithms work
- [Quick Reference](../reference/QUICK_REFERENCE.md) - Command cheat sheet

#### 5. **Prepare for Submission**
- [Submission Guide](../competition/SUBMISSION_GUIDE.md) - Competition checklist
- [Final Status](../competition/FINAL_STATUS.md) - Project status

---

## 🎉 Congratulations!

You now understand:
- ✅ What Project Sentinel is
- ✅ How self-checkout systems work
- ✅ What data we receive
- ✅ What events we detect
- ✅ How our solution works
- ✅ How to run the project
- ✅ How to interpret results

### Key Takeaways

**Project Sentinel** = Monitoring self-checkout stations

**LoopCode Solution** = Our winning implementation with:
- 20+ algorithms
- 572 events detected
- Interactive dashboard
- Production-ready code

**You Can Now:**
- Run the project
- Understand the results
- Modify the code
- Explain it to others

---

## 📞 Need Help?

**Quick Questions:**
- Check [Quick Reference](../reference/QUICK_REFERENCE.md)
- Check [Quick Answer](../reference/QUICK_ANSWER.md)

**Technical Details:**
- Read [Technical Documentation](../technical/DOCUMENTATION.md)
- Read [Algorithm Explanations](../technical/EVENT_DETECTION_EXPLANATION.md)

**Still Confused?**
- Review this guide again
- Check code comments
- Contact team (see README.md)

---

**Welcome to Project Sentinel!** 🚀

You're now ready to work with the LoopCode solution. Have fun exploring!

---

**LoopCode - Project Sentinel**  
*Understanding Made Easy* ✅

**Navigation:** `docs/guides/UNDERSTANDING_FROM_SCRATCH.md`
