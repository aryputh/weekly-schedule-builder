import streamlit as st
import utils.time_utils as tu
import utils.render_calendar as rc
import utils.event_form as ef

# App config
st.set_page_config(
    page_title = "Weekly Schedule Builder",
    page_icon="📅",
    layout = "wide"
    )
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
    st.session_state.day_toggles = {day: True for day in days_options}

st.sidebar.subheader("Day Settings")
cols = st.sidebar.columns(2)

for i, day in enumerate(days_options):
    col = cols[i % len(cols)]
    st.session_state.day_toggles[day] = col.toggle(day, value = st.session_state.day_toggles.get(day, False))

visible_days = [day for day, selected in st.session_state.day_toggles.items() if selected]

# Time format selection
st.sidebar.subheader("Time Settings")
time_format = st.sidebar.radio("Time Format", ["12-hour", "24-hour"], horizontal = True)

# Let user select times using time input
start_hour = tu.get_time_from_inputs(st.sidebar, "Start", 8, time_format, "start", False)
end_hour = tu.get_time_from_inputs(st.sidebar, "End", 18, time_format, "end", False)

if start_hour >= end_hour:
    st.sidebar.error("Start time must be before end time.")

# Render the form
with st.expander("Add New Event", expanded = True):
    ef.render_event_form(
        time_format = time_format,
        start_hour = start_hour,
        end_hour = end_hour,
        days_options = days_options
    )

# Display calendar
filtered_events = [
    e for e in st.session_state["events"] if e["day"] in visible_days
]

calendar_html = rc.render_calendar(
    events = filtered_events,
    visible_days = visible_days,
    start_hour = start_hour,
    end_hour = end_hour,
    time_format = time_format
)

# Inject calendar style and style
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

st.markdown(calendar_html, unsafe_allow_html = True)