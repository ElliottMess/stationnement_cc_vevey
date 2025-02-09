import json
import os

from youtube_transcript_api import YouTubeTranscriptApi

# Dictionary mapping dates to video IDs
video_conseils_id = {
    "06-02-2025": "5pDGa9xPHCI",
    "05-12-2024": "V96S9AKLKRg",
    "14-11-2024": "CiTpmUVJknw",
    "03-10-2024": "X7wpBAIA00E",
    "05-09-2024": "xOqlNB2QotU",
    "20-06-2024": "ecAPSv_dUvo",
    "13-06-2024": "6poMM7abcxo",
    "02-05-2024": "bszn0dhE2L0",
    "14-03-2024": "ypgOLGqsbsw",
    "01-02-2024": "oBFVkTc9XNg",
    "14-12-2023": "gIxTj562cZ0"
}

# Create transcripts directory if it doesn't exist
os.makedirs('transcripts', exist_ok=True)

# Iterate over each video
for date, video_id in video_conseils_id.items():
    try:
        # Get transcript
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id, languages=['fr'])

        # Save to file
        output_file = f'transcripts/transcript_cc_{date}.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(transcript, f, ensure_ascii=False, indent=2)
        print(f"Successfully saved transcript for video {date} ({video_id})")

    except Exception as e:
        print(
            f"Error getting transcript for video {date} ({video_id}): {str(e)}")
