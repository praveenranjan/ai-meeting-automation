#!/bin/bash
set -e

# Ask for meeting name
echo "Enter meeting name (or press ENTER to use timestamp):"
read MEETING_NAME

echo "Starting OBS recording..."
python3 -c "import obs_control; obs_control.start_obs_recording()"

echo "Press ENTER when meeting is finished to stop recording."
read

python3 -c "import obs_control; obs_control.stop_obs_recording()"

echo "Waiting for recording file..."
python3 -c "import watcher; import sys; print(watcher.watch_for_recording(meeting_name='$MEETING_NAME'))" > last_file.txt
recording=$(cat last_file.txt)
echo "Recording file: $recording"

echo "Generating related filenames..."
python3 - <<EOF > filenames.txt
from obs_control import generate_related_filenames
tfile, sfile = generate_related_filenames("$recording")
print(tfile)
print(sfile)
EOF
transcript=$(sed -n '1p' filenames.txt)
summary=$(sed -n '2p' filenames.txt)

echo "Transcribing..."
python3 -c "import transcriber; print(transcriber.transcribe('$recording', '$transcript'))"

echo "Summarizing..."
python3 -c "import summarizer; print(summarizer.summarize('$transcript', '$summary'))"

echo "Uploading to Google Drive..."
python3 - <<EOF
import gdrive_upload
gdrive_upload.upload_to_gdrive(["$transcript", "$summary"])
EOF

echo "Done! Meeting transcript and summary saved and uploaded."