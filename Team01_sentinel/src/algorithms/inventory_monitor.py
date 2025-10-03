"""
Inventory Monitoring Algorithms
================================

This module contains algorithms for monitoring inventory levels,
detecting discrepancies, and tracking stock movements.

Author: Team 01
Date: October 2025
"""

from typing import List, Dict, Tuple
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_models import DetectedEvent, InventorySnapshot, POSTransaction


# @algorithm Inventory Reconciliation | Compare expected vs actual inventory levels
def detect_inventory_discrepancies(initial_snapshot: InventorySnapshot,
                                   final_snapshot: InventorySnapshot,
                                   pos_transactions: List[POSTransaction],
                                   tolerance: int = 5) -> List[DetectedEvent]:
    """
    Detect inventory discrepancies by reconciling expected vs actual stock.
    
    Algorithm:
    1. Calculate expected inventory: initial - sold items
    2. Compare expected with actual final inventory
    3. If difference exceeds tolerance, flag as discrepancy
    4. Consider shrinkage, theft, or system errors
    
    Args:
        initial_snapshot: Starting inventory snapshot
        final_snapshot: Ending inventory snapshot
        pos_transactions: List of sales transactions
        tolerance: Acceptable variance in inventory count
        
    Returns:
        List of inventory discrepancy events
    """
    events = []
    
    # Calculate expected inventory based on transactions
    expected_inventory = initial_snapshot.inventory.copy()
    
    # Deduct sold items
    for transaction in pos_transactions:
        sku = transaction.sku
        if sku in expected_inventory:
            expected_inventory[sku] -= 1
            if expected_inventory[sku] < 0:
                expected_inventory[sku] = 0
    
    # Compare with actual final inventory
    for sku in expected_inventory:
        expected_qty = expected_inventory[sku]
        actual_qty = final_snapshot.inventory.get(sku, 0)
        
        # Check if discrepancy exceeds tolerance
        if abs(expected_qty - actual_qty) > tolerance:
            event = DetectedEvent.create_inventory_discrepancy(
                timestamp=final_snapshot.timestamp,
                sku=sku,
                expected_inventory=expected_qty,
                actual_inventory=actual_qty
            )
            events.append(event)
    
    return events


# @algorithm Stock Level Monitoring | Monitor inventory levels for low stock alerts
def monitor_stock_levels(inventory: InventorySnapshot,
                        products_catalog: Dict[str, Dict],
                        low_stock_threshold: float = 0.2) -> List[Dict]:
    """
    Monitor inventory levels and identify low stock situations.
    
    Algorithm:
    1. For each product, compare current stock with catalog quantity
    2. Calculate stock level percentage
    3. If below threshold, flag as low stock
    4. Prioritize high-value or high-demand items
    
    Args:
        inventory: Current inventory snapshot
        products_catalog: Product catalog with expected quantities
        low_stock_threshold: Percentage threshold for low stock (0-1)
        
    Returns:
        List of low stock alerts
    """
    low_stock_items = []
    
    for sku, current_qty in inventory.inventory.items():
        if sku not in products_catalog:
            continue
        
        expected_qty = products_catalog[sku]['quantity']
        
        if expected_qty > 0:
            stock_percentage = current_qty / expected_qty
            
            if stock_percentage <= low_stock_threshold:
                low_stock_items.append({
                    'sku': sku,
                    'product_name': products_catalog[sku]['product_name'],
                    'current_quantity': current_qty,
                    'expected_quantity': expected_qty,
                    'stock_percentage': stock_percentage * 100,
                    'timestamp': inventory.timestamp
                })
    
    return low_stock_items


