"""
Helper Utilities for Project Sentinel
======================================

This module provides utility functions for data loading, parsing,
and common operations used throughout the system.

Author: Team 01
Date: October 2025
"""

import csv
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime, timedelta


def load_products_catalog(csv_path: str) -> Dict[str, Dict]:
    """
    Load products catalog from CSV file.
    
    Args:
        csv_path: Path to products_list.csv
        
    Returns:
        Dictionary mapping SKU to product attributes
    """
    products = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sku = row['SKU']
            products[sku] = {
                'product_name': row['product_name'],
                'quantity': int(row['quantity']),
                'epc_range': row['EPC_range'],
                'barcode': row['barcode'],
                'weight': float(row['weight']),
                'price': float(row['price'])
            }
    return products


def load_customers_data(csv_path: str) -> Dict[str, Dict]:
    """
    Load customer data from CSV file.
    
    Args:
        csv_path: Path to customer_data.csv
        
    Returns:
        Dictionary mapping Customer_ID to customer attributes
    """
    customers = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            customer_id = row['Customer_ID']
            customers[customer_id] = {
                'name': row.get('Name', ''),
                'age': row.get('Age', ''),
                'address': row.get('Address', ''),
                'phone': row.get('TP', row.get('Phone', ''))
            }
    return customers


def load_jsonl_file(file_path: str) -> List[Dict]:
    """
    Load data from JSONL (JSON Lines) file.
    
    Args:
        file_path: Path to JSONL file
        
    Returns:
        List of parsed JSON objects
    """
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    return data


def parse_timestamp(timestamp_str: str) -> datetime:
    """
    Parse timestamp string to datetime object.
    
    Args:
        timestamp_str: Timestamp string in ISO format
        
    Returns:
        datetime object
    """
    return datetime.fromisoformat(timestamp_str)


def format_timestamp(dt: datetime) -> str:
    """
    Format datetime object to timestamp string.
    
    Args:
        dt: datetime object
        
    Returns:
        ISO format timestamp string
    """
    return dt.strftime('%Y-%m-%dT%H:%M:%S')


def calculate_time_difference(timestamp1: str, timestamp2: str) -> float:
    """
    Calculate time difference in seconds between two timestamps.
    
    Args:
        timestamp1: First timestamp
        timestamp2: Second timestamp
        
    Returns:
        Time difference in seconds
    """
    dt1 = parse_timestamp(timestamp1)
    dt2 = parse_timestamp(timestamp2)
    return abs((dt2 - dt1).total_seconds())


def is_epc_in_range(epc: str, epc_range: str) -> bool:
    """
    Check if an EPC is within a given range.
    
    Args:
        epc: EPC tag value
        epc_range: Range string (e.g., "START-END")
        
    Returns:
        True if EPC is in range, False otherwise
    """
    if '-' not in epc_range:
        return False
    start, end = epc_range.split('-')
    return start <= epc <= end


def find_product_by_epc(epc: str, products: Dict[str, Dict]) -> str:
    """
    Find product SKU by EPC tag.
    
    Args:
        epc: EPC tag value
        products: Products catalog dictionary
        
    Returns:
        SKU if found, empty string otherwise
    """
    for sku, product in products.items():
        if is_epc_in_range(epc, product['epc_range']):
            return sku
    return ''


def calculate_expected_inventory(initial_inventory: Dict[str, int],
                                 transactions: List[Dict]) -> Dict[str, int]:
    """
    Calculate expected inventory based on initial stock and transactions.
    
    Args:
        initial_inventory: Initial inventory snapshot {SKU: quantity}
        transactions: List of POS transactions
        
    Returns:
        Expected inventory {SKU: quantity}
    """
    expected = initial_inventory.copy()
    
    for transaction in transactions:
        sku = transaction.get('sku')
        if sku in expected:
            expected[sku] -= 1  # Each transaction reduces inventory by 1
            if expected[sku] < 0:
                expected[sku] = 0
    
    return expected


def save_events_to_jsonl(events: List[Any], output_path: str):
    """
    Save detected events to JSONL file.
    
    Args:
        events: List of DetectedEvent objects
        output_path: Output file path
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        for event in events:
            f.write(event.to_json() + '\n')


def group_events_by_station(events: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Group events by station ID.
    
    Args:
        events: List of event dictionaries
        
    Returns:
        Dictionary mapping station_id to list of events
    """
    grouped = {}
    for event in events:
        station_id = event.get('station_id', 'UNKNOWN')
        if station_id not in grouped:
            grouped[station_id] = []
        grouped[station_id].append(event)
    return grouped


def sort_events_by_timestamp(events: List[Dict]) -> List[Dict]:
    """
    Sort events chronologically by timestamp.
    
    Args:
        events: List of event dictionaries
        
    Returns:
        Sorted list of events
    """
    return sorted(events, key=lambda x: x.get('timestamp', ''))


class EventCounter:
    """Helper class to track event IDs and counts"""
    
    def __init__(self):
        self.counts = {}
        self.total = 0
    
    def increment(self, event_type: str):
        """Increment counter for specific event type"""
        if event_type not in self.counts:
            self.counts[event_type] = 0
        self.counts[event_type] += 1
        self.total += 1
    
    def get_count(self, event_type: str) -> int:
        """Get count for specific event type"""
        return self.counts.get(event_type, 0)
    
    def get_summary(self) -> Dict[str, int]:
        """Get summary of all counts"""
        return {
            'total': self.total,
            **self.counts
        }
