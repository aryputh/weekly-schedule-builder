import streamlit as st
from utils.time_utils import *

# App config
st.set_page_config(page_title = "Weekly Schedule Builder", layout = "wide")
st.title("Weekly Schedule Builder")

# Set minimum sidebar width
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        min-width: 300px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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
    st.session_state.day_toggles[day] = col.toggle(day, value = st.session_state.day_toggles.get(day, False))

visible_days = [day for day, selected in st.session_state.day_toggles.items() if selected]
st.session_state["event_days"] = visible_days.copy()

# Time format selection
st.sidebar.subheader("Time Settings")
time_format = st.sidebar.radio("Time Format", ["12-hour", "24-hour"])

# Let user select times using time input
start_hour = get_time_from_inputs(st.sidebar, "Start", 8, time_format, "start", False)
end_hour = get_time_from_inputs(st.sidebar, "End", 18, time_format, "end", False)

if start_hour >= end_hour:
    st.sidebar.error("Start time must be before end time.")

# Main Area: Event Input
st.subheader("Add a New Event")

# Initialize form stats
form_keys = ["event_title", "event_description", "event_days"]
for key in form_keys:
    if key not in st.session_state:
        st.session_state[key] = "" if key != "event_days" else []

with st.form("event_form", clear_on_submit = False):
    col1, col2 = st.columns(2)

    with col1:
        title = st.text_input("Event Title *", value = st.session_state["event_title"], key = "event_title")
        description = st.text_area("Description", height = 100, value = st.session_state["event_description"], key = "event_description")
        selected_days = st.multiselect("Days *", options = visible_days, default = st.session_state["event_days"], key = "event_days")

    with col2:
        start_time = get_time_from_inputs(col2, "Start Time", start_hour.hour, time_format, "event_start", True)
        end_time = get_time_from_inputs(col2, "End Time", end_hour.hour, time_format, "event_end", True)
        color = st.color_picker("Color *", "#FF5733")

    submitted = st.form_submit_button("Add Event")

    if submitted:
        if not title:
            st.warning("Please title your event.")
        elif not selected_days:
            st.warning("Please select at least one day.")
        elif start_time < start_hour or end_time > end_hour:
            st.warning(
                f"Times must be between {start_hour.strftime("%I:%M %p" if time_format == "12-hour" else "%H:%M")}\
                      and {end_hour.strftime("%I:%M %p" if time_format == "12-hour" else "%H:%M")}."
                )
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
                    "color" : color,
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