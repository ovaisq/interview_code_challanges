#!/usr/bin/env python3
"""Time Zone Converter Application

        This application provides functions to convert times between various time zones:
        - Pacific Standard Time (America/Los_Angeles)
        - Indian Standard Time (Asia/Kolkata)
        - Central Standard Time (US/Central)

        Users can input a time in any of these formats, and the system will calculate
        the equivalent times for the other two time zones.
"""

import gradio as gr
from datetime import datetime
import pytz

def update_from_pacific(pst_time_str):
    """Converts a given Pacific Standard Time string to Indian Standard Time
		and Central Standard Time

		This function takes a PST time in "HH:MM" format as input, then converts
		it to equivalent times in IST and CST

		Parameters:
		pst_time_str (str): A string representing the time in Pacific Standard
							Time in "HH:MM" format

		Returns:
		list: A list containing three strings. The first is Pacific Standard
			  Time, the second is Indian Standard Time, and the third is
              Central Standard Time. If conversion fails due to parsing
              errors or invalid times, returns ["Invalid", "Invalid", "Invalid"]

		Raises:
		ValueError: If `pst_time_str` is not in the expected format.
    """

    try:
        pacific_tz = pytz.timezone('America/Los_Angeles')
        parsed_time = datetime.strptime(pst_time_str.strip(), "%H:%M")
        naive_dt = datetime.combine(datetime.today(), parsed_time.time())
        local_dt = pacific_tz.localize(naive_dt)

        utc_dt = local_dt.astimezone(pytz.utc)
        ist_tz = pytz.timezone('Asia/Kolkata')
        cst_tz = pytz.timezone('US/Central')

        ist_time_str = utc_dt.astimezone(ist_tz).strftime("%H:%M")
        cst_time_str = utc_dt.astimezone(cst_tz).strftime("%H:%M")

        return [pacific_tz.normalize(local_dt).strftime("%H:%M"), ist_time_str, cst_time_str]
    except (ValueError, pytz.exceptions.AmbiguousTimeError, pytz.exceptions.NonExistentTimeError):
        return ["Invalid", "Invalid", "Invalid"]

def update_from_ist(ist_time_str):
    """Converts a given Indian Standard Time string to Pacific Standard Time
       and Central Standard Time.

		This function takes an IST time in "HH:MM" format as input, then
        converts it to equivalent times in PST and CST.

		Parameters:
		ist_time_str (str): A string representing the time in Indian Standard Time in "HH:MM" format.

		Returns:
		list: A list containing three strings. The first is Pacific Standard Time,
			  the second is Indian Standard Time as provided or calculated, and the third is Central Standard Time.
			  If conversion fails due to parsing errors or invalid times, returns ["Invalid", "Invalid", "Invalid"].

		Raises:
		ValueError: If `ist_time_str` is not in the expected format.
    """

    try:
        ist_tz = pytz.timezone('Asia/Kolkata')
        parsed_time = datetime.strptime(ist_time_str.strip(), "%H:%M")
        naive_dt = datetime.combine(datetime.today(), parsed_time.time())
        local_dt = ist_tz.localize(naive_dt)

        utc_dt = local_dt.astimezone(pytz.utc)
        pacific_tz = pytz.timezone('America/Los_Angeles')
        cst_tz = pytz.timezone('US/Central')

        pacific_time_str = utc_dt.astimezone(pacific_tz).strftime("%H:%M")
        cst_time_str = utc_dt.astimezone(cst_tz).strftime("%H:%M")

        return [pacific_time_str, ist_tz.normalize(local_dt).strftime("%H:%M"), cst_time_str]
    except (ValueError, pytz.exceptions.AmbiguousTimeError, pytz.exceptions.NonExistentTimeError):
        return ["Invalid", "Invalid", "Invalid"]

def update_from_cst(cst_time_str):
    """Converts a given Central Standard Time string to Pacific Standard Time and Indian Standard Time.

		This function takes a CST time in "HH:MM" format as input, then converts it to equivalent times in PST and IST.

		Parameters:
		cst_time_str (str): A string representing the time in Central Standard Time in "HH:MM" format.

		Returns:
		list: A list containing three strings. The first is Pacific Standard Time,
			  the second is Indian Standard Time, and the third is Central Standard Time.
			  If conversion fails due to parsing errors or invalid times, returns ["Invalid", "Invalid", "Invalid"].

		Raises:
		ValueError: If `cst_time_str` is not in the expected format.
    """

    try:
        cst_tz = pytz.timezone('US/Central')
        parsed_time = datetime.strptime(cst_time_str.strip(), "%H:%M")
        naive_dt = datetime.combine(datetime.today(), parsed_time.time())
        local_dt = cst_tz.localize(naive_dt)

        utc_dt = local_dt.astimezone(pytz.utc)
        pacific_tz = pytz.timezone('America/Los_Angeles')
        ist_tz = pytz.timezone('Asia/Kolkata')

        pacific_time_str = utc_dt.astimezone(pacific_tz).strftime("%H:%M")
        ist_time_str = utc_dt.astimezone(ist_tz).strftime("%H:%M")

        return [pacific_time_str, ist_time_str, cst_tz.normalize(local_dt).strftime("%H:%M")]
    except (ValueError, pytz.exceptions.AmbiguousTimeError, pytz.exceptions.NonExistentTimeError):
        return ["Invalid", "Invalid", "Invalid"]

def get_initial_times():
    """Retrieves the current times in Pacific Standard Time, Indian Standard Time, and Central Standard Time.

		This function calculates and returns the current local time for PST, IST, and CST using UTC as a reference point.

		Returns:
		tuple: A tuple containing three strings. Each string represents the current time in "HH:MM" format
			   for Pacific Standard Time, Indian Standard Time, and Central Standard Time respectively.
    """

    now_utc = datetime.now(pytz.utc)

    pst_tz = pytz.timezone('America/Los_Angeles')
    ist_tz = pytz.timezone('Asia/Kolkata')
    cst_tz = pytz.timezone('US/Central')

    pacific_dt_str = now_utc.astimezone(pst_tz).strftime("%H:%M")
    ist_dt_str = now_utc.astimezone(ist_tz).strftime("%H:%M")
    cst_dt_str = now_utc.astimezone(cst_tz).strftime("%H:%M")

    return pacific_dt_str, ist_dt_str, cst_dt_str

# Gradio Interface
with gr.Blocks(title="Timezone Converter", theme=gr.themes.Soft(), css='footer {display: none !important;}') as app:
    init_pacific, init_ist, init_cst = get_initial_times()

    gr.Markdown("# Time Zone Converter")
    gr.Markdown("### (24hr Clock)")
    gr.Markdown("**Current Time**")

    with gr.Row():
        cpacific_input = gr.Textbox(label="Pacific Time (PST/PDT)", value=init_pacific)
        cist_input = gr.Textbox(label="India Time (IST)", value=init_ist)
        ccst_input = gr.Textbox(label="Central Time (CST/CDT)", value=init_cst)

    with gr.Row():
        refresh_button = gr.Button("Refresh Current Time")

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

app.launch(server_name='0.0.0.0', server_port=7860, pwa=True)
