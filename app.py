import streamlit as st
from datetime import time

# App config
st.set_page_config(page_title = "Weekly Schedule Builder", layout = "wide")
st.title("Weekly Schedule Builder - MVP")

# Initialize session state
if "events" not in st.session_state:
    st.session_state["events"] = []

# Sidebar customization options
st.sidebar.header("Calendar Settings")

# Days of the week
days_options = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
visible_days = st.sidebar.multiselect("Select Days to Show", options = days_options, default = days_options[1:6])

# Time range
start_hour = st.sidebar.slider("Start Hour", 0, 23, 8)
end_hour = st.sidebar.slider("End Hour", 1, 24, 18)

# Time format
time_format = st.sidebar.radio("Time Format", ["12-hour", "24-hour"])

# Main Area: Event Input

# Display saved events