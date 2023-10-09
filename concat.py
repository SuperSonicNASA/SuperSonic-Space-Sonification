from moviepy.editor import VideoFileClip, concatenate_videoclips

video_paths = []

for i in range(0, 1276, 5):
    video_path = f'Webb{i}.mp4'
    video_paths.append(video_path)


processed_count = 0
video_clips = []
for video_path in video_paths:
    video_clip = VideoFileClip(video_path)
    video_clips.append(video_clip)
    
    # Increment the processed count and print progress
    processed_count += 1
    print(f'Processed {processed_count}/{len(video_paths)} videos')

final_video = concatenate_videoclips(video_clips, method="compose")

output_file = 'concatenated_video.mp4'

final_video.write_videofile(output_file, codec="libx264")
for video_clip in video_clips:
    video_clip.close()

print(f'Concatenated video saved as {output_file}')