# @algorithm Inventory Velocity Analysis | Calculate inventory turnover rates
def analyze_inventory_velocity(inventory_snapshots: List[InventorySnapshot],
                               pos_transactions: List[POSTransaction]) -> Dict[str, Dict]:
    """
    Analyze inventory velocity and turnover rates.
    
    Algorithm:
    1. Track inventory changes over time
    2. Calculate sales velocity for each SKU
    3. Identify fast-moving and slow-moving items
    4. Estimate days until stockout
    
    Args:
        inventory_snapshots: List of inventory snapshots over time
        pos_transactions: List of sales transactions
        
    Returns:
        Dictionary of velocity metrics by SKU
    """
    if not inventory_snapshots or not pos_transactions:
        return {}
    
    # Count sales per SKU
    sales_count = {}
    for transaction in pos_transactions:
        sku = transaction.sku
        sales_count[sku] = sales_count.get(sku, 0) + 1
    
    # Get initial and final inventory
    initial = inventory_snapshots[0]
    final = inventory_snapshots[-1]
    
    # Calculate velocity metrics
    velocity = {}
    for sku in initial.inventory:
        initial_qty = initial.inventory[sku]
        final_qty = final.inventory.get(sku, 0)
        sold = sales_count.get(sku, 0)
        
        velocity[sku] = {
            'initial_quantity': initial_qty,
            'final_quantity': final_qty,
            'sold_units': sold,
            'turnover_rate': (sold / initial_qty * 100) if initial_qty > 0 else 0,
            'remaining_days': (final_qty / (sold / len(inventory_snapshots))) if sold > 0 else 999
        }
    
    return velocity


# @algorithm Shrinkage Detection | Detect unexplained inventory losses
def detect_shrinkage(inventory_changes: Dict[str, int],
                    expected_changes: Dict[str, int],
                    shrinkage_threshold: int = 3) -> List[Dict]:
    """
    Detect inventory shrinkage (theft, damage, error).
    
    Algorithm:
    1. Compare actual inventory changes with expected changes
    2. Calculate unexplained losses
    3. If losses exceed threshold, flag as potential shrinkage
    4. Identify patterns and high-risk items
    
    Args:
        inventory_changes: Actual inventory changes {SKU: change}
        expected_changes: Expected inventory changes {SKU: change}
        shrinkage_threshold: Acceptable unexplained loss count
        
    Returns:
        List of shrinkage alerts
    """
    shrinkage_alerts = []
    
    for sku in expected_changes:
        expected = expected_changes[sku]
        actual = inventory_changes.get(sku, 0)
        
        # Calculate unexplained loss (negative difference)
        unexplained_loss = expected - actual
        
        if unexplained_loss > shrinkage_threshold:
            shrinkage_alerts.append({
                'sku': sku,
                'expected_change': expected,
                'actual_change': actual,
                'unexplained_loss': unexplained_loss,
                'severity': 'high' if unexplained_loss > shrinkage_threshold * 2 else 'medium'
            })
    
    return shrinkage_alerts


# @algorithm Reorder Point Calculation | Calculate optimal reorder points for inventory
def calculate_reorder_points(inventory: InventorySnapshot,
                            velocity: Dict[str, Dict],
                            lead_time_days: int = 3,
                            safety_stock_days: int = 2) -> Dict[str, int]:
    """
    Calculate reorder points for inventory items.
    
    Algorithm:
    1. Estimate daily sales rate from velocity data
    2. Calculate lead time demand
    3. Add safety stock buffer
    4. Set reorder point = lead time demand + safety stock
    
    Args:
        inventory: Current inventory snapshot
        velocity: Velocity metrics by SKU
        lead_time_days: Days required to restock
        safety_stock_days: Additional buffer days
        
    Returns:
        Dictionary of reorder points {SKU: reorder_point}
    """
    reorder_points = {}
    
    for sku, metrics in velocity.items():
        if metrics['sold_units'] > 0:
            # Estimate daily sales rate
            daily_rate = metrics['sold_units'] / max(1, metrics.get('days', 1))
            
            # Calculate reorder point
            lead_time_demand = daily_rate * lead_time_days
            safety_stock = daily_rate * safety_stock_days
            reorder_point = int(lead_time_demand + safety_stock)
            
            reorder_points[sku] = reorder_point
    
    return reorder_points
