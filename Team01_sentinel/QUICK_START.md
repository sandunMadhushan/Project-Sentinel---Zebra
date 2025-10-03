# Quick Test Guide

## Run the Full Solution

```bash
cd Team01_sentinel/evidence/executables
python run_demo.py --data-dir ../../../data/input --dataset-type test
```

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
python run_demo.py --data-dir ../../../data/input --launch-dashboard
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
