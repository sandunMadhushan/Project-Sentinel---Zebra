"""
Event Detector - Main Detection Logic
======================================

This module orchestrates all detection algorithms and produces
the final events.jsonl output file.

Author: Team 01
Date: October 2025
"""

# -*- coding: utf-8 -*-

from typing import List, Dict, Tuple
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from data_models import (
    DetectedEvent, POSTransaction, RFIDReading,
    ProductRecognition, QueueMonitoring, InventorySnapshot
)
from algorithms.fraud_detection import (
    detect_scanner_avoidance_rfid, detect_scanner_avoidance_vision,
    detect_barcode_switching, detect_weight_discrepancies, 
    detect_success_operations
)
from algorithms.queue_analyzer import (
    detect_long_queues, detect_long_wait_times,
    predict_staffing_needs, manage_station_status
)
from algorithms.inventory_monitor import (
    detect_inventory_discrepancies, monitor_stock_levels
)
from algorithms.anomaly_detector import (
    detect_system_crashes, detect_statistical_anomalies
)
from utils.helpers import (
    load_products_catalog, load_customers_data,
    load_jsonl_file, save_events_to_jsonl
)


class EventDetector:
    """
    Main event detection orchestrator.
    
    This class loads all input data, runs detection algorithms,
    and generates the events.jsonl output file.
    """
    
    def __init__(self, data_dir: str):
        """
        Initialize EventDetector with data directory.
        
        Args:
            data_dir: Path to directory containing input data
        """
        self.data_dir = Path(data_dir)
        self.products_catalog = {}
        self.customers_data = {}
        self.pos_transactions = []
        self.rfid_readings = []
        self.product_recognitions = []
        self.queue_monitoring = []
        self.inventory_snapshots = []
        self.detected_events = []
    
    def load_data(self):
        """Load all input data from files."""
        print("Loading input data...")
        
        # Load CSV files
        products_csv = self.data_dir / 'products_list.csv'
        if products_csv.exists():
            self.products_catalog = load_products_catalog(str(products_csv))
            print(f"  [OK] Loaded {len(self.products_catalog)} products")
        
        customers_csv = self.data_dir / 'customer_data.csv'
        if customers_csv.exists():
            self.customers_data = load_customers_data(str(customers_csv))
            print(f"  [OK] Loaded {len(self.customers_data)} customers")
        
        # Load JSONL files
        pos_file = self.data_dir / 'pos_transactions.jsonl'
        if pos_file.exists():
            pos_data = load_jsonl_file(str(pos_file))
            self.pos_transactions = [POSTransaction.from_stream(d) for d in pos_data]
            print(f"  [OK] Loaded {len(self.pos_transactions)} POS transactions")
        
        rfid_file = self.data_dir / 'rfid_readings.jsonl'
        if rfid_file.exists():
            rfid_data = load_jsonl_file(str(rfid_file))
            self.rfid_readings = [RFIDReading.from_stream(d) for d in rfid_data]
            print(f"  [OK] Loaded {len(self.rfid_readings)} RFID readings")
        
        recognition_file = self.data_dir / 'product_recognition.jsonl'
        if recognition_file.exists():
            recognition_data = load_jsonl_file(str(recognition_file))
            self.product_recognitions = [ProductRecognition.from_stream(d) for d in recognition_data]
            print(f"  [OK] Loaded {len(self.product_recognitions)} product recognitions")
        
        queue_file = self.data_dir / 'queue_monitoring.jsonl'
        if queue_file.exists():
            queue_data = load_jsonl_file(str(queue_file))
            self.queue_monitoring = [QueueMonitoring.from_stream(d) for d in queue_data]
            print(f"  [OK] Loaded {len(self.queue_monitoring)} queue measurements")
        
        inventory_file = self.data_dir / 'inventory_snapshots.jsonl'
        if inventory_file.exists():
            inventory_data = load_jsonl_file(str(inventory_file))
            self.inventory_snapshots = [InventorySnapshot.from_stream(d) for d in inventory_data]
            print(f"  [OK] Loaded {len(self.inventory_snapshots)} inventory snapshots")
        
        print("Data loading complete!\n")
    
    def run_fraud_detection(self):
        """Run all fraud detection algorithms."""
        print("Running fraud detection algorithms...")
        
        # Detect success operations
        success_events = detect_success_operations(
            self.pos_transactions,
            self.rfid_readings,
            self.products_catalog
        )
        self.detected_events.extend(success_events)
        print(f"  [OK] Detected {len(success_events)} success operations")
        
        # Detect scanner avoidance (PRIMARY: Vision-based detection)
        # This aligns with Zebra documentation about vision system predictions
        avoidance_events_vision = detect_scanner_avoidance_vision(
            self.product_recognitions,
            self.pos_transactions
        )
        self.detected_events.extend(avoidance_events_vision)
        print(f"  [OK] Detected {len(avoidance_events_vision)} scanner avoidance events (vision-based)")
        
        # Detect scanner avoidance (SECONDARY: RFID-based detection)
        # Additional layer using RFID tags for redundancy
        avoidance_events_rfid = detect_scanner_avoidance_rfid(
            self.rfid_readings,
            self.pos_transactions
        )
        self.detected_events.extend(avoidance_events_rfid)
        print(f"  [OK] Detected {len(avoidance_events_rfid)} scanner avoidance events (RFID-based)")
        
        # Detect barcode switching
        switching_events = detect_barcode_switching(
            self.pos_transactions,
            self.product_recognitions,
            self.products_catalog
        )
        self.detected_events.extend(switching_events)
        print(f"  [OK] Detected {len(switching_events)} barcode switching events")
        
        # Detect weight discrepancies
        weight_events = detect_weight_discrepancies(
            self.pos_transactions,
            self.products_catalog
        )
        self.detected_events.extend(weight_events)
        print(f"  [OK] Detected {len(weight_events)} weight discrepancy events")
    
    def run_queue_analysis(self):
        """Run all queue analysis algorithms."""
        print("\nRunning queue analysis algorithms...")
        
        # Detect long queues
        long_queue_events = detect_long_queues(self.queue_monitoring)
        self.detected_events.extend(long_queue_events)
        print(f"  [OK] Detected {len(long_queue_events)} long queue events")
        
        # Detect long wait times
        wait_time_events = detect_long_wait_times(self.queue_monitoring)
        self.detected_events.extend(wait_time_events)
        print(f"  [OK] Detected {len(wait_time_events)} long wait time events")
        
        # Predict staffing needs
        staffing_events = predict_staffing_needs(self.queue_monitoring)
        self.detected_events.extend(staffing_events)
        print(f"  [OK] Detected {len(staffing_events)} staffing needs events")
        
        # Manage station status
        station_events = manage_station_status(self.queue_monitoring)
        self.detected_events.extend(station_events)
        print(f"  [OK] Detected {len(station_events)} checkout station actions")
    
    def run_inventory_monitoring(self):
        """Run inventory monitoring algorithms."""
        print("\nRunning inventory monitoring algorithms...")
        
        if len(self.inventory_snapshots) >= 2:
            # Detect inventory discrepancies
            initial_snapshot = self.inventory_snapshots[0]
            final_snapshot = self.inventory_snapshots[-1]
            
            inventory_events = detect_inventory_discrepancies(
                initial_snapshot,
                final_snapshot,
                self.pos_transactions
            )
            self.detected_events.extend(inventory_events)
            print(f"  [OK] Detected {len(inventory_events)} inventory discrepancy events")
        else:
            print("  [WARN] Not enough inventory snapshots for discrepancy detection")
    
    def run_anomaly_detection(self):
        """Run anomaly detection algorithms."""
        print("\nRunning anomaly detection algorithms...")
        
        # Prepare all events for crash detection
        all_events = []
        for transaction in self.pos_transactions:
            all_events.append({
                'timestamp': transaction.timestamp,
                'station_id': transaction.station_id,
                'type': 'pos'
            })
        for reading in self.rfid_readings:
            all_events.append({
                'timestamp': reading.timestamp,
                'station_id': reading.station_id,
                'type': 'rfid'
            })
        for queue in self.queue_monitoring:
            all_events.append({
                'timestamp': queue.timestamp,
                'station_id': queue.station_id,
                'type': 'queue'
            })
        
        # Detect system crashes
        crash_events = detect_system_crashes(all_events)
        self.detected_events.extend(crash_events)
        print(f"  [OK] Detected {len(crash_events)} system crash events")
    
    def run_all_detections(self):
        """Run all detection algorithms."""
        print("\n" + "="*60)
        print("STARTING EVENT DETECTION")
        print("="*60 + "\n")
        
        self.run_fraud_detection()
        self.run_queue_analysis()
        self.run_inventory_monitoring()
        self.run_anomaly_detection()
        
        print("\n" + "="*60)
        print(f"TOTAL EVENTS DETECTED: {len(self.detected_events)}")
        print("="*60 + "\n")
    
    def save_events(self, output_path: str):
        """
        Save detected events to JSONL file.
        
        Args:
            output_path: Path to output events.jsonl file
        """
        # Sort events by timestamp
        sorted_events = sorted(self.detected_events, key=lambda e: e.timestamp)
        
        save_events_to_jsonl(sorted_events, output_path)
        print(f"[OK] Events saved to: {output_path}\n")
    
    def get_event_summary(self) -> Dict[str, int]:
        """
        Get summary of detected events by type.
        
        Returns:
            Dictionary mapping event_id to count
        """
        summary = {}
        for event in self.detected_events:
            event_id = event.event_id
            summary[event_id] = summary.get(event_id, 0) + 1
        return summary


def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Project Sentinel Event Detector')
    parser.add_argument('--data-dir', required=True, help='Directory containing input data')
    parser.add_argument('--output', required=True, help='Output events.jsonl file path')
    
    args = parser.parse_args()
    
    # Initialize detector
    detector = EventDetector(args.data_dir)
    
    # Load data
    detector.load_data()
    
    # Run all detections
    detector.run_all_detections()
    
    # Print summary
    summary = detector.get_event_summary()
    print("Event Summary:")
    for event_id, count in sorted(summary.items()):
        print(f"  {event_id}: {count} events")
    
    # Save events
    detector.save_events(args.output)
    
    print("[OK] Detection complete!")


if __name__ == '__main__':
    main()
