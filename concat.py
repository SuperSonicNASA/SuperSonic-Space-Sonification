from moviepy.editor import VideoFileClip, concatenate_videoclips

# List of video file paths to be concatenated
video_paths = []

for i in range(0, 1276, 5):
    video_path = f'Webb{i}.mp4'
    video_paths.append(video_path)

# Initialize a counter for progress tracking
processed_count = 0

# Load each video clip, and print the progress
video_clips = []
for video_path in video_paths:
    video_clip = VideoFileClip(video_path)
    video_clips.append(video_clip)
    
    # Increment the processed count and print progress
    processed_count += 1
    print(f'Processed {processed_count}/{len(video_paths)} videos')

# Concatenate the video clips into a single video
final_video = concatenate_videoclips(video_clips, method="compose")

# Define the output file name
output_file = 'concatenated_video.mp4'

# Write the final concatenated video to the output file
final_video.write_videofile(output_file, codec="libx264")

# Close all video clips
for video_clip in video_clips:
    video_clip.close()

print(f'Concatenated video saved as {output_file}')


