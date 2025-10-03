"""
Anomaly Detection Algorithms
=============================

This module contains algorithms for detecting system anomalies,
crashes, unusual patterns, and operational issues.

Author: Team 01
Date: October 2025
"""

from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_models import DetectedEvent


# @algorithm System Downtime Detection | Detect system crashes and downtime periods
def detect_system_crashes(all_events: List[Dict],
                         min_gap_seconds: int = 120,
                         min_crash_duration: int = 60) -> List[DetectedEvent]:
    """
    Detect system crashes by identifying gaps in event streams.
    
    Algorithm:
    1. Sort all events by timestamp
    2. Calculate time gaps between consecutive events
    3. If gap exceeds threshold, classify as potential crash
    4. Estimate crash duration and severity
    
    Args:
        all_events: List of all system events
        min_gap_seconds: Minimum gap to consider as crash
        min_crash_duration: Minimum duration to flag as crash
        
    Returns:
        List of system crash events
    """
    events = []
    
    if not all_events:
        return events
    
    # Sort events by timestamp
    sorted_events = sorted(all_events, key=lambda x: x.get('timestamp', ''))
    
    # Group by station
    events_by_station = defaultdict(list)
    for event in sorted_events:
        station_id = event.get('station_id', 'UNKNOWN')
        if station_id != 'UNKNOWN':
            events_by_station[station_id].append(event)
    
    # Check for gaps in each station's event stream
    for station_id, station_events in events_by_station.items():
        for i in range(len(station_events) - 1):
            current = station_events[i]
            next_event = station_events[i + 1]
            
            # Parse timestamps
            try:
                current_time = datetime.fromisoformat(current['timestamp'])
                next_time = datetime.fromisoformat(next_event['timestamp'])
                gap_seconds = (next_time - current_time).total_seconds()
                
                # Check if gap indicates crash
                if gap_seconds >= min_gap_seconds:
                    duration = int(gap_seconds)
                    
                    if duration >= min_crash_duration:
                        event = DetectedEvent.create_system_crash(
                            timestamp=current['timestamp'],
                            station_id=station_id,
                            duration_seconds=duration
                        )
                        events.append(event)
            except (ValueError, KeyError):
                continue
    
    return events


# @algorithm Statistical Anomaly Detection | Detect statistical outliers in metrics
def detect_statistical_anomalies(metrics: List[float],
                                 threshold_std: float = 2.0) -> List[int]:
    """
    Detect statistical anomalies using standard deviation method.
    
    Algorithm:
    1. Calculate mean and standard deviation of metrics
    2. Identify values beyond threshold * std deviation
    3. Flag as anomalies
    4. Use Z-score for normalization
    
    Args:
        metrics: List of metric values
        threshold_std: Number of standard deviations for anomaly threshold
        
    Returns:
        List of indices of anomalous values
    """
    if not metrics or len(metrics) < 3:
        return []
    
    # Calculate mean
    mean = sum(metrics) / len(metrics)
    
    # Calculate standard deviation
    variance = sum((x - mean) ** 2 for x in metrics) / len(metrics)
    std_dev = variance ** 0.5
    
    if std_dev == 0:
        return []
    
    # Find anomalies
    anomalies = []
    for i, value in enumerate(metrics):
        z_score = abs((value - mean) / std_dev)
        if z_score > threshold_std:
            anomalies.append(i)
    
    return anomalies


# @algorithm Pattern-based Anomaly Detection | Detect anomalies based on expected patterns
def detect_pattern_anomalies(time_series: List[Tuple[str, float]],
                            expected_pattern: str = 'stable') -> List[Dict]:
    """
    Detect anomalies by comparing against expected patterns.
    
    Algorithm:
    1. Define expected patterns (stable, increasing, decreasing, periodic)
    2. Compare actual data against expected pattern
    3. Calculate deviation score
    4. Flag significant deviations as anomalies
    
    Args:
        time_series: List of (timestamp, value) tuples
        expected_pattern: Expected pattern type
        
    Returns:
        List of anomaly details
    """
    anomalies = []
    
    if len(time_series) < 3:
        return anomalies
    
    values = [v for _, v in time_series]
    
    # Calculate moving average
    window_size = min(3, len(values))
    for i in range(window_size, len(values)):
        window = values[i-window_size:i]
        moving_avg = sum(window) / window_size
        current_value = values[i]
        
        # Check deviation
        if moving_avg > 0:
            deviation = abs(current_value - moving_avg) / moving_avg
            
            if deviation > 0.5:  # 50% deviation
                anomalies.append({
                    'timestamp': time_series[i][0],
                    'value': current_value,
                    'expected': moving_avg,
                    'deviation': deviation * 100
                })
    
    return anomalies


