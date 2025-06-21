import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import random
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="WinFi Router Dashboard",
    page_icon="📶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for devices
if 'devices' not in st.session_state:
    st.session_state.devices = []

if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()

# GHz options
ghz_bands = [2.4, 5, 6]

# Device structure template
def generate_device(device_id):
    return {
        "id": device_id,
        "name": f"Device-{device_id}",
        "ip": f"192.168.1.{device_id}",
        "mac": f"00:1B:44:11:3A:{device_id:02X}",
        "ghz": random.choice(ghz_bands),
        "priority": random.choice(["High", "Medium", "Low"]),
        "enabled": True,
        "signal": random.randint(50, 100),
        "bandwidth": random.randint(10, 100),
        "connected_time": random.randint(1, 1440)  # minutes
    }

# Simulate real-time updates
def update_device_signals():
    for device in st.session_state.devices:
        # Simulate signal fluctuation
        device["signal"] = max(30, min(100, device["signal"] + random.randint(-5, 5)))
        device["bandwidth"] = max(5, min(100, device["bandwidth"] + random.randint(-10, 10)))

# Main dashboard header
st.title("📶 WinFi v1.0 Router Dashboard")
st.markdown("---")

# Sidebar for controls
with st.sidebar:
    st.header("🛠️ Device Management")
    
    # Add device button
    if st.button("➕ Add New Device", use_container_width=True):
        device_id = len(st.session_state.devices) + 1
        new_device = generate_device(device_id)
        st.session_state.devices.append(new_device)
        st.success(f"Device-{device_id} added successfully!")
        st.rerun()
    
    st.markdown("---")
    
    # GHz band filter
    st.subheader("🌐 Filter by GHz Band")
    selected_ghz = st.selectbox(
        "Select GHz Band:",
        ["All"] + [f"{band} GHz" for band in ghz_bands]
    )
    
    # Priority filter
    st.subheader("⚡ Filter by Priority")
    selected_priority = st.selectbox(
        "Select Priority:",
        ["All", "High", "Medium", "Low"]
    )
    
    # Status filter
    st.subheader("🔌 Filter by Status")
    selected_status = st.selectbox(
        "Select Status:",
        ["All", "Enabled", "Disabled"]
    )
    
    st.markdown("---")
    
    # Auto-refresh toggle
    auto_refresh = st.checkbox("🔄 Auto-refresh (5s)", value=True)
    
    if st.button("🔄 Manual Refresh", use_container_width=True):
        update_device_signals()
        st.session_state.last_update = datetime.now()
        st.rerun()

# Auto-refresh functionality
if auto_refresh:
    current_time = datetime.now()
    if (current_time - st.session_state.last_update).seconds >= 5:
        update_device_signals()
        st.session_state.last_update = current_time
        st.rerun()

# Main dashboard content
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📱 Connected Devices",
        value=len([d for d in st.session_state.devices if d["enabled"]]),
        delta=len(st.session_state.devices) - len([d for d in st.session_state.devices if d["enabled"]])
    )

with col2:
    total_bandwidth = sum([d["bandwidth"] for d in st.session_state.devices if d["enabled"]])
    st.metric(
        label="📊 Total Bandwidth",
        value=f"{total_bandwidth} Mbps",
        delta=f"{random.randint(-5, 15)} Mbps"
    )

with col3:
    avg_signal = sum([d["signal"] for d in st.session_state.devices if d["enabled"]]) / max(1, len([d for d in st.session_state.devices if d["enabled"]]))
    st.metric(
        label="📶 Avg Signal Strength",
        value=f"{avg_signal:.0f}%",
        delta=f"{random.randint(-3, 3)}%"
    )

with col4:
    high_priority_count = len([d for d in st.session_state.devices if d["priority"] == "High" and d["enabled"]])
    st.metric(
        label="🔴 High Priority Devices",
        value=high_priority_count,
        delta=0
    )

st.markdown("---")

# Filter devices based on selections
filtered_devices = st.session_state.devices.copy()

if selected_ghz != "All":
    ghz_value = float(selected_ghz.split()[0])
    filtered_devices = [d for d in filtered_devices if d["ghz"] == ghz_value]

if selected_priority != "All":
    filtered_devices = [d for d in filtered_devices if d["priority"] == selected_priority]

if selected_status != "All":
    status_value = selected_status == "Enabled"
    filtered_devices = [d for d in filtered_devices if d["enabled"] == status_value]

