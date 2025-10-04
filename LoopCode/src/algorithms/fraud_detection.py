"""
Fraud Detection Algorithms
===========================

This module contains algorithms for detecting fraudulent activities
at self-checkout stations, including scanner avoidance, barcode switching,
and weight discrepancies.

Author: Team 01
Date: October 2025
"""

from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_models import (DetectedEvent, POSTransaction, RFIDReading, 
                          ProductRecognition)


# @algorithm Scanner Avoidance Detection (RFID-based) | Detect items that were detected by RFID but not scanned at POS
def detect_scanner_avoidance_rfid(rfid_readings: List[RFIDReading],
                                  pos_transactions: List[POSTransaction],
                                  time_window_seconds: int = 60) -> List[DetectedEvent]:
    """
    Detect scanner avoidance by comparing RFID readings with POS transactions.
    
    Algorithm:
    1. Group RFID readings by station and time window
    2. Group POS transactions by station and time window
    3. For each station, compare RFID-detected items vs scanned items
    4. If RFID detected an item but it wasn't scanned, flag as scanner avoidance
    
    Args:
        rfid_readings: List of RFID reading events
        pos_transactions: List of POS transaction events
        time_window_seconds: Time window for matching events
        
    Returns:
        List of detected scanner avoidance events
    """
    events = []
    
    # Group RFID readings by station
    rfid_by_station = {}
    for reading in rfid_readings:
        station = reading.station_id
        if station not in rfid_by_station:
            rfid_by_station[station] = []
        rfid_by_station[station].append(reading)
    
    # Group POS transactions by station
    pos_by_station = {}
    for transaction in pos_transactions:
        station = transaction.station_id
        if station not in pos_by_station:
            pos_by_station[station] = []
        pos_by_station[station].append(transaction)
    
    # Compare RFID vs POS for each station
    for station_id in rfid_by_station:
        rfid_items = rfid_by_station[station_id]
        pos_items = pos_by_station.get(station_id, [])
        
        # Track which SKUs were scanned
        scanned_skus = {item.sku for item in pos_items}
        
        # Check for unscanned items detected by RFID
        for rfid_item in rfid_items:
            if rfid_item.sku not in scanned_skus and rfid_item.sku:
                # Scanner avoidance detected
                customer_id = pos_items[0].customer_id if pos_items else "UNKNOWN"
                event = DetectedEvent.create_scanner_avoidance(
                    timestamp=rfid_item.timestamp,
                    station_id=station_id,
                    customer_id=customer_id,
                    product_sku=rfid_item.sku
                )
                events.append(event)
    
    return events


# @algorithm Vision-Based Scanner Avoidance Detection | Detect items seen by vision system but not scanned at POS
def detect_scanner_avoidance_vision(vision_predictions: List[ProductRecognition],
                                   pos_transactions: List[POSTransaction],
                                   confidence_threshold: float = 0.70) -> List[DetectedEvent]:
    """
    Detect scanner avoidance using vision system predictions.
    
    This is the PRIMARY scanner avoidance detection method that aligns with
    Zebra's documentation about vision system predictions. It detects when
    the vision system sees a product with high confidence but no matching
    POS transaction occurs within a reasonable time window.
    
    Algorithm:
    1. Filter vision predictions by confidence threshold (default 70%)
    2. For each high-confidence prediction, define time window [-5s, +10s]
    3. Search for matching POS transaction in that window
    4. Match criteria: same station_id AND same SKU
    5. If no match found, flag as scanner avoidance
    
    Time window rationale:
    - Look back 5s: Customer may scan before vision system confirms
    - Look ahead 10s: Vision may detect before customer finishes scanning
    
    Args:
        vision_predictions: List of vision system predictions
        pos_transactions: List of POS transactions
        confidence_threshold: Minimum confidence to consider (default 0.70)
        
    Returns:
        List of detected scanner avoidance events
    """
    events = []
    
    # Filter predictions by confidence
    reliable_predictions = [
        pred for pred in vision_predictions 
        if pred.accuracy >= confidence_threshold
    ]
    
    # Convert timestamps to datetime for comparison
    for prediction in reliable_predictions:
        vision_time = datetime.fromisoformat(prediction.timestamp)
        station_id = prediction.station_id
        predicted_sku = prediction.predicted_product
        
        # Define time window: -5 seconds to +10 seconds from vision detection
        window_start = vision_time - timedelta(seconds=5)
        window_end = vision_time + timedelta(seconds=10)
        
        # Search for matching POS transaction
        matching_found = False
        for transaction in pos_transactions:
            if transaction.station_id != station_id:
                continue
            
            trans_time = datetime.fromisoformat(transaction.timestamp)
            
            # Check if transaction is within time window and matches SKU
            if (window_start <= trans_time <= window_end and 
                transaction.sku == predicted_sku):
                matching_found = True
                break
        
        # If no matching transaction found, this is scanner avoidance
        if not matching_found:
            event = DetectedEvent.create_scanner_avoidance(
                timestamp=prediction.timestamp,
                station_id=station_id,
                customer_id="UNKNOWN",  # Vision system doesn't track customer ID
                product_sku=predicted_sku
            )
            events.append(event)
    
    return events


