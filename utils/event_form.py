import streamlit as st
import utils.time_utils as tu
import utils.render_calendar as rc
import random

COLOR_PALETTE = [
    "#FF5733", "#8EA604", "#F5BB00", "#2B4162"
]

def render_event_form(time_format, start_hour, end_hour, days_options):
    # Initialize form stats
    if "event_title" not in st.session_state:
        st.session_state["event_title"] = ""
    if "event_description" not in st.session_state:
        st.session_state["event_description"] = ""
    if "event_days" not in st.session_state:
        st.session_state["event_days"] = []
    if "event_color" not in st.session_state:
        st.session_state["event_color"] = random.choice(COLOR_PALETTE)

    with st.form("event_form", clear_on_submit = False):
        col1, col2 = st.columns(2)

        with col1:
            title = st.text_input("Event Title *", value = st.session_state["event_title"], key = "event_title")
            description = st.text_area("Description", height = 100, value = st.session_state["event_description"], key = "event_description")
            selected_days = st.multiselect("Days *", options = days_options, key = "event_days")

        with col2:
            start_time = tu.get_time_from_inputs(col2, "Start Time", start_hour.hour, time_format, "event_start", True)
            end_time = tu.get_time_from_inputs(col2, "End Time", end_hour.hour, time_format, "event_end", True)
            color = st.color_picker("Color *", value = st.session_state["event_color"], key = "event_color")

        submitted = st.form_submit_button("Add Event")

        if submitted:
            if not title or title.isspace():
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
                        "start_time" : start_time.strftime("%H:%M"),
                        "end_time" : end_time.strftime("%H:%M"),
                        "color" : color,
                    }
                    st.session_state["events"].append(event)

                st.success(f"Event '{title}' added to: {', '.join(selected_days)}")