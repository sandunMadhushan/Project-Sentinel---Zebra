"""
Data Models for Project Sentinel
==================================

This module defines the data structures used throughout the Project Sentinel system.
It includes models for events, transactions, RFID readings, queue monitoring, and more.

Author: Team 01
Date: October 2025
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
import json


@dataclass
class Product:
    """Product catalog entry with all attributes"""
    sku: str
    product_name: str
    quantity: int
    epc_range: str
    barcode: str
    weight: float  # in grams
    price: float
    
    def is_epc_in_range(self, epc: str) -> bool:
        """Check if an EPC is within this product's range"""
        if '-' not in self.epc_range:
            return False
        start, end = self.epc_range.split('-')
        return start <= epc <= end


@dataclass
class Customer:
    """Customer information"""
    customer_id: str
    name: str
    email: str
    phone: str


@dataclass
class POSTransaction:
    """Point of Sale transaction record"""
    timestamp: str
    station_id: str
    status: str
    customer_id: str
    sku: str
    product_name: str
    barcode: str
    price: float
    weight_g: float
    
    @classmethod
    def from_stream(cls, stream_data: Dict) -> 'POSTransaction':
        """Create POSTransaction from streaming data"""
        data = stream_data['data']
        return cls(
            timestamp=stream_data['timestamp'],
            station_id=stream_data['station_id'],
            status=stream_data['status'],
            customer_id=data['customer_id'],
            sku=data['sku'],
            product_name=data['product_name'],
            barcode=data['barcode'],
            price=data['price'],
            weight_g=data['weight_g']
        )


@dataclass
class RFIDReading:
    """RFID tag reading event"""
    timestamp: str
    station_id: str
    status: str
    epc: str
    location: str
    sku: str
    
    @classmethod
    def from_stream(cls, stream_data: Dict) -> 'RFIDReading':
        """Create RFIDReading from streaming data"""
        data = stream_data['data']
        return cls(
            timestamp=stream_data['timestamp'],
            station_id=stream_data['station_id'],
            status=stream_data['status'],
            epc=data['epc'],
            location=data['location'],
            sku=data['sku']
        )


@dataclass
class ProductRecognition:
    """Vision system product recognition event"""
    timestamp: str
    station_id: str
    status: str
    predicted_product: str
    accuracy: float
    
    @classmethod
    def from_stream(cls, stream_data: Dict) -> 'ProductRecognition':
        """Create ProductRecognition from streaming data"""
        data = stream_data['data']
        return cls(
            timestamp=stream_data['timestamp'],
            station_id=stream_data['station_id'],
            status=stream_data['status'],
            predicted_product=data['predicted_product'],
            accuracy=data['accuracy']
        )


@dataclass
class QueueMonitoring:
    """Queue monitoring metrics"""
    timestamp: str
    station_id: str
    status: str
    customer_count: int
    average_dwell_time: float
    
    @classmethod
    def from_stream(cls, stream_data: Dict) -> 'QueueMonitoring':
        """Create QueueMonitoring from streaming data"""
        data = stream_data['data']
        return cls(
            timestamp=stream_data['timestamp'],
            station_id=stream_data['station_id'],
            status=stream_data['status'],
            customer_count=data['customer_count'],
            average_dwell_time=data['average_dwell_time']
        )


@dataclass
class InventorySnapshot:
    """Inventory snapshot for all products"""
    timestamp: str
    inventory: Dict[str, int]  # SKU -> quantity
    
    @classmethod
    def from_stream(cls, stream_data: Dict) -> 'InventorySnapshot':
        """Create InventorySnapshot from streaming data"""
        return cls(
            timestamp=stream_data['timestamp'],
            inventory=stream_data['data']
        )


