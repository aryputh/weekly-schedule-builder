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

# Chunk list into N-sized parts
def chunk(lst, n):
    return [lst[i:i + n] for i in range(0, len(lst), n)]

st.sidebar.subheader("Visible Days")
days_per_row = 3
cols = st.sidebar.columns(len(days_options))

day_chunks = chunk(days_options, days_per_row)

for row in day_chunks:
    cols = st.sidebar.columns(len(row))
    for i, day in enumerate(row):
        if cols[i].button(day, use_container_width = True):
            st.session_state.day_toggles[day] = not st.session_state.day_toggles[day]

visible_days = [day for day, selected in st.session_state.day_toggles.items() if selected]

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
        description = st.text_area("Description", height = 100)
        selected_days = st.multiselect("Days", options = visible_days)

    with col2:
        start_time = st.time_input("Start Time", value = time(9, 0))
        end_time = st.time_input("End Time", value = time(10, 0))
        color = st.color_picker("Color", "#FF5733")

    submitted = st.form_submit_button("Add Event")

    if submitted:
        if not selected_days:
            st.warning("Please select at least one day.")
        elif start_time >= end_time:
            st.warning("End time must be after start time.")
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
            st.markdown(f"- **Color**: '{event['color']}'")