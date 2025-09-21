import subprocess
import yaml
import os
from obswebsocket import obsws, requests

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def run_applescript(script):
    try:
        subprocess.run(["osascript", "-e", script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"AppleScript error: {e}")

def start_obs_recording():
    cfg = load_config()
    mode = cfg["obs"].get("mode", "auto")

    if mode == "apple_script":
        _start_with_applescript()
    elif mode == "websocket":
        if not _start_with_websocket(cfg):
            print("⚠️ WebSocket failed, falling back to AppleScript...")
            _start_with_applescript()
    elif mode == "auto":
        if not _start_with_websocket(cfg):
            print("ℹ️ Falling back to AppleScript...")
            _start_with_applescript()
    else:
        print(f"Unknown OBS mode: {mode}")

def stop_obs_recording():
    cfg = load_config()
    mode = cfg["obs"].get("mode", "auto")

    if mode == "apple_script":
        _stop_with_applescript()
    elif mode == "websocket":
        if not _stop_with_websocket(cfg):
            print("⚠️ WebSocket failed, falling back to AppleScript...")
            _stop_with_applescript()
    elif mode == "auto":
        if not _stop_with_websocket(cfg):
            print("ℹ️ Falling back to AppleScript...")
            _stop_with_applescript()
    else:
        print(f"Unknown OBS mode: {mode}")

# --- Helpers ---

def _start_with_applescript():
    script = '''
    tell application "System Events"
        tell application "OBS" to activate
        keystroke "r" using {command down, option down}
    end tell
    '''
    print("▶️ Starting OBS recording via AppleScript (hotkey)...")
    run_applescript(script)

def _stop_with_applescript():
    script = '''
    tell application "System Events"
        tell application "OBS" to activate
        keystroke "r" using {command down, option down}
    end tell
    '''
    print("⏹️ Stopping OBS recording via AppleScript (hotkey)...")
    run_applescript(script)

def _start_with_websocket(cfg):
    try:
        ws = obsws(cfg["obs"]["websocket_host"],
                   cfg["obs"]["websocket_port"],
                   cfg["obs"]["websocket_password"])
        ws.connect()
        ws.call(requests.StartRecord())
        ws.disconnect()
        print("▶️ Starting OBS recording via WebSocket...")
        return True
    except Exception as e:
        print(f"WebSocket error: {e}")
        return False

def _stop_with_websocket(cfg):
    try:
        ws = obsws(cfg["obs"]["websocket_host"],
                   cfg["obs"]["websocket_port"],
                   cfg["obs"]["websocket_password"])
        ws.connect()
        ws.call(requests.StopRecord())
        ws.disconnect()
        print("⏹️ Stopping OBS recording via WebSocket...")
        return True
    except Exception as e:
        print(f"WebSocket error: {e}")
        return False

def generate_related_filenames(video_file_path: str, meeting_name: str = None):
    base_name = os.path.splitext(os.path.basename(video_file_path))[0]

    # generate files in the recording path
    directory = os.path.dirname(video_file_path)
    
    # generate files in the project directory
    # directory = os.path.dirname(os.path.abspath(__file__))

    # Use meeting_name if provided, otherwise default to video base name
    file_base = meeting_name if meeting_name else base_name

    transcript_file = os.path.join(directory, f"{file_base}_transcript.txt")
    summary_file = os.path.join(directory, f"{file_base}_meeting_summary.txt")

    return transcript_file, summary_file