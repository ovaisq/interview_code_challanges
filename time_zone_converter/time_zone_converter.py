#!/usr/bin/env python3
"""Time Zone Converter Application

	This application provides functions to convert times between various time zones:
	- Pacific Standard Time (America/Los_Angeles)
	- Indian Standard Time (Asia/Kolkata)
	- Central Standard Time (US/Central)

	Functions in this module include methods for getting current initial times,
	updating times based on input, and handling potential errors related to time conversion.
"""

import gradio as gr
from datetime import datetime
import pytz

def update_from_pacific(pacific_str):
    """Converts a given Pacific Standard Time string to Indian Standard Time and Central Standard Time.

        This function takes a time in PST format ("HH:MM") as input, then converts it to equivalent times in IST 
        (Indian Standard Time) and CST (Central Standard Time). It handles the conversion using UTC as an intermediary
        step for accurate time zone adjustments.
    
        Parameters:
        pacific_str (str): A string representing the time in Pacific Standard Time in "HH:MM" format.

        Returns:
        list: A list containing three strings. The first is the original Pacific Standard Time, 
            the second is the converted Indian Standard Time, and the third is Central Standard Time.
            If conversion fails due to parsing errors or invalid times (e.g., ambiguous time during daylight saving changes),
            returns ["Invalid", "Invalid", "Invalid"].

        Raises:
        ValueError: If `pacific_str` is not in the expected format.
        pytz.exceptions.AmbiguousTimeError: If an ambiguous time error occurs due to daylight saving time transitions.
        pytz.exceptions.NonExistentTimeError: If a non-existent time error occurs during localization, such as when clocks are set forward.

        Examples:
            >>> update_from_pacific("15:30")
            ['15:30', '00:30', '20:30']  # Output times may vary depending on the current date and DST rules

        Notes:
        - The function relies on the `pytz` library for accurate timezone conversions, which considers daylight saving time
            changes automatically.
    """

    try:
        pst = pytz.timezone('America/Los_Angeles')
        ist_tz = pytz.timezone('Asia/Kolkata')
        cst_tz = pytz.timezone('US/Central')

        current_utc = datetime.now(pytz.utc)
        today_pst_date = current_utc.astimezone(pst).date()

        parsed_time = datetime.strptime(pacific_str.strip(), "%H:%M")

        naive_dt = datetime(
            year=today_pst_date.year,
            month=today_pst_date.month,
            day=today_pst_date.day,
            hour=parsed_time.hour,
            minute=parsed_time.minute
        )
        
        new_pacific_dt = pst.localize(naive_dt)
        
        utc_dt = new_pacific_dt.astimezone(pytz.utc)
        
        ist_dt_str = utc_dt.astimezone(ist_tz).strftime("%H:%M")
        cst_dt_str = utc_dt.astimezone(cst_tz).strftime("%H:%M")

        return [
            new_pacific_dt.strftime("%H:%M"),
            ist_dt_str,
            cst_dt_str
        ]
    except (ValueError, pytz.exceptions.AmbiguousTimeError, pytz.exceptions.NonExistentTimeError):
        return ["Invalid", "Invalid", "Invalid"]

def update_from_ist(ist_str):
    """Converts a given Indian Standard Time string to Pacific Standard Time and Central Standard Time.

        This function takes an IST time in "HH:MM" format as input, then converts it to equivalent times in PST 
        and CST.

        Parameters:
        ist_str (str): A string representing the time in Indian Standard Time in "HH:MM" format.

        Returns:
        list: A list containing three strings. The first is Pacific Standard Time, 
              the second is Indian Standard Time as provided or calculated, and the third is Central Standard Time.
            If conversion fails due to parsing errors or invalid times, returns ["Invalid", "Invalid", "Invalid"].

        Raises:
        ValueError: If `ist_str` is not in the expected format.
        pytz.exceptions.AmbiguousTimeError: If an ambiguous time error occurs during localization.
        pytz.exceptions.NonExistentTimeError: If a non-existent time error occurs during localization.
    """

    try:
        ist_tz = pytz.timezone('Asia/Kolkata')
        current_utc = datetime.now(pytz.utc)
        today_ist_date = current_utc.astimezone(ist_tz).date()

        parsed_time = datetime.strptime(ist_str.strip(), "%H:%M")
        
        naive_dt = datetime(
            year=today_ist_date.year,
            month=today_ist_date.month,
            day=today_ist_date.day,
            hour=parsed_time.hour,
            minute=parsed_time.minute
        )
        
        new_ist_dt = ist_tz.localize(naive_dt)
        
        utc_dt = new_ist_dt.astimezone(pytz.utc)
        
        pacific_tz = pytz.timezone('America/Los_Angeles')
        pacific_str = utc_dt.astimezone(pacific_tz).strftime("%H:%M")
        
        cst_tz = pytz.timezone('US/Central')
        cst_str = utc_dt.astimezone(cst_tz).strftime("%H:%M")

        return [pacific_str, new_ist_dt.strftime("%H:%M"), cst_str]
    except (ValueError, pytz.exceptions.AmbiguousTimeError, pytz.exceptions.NonExistentTimeError):
        return ["Invalid", "Invalid", "Invalid"]

