#!/usr/bin/env python3

import gradio as gr
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

# Configuration: Display Name -> IANA Timezone ID
TIMEZONES = {
    "Pacific": "America/Los_Angeles",
    "India": "Asia/Kolkata",
    "Central": "US/Central",
    "Eastern": "America/New_York"
}

def format_dt(dt: datetime, tz_id: str) -> str:
    """Converts a datetime to target timezone and formats as HH:MM."""
    return dt.astimezone(ZoneInfo(tz_id)).strftime("%H:%M")

def get_all_times(base_dt: datetime = None):
    """Returns a list of formatted times for all configured timezones."""
    # Default to current UTC time if no base provided
    dt = base_dt or datetime.now(ZoneInfo("UTC"))
    return [format_dt(dt, tz) for tz in TIMEZONES.values()]

def handle_slider_change(slider_val):
    """Converts slider minutes (0-1439) to formatted times across all zones."""
    hours = int(slider_val // 60)
    minutes = int(slider_val % 60)
    
    # Use Pacific as the anchor for the slider (as per original logic)
    anchor_tz = ZoneInfo(TIMEZONES["Pacific"])
    # Create a localized datetime for today at the slider's time
    naive_dt = datetime.combine(datetime.today(), time(hours, minutes))
    localized_dt = naive_dt.replace(tzinfo=anchor_tz)
    
    return get_all_times(localized_dt)

def get_local_tz_name():
    """Returns the system's local timezone name."""
    return datetime.now().astimezone().tzname()

# Gradio Interface
with gr.Blocks(title="Timezone Converter", css='footer {display: none !important;}') as app:
    gr.Markdown("# Time Zone Converter")
    
    with gr.Group():
        gr.Markdown(f"**Local System Timezone:** `{get_local_tz_name()}`")
        
        with gr.Row():
            # Current Time Row
            curr_inputs = [
                gr.Textbox(label=f"{name} (Current)", value=val) 
                for name, val in zip(TIMEZONES.keys(), get_all_times())
            ]
        
        refresh_btn = gr.Button("Sync to Current Time", variant="secondary")

    gr.Markdown("---")
    gr.Markdown("### Interactive Conversion (24hr)")
    
    # Slider: 0 to 1439 (minutes in a day)
    time_slider = gr.Slider(
        minimum=0, maximum=1439, value=0, step=1,
        label="Slide to adjust time (Anchor: Pacific Time)"
    )
    
    with gr.Row():
        conv_inputs = [gr.Textbox(label=name, value="00:00") for name in TIMEZONES.keys()]

    # Event Handlers
    refresh_btn.click(fn=lambda: get_all_times(), outputs=curr_inputs)
    
    time_slider.input(
        fn=handle_slider_change,
        inputs=time_slider,
        outputs=conv_inputs
    )

if __name__ == "__main__":
    app.launch(theme=gr.themes.Soft(),server_name='0.0.0.0', server_port=7860)
