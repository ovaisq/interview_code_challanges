#!/usr/bin/env python3

"""Time Zone Converter Application
        This application provides functions to convert times between various time zones:
        - Pacific Standard Time (America/Los_Angeles)
        - Indian Standard Time (Asia/Kolkata)
        - Central Standard Time (US/Central)
        - Eastern Standard Time (America/New_York)
        Users can input a time in any of these formats, and the system will calculate
        the equivalent times for the other three time zones.
"""
import gradio as gr
from datetime import datetime
import pytz

# Time zone constants for reuse
TIMEZONES = {
    'pst': pytz.timezone('America/Los_Angeles'),
    'ist': pytz.timezone('Asia/Kolkata'),
    'cst': pytz.timezone('US/Central'),
    'est': pytz.timezone('America/New_York')
}

def _convert_time(time_str, from_tz_key, to_tz_keys):
    """Converts a given time string from one timezone to multiple target timezones.
    
    Args:
        time_str (str): Time string in "HH:MM" format
        from_tz_key (str): Key for source timezone ('pst', 'ist', 'cst', 'est')
        to_tz_keys (list): List of keys for target timezones
        
    Returns:
        list: List of time strings in target timezones or ["Invalid", ...] on error
    """
    try:
        from_tz = TIMEZONES[from_tz_key]
        parsed_time = datetime.strptime(time_str.strip(), "%H:%M")
        naive_dt = datetime.combine(datetime.today(), parsed_time.time())
        local_dt = from_tz.localize(naive_dt)
        utc_dt = local_dt.astimezone(pytz.utc)
        
        result = []
        for tz_key in to_tz_keys:
            tz = TIMEZONES[tz_key]
            result.append(utc_dt.astimezone(tz).strftime("%H:%M"))
        
        # Add the original time in its timezone
        result.insert(0, from_tz.normalize(local_dt).strftime("%H:%M"))
        return result
    except (ValueError, pytz.exceptions.AmbiguousTimeError, 
            pytz.exceptions.NonExistentTimeError):
        return ["Invalid"] * (len(to_tz_keys) + 1)

def update_from_pacific(pst_time_str):
    """Converts a given Pacific Standard Time string to Indian Standard Time,
       Central Standard Time, and Eastern Standard Time
    """
    return _convert_time(pst_time_str, 'pst', ['ist', 'cst', 'est'])

def update_from_ist(ist_time_str):
    """Converts a given Indian Standard Time string to Pacific Standard Time,
       Central Standard Time, and Eastern Standard Time.
    """
    return _convert_time(ist_time_str, 'ist', ['pst', 'cst', 'est'])

def update_from_cst(cst_time_str):
    """Converts a given Central Standard Time string to Pacific Standard Time,
       Indian Standard Time, and Eastern Standard Time.
    """
    return _convert_time(cst_time_str, 'cst', ['pst', 'ist', 'est'])

def update_from_est(est_time_str):
    """Converts a given Eastern Standard Time string to Pacific Standard Time,
       Indian Standard Time, and Central Standard Time.
    """
    return _convert_time(est_time_str, 'est', ['pst', 'ist', 'cst'])

def get_initial_times():
    """Retrieves the current times in all supported time zones."""
    now_utc = datetime.now(pytz.utc)
    return tuple(
        now_utc.astimezone(tz).strftime("%H:%M") 
        for tz in TIMEZONES.values()
    )

def update_all_timezones(time_value):
    """Updates all timezones based on a single slider value.
    
    Args:
        time_value (float): Time value in 24-hour format (0.0 to 24.0)
        
    Returns:
        tuple: Updated times for all timezones
    """
    # Convert slider value to HH:MM format
    hours = int(time_value)
    minutes = int((time_value - hours) * 60)
    time_str = f"{hours:02d}:{minutes:02d}"
    
    # Update all timezones based on Pacific time
    result = update_from_pacific(time_str)
    return result

# Gradio Interface
with gr.Blocks(title="Timezone Converter",
               css='footer {display: none !important;}') as app:
    
    init_pacific, init_ist, init_cst, init_est = get_initial_times()
    
    gr.Markdown("# Time Zone Converter")
    gr.Markdown("### (24hr Clock)")
    gr.Markdown("**Current Time**")
    
    with gr.Row():
        cpacific_input = gr.Textbox(label="Pacific Time (PST/PDT)", value=init_pacific)
        cist_input = gr.Textbox(label="India Time (IST)", value=init_ist)
        ccst_input = gr.Textbox(label="Central Time (CST/CDT)", value=init_cst)
        cest_input = gr.Textbox(label="Eastern Time (EST/EDT)", value=init_est)
    
    with gr.Row():
        refresh_button = gr.Button("Refresh Current Time")
    
    def update_times():
        new_pacific, new_ist, new_cst, new_est = get_initial_times()
        return new_pacific, new_ist, new_cst, new_est
    
    # Linking the button click to trigger update function
    refresh_button.click(fn=update_times, 
                         outputs=[cpacific_input, cist_input, ccst_input, cest_input])
    
    gr.Markdown("**Time conversions**")
    
    # Slider for 24-hour time scale
    time_slider = gr.Slider(
        minimum=0.0,
        maximum=24.0,
        value=0.0,
        step=0.1,
        label="Select Time (24-hour format)",
        interactive=True
    )
    
    # Textboxes for displaying times in each timezone
    with gr.Row():
        pacific_input = gr.Textbox(label="Pacific Time (PST/PDT)", value="00:00")
        ist_input = gr.Textbox(label="India Time (IST)", value="00:00")
        cst_input = gr.Textbox(label="Central Time (CST/CDT)", value="00:00")
        est_input = gr.Textbox(label="Eastern Time (EST/EDT)", value="00:00")
    
    # Update only the bottom row when slider changes (responsive)
    time_slider.input(
        fn=update_all_timezones,
        inputs=time_slider,
        outputs=[pacific_input, ist_input, cst_input, est_input]
    )

# Move launch call to main execution block
if __name__ == "__main__":
    app.launch(theme=gr.themes.Soft(), server_name='0.0.0.0', server_port=7860, pwa=True)