# @algorithm Behavioral Anomaly Detection | Detect unusual customer behavior patterns
def detect_behavioral_anomalies(transactions: List[Dict],
                               baseline_metrics: Dict[str, float]) -> List[Dict]:
    """
    Detect unusual customer behavior based on transaction patterns.
    
    Algorithm:
    1. Establish baseline metrics (avg transaction value, time, items)
    2. Compare individual transactions against baseline
    3. Score transactions on multiple dimensions
    4. Flag high-score transactions as anomalous
    
    Args:
        transactions: List of transaction records
        baseline_metrics: Baseline metrics for comparison
        
    Returns:
        List of behavioral anomaly alerts
    """
    anomalies = []
    
    for transaction in transactions:
        anomaly_score = 0
        anomaly_factors = []
        
        # Check transaction value
        if 'price' in transaction:
            price = transaction['price']
            if price < baseline_metrics.get('min_price', 0):
                anomaly_score += 1
                anomaly_factors.append('unusually_low_price')
            elif price > baseline_metrics.get('max_price', 999999):
                anomaly_score += 1
                anomaly_factors.append('unusually_high_price')
        
        # Check weight
        if 'weight_g' in transaction:
            weight = transaction['weight_g']
            if weight == 0:
                anomaly_score += 2
                anomaly_factors.append('zero_weight')
        
        # Check time patterns
        if 'timestamp' in transaction:
            try:
                ts = datetime.fromisoformat(transaction['timestamp'])
                hour = ts.hour
                # Unusual hours (very early morning)
                if hour < 6 or hour > 23:
                    anomaly_score += 1
                    anomaly_factors.append('unusual_hour')
            except ValueError:
                pass
        
        # If anomaly score is high, flag it
        if anomaly_score >= 2:
            anomalies.append({
                'transaction': transaction,
                'anomaly_score': anomaly_score,
                'factors': anomaly_factors
            })
    
    return anomalies


# @algorithm Correlation Analysis | Detect anomalies through correlation between metrics
def detect_correlation_anomalies(metric1: List[float],
                                metric2: List[float],
                                expected_correlation: str = 'positive') -> List[int]:
    """
    Detect anomalies by analyzing correlation between two metrics.
    
    Algorithm:
    1. Calculate correlation coefficient between metrics
    2. Identify points where correlation breaks down
    3. Flag unexpected correlations or anti-correlations
    
    Args:
        metric1: First metric series
        metric2: Second metric series
        expected_correlation: Expected correlation ('positive', 'negative', 'none')
        
    Returns:
        List of indices where correlation anomalies occur
    """
    anomalies = []
    
    if len(metric1) != len(metric2) or len(metric1) < 3:
        return anomalies
    
    # Simple correlation check: compare direction of change
    for i in range(1, len(metric1)):
        change1 = metric1[i] - metric1[i-1]
        change2 = metric2[i] - metric2[i-1]
        
        if expected_correlation == 'positive':
            # Both should change in same direction
            if (change1 > 0 and change2 < 0) or (change1 < 0 and change2 > 0):
                if abs(change1) > 0.1 * abs(metric1[i-1]) or abs(change2) > 0.1 * abs(metric2[i-1]):
                    anomalies.append(i)
        
        elif expected_correlation == 'negative':
            # Should change in opposite directions
            if (change1 > 0 and change2 > 0) or (change1 < 0 and change2 < 0):
                if abs(change1) > 0.1 * abs(metric1[i-1]) or abs(change2) > 0.1 * abs(metric2[i-1]):
                    anomalies.append(i)
    
    return anomalies
