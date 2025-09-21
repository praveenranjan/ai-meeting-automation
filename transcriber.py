import whisper
import yaml
import os

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def transcribe(video_file_path, transcript_file=None):
    """
    Transcribe a video file using Whisper.

    Args:
        video_file_path (str): Path to the recorded video file.
        transcript_file (str, optional): Path to save the transcript text. 
            If None, generates a filename based on the video file.

    Returns:
        str: Path to the saved transcript file.
    """
    cfg = load_config()
    model = whisper.load_model(cfg["transcription"]["model"])

    # Generate transcript filename if not provided
    if transcript_file is None:
        base_name = os.path.splitext(os.path.basename(video_file_path))[0]
        transcript_file = f"{base_name}_transcript.txt"

    result = model.transcribe(video_file_path)

    with open(transcript_file, "w") as f:
        f.write(result["text"])

    return transcript_file