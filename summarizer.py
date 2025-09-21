import yaml
import os
from langchain_ollama import OllamaLLM

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def summarize(transcript_file, summary_file=None):
    """
    Summarize a meeting transcript using Ollama LLM.
    
    Args:
        transcript_file (str): Path to the transcript text file.
        summary_file (str, optional): Path to save the meeting summary. 
            If None, generates a filename based on transcript file.
            
    Returns:
        str: Path to the saved summary file.
    """
    cfg = load_config()
    llm = OllamaLLM(model=cfg["ollama"]["model"])

    # Generate summary file name if not provided
    if summary_file is None:
        base_name = os.path.splitext(os.path.basename(transcript_file))[0].replace("_transcript", "")
        summary_file = f"{base_name}_meeting_summary.txt"

    with open(transcript_file, "r") as f:
        text = f.read()

    prompt = f"Summarize the following meeting transcript. Provide key points and action items. Transcript: {text}"
    summary = llm.invoke(prompt)

    with open(summary_file, "w") as f:
        f.write(summary)

    return summary_file