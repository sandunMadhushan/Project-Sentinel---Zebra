# Project Sentinel Tools

This directory contains utility scripts for testing and development.

## Test Data Generator

Generate realistic synthetic data to test all detection algorithms.

### Quick Start

```bash
cd tools
python generate_test_data.py
```

This creates `generated_test_data/` with:
- 100 POS transactions
- 200 queue measurements
- 12 inventory snapshots
- Multiple fraud scenarios
- Queue patterns with peak hours
- Inventory discrepancies

### Usage Examples

**Generate default dataset:**
```bash
python generate_test_data.py
```

**Generate large dataset (500 transactions):**
```bash
python generate_test_data.py --num-transactions 500 --num-queue-measurements 500
```

**Custom output location:**
```bash
python generate_test_data.py --output-dir ../test_datasets/scenario1
```

**All options:**
```bash
python generate_test_data.py \
  --output-dir ./my_data \
  --num-transactions 200 \
  --num-queue-measurements 400 \
  --num-snapshots 24 \
  --seed 123
```

### Running Detection on Generated Data

After generating data:

```bash
cd ../evidence/executables
python run_demo.py --data-dir ../../tools/generated_test_data --dataset-type test
```

### What Gets Generated

**CSV Files:**
- `products_list.csv` - 15 products with realistic prices/weights
- `customer_data.csv` - 10 customers with contact info

**JSONL Files:**
- `pos_transactions.jsonl` - Transactions with fraud patterns
- `rfid_readings.jsonl` - RFID tag readings (80% coverage)
- `product_recognition.jsonl` - Vision system predictions (90% coverage)
- `queue_monitoring.jsonl` - Queue metrics with peak hours
- `inventory_snapshots.jsonl` - Inventory changes with shrinkage

### Event Scenarios Included

The generator creates realistic scenarios for:

1. **Fraud Detection:**
   - Scanner avoidance (10% of transactions)
   - Barcode switching (10% of transactions)
   - Weight discrepancies (10% of transactions)

2. **Queue Issues:**
   - Long queues during lunch (12-1pm) and evening (5-7pm)
   - Extended wait times at peak hours
   - Staffing optimization scenarios

3. **Inventory Problems:**
   - Gradual inventory depletion
   - Unexpected shrinkage events
   - Restock patterns
   - Low stock warnings

4. **Product Recognition:**
   - 95% accuracy rate
   - 5% misidentification scenarios
   - Confidence score variations

### Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--output-dir` | `./generated_test_data` | Where to save files |
| `--num-transactions` | `100` | Number of POS transactions |
| `--num-queue-measurements` | `200` | Queue monitoring data points |
| `--num-snapshots` | `12` | Inventory snapshots (hourly) |
| `--seed` | `42` | Random seed for reproducibility |

### Tips

- Use `--seed` with same value to reproduce exact same data
- Increase `--num-transactions` to generate more fraud events
- More snapshots (`--num-snapshots`) enables better inventory discrepancy detection
- Queue measurements should be ~2x transactions for realistic monitoring

### Expected Detection Results

With default settings (100 transactions), expect to detect:
- ~10 scanner avoidance events
- ~10 barcode switching events  
- ~10 weight discrepancy events
- ~5-10 long queue warnings
- ~5-10 wait time alerts
- ~2-5 inventory discrepancies
- ~1-3 shrinkage events

**Total: 40-60 events detected**

### Troubleshooting

**Issue:** No fraud events detected
- **Solution:** Increase `--num-transactions` to 200+

**Issue:** No queue events detected
- **Solution:** Ensure `--num-queue-measurements` is high enough (400+)

**Issue:** No inventory discrepancies
- **Solution:** Use `--num-snapshots 24` for more comparison points

### Development Notes

The generator uses:
- Reproducible random seed for testing
- Realistic product catalog (phones, laptops, TVs, etc.)
- Time-based patterns (peak hours, gradual changes)
- Multi-modal sensor correlation (POS + RFID + Vision)
