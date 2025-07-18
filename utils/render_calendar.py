from datetime import datetime

def render_calendar(events, visible_days, start_hour, end_hour, time_format):
    # Vertical spacing for events
    vertical_event_padding_px = 4
    horizontal_event_padding_px = 2

    # Height of hour rows
    vertical_hour_height_px = 60
    vertical_day_height_px = vertical_hour_height_px * (end_hour.hour - start_hour.hour)
    column_width = f"{100 / len(visible_days)}%"

    # Generate time labels (left sidebar)
    time_labels_html = ""
    for h in range(start_hour.hour, end_hour.hour + 1):
        raw_label = datetime.strptime(str(h), "%H")

        if time_format == "12-hour":
            label = raw_label.strftime("%I %p").lstrip("0")
        else:
            label = raw_label.strftime("%H:00")

        time_labels_html += f'<div class = "time-label" style = "height: {vertical_hour_height_px}px">{label}</div>'
    
    # Generate grid columns for days
    day_columns_html = ""
    for day in visible_days:
        day_events = [e for e in events if e["day"] == day]
        events_html = ""

        # Place each event in absolutely positioned block
        for event in day_events:
            start_time = datetime.strptime(event["start_time"], "%H:%M")
            end_time = datetime.strptime(event["end_time"], "%H:%M")
            start_offset = (start_time.hour + start_time.minute / 60) - start_hour.hour
            duration = (end_time - start_time).seconds / 3600

            height_px = duration * vertical_hour_height_px - (vertical_event_padding_px * 2)

            events_html += (
                '<div class = "event" style = "'
                f'top: {horizontal_event_padding_px}px;'
                f'height: {height_px}px;'
                f'background-color: {event["color"]};">'
                f'<div class = "event-title">{event["title"]}</div>'
                '</div>'
            )

        day_columns_html += (
            f'<div class = "day-column" style = "width" {column_width};">'
            f'<div class = "day-header">{day}</div>'
            f'<div class = "day-body" style = "height: {vertical_day_height_px}px;">{events_html}</div>'
            '</div>'
        )

    # Combine everything into one grid
    calendar_html = (
        '<div class = "calendar-container">'
        f'<div class = "time-column">{time_labels_html}</div>'
        f'<div class = "days-container">{day_columns_html}</div>'
        '</div>'
    )

    return calendar_html