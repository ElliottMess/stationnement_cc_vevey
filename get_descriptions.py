import json
import os

from yt_dlp import YoutubeDL

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

# Create descriptions directory if it doesn't exist
os.makedirs('descriptions', exist_ok=True)

# Configure yt-dlp
ydl_opts = {
    'quiet': True,
    'no_warnings': True,
    'extract_flat': False,  # We need full extraction for descriptions
    'format': 'worst',  # Use worst quality to speed up metadata extraction
    'skip_download': True,  # Don't download the video
    'writesubtitles': False,
    'writeautomaticsub': False
}

# Initialize youtube-dl
ydl = YoutubeDL(ydl_opts)

# Iterate over each video
for date, video_id in video_conseils_id.items():
    try:
        # Get video info
        url = f'https://www.youtube.com/watch?v={video_id}'
        info = ydl.extract_info(url, download=False)

        # Extract relevant information
        description_data = {
            'title': info.get('title', ''),
            'description': info.get('description', ''),
            'upload_date': info.get('upload_date', ''),
            'duration': info.get('duration', 0),
            'view_count': info.get('view_count', 0),
        }

        # Save to file
        output_file = f'descriptions/description_cc_{date}.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(description_data, f, ensure_ascii=False, indent=2)
        print(f"Successfully saved description for video {date} ({video_id})")

    except Exception as e:
        print(
            f"Error getting description for video {date} ({video_id}): {str(e)}")