# @algorithm Barcode Switching Detection | Detect when a customer scans a different product barcode than what was detected
def detect_barcode_switching(pos_transactions: List[POSTransaction],
                             vision_predictions: List[ProductRecognition],
                             products_catalog: Dict[str, Dict]) -> List[DetectedEvent]:
    """
    Detect barcode switching by comparing vision system predictions with POS scans.
    
    Algorithm:
    1. Match vision predictions with POS transactions by station and timestamp
    2. Compare predicted product SKU with scanned product SKU
    3. If they don't match and vision accuracy is high, flag as barcode switching
    
    Args:
        pos_transactions: List of POS transactions
        vision_predictions: List of vision system predictions
        products_catalog: Product catalog with SKU information
        
    Returns:
        List of detected barcode switching events
    """
    events = []
    
    # Accuracy threshold for considering vision prediction reliable
    ACCURACY_THRESHOLD = 0.85
    
    # Group by station for comparison
    pos_by_station = {}
    for transaction in pos_transactions:
        station = transaction.station_id
        if station not in pos_by_station:
            pos_by_station[station] = []
        pos_by_station[station].append(transaction)
    
    vision_by_station = {}
    for prediction in vision_predictions:
        station = prediction.station_id
        if station not in vision_by_station:
            vision_by_station[station] = []
        vision_by_station[station].append(prediction)
    
    # Compare predictions with actual scans
    for station_id in vision_by_station:
        if station_id not in pos_by_station:
            continue
            
        predictions = vision_by_station[station_id]
        transactions = pos_by_station[station_id]
        
        # Simple matching: compare sequential items
        for i, prediction in enumerate(predictions):
            if prediction.accuracy >= ACCURACY_THRESHOLD and i < len(transactions):
                transaction = transactions[i]
                
                # Check if predicted product differs from scanned product
                if prediction.predicted_product != transaction.sku:
                    event = DetectedEvent.create_barcode_switching(
                        timestamp=transaction.timestamp,
                        station_id=station_id,
                        customer_id=transaction.customer_id,
                        actual_sku=prediction.predicted_product,
                        scanned_sku=transaction.sku
                    )
                    events.append(event)
    
    return events


# @algorithm Weight Verification | Detect weight discrepancies between expected and actual product weights
def detect_weight_discrepancies(pos_transactions: List[POSTransaction],
                                products_catalog: Dict[str, Dict],
                                tolerance_percent: float = 10.0) -> List[DetectedEvent]:
    """
    Detect weight discrepancies by comparing actual weights with expected weights.
    
    Algorithm:
    1. For each POS transaction, get the expected weight from catalog
    2. Compare actual scanned weight with expected weight
    3. If difference exceeds tolerance threshold, flag as weight discrepancy
    
    Args:
        pos_transactions: List of POS transactions with weight data
        products_catalog: Product catalog with expected weights
        tolerance_percent: Acceptable weight variance percentage
        
    Returns:
        List of detected weight discrepancy events
    """
    events = []
    
    for transaction in pos_transactions:
        sku = transaction.sku
        
        if sku not in products_catalog:
            continue
        
        expected_weight = products_catalog[sku]['weight']
        actual_weight = transaction.weight_g
        
        # Calculate percentage difference
        if expected_weight > 0:
            percent_diff = abs(actual_weight - expected_weight) / expected_weight * 100
            
            # Check if difference exceeds tolerance
            if percent_diff > tolerance_percent:
                event = DetectedEvent.create_weight_discrepancy(
                    timestamp=transaction.timestamp,
                    station_id=transaction.station_id,
                    customer_id=transaction.customer_id,
                    product_sku=sku,
                    expected_weight=expected_weight,
                    actual_weight=actual_weight
                )
                events.append(event)
    
    return events


# @algorithm Success Operation Detection | Detect successful checkout operations with no anomalies
def detect_success_operations(pos_transactions: List[POSTransaction],
                              rfid_readings: List[RFIDReading],
                              products_catalog: Dict[str, Dict],
                              weight_tolerance: float = 15.0) -> List[DetectedEvent]:
    """
    Detect successful checkout operations where everything went smoothly.
    
    Algorithm:
    1. Identify POS transactions that have matching RFID readings
    2. Verify weight is within acceptable tolerance
    3. Confirm transaction status is successful
    4. Flag as success operation if all checks pass
    
    Args:
        pos_transactions: List of POS transactions
        rfid_readings: List of RFID readings
        products_catalog: Product catalog
        weight_tolerance: Weight tolerance percentage
        
    Returns:
        List of success operation events
    """
    events = []
    
    # Create set of RFID-detected SKUs by station
    rfid_skus_by_station = {}
    for reading in rfid_readings:
        station = reading.station_id
        if station not in rfid_skus_by_station:
            rfid_skus_by_station[station] = set()
        rfid_skus_by_station[station].add(reading.sku)
    
    for transaction in pos_transactions:
        # Check if transaction was successful
        if transaction.status.lower() != 'success':
            continue
        
        # Check if RFID detected this item
        rfid_detected = (transaction.station_id in rfid_skus_by_station and 
                        transaction.sku in rfid_skus_by_station[transaction.station_id])
        
        # Check weight
        weight_ok = True
        if transaction.sku in products_catalog:
            expected_weight = products_catalog[transaction.sku]['weight']
            if expected_weight > 0:
                percent_diff = abs(transaction.weight_g - expected_weight) / expected_weight * 100
                weight_ok = percent_diff <= weight_tolerance
        
        # If all checks pass, mark as success operation
        if rfid_detected and weight_ok:
            event = DetectedEvent.create_success_operation(
                timestamp=transaction.timestamp,
                station_id=transaction.station_id,
                customer_id=transaction.customer_id,
                product_sku=transaction.sku
            )
            events.append(event)
    
    return events
