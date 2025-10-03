#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Data Generator for Project Sentinel
==========================================

Generates realistic synthetic data to demonstrate all detection algorithms.
Creates comprehensive test datasets with multiple event scenarios.

Usage:
    python generate_test_data.py --output-dir ./test_data --num-transactions 100

Features:
    - Multiple fraud scenarios (scanner avoidance, barcode switching, weight discrepancies)
    - Queue buildup patterns (long queues, wait times, staffing needs)
    - Inventory discrepancies and shrinkage
    - System anomalies and crashes
    - Statistical and behavioral anomalies

Author: LoopCode
Date: October 2025
"""

import json
import random
import csv
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import argparse


class TestDataGenerator:
    """Generates realistic test data for Project Sentinel"""
    
    def __init__(self, seed: int = 42):
        """Initialize generator with random seed for reproducibility"""
        random.seed(seed)
        
        # Product catalog
        self.products = [
            {"sku": "PRD_001", "name": "Apple iPhone 14", "price": 999.00, "weight": 174, "barcode": "123456789012"},
            {"sku": "PRD_002", "name": "Samsung Galaxy S23", "price": 849.00, "weight": 168, "barcode": "123456789013"},
            {"sku": "PRD_003", "name": "Sony WH-1000XM5", "price": 399.00, "weight": 250, "barcode": "123456789014"},
            {"sku": "PRD_004", "name": "Apple AirPods Pro", "price": 249.00, "weight": 56, "barcode": "123456789015"},
            {"sku": "PRD_005", "name": "Dell XPS 15 Laptop", "price": 1499.00, "weight": 1800, "barcode": "123456789016"},
            {"sku": "PRD_006", "name": "iPad Air", "price": 599.00, "weight": 461, "barcode": "123456789017"},
            {"sku": "PRD_007", "name": "Samsung 4K TV 55\"", "price": 799.00, "weight": 15000, "barcode": "123456789018"},
            {"sku": "PRD_008", "name": "Canon EOS R6", "price": 2499.00, "weight": 680, "barcode": "123456789019"},
            {"sku": "PRD_009", "name": "Nintendo Switch", "price": 299.00, "weight": 398, "barcode": "123456789020"},
            {"sku": "PRD_010", "name": "Bose SoundLink", "price": 149.00, "weight": 287, "barcode": "123456789021"},
            {"sku": "PRD_011", "name": "Apple Watch Series 8", "price": 429.00, "weight": 38, "barcode": "123456789022"},
            {"sku": "PRD_012", "name": "GoPro Hero 11", "price": 399.00, "weight": 154, "barcode": "123456789023"},
            {"sku": "PRD_013", "name": "Kindle Paperwhite", "price": 139.00, "weight": 205, "barcode": "123456789024"},
            {"sku": "PRD_014", "name": "Fitbit Charge 5", "price": 179.00, "weight": 29, "barcode": "123456789025"},
            {"sku": "PRD_015", "name": "Logitech MX Master 3", "price": 99.00, "weight": 141, "barcode": "123456789026"},
        ]
        
        # Customer database
        self.customers = [
            {"id": "C001", "name": "John Smith", "age": 35, "address": "123 Main St", "phone": "+1234567890"},
            {"id": "C002", "name": "Emma Johnson", "age": 28, "address": "456 Oak Ave", "phone": "+1234567891"},
            {"id": "C003", "name": "Michael Brown", "age": 42, "address": "789 Pine Rd", "phone": "+1234567892"},
            {"id": "C004", "name": "Sophia Davis", "age": 31, "address": "321 Elm St", "phone": "+1234567893"},
            {"id": "C005", "name": "William Wilson", "age": 39, "address": "654 Maple Dr", "phone": "+1234567894"},
            {"id": "C006", "name": "Olivia Martinez", "age": 26, "address": "987 Cedar Ln", "phone": "+1234567895"},
            {"id": "C007", "name": "James Anderson", "age": 45, "address": "147 Birch Ct", "phone": "+1234567896"},
            {"id": "C008", "name": "Ava Taylor", "age": 33, "address": "258 Spruce Way", "phone": "+1234567897"},
            {"id": "C009", "name": "Robert Thomas", "age": 51, "address": "369 Walnut Blvd", "phone": "+1234567898"},
            {"id": "C010", "name": "Isabella Moore", "age": 29, "address": "741 Cherry Ave", "phone": "+1234567899"},
        ]
        
        # Stations
        self.stations = ["SCC1", "SCC2", "SCC3", "SCC4"]
        
        # Base timestamp
        self.base_time = datetime(2025, 10, 4, 9, 0, 0)
        
    def generate_products_csv(self, output_path: Path):
        """Generate products_list.csv"""
        filepath = output_path / "products_list.csv"
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['SKU', 'product_name', 'quantity', 'EPC_range', 'barcode', 'weight', 'price'])
            for product in self.products:
                epc_range = f"EPC_{product['sku']}_001-100"
                quantity = random.randint(50, 200)
                writer.writerow([
                    product['sku'],
                    product['name'],
                    quantity,
                    epc_range,
                    product['barcode'],
                    product['weight'],
                    product['price']
                ])
        print(f"[OK] Generated: {filepath}")
    
    def generate_customers_csv(self, output_path: Path):
        """Generate customer_data.csv"""
        filepath = output_path / "customer_data.csv"
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Customer_ID', 'Name', 'Age', 'Address', 'TP'])
            for customer in self.customers:
                writer.writerow([
                    customer['id'],
                    customer['name'],
                    customer['age'],
                    customer['address'],
                    customer['phone']
                ])
        print(f"[OK] Generated: {filepath}")
    
    def generate_pos_transactions(self, output_path: Path, num_transactions: int):
        """Generate pos_transactions.jsonl with various fraud scenarios"""
        filepath = output_path / "pos_transactions.jsonl"
        transactions = []
        
        current_time = self.base_time
        
        for i in range(num_transactions):
            product = random.choice(self.products)
            customer = random.choice(self.customers)
            station = random.choice(self.stations)
            
            # Determine transaction type
            transaction_type = random.choices(
                ['normal', 'scanner_avoidance', 'barcode_switch', 'weight_discrepancy'],
                weights=[70, 10, 10, 10]
            )[0]
            
            if transaction_type == 'normal':
                status = 'success'
                weight = product['weight']
                barcode = product['barcode']
            elif transaction_type == 'scanner_avoidance':
                status = 'unknown'  # No barcode scan
                weight = product['weight']
                barcode = None
            elif transaction_type == 'barcode_switch':
                # Scan cheap item, take expensive item
                cheap_product = min(self.products, key=lambda p: p['price'])
                status = 'success'
                weight = product['weight']
                barcode = cheap_product['barcode']  # Wrong barcode
            else:  # weight_discrepancy
                status = 'success'
                weight = int(product['weight'] * random.uniform(0.3, 0.7))  # Significant difference
                barcode = product['barcode']
            
            transaction = {
                "timestamp": current_time.isoformat(),
                "station_id": station,
                "status": status,
                "data": {
                    "customer_id": customer['id'],
                    "sku": product['sku'],
                    "product_name": product['name'],
                    "barcode": barcode,
                    "price": product['price'],
                    "weight_g": weight
                }
            }
            transactions.append(transaction)
            
            # Increment time by 10-60 seconds
            current_time += timedelta(seconds=random.randint(10, 60))
        
        with open(filepath, 'w', encoding='utf-8') as f:
            for transaction in transactions:
                f.write(json.dumps(transaction) + '\n')
        
        print(f"[OK] Generated: {filepath} ({len(transactions)} transactions)")
        return transactions
    
    def generate_rfid_readings(self, output_path: Path, transactions: List[Dict]):
        """Generate rfid_readings.jsonl aligned with transactions"""
        filepath = output_path / "rfid_readings.jsonl"
        readings = []
        
        for transaction in transactions:
            # 80% of transactions have RFID readings
            if random.random() < 0.8:
                product_sku = transaction['data']['sku']
                product = next(p for p in self.products if p['sku'] == product_sku)
                
                reading = {
                    "timestamp": transaction['timestamp'],
                    "station_id": transaction['station_id'],
                    "status": "detected",
                    "data": {
                        "epc": f"EPC_{product_sku}_{random.randint(1, 100):03d}",
                        "location": transaction['station_id'],
                        "sku": product_sku
                    }
                }
                readings.append(reading)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            for reading in readings:
                f.write(json.dumps(reading) + '\n')
        
        print(f"[OK] Generated: {filepath} ({len(readings)} readings)")
    
    def generate_product_recognition(self, output_path: Path, transactions: List[Dict]):
        """Generate product_recognition.jsonl with vision predictions"""
        filepath = output_path / "product_recognition.jsonl"
        recognitions = []
        
        for transaction in transactions:
            # 90% of transactions have product recognition
            if random.random() < 0.9:
                product_sku = transaction['data']['sku']
                
                # Sometimes misidentify (5% error rate)
                if random.random() < 0.05:
                    predicted_sku = random.choice(self.products)['sku']
                    accuracy = random.uniform(0.4, 0.6)
                else:
                    predicted_sku = product_sku
                    accuracy = random.uniform(0.85, 0.99)
                
                recognition = {
                    "timestamp": transaction['timestamp'],
                    "station_id": transaction['station_id'],
                    "status": "detected",
                    "data": {
                        "predicted_product": predicted_sku,
                        "accuracy": round(accuracy, 2)
                    }
                }
                recognitions.append(recognition)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            for recognition in recognitions:
                f.write(json.dumps(recognition) + '\n')
        
        print(f"[OK] Generated: {filepath} ({len(recognitions)} recognitions)")
    
    def generate_queue_monitoring(self, output_path: Path, num_measurements: int):
        """Generate queue_monitoring.jsonl with queue patterns"""
        filepath = output_path / "queue_monitoring.jsonl"
        measurements = []
        
        current_time = self.base_time
        
        for i in range(num_measurements):
            station = random.choice(self.stations)
            
            # Simulate queue patterns - peaks during lunch and evening
            hour = current_time.hour
            if 12 <= hour <= 13 or 17 <= hour <= 19:
                # Peak hours - longer queues
                customer_count = random.randint(8, 15)
                avg_dwell = random.uniform(180, 420)  # 3-7 minutes
                status = 'busy'
            else:
                # Normal hours
                customer_count = random.randint(1, 5)
                avg_dwell = random.uniform(60, 180)  # 1-3 minutes
                status = 'normal'
            
            measurement = {
                "timestamp": current_time.isoformat(),
                "station_id": station,
                "status": status,
                "data": {
                    "customer_count": customer_count,
                    "average_dwell_time": round(avg_dwell, 2)
                }
            }
            measurements.append(measurement)
            
            # Every 30 seconds
            current_time += timedelta(seconds=30)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            for measurement in measurements:
                f.write(json.dumps(measurement) + '\n')
        
        print(f"[OK] Generated: {filepath} ({len(measurements)} measurements)")
    
    def generate_inventory_snapshots(self, output_path: Path, num_snapshots: int):
        """Generate inventory_snapshots.jsonl with discrepancies"""
        filepath = output_path / "inventory_snapshots.jsonl"
        snapshots = []
        
        current_time = self.base_time
        
        # Initial inventory
        inventory = {p['sku']: random.randint(80, 150) for p in self.products}
        
        for i in range(num_snapshots):
            # Update inventory with random changes
            for sku in inventory:
                # Natural sales (decrease)
                change = random.randint(-5, -1)
                
                # Occasional shrinkage (unexpected decrease)
                if random.random() < 0.1:
                    change -= random.randint(10, 20)
                
                # Occasional restock
                if random.random() < 0.05:
                    change += random.randint(50, 100)
                
                inventory[sku] = max(0, inventory[sku] + change)
            
            snapshot = {
                "timestamp": current_time.isoformat(),
                "data": inventory.copy()
            }
            snapshots.append(snapshot)
            
            # Every hour
            current_time += timedelta(hours=1)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            for snapshot in snapshots:
                f.write(json.dumps(snapshot) + '\n')
        
        print(f"[OK] Generated: {filepath} ({len(snapshots)} snapshots)")
    
    def generate_all(self, output_dir: Path, num_transactions: int = 100, num_queue_measurements: int = 200, num_snapshots: int = 12):
        """Generate complete test dataset"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print("\n" + "="*70)
        print("GENERATING TEST DATA FOR PROJECT SENTINEL".center(70))
        print("="*70 + "\n")
        
        print(f"Output directory: {output_dir}")
        print(f"Transactions: {num_transactions}")
        print(f"Queue measurements: {num_queue_measurements}")
        print(f"Inventory snapshots: {num_snapshots}")
        print()
        
        # Generate CSV files
        self.generate_products_csv(output_dir)
        self.generate_customers_csv(output_dir)
        
        # Generate JSONL files
        transactions = self.generate_pos_transactions(output_dir, num_transactions)
        self.generate_rfid_readings(output_dir, transactions)
        self.generate_product_recognition(output_dir, transactions)
        self.generate_queue_monitoring(output_dir, num_queue_measurements)
        self.generate_inventory_snapshots(output_dir, num_snapshots)
        
        print("\n" + "="*70)
        print("DATA GENERATION COMPLETE".center(70))
        print("="*70)
        print(f"\nAll files created in: {output_dir}")
        print("\nExpected events to detect:")
        print("  - Scanner avoidance events (no barcode)")
        print("  - Barcode switching (wrong item)")
        print("  - Weight discrepancies")
        print("  - Long queue warnings (peak hours)")
        print("  - Long wait times")
        print("  - Inventory discrepancies")
        print("  - Shrinkage detection")
        print("\nNext steps:")
        print(f"  1. Run detection: python run_demo.py --data-dir {output_dir}")
        print(f"  2. View results: cat results/events.jsonl")
        print(f"  3. Launch dashboard: python run_demo.py --dashboard-only")


