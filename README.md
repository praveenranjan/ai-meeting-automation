# 🎥 Meeting Automation with OBS + Whisper + LangChain (Ollama) + Google Drive

This project automates the full workflow of **recording meetings, transcribing, summarizing, and storing notes** in Google Drive. It is built with **Python, LangChain, Whisper, Ollama, OBS, and PyDrive2**.

---

## 📦 Features
- **OBS Recording Control**  
  - WebSocket or AppleScript mode (auto-fallback).  
  - Start/Stop recording directly from the shell script.  
  - Optionally, provide a meeting name to use as filenames for recording, transcript, and summary.
- **File Watcher**  
  - Monitors your OBS recordings folder for new `.mkv` or `.mp4` files.  
  - Automatically renames files based on meeting name if provided.
- **Transcription**  
  - Uses [OpenAI Whisper](https://github.com/openai/whisper) for accurate speech-to-text.  
- **Summarization**  
  - Powered by [LangChain](https://www.langchain.com/) with Ollama models (e.g., `gpt-oss`, `llama2`, `mistral`).  
- **Cloud Storage**  
  - Automatically uploads transcripts & summaries to Google Drive via [PyDrive2](https://docs.iterative.ai/PyDrive2/).

---

## 🛠️ Setup

### 1. Create a Virtual Environment (Recommended)
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Requirements
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Make the pipeline executable
```bash
chmod +x run_pipeline.sh
```

### 4. Deactivate when finished
```bash
deactivate
```
---

## ⚙️ Configuration

Rename `config-template.yaml` to `config.yaml` 
Edit `config.yaml`:

```yaml
obs:
  mode: auto   # options: auto, websocket, apple_script
  recording_path: "/Users/Shared/OBSRecordings"
  websocket_host: "localhost"
  websocket_port: 4455
  websocket_password: "yourpassword"

transcription:
  model: "small"  # options: tiny, base, small, medium, large

ollama:
  model: "phi4"  # options: gpt-oss, llama2, mistral, etc.

google_drive:
  enabled: true
  folder_id: "your_google_drive_folder_id"
```

- `obs.mode`:
  - `websocket` → uses OBS WebSocket plugin.  
  - `apple_script` → uses macOS automation (requires hotkey in OBS for **Start/Stop Recording**).  
  - `auto` → tries WebSocket first, falls back to AppleScript.  

---

## ▶️ Usage

### Start a Meeting Recording and Automation Pipeline
```bash
source .venv/bin/activate
./run_pipeline.sh
```

1. Script asks for meeting name (optional).
2. OBS recording starts automatically.  
3. Script waits until you press **Enter**.  
4. OBS recording stops.  
5. File watcher picks up the recording, generates related filenames (using meeting name if provided), transcribes, summarizes, and uploads to Google Drive.

---

## 📂 Project Structure

```
.
├── run_pipeline.sh        # Main entry point
├── obs_control.py         # OBS integration (WebSocket + AppleScript fallback)
├── watcher.py             # File watcher for new recordings (supports meeting name)
├── transcriber.py         # Whisper-based transcription
├── summarizer.py          # LangChain summarization
├── drive_uploader.py      # Uploads to Google Drive
├── config.yaml            # Configuration file
├── requirements.txt
└── README.md
```

---

## 🔐 Google Drive Setup

1. Follow [PyDrive2 Quickstart](https://docs.iterative.ai/PyDrive2/quickstart/)  
2. Place `client_secrets.json` in the project root.  
3. On first run, authentication will open in a browser.  

## To get the Google Drive folder ID:

1.	Open Google Drive in your browser.
2.	Navigate to the folder where you want to upload files.
3.	Look at the URL in your browser’s address bar. Example:
https://drive.google.com/drive/folders/1a2B3cD4EfGhIJkLmNoPQRstuVwXYZ
4.	Copy the part after /folders/ as the folder ID: 1a2B3cD4EfGhIJkLmNoPQRstuVwXYZ
5.	Use this ID in your config.yaml.
Once this is set, your script can upload files directly into that folder.
