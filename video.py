import cv2
import os

video_path = 'testv.mp4'
output_directory = 'output_video_images'

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

cap = cv2.VideoCapture(video_path)
image_counter = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    #Save frame 
    image_filename = os.path.join(output_directory, f'image_{image_counter:04d}.png')
    cv2.imwrite(image_filename, frame)
    image_counter += 1

cap.release()

print(f'{image_counter} images saved in {output_directory}')