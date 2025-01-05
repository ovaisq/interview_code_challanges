# utils.py
# ©2024, Ovais Quraishi
"""Utility functions
"""

def get_version():
    """Reads the first line from ver.txt, checks if it matches 
        semver (0.1.2) format and returns it.

        Returns:
            str: The version string if valid, otherwise False.
    """

    ver_file_path = 'ver.txt'

    try:
        with open(str(Path(ver_file_path).resolve()), 'r') as f:
            first_line = f.readline().strip()
    except FileNotFoundError:
        log_message = f"File {ver_file_path} not found."
        logging.error(log_message)
        return False

    semver_pattern = r'^\d+\.\d+\.\d+$'

    if re.match(semver_pattern, first_line):
        return {"version":first_line}
    else:
        log_message = "Invalid version format. Expected semver (0.1.2)."
        logging.error(log_message)
        return False
