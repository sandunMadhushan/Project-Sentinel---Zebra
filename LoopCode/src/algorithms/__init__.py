"""
Algorithms Package for Project Sentinel
========================================

This package contains all detection algorithms organized by category:
- fraud_detection: Fraud and theft detection algorithms
- queue_analyzer: Queue management and analysis algorithms
- inventory_monitor: Inventory tracking and reconciliation algorithms
- anomaly_detector: System anomaly and pattern detection algorithms

Author: Team 01
Date: October 2025
"""

from . import fraud_detection
from . import queue_analyzer
from . import inventory_monitor
from . import anomaly_detector

__all__ = [
    'fraud_detection',
    'queue_analyzer',
    'inventory_monitor',
    'anomaly_detector'
]
