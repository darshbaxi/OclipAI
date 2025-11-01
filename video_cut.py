import yt_dlp
import subprocess

# --------------------------
# Step 1: YouTube Video URL
# --------------------------
# youtube_url = "www.youtube.com/watch?v=xAt1xcC6qfM"  # replace with your YouTube link
video_file = "/Users/darshbaxi/Desktop/oclipsai/videoplayback.mp4"

# Download the YouTube video
# ydl_opts = {
#     'format': 'best',
#     'outtmpl': video_file
# }

# with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#     ydl.download([youtube_url])

# --------------------------
# Step 2: Timestamps
# --------------------------
# List of segments with start and end times in seconds
segments = [
    {"start_reel": 258.6, "end_reel": 288.6} # example additional segment
    # Add more segments as needed
]

# --------------------------
# Step 3: Cut video segments
# --------------------------
for i, seg in enumerate(segments, start=1):
    start = seg["start_reel"]
    end = seg["end_reel"]
    output_file = f"segment_{i}.mp4"

    cmd = [
        "ffmpeg",
        "-i", video_file,
        "-ss", str(start),
        "-to", str(end),
        "-c", "copy",
        output_file
    ]
    
    print(f"Creating {output_file} from {start} to {end} seconds...")
    subprocess.run(cmd)

print("All segments created successfully!")
