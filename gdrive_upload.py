import os
import yaml
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def upload_to_gdrive(file_path):
    """
    Upload a file to Google Drive using PyDrive2.

    Args:
        file_path (str): Path to the file to upload.

    Returns:
        str: Path to the uploaded file.
    """
    cfg = load_config()
    if not cfg["google_drive"]["enabled"]:
        print("⚠️ Google Drive upload is disabled in config.")
        return file_path

    # Authenticate with Google Drive
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    folder_id = cfg["google_drive"]["folder_id"]
    file_name = os.path.basename(file_path)

    # Create file in the target folder on Google Drive
    file = drive.CreateFile({
        "parents": [{"id": folder_id}],
        "title": file_name
    })
    file.SetContentFile(file_path)
    file.Upload()

    print(f"✅ Uploaded {file_name} to Google Drive folder ID: {folder_id}")
    return file_path