# Device management section
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📋 Device List")
    
    if not filtered_devices:
        st.info("No devices match the current filters.")
    else:
        # Create DataFrame for device display
        device_data = []
        for i, device in enumerate(filtered_devices):
            status_icon = "✅" if device["enabled"] else "❌"
            priority_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
            
            device_data.append({
                "Status": status_icon,
                "Device Name": device["name"],
                "IP Address": device["ip"],
                "MAC Address": device["mac"],
                "GHz Band": f"{device['ghz']} GHz",
                "Signal": f"{device['signal']}%",
                "Priority": f"{priority_color[device['priority']]} {device['priority']}",
                "Bandwidth": f"{device['bandwidth']} Mbps",
                "Connected Time": f"{device['connected_time']} min"
            })
        
        df = pd.DataFrame(device_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

with col_right:
    st.subheader("⚙️ Device Actions")
    
    if st.session_state.devices:
        # Device selection for actions
        device_names = [f"{d['name']} ({d['ip']})" for d in st.session_state.devices]
        selected_device_idx = st.selectbox(
            "Select Device:",
            range(len(device_names)),
            format_func=lambda x: device_names[x]
        )
        
        selected_device = st.session_state.devices[selected_device_idx]
        
        # Device actions
        st.write(f"**Selected:** {selected_device['name']}")
        st.write(f"**Status:** {'Enabled' if selected_device['enabled'] else 'Disabled'}")
        
        # Toggle device status
        if st.button("🔄 Toggle Status", use_container_width=True):
            st.session_state.devices[selected_device_idx]["enabled"] = not selected_device["enabled"]
            st.success(f"Status toggled for {selected_device['name']}")
            st.rerun()
        
        # Change priority
        new_priority = st.selectbox(
            "Change Priority:",
            ["High", "Medium", "Low"],
            index=["High", "Medium", "Low"].index(selected_device["priority"]),
            key="priority_select"
        )
        
        if st.button("✅ Update Priority", use_container_width=True):
            st.session_state.devices[selected_device_idx]["priority"] = new_priority
            st.success(f"Priority updated to {new_priority}")
            st.rerun()
        
        # Remove device
        if st.button("🗑️ Remove Device", use_container_width=True, type="secondary"):
            removed_device = st.session_state.devices.pop(selected_device_idx)
            st.success(f"Removed {removed_device['name']}")
            st.rerun()

st.markdown("---")

# Network visualization section
if st.session_state.devices:
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("📊 Signal Strength Distribution")
        
        # Signal strength chart
        signals = [d["signal"] for d in st.session_state.devices]
        signal_ranges = ["30-50%", "51-70%", "71-85%", "86-100%"]
        signal_counts = [
            len([s for s in signals if 30 <= s <= 50]),
            len([s for s in signals if 51 <= s <= 70]),
            len([s for s in signals if 71 <= s <= 85]),
            len([s for s in signals if 86 <= s <= 100])
        ]
        
        fig_signal = px.bar(
            x=signal_ranges,
            y=signal_counts,
            title="Devices by Signal Strength Range",
            color=signal_counts,
            color_continuous_scale="RdYlGn"
        )
        fig_signal.update_layout(showlegend=False)
        st.plotly_chart(fig_signal, use_container_width=True)
    
    with col_chart2:
        st.subheader("🌐 GHz Band Distribution")
        
        # GHz band pie chart
        ghz_counts = {}
        for device in st.session_state.devices:
            ghz = f"{device['ghz']} GHz"
            ghz_counts[ghz] = ghz_counts.get(ghz, 0) + 1
        
        if ghz_counts:
            fig_ghz = px.pie(
                values=list(ghz_counts.values()),
                names=list(ghz_counts.keys()),
                title="Device Distribution by GHz Band"
            )
            st.plotly_chart(fig_ghz, use_container_width=True)
    
    # Priority distribution chart
    st.subheader("⚡ Priority & Bandwidth Analysis")
    
    col_priority, col_bandwidth = st.columns(2)
    
    with col_priority:
        priority_counts = {"High": 0, "Medium": 0, "Low": 0}
        for device in st.session_state.devices:
            priority_counts[device["priority"]] += 1
        
        fig_priority = px.bar(
            x=list(priority_counts.keys()),
            y=list(priority_counts.values()),
            title="Devices by Priority Level",
            color=list(priority_counts.values()),
            color_discrete_sequence=["#FF6B6B", "#FFE66D", "#4ECDC4"]
        )
        st.plotly_chart(fig_priority, use_container_width=True)
    
    with col_bandwidth:
        # Real-time bandwidth usage chart
        device_names = [d["name"] for d in st.session_state.devices if d["enabled"]]
        bandwidths = [d["bandwidth"] for d in st.session_state.devices if d["enabled"]]
        
        if device_names and bandwidths:
            fig_bandwidth = go.Figure(data=go.Scatter(
                x=device_names,
                y=bandwidths,
                mode='lines+markers',
                name='Bandwidth Usage',
                line=dict(color='#1f77b4', width=2),
                marker=dict(size=8)
            ))
            fig_bandwidth.update_layout(
                title="Real-time Bandwidth Usage",
                xaxis_title="Devices",
                yaxis_title="Bandwidth (Mbps)",
                showlegend=False
            )
            st.plotly_chart(fig_bandwidth, use_container_width=True)

# Footer with last update time
st.markdown("---")
st.caption(f"Last updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}")

# Auto-refresh script
if auto_refresh:
    time.sleep(1)
    st.rerun()
