import csv
import json
import os
from datetime import datetime

from yt_dlp import YoutubeDL

# Create descriptions directory if it doesn't exist
os.makedirs('data/descriptions', exist_ok=True)

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


def get_video_descriptions():
    """Get descriptions for all videos in the CSV file."""
    successful = 0
    failed = 0

    # Initialize youtube-dl
    ydl = YoutubeDL(ydl_opts)

    # Read video IDs from CSV
    with open('data/youtube_videos_cc.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                # Convert date format from YYYY-MM-DD to DD-MM-YYYY
                date_obj = datetime.strptime(row['date'], '%Y-%m-%d')
                formatted_date = date_obj.strftime('%d-%m-%Y')
                video_id = row['video_id']

                # Skip if description already exists
                output_file = f'data/descriptions/description_cc_{formatted_date}.json'
                if os.path.exists(output_file):
                    print(f"Skipping {video_id} - description already exists")
                    continue

                # Get video info
                url = f'https://www.youtube.com/watch?v={video_id}'
                info = ydl.extract_info(url, download=False)

                # Extract relevant information
                description_data = {
                    'video_id': video_id,
                    'title': info.get('title', ''),
                    'description': info.get('description', ''),
                    'upload_date': info.get('upload_date', ''),
                    'duration': info.get('duration', 0),
                    'view_count': info.get('view_count', 0),
                }

                # Save to file
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(description_data, f,
                              ensure_ascii=False, indent=2)
                print(
                    f"Successfully saved description for video {formatted_date} ({video_id})")
                successful += 1

            except Exception as e:
                print(
                    f"Error getting description for video {row['date']} ({row['video_id']}): {str(e)}")
                failed += 1

    print(f"\nDescription extraction complete!")
    print(f"Successfully processed: {successful}")
    print(f"Failed: {failed}")


if __name__ == "__main__":
    get_video_descriptions()
