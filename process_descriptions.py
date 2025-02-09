import json
import os
import re
from datetime import datetime

import pandas as pd


def timestamp_to_seconds(timestamp):
    """Convert timestamp string (HH:MM:SS or MM:SS) to seconds"""
    parts = timestamp.split(':')
    if len(parts) == 2:
        minutes, seconds = parts
        hours = 0
    else:
        hours, minutes, seconds = parts
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds)


def process_description_file(file_path):
    """Process a single description file and return a list of rows"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Extract video date and ID from filename
    video_date = re.search(
        r'description_cc_(\d{2}-\d{2}-\d{4})', file_path).group(1)

    # Get video ID from the URL in the description or from the data
    video_id = ''
    if 'https://www.youtube.com/watch?v=' in data.get('description', ''):
        video_id = re.search(r'watch\?v=([a-zA-Z0-9_-]+)',
                             data.get('description', '')).group(1)

    # Split description into lines
    lines = data['description'].split('\n')
    rows = []

    # Regular expression to match timestamps at the start of lines
    timestamp_pattern = r'^(\d{1,2}:\d{2}(?::\d{2})?)\s+(.+)$'

    # Process each line
    for i, line in enumerate(lines):
        if not line.strip():  # Skip empty lines
            continue

        match = re.match(timestamp_pattern, line.strip())
        if match:
            start_timestamp, content = match.groups()

            # Get end timestamp from next line or video duration
            end_timestamp = None
            for next_line in lines[i+1:]:
                next_match = re.match(timestamp_pattern, next_line.strip())
                if next_match:
                    end_timestamp = next_match.group(1)
                    break

            # If no next timestamp found, use video duration
            if not end_timestamp:
                hours = data['duration'] // 3600
                minutes = (data['duration'] % 3600) // 60
                seconds = data['duration'] % 60
                if hours > 0:
                    end_timestamp = f"{hours}:{minutes:02d}:{seconds:02d}"
                else:
                    end_timestamp = f"{minutes}:{seconds:02d}"

            # Calculate duration in seconds
            start_seconds = timestamp_to_seconds(start_timestamp)
            end_seconds = timestamp_to_seconds(end_timestamp)
            duration = end_seconds - start_seconds

            rows.append({
                'video_date': video_date,
                'video_id': video_id,
                'title': data.get('title', ''),
                'line_number': i + 1,
                'start_timestamp': start_timestamp,
                'end_timestamp': end_timestamp,
                'duration_seconds': duration,
                'content': content
            })

    return rows


def main():
    # Process all description files
    all_rows = []
    description_dir = 'descriptions'

    for filename in os.listdir(description_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(description_dir, filename)
            try:
                rows = process_description_file(file_path)
                all_rows.extend(rows)
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

    # Create DataFrame
    df = pd.DataFrame(all_rows)

    # Sort by video date and line number
    df['video_date'] = pd.to_datetime(df['video_date'], format='%d-%m-%Y')
    df = df.sort_values(['video_date', 'line_number'])

    # Save to CSV
    output_file = 'video_descriptions_table.csv'
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Successfully created {output_file}")


if __name__ == '__main__':
    main()
