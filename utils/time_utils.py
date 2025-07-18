from datetime import time

def get_time_from_inputs(container, label, default_hour, time_format, key_prefix):
    if time_format == "12-hour":
        # Convert 24h to 12h + meridiem
        if default_hour == 0:
            default_12 = 12
            default_meridiem = "AM"
        elif 1 <= default_hour <= 11:
            default_12 = default_hour
            default_meridiem = "AM"
        elif default_hour == 12:
            default_12 = 12
            default_meridiem = "PM"
        else:
            default_12 = default_hour - 12
            default_meridiem = "PM"

        hour = container.number_input(
            f"{label} Hour (1-12)", min_value = 1, max_value = 12, value = default_12, key = f"{key_prefix}_hour"
        )
        meridiem = container.radio(
            f"{label} AM/PM", options = ["AM", "PM"], index = 0 if default_meridiem == "AM" else 1, key = f"{key_prefix}_ampm"
            )

        if meridiem == "AM" and hour == 12:
            conv_hour = 0
        elif meridiem == "PM" and hour != 12:
            conv_hour = hour + 12
        else:
            conv_hour = hour
    else:
        conv_hour = container.number_input(
            f"{label} Hour (0-23)", min_value = 0, max_value = 23, value = default_hour, key = f"{key_prefix}_hour"
        )
    return time(conv_hour, 0)