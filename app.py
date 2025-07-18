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
days_options = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]

# Initialize day selection toggles
if "day_toggles" not in st.session_state:
    st.session_state.day_toggles = {day: day in ["MON", "TUE", "WED", "THU", "FRI"] for day in days_options}

st.sidebar.subheader("Day Settings")
cols = st.sidebar.columns(2)

for i, day in enumerate(days_options):
    col = cols[i % len(cols)]
    st.session_state.day_toggles[day] = col.checkbox(day, value = st.session_state.day_toggles[day])

visible_days = [day for day, selected in st.session_state.day_toggles.items() if selected]

# Time format selection
st.sidebar.subheader("Time Settings")
time_format = st.sidebar.radio("Time Format", ["12-hour", "24-hour"])

def get_sidebar_time(label, default_hour, key_prefix):
    if time_format == "12-hour":
        hour = st.sidebar.number_input(
            f"{label} Hour (1-12)", min_value = 1, max_value = 12, value = default_hour % 12 or 12, key = f"{key_prefix}_hour"
        )
        meridiem = st.sidebar.radio(f"{label} AM/PM", options = ["AM", "PM"], key = f"{key_prefix}_ampm")

        if meridiem == "AM" and hour == 12:
            conv_hour = 0
        elif meridiem == "PM" and hour != 12:
            conv_hour = hour + 12
        else:
            conv_hour = hour
    else:
        conv_hour = st.sidebar.number_input(
            f"{label} Hour (0-23)", min_value = 0, max_value = 23, value = default_hour, key = f"{key_prefix}_hour"
        )
    return time(conv_hour, 0)

# Let user select times using time input
start_hour = get_sidebar_time("Start", default_hour = 8, key_prefix = "start")
end_hour = get_sidebar_time("End", default_hour = 18, key_prefix = "end")

if start_hour >= end_hour:
    st.sidebar.error("Start time must be before end time.")

# Main Area: Event Input
st.subheader("+ Add New Event")

with st.form("event_form", clear_on_submit = True):
    col1, col2 = st.columns(2)

    with col1:
        title = st.text_input("Event Title")
        description = st.text_area("Description", height = 100)
        selected_days = st.multiselect("Days", options = visible_days)

    with col2:
        start_time = st.time_input("Start Time", value = start_hour)
        end_time = st.time_input("End Time", value = end_hour)
        color = st.color_picker("Color", "#FF5733")

    submitted = st.form_submit_button("Add Event")

    if submitted:
        if not selected_days:
            st.warning("Please select at least one day.")
        elif start_time < start_hour or end_time > end_hour:
            st.warning(f"Times must be between {format_time_label(start_hour)} and {format_time_label(end_hour)}.")
        elif start_time >= end_time:
            st.warning("Start time must be before end time.")
        else:
            for day in selected_days:
                event = {
                    "title" : title,
                    "description" : description,
                    "day" : day,
                    "start_time" : str(start_time),
                    "end_time" : str(end_time),
                    "color" : color
                }

                st.session_state["events"].append(event)
            st.success(f"Event '{title}' added to: {', '.join(selected_days)}")

# Display saved events (for now)
st.subheader("Current Events")

if not st.session_state["events"]:
    st.info("No events added yet.")
else:
    for event in st.session_state["events"]:
        with st.expander(f"{event['title']} ({event['day']})"):
            st.markdown(f"- **Time**: {event['start_time']} to {event['end_time']}")
            st.markdown(f"- **Description**: {event['description']}")
            st.markdown(f"- **Color**: '{event['color']}'")