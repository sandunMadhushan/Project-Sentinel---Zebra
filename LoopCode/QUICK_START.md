# QuGenerate realistic test data to see all algorithms in action:

```bash
cd LoopCode_sentinel/tools
python generate_test_data.py

# Run detection on generated data
cd ../evidence/executables
python run_demo.py --data-dir ../../tools/generated_test_data --dataset-type test
```uide

## Option 1: Generate Test Data (Recommended)

Generate realistic test data to see all detection algorithms in action:

```bash
cd Team01_sentinel/tools
python generate_test_data.py

# Run detection on generated data
cd ../evidence/executables
python run_demo.py --data-dir ../../tools/generated_test_data --dataset-type test
```

This generates 100+ transactions with multiple fraud scenarios, queue patterns, and inventory issues.

## Option 2: Use Provided Sample Data

```bash
cd LoopCode_sentinel/evidence/executables
python run_demo.py --data-dir ../../../data/input --dataset-type test
```

Note: Sample data has minimal records (1-2 per file), so you'll see fewer events.

## Check Output

```bash
# View generated events
cat results/events.jsonl

# View summary
cat results/summary_report.txt

# Check evidence folder
ls -la ../../evidence/output/test/
```

## Launch Dashboard

```bash
# Launch dashboard with latest results
python run_demo.py --dashboard-only
```

Or run full pipeline with dashboard:

```bash
python run_demo.py --data-dir ../../tools/generated_test_data --launch-dashboard
```

## What Gets Created

After running, you'll have:
- `results/events.jsonl` - Main output file
- `results/summary_report.txt` - Statistical summary
- `evidence/output/test/events.jsonl` - Copy for judges

## Troubleshooting

If you get import errors, run from the executables directory:
```bash
cd evidence/executables
python run_demo.py --data-dir ../../../data/input
```
