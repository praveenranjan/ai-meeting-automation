# 🎥 AI Meeting Automation with OBS + Whisper + LangChain (Ollama) + Google Drive

This project automates the full workflow of **recording meetings, transcribing, summarizing, and storing notes** in Google Drive. It is built with **Python, LangChain, Whisper, Ollama, OBS, and PyDrive2**.

---

## 📦 Features
- **OBS Recording Control**  
  - WebSocket or AppleScript mode (auto-fallback).  
  - Start/Stop recording directly from the shell script.  
  - Optionally, provide a meeting name to use as filenames for recording, transcript, and summary.
- **File Watcher**  
  - Monitors your OBS recordings folder for new `.mov`, `.mkv` or `.mp4` files.  
  - Automatically renames files based on meeting name if provided.
- **Transcription**  
  - Uses [OpenAI Whisper](https://github.com/openai/whisper) for accurate speech-to-text.  
- **Summarization**  
  - Powered by [LangChain](https://www.langchain.com/) with Ollama models (e.g., `gpt-oss`, `llama2`, `mistral`).  
- **Cloud Storage**  
  - Automatically uploads transcripts & summaries to Google Drive via [PyDrive2](https://docs.iterative.ai/PyDrive2/).

---

## 🛠️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/praveenranjan/ai-meeting-automation.git
cd ai-meeting-automation
```

### 2. Create a Virtual Environment (Recommended)
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Requirements
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Make the pipeline executable
```bash
chmod +x run_pipeline.sh
```

### 5. Run the pipeline
```bash
./run_pipeline.sh
```

### 6. Deactivate when finished
```bash
deactivate
```
---

## ⚙️ Configuration

Rename `config-template.yaml` to `config.yaml` 
Edit `config.yaml`:

```yaml
obs:
  mode: auto  # options: auto, websocket, apple_script
  recording_path: "/Users/Shared/OBSRecordings"  # as defined in OBS Studio
  websocket_host: "localhost"  # as defined in OBS Studio
  websocket_port: 4455  # as defined in OBS Studio
  websocket_password: "yourpassword"  # as defined in OBS Studio

transcription:
  model: "small"  # options: tiny, base, small, medium, large

ollama:
  model: "gpt-oss"  # options: gpt-oss, phi4, llama2, mistral, etc.

google_drive:
  enabled: true  # options: true, false
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
cd ai-meeting-automation
source .venv/bin/activate
./run_pipeline.sh
```

1. Script asks for meeting name (optional).
2. OBS recording starts automatically.  
3. Script waits until you press **Enter**.  
4. OBS recording stops.  
5. File watcher picks up the recording, generates related filenames (using meeting name if provided), transcribes & summarizes the meeting.
6. Transcript and meeting summary are uploaded to Google Drive.
---

## ⚡ Prerequisites

Before running the pipeline, make sure you have the following installed and set up:

### OBS Studio 🎥
- Required for recording meetings  
- Download: [OBS Studio](https://obsproject.com/)  
- Configure a recording path (update `config.yaml` accordingly)  
- **If using WebSocket mode**: enable OBS WebSocket and update `config.yaml`  
- **If using AppleScript mode**: set up a Hotkey (⌘⌥R) for Start/Stop Recording in OBS, and update `obs_control.py` accordingly  

### Whisper 📝
- Already included in `requirements.txt` (`openai-whisper`).
- By default, Whisper will download the model specified in config.yaml (e.g., base, small, medium, or large).
- Pre-download the model to avoid delays:
```bash
whisper --model small test.mp3
```

### Ollama 🤖
- Download: [https://ollama.ai/download](https://ollama.ai/download)
- Pull a model (e.g., `llama3` or `mistral`):
```bash
ollama pull llama3
```
- Configure in `config.yaml`:
```yaml
ollama:
  model: llama3
```

### Google Drive (Optional) ☁️
Only needed if you want transcripts & summaries uploaded.  

- Follow [PyDrive2 Quickstart](https://docs.iterative.ai/PyDrive2/quickstart/) and place `client_secrets.json` in the project root.  
- On the first run, a browser will open for authentication.  
- Update `config.yaml`:  
```yaml
google_drive:
  enabled: true
  folder_id: your-folder-id
```

How to get your Google Drive folder ID:
1.	Open Google Drive in your browser.
2.	Navigate to the folder where you want to upload files.
3.	Look at the URL in your browser’s address bar. Example:
https://drive.google.com/drive/folders/1a2B3cD4EfGhIJkLmNoPQRstuVwXYZ
4.	Copy the part after /folders/ as the folder ID: 1a2B3cD4EfGhIJkLmNoPQRstuVwXYZ
5.	Use this ID in your config.yaml.

Once set, transcripts and summaries will automatically upload into that folder.

---

## 📂 Project Structure

```
.
├── run_pipeline.sh        # Main entry point
├── obs_control.py         # OBS integration (WebSocket with AppleScript fallback)
├── watcher.py             # File watcher for new recordings (supports meeting name)
├── transcriber.py         # OpenAI Whisper-based transcription
├── summarizer.py          # LangChain with Ollama-based summarization
├── drive_uploader.py      # Uploads transcript & summary to Google Drive
├── config.yaml            # Configuration file
├── requirements.txt
└── README.md
```

---
