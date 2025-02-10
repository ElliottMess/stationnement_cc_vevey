from __future__ import unicode_literals

import os
from datetime import datetime

import pandas as pd
import yt_dlp

# Create audio directory if it doesn't exist
if not os.path.exists('data/audio'):
    os.makedirs('data/audio')

# Read the CSV file
df = pd.read_csv('data/youtube_videos_cc.csv')

# Configure yt-dlp
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': 'data/audio/%(id)s.%(ext)s',  # Output template
    'quiet': False,  # Show progress
    'no_warnings': False,
}


def download_audio(date, video_id):
    # Check if file already exists
    expected_file = f'data/audio/{video_id}.mp3'
    if os.path.exists(expected_file):
        print(f"Skipping {video_id} - file already exists")
        return True

    url = f'https://www.youtube.com/watch?v={video_id}'
    print(f"\nDownloading audio for video {video_id} (dated {date})...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Successfully downloaded audio for {video_id}")
        return True
    except Exception as e:
        print(f"Error downloading {video_id}: {str(e)}")
        return False


# Download audio for each video
successful = 0
failed = 0
skipped = 0

for index, row in df.iterrows():
    if os.path.exists(f'data/audio/{row["video_id"]}.mp3'):
        skipped += 1
        continue

    if download_audio(row['date'], row['video_id']):
        successful += 1
    else:
        failed += 1

print(f"\nDownload complete!")
print(f"Successfully downloaded: {successful}")
print(f"Failed downloads: {failed}")
print(f"Skipped (already exists): {skipped}")