def update_from_cst(cst_str):
    """Converts a given Central Standard Time string to Pacific Standard Time and Indian Standard Time.

        This function takes a time in CST format ("HH:MM") as input and calculates its equivalent times in PST and IST.

        Parameters:
        cst_str (str): A string representing the time in Central Standard Time in "HH:MM" format.

        Returns:
        list: A list containing three strings. The first is the converted Pacific Standard Time, 
          the second is Indian Standard Time, and the third is the original CST time.
          If conversion fails due to parsing errors or invalid times, returns ["Invalid", "Invalid", "Invalid"].

        Raises:
        ValueError: If `cst_str` is not in the expected format.
        pytz.exceptions.AmbiguousTimeError: If an ambiguous time error occurs during localization.
        pytz.exceptions.NonExistentTimeError: If a non-existent time error occurs during localization.
    """

    try:
        cst_tz = pytz.timezone('US/Central')
        current_utc = datetime.now(pytz.utc)
        today_cst_date = current_utc.astimezone(cst_tz).date()

        parsed_time = datetime.strptime(cst_str.strip(), "%H:%M")

        naive_dt = datetime(
            year=today_cst_date.year,
            month=today_cst_date.month,
            day=today_cst_date.day,
            hour=parsed_time.hour,
            minute=parsed_time.minute
        )

        new_cst_dt = cst_tz.localize(naive_dt)

        utc_dt = new_cst_dt.astimezone(pytz.utc)

        pacific_tz = pytz.timezone('America/Los_Angeles')
        pacific_str = utc_dt.astimezone(pacific_tz).strftime("%H:%M")

        ist_tz = pytz.timezone('Asia/Kolkata')
        ist_str_out = utc_dt.astimezone(ist_tz).strftime("%H:%M")

        return [pacific_str, ist_str_out, new_cst_dt.strftime("%H:%M")]
    except (ValueError, pytz.exceptions.AmbiguousTimeError, pytz.exceptions.NonExistentTimeError):
        return ["Invalid", "Invalid", "Invalid"]

def get_initial_times():
    """ Retrieves the current times in Pacific Standard Time, Indian Standard Time, and Central Standard Time.

        This function calculates and returns the current local time for PST, IST, and CST using UTC as a reference point.

        Returns:
        tuple: A tuple containing three strings. Each string represents the current time in "HH:MM" format 
               for Pacific Standard Time, Indian Standard Time, and Central Standard Time respectively.

        Raises:
        None
    """

    now_utc = datetime.now(pytz.utc)
    
    pst_tz = pytz.timezone('America/Los_Angeles')
    pacific_dt_str = now_utc.astimezone(pst_tz).strftime("%H:%M")
    
    ist_tz = pytz.timezone('Asia/Kolkata')
    ist_dt_str = now_utc.astimezone(ist_tz).strftime("%H:%M")
    
    cst_tz = pytz.timezone('US/Central')
    cst_dt_str = now_utc.astimezone(cst_tz).strftime("%H:%M")
    
    return pacific_dt_str, ist_dt_str, cst_dt_str

with gr.Blocks(theme=gr.themes.Soft()) as app:
    init_pacific, init_ist, init_cst = get_initial_times()

    gr.Markdown("# Time Zone Converter")
    gr.Markdown("### (24hr Clock)")
    gr.Markdown("**Current Time**")
    
    with gr.Row():
        cpacific_input = gr.Textbox(label="Pacific Time (PST/PDT)", value=init_pacific)
        cist_input = gr.Textbox(label="India Time (IST)", value=init_ist)
        ccst_input = gr.Textbox(label="Central Time (CST/CDT)", value=init_cst)
        # Add a manual refresh button
    with gr.Row():
        refresh_button = gr.Button("Refresh Current Time", elem_id="refresh-button")

    def update_times(*args):
        new_pacific, new_ist, new_cst = get_initial_times()
        
        return new_pacific, new_ist, new_cst

    # Linking the button click to trigger update function
    refresh_button.click(fn=update_times, outputs=[cpacific_input, cist_input, ccst_input])
    
    gr.Markdown("**Time conversions**")
    with gr.Row():
        pacific_input = gr.Textbox(label="Pacific Time (PST/PDT)", value="00:00")
        ist_input = gr.Textbox(label="India Time (IST)", value="00:00")
        cst_input = gr.Textbox(label="Central Time (CST/CDT)", value="00:00")

    # Add both blur and submit events for each input
    pacific_input.blur(
        fn=update_from_pacific,
        inputs=pacific_input,
        outputs=[pacific_input, ist_input, cst_input]
    )
    pacific_input.submit(
        fn=update_from_pacific,
        inputs=pacific_input,
        outputs=[pacific_input, ist_input, cst_input]
    )

    ist_input.blur(
        fn=update_from_ist,
        inputs=ist_input,
        outputs=[pacific_input, ist_input, cst_input]
    )
    ist_input.submit(
        fn=update_from_ist,
        inputs=ist_input,
        outputs=[pacific_input, ist_input, cst_input]
    )

    cst_input.blur(
        fn=update_from_cst,
        inputs=cst_input,
        outputs=[pacific_input, ist_input, cst_input]
    )
    cst_input.submit(
        fn=update_from_cst,
        inputs=cst_input,
        outputs=[pacific_input, ist_input, cst_input]
    )
        # Define the function to update inputs when the refresh button is clicked
    def update_times(*args):
        new_pacific, new_ist, new_cst = refresh_times()
        
        pacific_input.value = new_pacific
        ist_input.value = new_ist
        cst_input.value = new_cst
    
app.launch(server_name="0.0.0.0", pwa=True)
