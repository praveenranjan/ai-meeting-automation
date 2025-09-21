import time
import os
import yaml
import shutil

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def watch_for_recording(meeting_name=None):
    """
    Watches OBS recording folder and returns the path of the last recorded file.
    Optionally renames the recording file based on meeting_name.
    """
    cfg = load_config()
    recording_path = cfg["obs"]["recording_path"]
    latest_file = None

    while True:
        files = [os.path.join(recording_path, f) for f in os.listdir(recording_path)]
        if files:
            latest_file = max(files, key=os.path.getctime)
            if not latest_file.endswith(".tmp"):
                break
        time.sleep(5)

    # If meeting_name is provided, rename the file
    if meeting_name:
        ext = os.path.splitext(latest_file)[1]
        new_file = os.path.join(recording_path, f"{meeting_name}{ext}")
        shutil.move(latest_file, new_file)
        latest_file = new_file

    return latest_file