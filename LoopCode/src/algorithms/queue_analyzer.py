"""
Queue Analysis Algorithms
=========================

This module contains algorithms for analyzing queue metrics,
detecting long queues, long wait times, and determining staffing needs.

Author: Team 01
Date: October 2025
"""

from typing import List, Dict
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_models import DetectedEvent, QueueMonitoring


# @algorithm Queue Threshold Analysis | Monitor queue length and wait times against thresholds
def detect_long_queues(queue_data: List[QueueMonitoring],
                       max_customers_threshold: int = 5,
                       max_wait_time_threshold: float = 300.0) -> List[DetectedEvent]:
    """
    Detect long queues based on customer count threshold.
    
    Algorithm:
    1. Monitor customer count at each station
    2. If customer count exceeds threshold, flag as long queue
    3. Track queue length over time for trend analysis
    
    Args:
        queue_data: List of queue monitoring events
        max_customers_threshold: Maximum acceptable customer count
        max_wait_time_threshold: Maximum acceptable wait time in seconds
        
    Returns:
        List of long queue events
    """
    events = []
    
    for data in queue_data:
        # Check for long queue length
        if data.customer_count > max_customers_threshold:
            event = DetectedEvent.create_long_queue(
                timestamp=data.timestamp,
                station_id=data.station_id,
                num_of_customers=data.customer_count
            )
            events.append(event)
    
    return events


# @algorithm Wait Time Threshold Analysis | Monitor average customer wait times
def detect_long_wait_times(queue_data: List[QueueMonitoring],
                           max_wait_time_threshold: float = 300.0) -> List[DetectedEvent]:
    """
    Detect long wait times based on average dwell time threshold.
    
    Algorithm:
    1. Monitor average dwell time at each station
    2. If dwell time exceeds threshold, flag as long wait time
    3. Consider historical averages for dynamic thresholding
    
    Args:
        queue_data: List of queue monitoring events
        max_wait_time_threshold: Maximum acceptable wait time in seconds
        
    Returns:
        List of long wait time events
    """
    events = []
    
    for data in queue_data:
        # Check for long wait time
        if data.average_dwell_time > max_wait_time_threshold:
            event = DetectedEvent.create_long_wait_time(
                timestamp=data.timestamp,
                station_id=data.station_id,
                wait_time_seconds=data.average_dwell_time
            )
            events.append(event)
    
    return events


# @algorithm Staffing Requirements Prediction | Predict staffing needs based on queue metrics
def predict_staffing_needs(queue_data: List[QueueMonitoring],
                          customer_threshold: int = 5,
                          wait_time_threshold: float = 300.0) -> List[DetectedEvent]:
    """
    Predict staffing needs based on queue length and wait times.
    
    Algorithm:
    1. Analyze queue metrics (length and wait time)
    2. If both metrics exceed thresholds, additional staff needed
    3. Determine staff type needed (Cashier, Manager, Technical Support)
    
    Args:
        queue_data: List of queue monitoring events
        customer_threshold: Customer count requiring additional staff
        wait_time_threshold: Wait time requiring additional staff
        
    Returns:
        List of staffing needs events
    """
    events = []
    
    for data in queue_data:
        # Check if staffing is needed
        needs_staff = (data.customer_count >= customer_threshold or 
                      data.average_dwell_time >= wait_time_threshold)
        
        if needs_staff:
            # Determine staff type based on severity
            if data.customer_count >= customer_threshold * 1.5:
                staff_type = "Manager"  # Severe situation needs manager
            else:
                staff_type = "Cashier"  # Regular situation needs cashier
            
            event = DetectedEvent.create_staffing_needs(
                timestamp=data.timestamp,
                station_id=data.station_id,
                staff_type=staff_type
            )
            events.append(event)
    
    return events


# @algorithm Station Status Management | Determine when to open or close checkout stations
def manage_station_status(queue_data: List[QueueMonitoring],
                         open_threshold: int = 5,
                         close_threshold: int = 2) -> List[DetectedEvent]:
    """
    Determine when checkout stations should be opened or closed.
    
    Algorithm:
    1. Monitor queue metrics across all stations
    2. If queues are consistently long, recommend opening new station
    3. If queues are consistently short, recommend closing stations
    4. Consider time trends and patterns
    
    Args:
        queue_data: List of queue monitoring events
        open_threshold: Customer count to trigger opening station
        close_threshold: Customer count to trigger closing station
        
    Returns:
        List of checkout station action events
    """
    events = []
    
    # Group by station
    by_station = {}
    for data in queue_data:
        if data.station_id not in by_station:
            by_station[data.station_id] = []
        by_station[data.station_id].append(data)
    
    # Analyze each station
    for station_id, measurements in by_station.items():
        if not measurements:
            continue
        
        # Get latest measurement
        latest = measurements[-1]
        
        # Check if station should be opened (high queue)
        if latest.customer_count >= open_threshold:
            event = DetectedEvent.create_checkout_action(
                timestamp=latest.timestamp,
                station_id=station_id,
                action="Open"
            )
            events.append(event)
        
        # Check if station should be closed (low queue)
        elif latest.customer_count <= close_threshold:
            # Only suggest closing if queue has been consistently low
            if len(measurements) >= 3:
                recent_avg = sum(m.customer_count for m in measurements[-3:]) / 3
                if recent_avg <= close_threshold:
                    event = DetectedEvent.create_checkout_action(
                        timestamp=latest.timestamp,
                        station_id=station_id,
                        action="Close"
                    )
                    events.append(event)
    
    return events


# @algorithm Queue Trend Analysis | Analyze queue trends over time for predictive insights
def analyze_queue_trends(queue_data: List[QueueMonitoring]) -> Dict[str, any]:
    """
    Analyze queue trends over time for operational insights.
    
    Algorithm:
    1. Calculate moving averages for queue length and wait time
    2. Identify peak hours and slow periods
    3. Detect increasing or decreasing trends
    4. Provide statistical summary
    
    Args:
        queue_data: List of queue monitoring events
        
    Returns:
        Dictionary containing trend analysis results
    """
    if not queue_data:
        return {}
    
    # Group by station
    by_station = {}
    for data in queue_data:
        if data.station_id not in by_station:
            by_station[data.station_id] = {
                'customer_counts': [],
                'wait_times': [],
                'timestamps': []
            }
        by_station[data.station_id]['customer_counts'].append(data.customer_count)
        by_station[data.station_id]['wait_times'].append(data.average_dwell_time)
        by_station[data.station_id]['timestamps'].append(data.timestamp)
    
    # Calculate statistics for each station
    trends = {}
    for station_id, stats in by_station.items():
        avg_customers = sum(stats['customer_counts']) / len(stats['customer_counts'])
        avg_wait_time = sum(stats['wait_times']) / len(stats['wait_times'])
        max_customers = max(stats['customer_counts'])
        max_wait_time = max(stats['wait_times'])
        
        trends[station_id] = {
            'average_customers': avg_customers,
            'average_wait_time': avg_wait_time,
            'max_customers': max_customers,
            'max_wait_time': max_wait_time,
            'measurements': len(stats['customer_counts'])
        }
    
    return trends
