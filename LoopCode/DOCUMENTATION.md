# Project Sentinel - Complete Documentation

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [File Structure](#file-structure)
4. [Algorithm Documentation](#algorithm-documentation)
5. [Data Models](#data-models)
6. [Usage Guide](#usage-guide)
7. [API Reference](#api-reference)
8. [Testing](#testing)
9. [Troubleshooting](#troubleshooting)

---

## Project Overview

Project Sentinel is an intelligent event detection system designed for self-checkout retail environments. It analyzes data from multiple sensors (POS, RFID, cameras, queue monitors) to detect:

- **Fraud Events**: Scanner avoidance, barcode switching, weight manipulation
- **Operational Issues**: System crashes, downtime, equipment failures
- **Queue Problems**: Long queues, excessive wait times, staffing needs
- **Inventory Issues**: Stock discrepancies, shrinkage, low stock

### Key Objectives

1. **Real-time Detection**: Identify events as they occur
2. **Multi-modal Analysis**: Combine data from multiple sources
3. **Automated Processing**: Run without manual intervention
4. **Actionable Insights**: Provide clear, actionable event data

---

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                    INPUT LAYER                          │
├─────────────────────────────────────────────────────────┤
│  • POS Transactions    • RFID Readings                  │
│  • Product Recognition • Queue Monitoring               │
│  • Inventory Snapshots • Product Catalog                │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│                   DATA LAYER                            │
├─────────────────────────────────────────────────────────┤
│  data_models.py                                         │
│  • POSTransaction    • RFIDReading                      │
│  • QueueMonitoring   • InventorySnapshot                │
│  • DetectedEvent     • Product, Customer                │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│                PROCESSING LAYER                         │
├─────────────────────────────────────────────────────────┤
│  event_detector.py - Main Orchestrator                  │
│  • load_data()        • run_fraud_detection()          │
│  • run_queue_analysis() • run_inventory_monitoring()    │
│  • run_anomaly_detection() • save_events()             │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│               ALGORITHM LAYER                           │
├─────────────────────────────────────────────────────────┤
│  algorithms/                                            │
│  ├── fraud_detection.py     (4 algorithms)             │
│  ├── queue_analyzer.py      (5 algorithms)             │
│  ├── inventory_monitor.py   (5 algorithms)             │
│  └── anomaly_detector.py    (5 algorithms)             │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│                 OUTPUT LAYER                            │
├─────────────────────────────────────────────────────────┤
│  • events.jsonl (JSONL format)                         │
│  • dashboard (Streamlit visualization)                  │
│  • summary_report.txt (Statistics)                      │
└─────────────────────────────────────────────────────────┘
```

### Design Principles

1. **Modularity**: Each algorithm is independent and testable
2. **Extensibility**: Easy to add new detection algorithms
3. **Robustness**: Comprehensive error handling
4. **Performance**: Efficient data processing
5. **Maintainability**: Clean, well-documented code

---

## File Structure

### Source Code (`src/`)

#### `data_models.py`
Defines all data structures:
- **Product**: Product catalog entry
- **Customer**: Customer information
- **POSTransaction**: Point of sale transaction
- **RFIDReading**: RFID tag reading
- **ProductRecognition**: Vision system prediction
- **QueueMonitoring**: Queue metrics
- **InventorySnapshot**: Inventory state
- **DetectedEvent**: Output event with factory methods

#### `event_detector.py`
Main orchestrator class:
- **EventDetector**: Coordinates all detection algorithms
  - `load_data()`: Load input files
  - `run_all_detections()`: Execute all algorithms
  - `save_events()`: Write output file
  - `get_event_summary()`: Generate statistics

#### `algorithms/fraud_detection.py`
Fraud detection algorithms:
1. `detect_scanner_avoidance()` - Compare RFID vs POS
2. `detect_barcode_switching()` - Vision vs actual scan
3. `detect_weight_discrepancies()` - Weight validation
4. `detect_success_operations()` - Normal transactions

#### `algorithms/queue_analyzer.py`
Queue management algorithms:
1. `detect_long_queues()` - Queue length monitoring
2. `detect_long_wait_times()` - Wait time analysis
3. `predict_staffing_needs()` - Staffing prediction
4. `manage_station_status()` - Station recommendations
5. `analyze_queue_trends()` - Trend analysis

#### `algorithms/inventory_monitor.py`
Inventory tracking algorithms:
1. `detect_inventory_discrepancies()` - Stock reconciliation
2. `monitor_stock_levels()` - Low stock alerts
3. `analyze_inventory_velocity()` - Turnover analysis
4. `detect_shrinkage()` - Loss detection
5. `calculate_reorder_points()` - Reorder optimization

#### `algorithms/anomaly_detector.py`
Anomaly detection algorithms:
1. `detect_system_crashes()` - Downtime detection
2. `detect_statistical_anomalies()` - Z-score outliers
3. `detect_pattern_anomalies()` - Pattern deviations
4. `detect_behavioral_anomalies()` - Unusual behavior
5. `detect_correlation_anomalies()` - Correlation breaks

#### `utils/helpers.py`
Utility functions:
- `load_products_catalog()` - Load CSV data
- `load_customers_data()` - Load customer data
- `load_jsonl_file()` - Parse JSONL files
- `parse_timestamp()` - Date/time parsing
- `calculate_time_difference()` - Time calculations
- `find_product_by_epc()` - EPC lookup
- `save_events_to_jsonl()` - Write output

#### `dashboard/dashboard_app.py`
Streamlit dashboard:
- Interactive visualization
- Real-time metrics
- Event filtering
- Data export
- Timeline analysis
- Station monitoring

### Evidence Files (`evidence/`)

#### `executables/run_demo.py`
Automation script:
- Dependency installation
- Data loading
- Algorithm execution
- Output generation
- Dashboard launching

---

## Algorithm Documentation

### Fraud Detection Algorithms

#### 1. Scanner Avoidance Detection

**Algorithm**: `detect_scanner_avoidance()`

**Purpose**: Detect items that passed through the checkout (detected by RFID) but were not scanned at the POS.

**Logic**:
```
1. Group RFID readings by station_id
2. Group POS transactions by station_id
3. For each station:
   a. Create set of scanned SKUs from POS
   b. For each RFID-detected SKU:
      - If SKU not in scanned set → Scanner Avoidance
4. Generate E001 event for each occurrence
```

**Inputs**:
- RFID readings (with SKU and station)
- POS transactions (with SKU and station)

**Output**: E001 events with station, customer, and SKU

---

#### 2. Barcode Switching Detection

**Algorithm**: `detect_barcode_switching()`

**Purpose**: Detect when a customer scans a different product than what the vision system detected.

**Logic**:
```
1. Group vision predictions by station
2. Group POS transactions by station
3. For each station:
   a. Match predictions with transactions sequentially
   b. For each high-confidence prediction (>85%):
      - If predicted SKU ≠ scanned SKU → Barcode Switching
4. Generate E002 event for each occurrence
```

**Inputs**:
- Vision system predictions (with accuracy)
- POS transactions

**Output**: E002 events with actual_sku and scanned_sku

---

#### 3. Weight Verification

**Algorithm**: `detect_weight_discrepancies()`

**Purpose**: Detect when product weight significantly differs from catalog weight.

**Logic**:
```
1. For each POS transaction:
   a. Get expected weight from catalog
   b. Get actual weight from transaction
   c. Calculate: % difference = |actual - expected| / expected * 100
   d. If % difference > tolerance (default 15%) → Weight Discrepancy
2. Generate E003 event for each occurrence
```

**Inputs**:
- POS transactions (with weight_g)
- Product catalog (with expected weights)

**Output**: E003 events with expected and actual weights

---

#### 4. Success Operation Detection

**Algorithm**: `detect_success_operations()`

**Purpose**: Identify normal, successful checkout operations.

**Logic**:
```
1. For each POS transaction with status='success':
   a. Check if RFID detected the item
   b. Check if weight is within tolerance
   c. If all checks pass → Success Operation
2. Generate E000 event for each occurrence
```

**Inputs**:
- POS transactions
- RFID readings
- Product catalog

**Output**: E000 events for successful checkouts

---

### Queue Analysis Algorithms

#### 5. Queue Threshold Analysis

**Algorithm**: `detect_long_queues()`

**Purpose**: Monitor queue length and detect when too many customers are waiting.

**Logic**:
```
1. For each queue monitoring event:
   a. Check customer_count
   b. If customer_count > threshold (default 5) → Long Queue
2. Generate E005 event for each occurrence
```

**Threshold**: 5 customers (configurable)

---

#### 6. Wait Time Threshold Analysis

**Algorithm**: `detect_long_wait_times()`

**Purpose**: Detect when customers wait too long.

**Logic**:
```
1. For each queue monitoring event:
   a. Check average_dwell_time
   b. If dwell_time > threshold (default 300s) → Long Wait Time
2. Generate E006 event for each occurrence
```

**Threshold**: 300 seconds = 5 minutes (configurable)

---

#### 7. Staffing Requirements Prediction

**Algorithm**: `predict_staffing_needs()`

**Purpose**: Predict when additional staff is needed.

**Logic**:
```
1. For each queue monitoring event:
   a. If customer_count >= threshold OR wait_time >= threshold:
      - If customer_count >= threshold * 1.5 → Need Manager
      - Else → Need Cashier
2. Generate E008 event with staff type
```

**Staff Types**: Cashier, Manager

---

#### 8. Station Status Management

**Algorithm**: `manage_station_status()`

**Purpose**: Recommend opening or closing checkout stations.

**Logic**:
```
1. Group queue data by station
2. For each station:
   a. Get latest measurement
   b. If customer_count >= open_threshold (5) → Recommend Open
   c. If customer_count <= close_threshold (2) AND
      recent average is low → Recommend Close
3. Generate E009 events with action
```

**Actions**: Open, Close

---

#### 9. Queue Trend Analysis

**Algorithm**: `analyze_queue_trends()`

**Purpose**: Analyze queue patterns over time for insights.

**Logic**:
```
1. Group data by station
2. For each station, calculate:
   - Average customer count
   - Average wait time
   - Maximum values
   - Number of measurements
3. Return trend statistics
```

**Output**: Dictionary of trend metrics

---

### Inventory Monitoring Algorithms

#### 10. Inventory Reconciliation

**Algorithm**: `detect_inventory_discrepancies()`

**Purpose**: Compare expected vs actual inventory levels.

**Logic**:
```
1. Start with initial inventory snapshot
2. Calculate expected inventory:
   expected = initial - sold_items
3. Compare with final snapshot:
   If |expected - actual| > tolerance (5) → Discrepancy
4. Generate E007 event for each SKU with discrepancy
```

**Tolerance**: 5 units (configurable)

---

#### 11. Stock Level Monitoring

**Algorithm**: `monitor_stock_levels()`

**Purpose**: Identify low stock situations.

**Logic**:
```
1. For each SKU in inventory:
   a. Get current quantity
   b. Get expected quantity from catalog
   c. Calculate: % remaining = current / expected
   d. If % remaining <= threshold (20%) → Low Stock
2. Return list of low stock items
```

**Threshold**: 20% of expected quantity

---

#### 12. Inventory Velocity Analysis

**Algorithm**: `analyze_inventory_velocity()`

**Purpose**: Calculate inventory turnover rates.

**Logic**:
```
1. Count total sales per SKU
2. Compare initial vs final inventory
3. Calculate:
   - Units sold
   - Turnover rate = (sold / initial) * 100
   - Days until stockout = remaining / daily_rate
4. Return velocity metrics
```

---

#### 13. Shrinkage Detection

**Algorithm**: `detect_shrinkage()`

**Purpose**: Detect unexplained inventory losses.

**Logic**:
```
1. For each SKU:
   a. Calculate expected change
   b. Get actual change
   c. Calculate: unexplained_loss = expected - actual
   d. If unexplained_loss > threshold (3) → Shrinkage
2. Return shrinkage alerts with severity
```

**Severity Levels**: Medium (>3 units), High (>6 units)

---

#### 14. Reorder Point Calculation

**Algorithm**: `calculate_reorder_points()`

**Purpose**: Calculate optimal reorder points.

**Logic**:
```
1. For each SKU:
   a. Estimate daily sales rate from velocity
   b. Calculate lead time demand = daily_rate * lead_time_days
   c. Calculate safety stock = daily_rate * safety_stock_days
   d. Reorder point = lead_time_demand + safety_stock
2. Return reorder points
```

**Parameters**: 
- Lead time: 3 days
- Safety stock: 2 days

---

### Anomaly Detection Algorithms

#### 15. System Downtime Detection

**Algorithm**: `detect_system_crashes()`

**Purpose**: Detect system crashes by identifying gaps in event streams.

**Logic**:
```
1. Collect all events from all sources
2. Sort by timestamp
3. Group by station
4. For each station:
   a. Calculate time gaps between consecutive events
   b. If gap > min_gap_seconds (120s) AND
      gap > min_crash_duration (60s) → System Crash
5. Generate E004 event with duration
```

**Thresholds**:
- Minimum gap: 120 seconds
- Minimum duration: 60 seconds

---

#### 16. Statistical Anomaly Detection

**Algorithm**: `detect_statistical_anomalies()`

**Purpose**: Detect statistical outliers using Z-score method.

**Logic**:
```
1. Calculate mean of metrics
2. Calculate standard deviation
3. For each value:
   a. Calculate Z-score = (value - mean) / std_dev
   b. If |Z-score| > threshold (2.0) → Anomaly
4. Return indices of anomalous values
```

**Threshold**: 2.0 standard deviations

---

#### 17. Pattern-based Anomaly Detection

**Algorithm**: `detect_pattern_anomalies()`

**Purpose**: Detect deviations from expected patterns.

**Logic**:
```
1. Calculate moving average (window size 3)
2. For each point:
   a. Compare actual value with moving average
   b. Calculate: deviation = |actual - expected| / expected
   c. If deviation > 50% → Anomaly
3. Return anomaly details
```

---

#### 18. Behavioral Anomaly Detection

**Algorithm**: `detect_behavioral_anomalies()`

**Purpose**: Detect unusual customer behavior.

**Logic**:
```
1. For each transaction:
   a. Score on multiple dimensions:
      - Unusually low/high price: +1 point
      - Zero weight: +2 points
      - Unusual hour (< 6am or > 11pm): +1 point
   b. If anomaly_score >= 2 → Behavioral Anomaly
2. Return anomalies with factors
```

---

#### 19. Correlation Analysis

**Algorithm**: `detect_correlation_anomalies()`

**Purpose**: Detect anomalies through correlation breaks.

**Logic**:
```
1. For each pair of consecutive measurements:
   a. Calculate direction of change for both metrics
   b. For positive correlation:
      - If metrics change in opposite directions → Anomaly
   c. For negative correlation:
      - If metrics change in same direction → Anomaly
2. Return anomaly indices
```

---

## Data Models

### Input Data Structures

#### POSTransaction
```python
{
    "timestamp": "2025-08-13T16:00:00",
    "station_id": "SCC1",
    "status": "success",
    "customer_id": "C001",
    "sku": "PRD_F_03",
    "product_name": "Product Name",
    "barcode": "1234567890",
    "price": 280.0,
    "weight_g": 150.0
}
```

#### RFIDReading
```python
{
    "timestamp": "2025-08-13T16:00:00",
    "station_id": "SCC1",
    "status": "detected",
    "epc": "E280116060000000000000001",
    "location": "checkout",
    "sku": "PRD_F_03"
}
```

#### QueueMonitoring
```python
{
    "timestamp": "2025-08-13T16:00:00",
    "station_id": "SCC1",
    "status": "active",
    "customer_count": 3,
    "average_dwell_time": 180.5
}
```

### Output Data Structure

#### DetectedEvent
```python
{
    "timestamp": "2025-08-13T16:00:00",
    "event_id": "E001",
    "event_data": {
        "event_name": "Scanner Avoidance",
        "station_id": "SCC1",
        "customer_id": "C004",
        "product_sku": "PRD_S_04"
    }
}
```

---

## Usage Guide

### Basic Usage

```bash
# Run detection on input data
cd evidence/executables
python3 run_demo.py --data-dir /path/to/data

# Launch dashboard
python3 run_demo.py --data-dir /path/to/data --launch-dashboard

# Specify dataset type
python3 run_demo.py --data-dir /path/to/data --dataset-type test
```

### Advanced Usage

```python
# Use EventDetector programmatically
from src.event_detector import EventDetector

detector = EventDetector('path/to/data')
detector.load_data()
detector.run_all_detections()
detector.save_events('output/events.jsonl')

# Get summary
summary = detector.get_event_summary()
print(summary)
```

---

## API Reference

### EventDetector Class

#### `__init__(data_dir: str)`
Initialize detector with data directory.

#### `load_data()`
Load all input files (CSV and JSONL).

#### `run_all_detections()`
Execute all detection algorithms.

#### `run_fraud_detection()`
Run fraud detection algorithms only.

#### `run_queue_analysis()`
Run queue analysis algorithms only.

#### `run_inventory_monitoring()`
Run inventory monitoring algorithms only.

#### `run_anomaly_detection()`
Run anomaly detection algorithms only.

#### `save_events(output_path: str)`
Save detected events to JSONL file.

#### `get_event_summary() -> Dict[str, int]`
Get count of events by type.

---

## Testing

### Unit Testing

```bash
# Test individual algorithms
python3 -m pytest src/algorithms/test_fraud_detection.py
python3 -m pytest src/algorithms/test_queue_analyzer.py
```

### Integration Testing

```bash
# Test complete pipeline
python3 run_demo.py --data-dir ../../../data/input

# Verify output
python3 -c "import json; [json.loads(line) for line in open('results/events.jsonl')]"
```

### Validation

```bash
# Check algorithm tags
grep -r "@algorithm" src/

# Count events
wc -l results/events.jsonl

# Verify JSON format
python3 -m json.tool results/events.jsonl > /dev/null
```

---

## Troubleshooting

### Common Issues

**Issue**: Module import errors
**Solution**: Ensure you're running from the correct directory (evidence/executables/)

**Issue**: No events detected
**Solution**: Verify input data files exist and are in correct format

**Issue**: Dashboard won't start
**Solution**: Install streamlit: `pip install streamlit`

**Issue**: Permission denied
**Solution**: Run with `python3` instead of `python`

### Debug Mode

Add verbose logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

**End of Documentation**

For additional help, see README.md or SUBMISSION_GUIDE.md
