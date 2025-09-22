import os
import yaml
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)


def upload_to_gdrive(files):
    """
    Upload one or more files to Google Drive using PyDrive2.

    Args:
        files (str | list[str]): Path or list of paths to the files to upload.

    Returns:
        list[str]: Paths to the uploaded files.
    """
    cfg = load_config()
    if not cfg["google_drive"]["enabled"]:
        print("⚠️ Google Drive upload is disabled in config.")
        return files if isinstance(files, list) else [files]

    # Normalize to list
    if isinstance(files, str):
        files = [files]

    # Authenticate with Google Drive
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    folder_id = cfg["google_drive"]["folder_id"]
    uploaded_files = []

    for file_path in files:
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            continue

        file_name = os.path.basename(file_path)
        gfile = drive.CreateFile({
            "parents": [{"id": folder_id}],
            "title": file_name
        })
        gfile.SetContentFile(file_path)
        gfile.Upload()

        print(f"✅ Uploaded {file_name} to Google Drive folder ID: {folder_id}")
        uploaded_files.append(file_path)

    return uploaded_files