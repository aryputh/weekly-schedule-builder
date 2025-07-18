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
st.subheader("+ Add New Event")

with st.form("event_form", clear_on_submit = True):
    col1, col2 = st.columns(2)

    with col1:
        title = st.text_input("Event Title")
        description = st.text_input("Description", height = 100)
        day = st.selectbox("Day", options = visible_days)

    with col2:
        start_time = st.time_input("Start Time", value = time(9, 0))
        end_time = st.time_input("End Time", value = time(10, 0))
        color = st.color_picker("Color", "#FF5733")

    submitted = st.form_submit_button("Add Event")

    if submitted:
        if start_time >= end_time:
            st.warning("End time must be after start time.")
        else:
            event = {
                "title" : title,
                "description" : description,
                "start_time" : str(start_time),
                "end_time" : str(end_time),
                "color" : color
            }

            st.session_state["events"].append(event)
            st.success(f"Event '{title}' added to {day}.")

# Display saved events (for now)
st.subheader("Current Events")

if not st.session_state["events"]:
    st.info("No events added yet.")
else:
    for event in st.session_state["events"]:
        with st.expander(f"{event['title']} ({event['day']})"):
            st.markdown(f"- **Time**: {event['start_time']} to {event['end_time']}")
            st.markdown(f"- **Description**: {event['description']}")
            st.markdown(f"- **Color**: '{event['color']}")