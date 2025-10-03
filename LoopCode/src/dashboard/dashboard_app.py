"""
Project Sentinel Dashboard
===========================

Interactive dashboard for visualizing detected events and system metrics.
Built with Streamlit for easy deployment and interaction.

Author: Team 01
Date: October 2025

Usage:
    streamlit run dashboard_app.py -- --events-file path/to/events.jsonl
"""

import streamlit as st
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))


def load_events(events_file: str) -> pd.DataFrame:
    """Load events from JSONL file into DataFrame."""
    events = []
    with open(events_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                events.append(json.loads(line))
    
    if not events:
        return pd.DataFrame()
    
    # Flatten event_data into main DataFrame
    df_data = []
    for event in events:
        row = {
            'timestamp': event['timestamp'],
            'event_id': event['event_id'],
            'event_name': event['event_data'].get('event_name', ''),
        }
        # Add all event_data fields
        row.update(event['event_data'])
        df_data.append(row)
    
    df = pd.DataFrame(df_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df


def create_dashboard(events_file: str):
    """Create the main dashboard interface."""
    
    # Page configuration
    st.set_page_config(
        page_title="Project Sentinel Dashboard",
        page_icon="🛡️",
        layout="wide"
    )
    
    # Title and header
    st.title("🛡️ Project Sentinel - Event Monitoring Dashboard")
    st.markdown("Real-time monitoring and analysis of self-checkout events")
    st.divider()
    
    # Load events
    try:
        df = load_events(events_file)
        
        if df.empty:
            st.error("No events found in the file!")
            return
        
        # Sidebar filters
        st.sidebar.header("📊 Filters")
        
        # Event type filter
        event_types = ['All'] + sorted(df['event_id'].unique().tolist())
        selected_event = st.sidebar.selectbox("Event Type", event_types)
        
        # Station filter
        if 'station_id' in df.columns:
            stations = ['All'] + sorted(df['station_id'].dropna().unique().tolist())
            selected_station = st.sidebar.selectbox("Station", stations)
        else:
            selected_station = 'All'
        
        # Apply filters
        filtered_df = df.copy()
        if selected_event != 'All':
            filtered_df = filtered_df[filtered_df['event_id'] == selected_event]
        if selected_station != 'All' and 'station_id' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['station_id'] == selected_station]
        
        # Key Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Events", len(filtered_df))
        
        with col2:
            fraud_events = len(filtered_df[filtered_df['event_id'].isin(['E001', 'E002', 'E003'])])
            st.metric("Fraud Events", fraud_events)
        
        with col3:
            queue_events = len(filtered_df[filtered_df['event_id'].isin(['E005', 'E006'])])
            st.metric("Queue Issues", queue_events)
        
        with col4:
            if 'station_id' in filtered_df.columns:
                stations_count = filtered_df['station_id'].nunique()
                st.metric("Stations Monitored", stations_count)
            else:
                st.metric("System Crashes", len(filtered_df[filtered_df['event_id'] == 'E004']))
        
        st.divider()
        
        # Event Distribution
        st.subheader("📈 Event Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Event type distribution
            event_counts = filtered_df['event_id'].value_counts().reset_index()
            event_counts.columns = ['Event ID', 'Count']
            
            st.bar_chart(event_counts.set_index('Event ID'))
            st.caption("Distribution of events by type")
        
        with col2:
            # Event names
            if 'event_name' in filtered_df.columns:
                event_names = filtered_df['event_name'].value_counts().head(10)
                st.bar_chart(event_names)
                st.caption("Top 10 events by name")
        
        st.divider()
        
        # Timeline Analysis
        st.subheader("⏱️ Timeline Analysis")
        
        # Events over time
        filtered_df['hour'] = filtered_df['timestamp'].dt.hour
        events_by_hour = filtered_df.groupby('hour').size().reset_index(name='count')
        
        st.line_chart(events_by_hour.set_index('hour'))
        st.caption("Events by hour of day")
        
        st.divider()
        
        # Station Analysis
        if 'station_id' in filtered_df.columns:
            st.subheader("🏪 Station Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                station_counts = filtered_df['station_id'].value_counts().head(10)
                st.bar_chart(station_counts)
                st.caption("Events by station")
            
            with col2:
                # Event types by station
                if len(filtered_df) > 0:
                    station_event_matrix = pd.crosstab(
                        filtered_df['station_id'], 
                        filtered_df['event_id']
                    )
                    st.dataframe(station_event_matrix, use_container_width=True)
                    st.caption("Event distribution across stations")
        
        st.divider()
        
        # Fraud Analysis
        st.subheader("🚨 Fraud Analysis")
        
        fraud_df = filtered_df[filtered_df['event_id'].isin(['E001', 'E002', 'E003'])]
        
        if len(fraud_df) > 0:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                scanner_avoidance = len(fraud_df[fraud_df['event_id'] == 'E001'])
                st.metric("Scanner Avoidance", scanner_avoidance)
            
            with col2:
                barcode_switching = len(fraud_df[fraud_df['event_id'] == 'E002'])
                st.metric("Barcode Switching", barcode_switching)
            
            with col3:
                weight_discrepancies = len(fraud_df[fraud_df['event_id'] == 'E003'])
                st.metric("Weight Discrepancies", weight_discrepancies)
            
            # Fraud by customer
            if 'customer_id' in fraud_df.columns:
                st.subheader("Fraud by Customer")
                customer_fraud = fraud_df['customer_id'].value_counts().head(10)
                st.bar_chart(customer_fraud)
                st.caption("Top 10 customers with fraud events")
        else:
            st.info("No fraud events detected in the selected period")
        
        st.divider()
        
        # Recent Events Table
        st.subheader("📋 Recent Events")
        
        # Show recent events
        display_columns = ['timestamp', 'event_id', 'event_name']
        if 'station_id' in filtered_df.columns:
            display_columns.append('station_id')
        if 'customer_id' in filtered_df.columns:
            display_columns.append('customer_id')
        
        recent_events = filtered_df.sort_values('timestamp', ascending=False).head(20)
        st.dataframe(
            recent_events[display_columns],
            use_container_width=True,
            hide_index=True
        )
        
        st.divider()
        
        # Download section
        st.subheader("💾 Export Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # CSV download
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name="sentinel_events.csv",
                mime="text/csv"
            )
        
        with col2:
            # JSON download
            json_str = filtered_df.to_json(orient='records', date_format='iso')
            st.download_button(
                label="📥 Download as JSON",
                data=json_str,
                file_name="sentinel_events.json",
                mime="application/json"
            )
        
        # Footer
        st.divider()
        st.caption("Project Sentinel Dashboard v1.0 | Team 01 | October 2025")
        
    except FileNotFoundError:
        st.error(f"❌ Events file not found: {events_file}")
        st.info("Please run the event detector first to generate events.jsonl")
    except Exception as e:
        st.error(f"❌ Error loading events: {str(e)}")
        st.exception(e)


def main():
    """Main entry point for the dashboard."""
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Project Sentinel Dashboard')
    parser.add_argument('--events-file', required=True, help='Path to events.jsonl file')
    
    args, unknown = parser.parse_known_args()
    
    # Create dashboard
    create_dashboard(args.events_file)


if __name__ == '__main__':
    main()
