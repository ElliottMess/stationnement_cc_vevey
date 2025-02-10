import json
import os
import re
from datetime import datetime
from pathlib import Path

import whisper
from pydub import AudioSegment
from tqdm import tqdm


def get_audio_files(audio_dir):
    """Get list of .mp3 files that don't have existing transcripts."""
    audio_files = []
    for file in os.listdir(audio_dir):
        if file.endswith('20min.mp3'):
            audio_path = os.path.join(audio_dir, file)
            video_id = file[:-4]  # Remove .mp3 extension
            transcript_path = os.path.join(
                'data/transcripts', f'transcript_{video_id}.json')
            if not os.path.exists(transcript_path):
                audio_files.append(audio_path)
    return audio_files


def save_transcript(transcript_data, audio_path):
    """Save transcript with metadata to JSON file."""
    filename = os.path.basename(audio_path)
    video_id = filename[:-4]  # Remove .mp3 extension
    output_path = os.path.join(
        'data/transcripts', f'transcript_{video_id}.json')

    # Prepare data with metadata
    data = {
        'audio_file': filename,
        'video_id': video_id,
        'date_processed': datetime.now().isoformat(),
        'transcript': transcript_data
    }

    # Create transcripts directory if it doesn't exist
    os.makedirs('data/transcripts', exist_ok=True)

    # Save to JSON file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return output_path


def load_transcript(transcript_path):
    """Load a previously generated transcript."""
    if os.path.exists(transcript_path):
        with open(transcript_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def process_audio_files():
    """Process all audio files that don't have existing transcripts."""
    # Load Whisper model
    print("Loading Whisper model...")
    try:
        model = whisper.load_model("small")
    except Exception as e:
        print(f"Error loading Whisper model: {str(e)}")
        return

    # Get list of audio files to process
    audio_files = get_audio_files('data/audio')

    if not audio_files:
        print("No new audio files to process.")
        return

    print(f"Found {len(audio_files)} new audio files to process.")

    # Process each audio file
    successful = 0
    failed = 0

    for audio_path in tqdm(audio_files, desc="Processing audio files"):
        try:
            # Transcribe audio with French language
            result = model.transcribe(audio_path, language="fr")

            # Save transcript
            output_path = save_transcript(result, audio_path)
            print(f"\nSaved transcript to: {output_path}")
            successful += 1

        except Exception as e:
            print(f"\nError processing {audio_path}: {str(e)}")
            failed += 1

    print(f"\nProcessing complete!")
    print(f"Successfully processed: {successful}")
    print(f"Failed: {failed}")


if __name__ == "__main__":
    process_audio_files()