@dataclass
class DetectedEvent:
    """Detected event to be output"""
    timestamp: str
    event_id: str
    event_data: Dict[str, Any]
    
    def to_json(self) -> str:
        """Convert to JSON string for output"""
        return json.dumps({
            'timestamp': self.timestamp,
            'event_id': self.event_id,
            'event_data': self.event_data
        })
    
    @staticmethod
    def create_success_operation(timestamp: str, station_id: str, 
                                 customer_id: str, product_sku: str) -> 'DetectedEvent':
        """Create E000: Success Operation event"""
        return DetectedEvent(
            timestamp=timestamp,
            event_id='E000',
            event_data={
                'event_name': 'Success Operation',
                'station_id': station_id,
                'customer_id': customer_id,
                'product_sku': product_sku
            }
        )
    
    @staticmethod
    def create_scanner_avoidance(timestamp: str, station_id: str,
                                 customer_id: str, product_sku: str) -> 'DetectedEvent':
        """Create E001: Scanner Avoidance event"""
        return DetectedEvent(
            timestamp=timestamp,
            event_id='E001',
            event_data={
                'event_name': 'Scanner Avoidance',
                'station_id': station_id,
                'customer_id': customer_id,
                'product_sku': product_sku
            }
        )
    
    @staticmethod
    def create_barcode_switching(timestamp: str, station_id: str,
                                 customer_id: str, actual_sku: str, 
                                 scanned_sku: str) -> 'DetectedEvent':
        """Create E002: Barcode Switching event"""
        return DetectedEvent(
            timestamp=timestamp,
            event_id='E002',
            event_data={
                'event_name': 'Barcode Switching',
                'station_id': station_id,
                'customer_id': customer_id,
                'actual_sku': actual_sku,
                'scanned_sku': scanned_sku
            }
        )
    
    @staticmethod
    def create_weight_discrepancy(timestamp: str, station_id: str,
                                  customer_id: str, product_sku: str,
                                  expected_weight: float, actual_weight: float) -> 'DetectedEvent':
        """Create E003: Weight Discrepancies event"""
        return DetectedEvent(
            timestamp=timestamp,
            event_id='E003',
            event_data={
                'event_name': 'Weight Discrepancies',
                'station_id': station_id,
                'customer_id': customer_id,
                'product_sku': product_sku,
                'expected_weight': int(expected_weight),
                'actual_weight': int(actual_weight)
            }
        )
    
    @staticmethod
    def create_system_crash(timestamp: str, station_id: str, 
                           duration_seconds: int) -> 'DetectedEvent':
        """Create E004: Unexpected Systems Crash event"""
        return DetectedEvent(
            timestamp=timestamp,
            event_id='E004',
            event_data={
                'event_name': 'Unexpected Systems Crash',
                'station_id': station_id,
                'duration_seconds': duration_seconds
            }
        )
    
    @staticmethod
    def create_long_queue(timestamp: str, station_id: str, 
                         num_of_customers: int) -> 'DetectedEvent':
        """Create E005: Long Queue Length event"""
        return DetectedEvent(
            timestamp=timestamp,
            event_id='E005',
            event_data={
                'event_name': 'Long Queue Length',
                'station_id': station_id,
                'num_of_customers': num_of_customers
            }
        )
    
    @staticmethod
    def create_long_wait_time(timestamp: str, station_id: str,
                             wait_time_seconds: float) -> 'DetectedEvent':
        """Create E006: Long Wait Time event"""
        return DetectedEvent(
            timestamp=timestamp,
            event_id='E006',
            event_data={
                'event_name': 'Long Wait Time',
                'station_id': station_id,
                'wait_time_seconds': int(wait_time_seconds)
            }
        )
    
    @staticmethod
    def create_inventory_discrepancy(timestamp: str, sku: str,
                                     expected_inventory: int, 
                                     actual_inventory: int) -> 'DetectedEvent':
        """Create E007: Inventory Discrepancy event"""
        return DetectedEvent(
            timestamp=timestamp,
            event_id='E007',
            event_data={
                'event_name': 'Inventory Discrepancy',
                'SKU': sku,
                'Expected_Inventory': expected_inventory,
                'Actual_Inventory': actual_inventory
            }
        )
    
    @staticmethod
    def create_staffing_needs(timestamp: str, station_id: str,
                             staff_type: str) -> 'DetectedEvent':
        """Create E008: Staffing Needs event"""
        return DetectedEvent(
            timestamp=timestamp,
            event_id='E008',
            event_data={
                'event_name': 'Staffing Needs',
                'station_id': station_id,
                'Staff_type': staff_type
            }
        )
    
    @staticmethod
    def create_checkout_action(timestamp: str, station_id: str,
                               action: str) -> 'DetectedEvent':
        """Create E009: Checkout Station Action event"""
        return DetectedEvent(
            timestamp=timestamp,
            event_id='E009',
            event_data={
                'event_name': 'Checkout Station Action',
                'station_id': station_id,
                'Action': action
            }
        )