def main():
    parser = argparse.ArgumentParser(
        description='Generate test data for Project Sentinel',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate default dataset (100 transactions)
  python generate_test_data.py
  
  # Generate large dataset (500 transactions)
  python generate_test_data.py --num-transactions 500
  
  # Custom output directory
  python generate_test_data.py --output-dir ./my_test_data
        """
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='./generated_test_data',
        help='Directory to save generated data (default: ./generated_test_data)'
    )
    
    parser.add_argument(
        '--num-transactions',
        type=int,
        default=100,
        help='Number of POS transactions to generate (default: 100)'
    )
    
    parser.add_argument(
        '--num-queue-measurements',
        type=int,
        default=200,
        help='Number of queue measurements (default: 200)'
    )
    
    parser.add_argument(
        '--num-snapshots',
        type=int,
        default=12,
        help='Number of inventory snapshots (default: 12)'
    )
    
    parser.add_argument(
        '--seed',
        type=int,
        default=42,
        help='Random seed for reproducibility (default: 42)'
    )
    
    args = parser.parse_args()
    
    generator = TestDataGenerator(seed=args.seed)
    output_path = Path(args.output_dir)
    
    generator.generate_all(
        output_path,
        num_transactions=args.num_transactions,
        num_queue_measurements=args.num_queue_measurements,
        num_snapshots=args.num_snapshots
    )


if __name__ == '__main__':
    main()
