import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine
from moviepy.editor import ImageSequenceClip, AudioFileClip
from PIL import Image, ImageDraw

pointer = 1

image = Image.open("./output_video_images/image_0000.png")
width, height = image.size

while pointer < width:
        
    image_link = "./test.png"

    # Function to map grayscale values to pitch
    def grayscale_to_pitch(value):
        pitch_value = value / 255.0  # Normalize to [0, 1]
        return pitch_value

    # Function to map RGB values to pitch
    def rgb_to_pitch(red, green, blue):
        pitch_value = (red + green + blue)/10
        return pitch_value

    # Function to generate a musical note based on pitch value
    def pitch_to_note(pitch):
        # Map pitch to frequency (adjust as needed)
        semitone_ratio = 2 ** (1 / 12)  # The ratio between pitches for one semitone
        base_frequency = 130.81  # C3 frequency in Hz
        return base_frequency * (semitone_ratio ** pitch)

    # Function to generate a musical instrument sound based on pitch value
    def generate_instrument_sound(pitch, duration_ms, instrument='piano'):
        # Map pitch to a musical note
        frequency = pitch_to_note(pitch)

        # Create a complex waveform using a combination of sine waves
        audio = (
            Sine(frequency).to_audio_segment(duration=duration_ms) +
            Sine(2 * frequency).to_audio_segment(duration=duration_ms) +
            Sine(3 * frequency).to_audio_segment(duration=duration_ms)
        )

        # Apply a fade-out effect
        audio = audio.fade_out(int(duration_ms * 0.9))

        return audio


    def generate_sound_from_image(image_path, duration_ms, column_interval=3, instrument='piano'):
        image = Image.open(image_path)
        width, height = image.size

        # Calculate the duration for each note and the skip value for columns
        note_duration = int(duration_ms / (width // column_interval) / 2)
        column_skip = column_interval

        sound = 0  # Initial silent audio

        for x in range(0, width, column_skip):
            total_r, total_g, total_b = 0, 0, 0

            for y in range(height):
                if image.mode == 'RGB' or "RGBA":
                    r, g, b= image.getpixel((x, y))
                elif image.mode == 'L':
                    # Grayscale image, use grayscale value for all channels
                    grayscale_value = image.getpixel((x, y))
                    r = g = b = grayscale_value

                total_r += r
                total_g += g
                total_b += b

            avg_r = total_r // height
            avg_g = total_g // height
            avg_b = total_b // height

            if image.mode == 'RGB' or "RGBA":
                pitch_value = rgb_to_pitch(avg_r, avg_g, avg_b)
            elif image.mode == 'L':
                pitch_value = grayscale_to_pitch(avg_r)

            # Move the pitch_value assignment outside the if-elif block to ensure it's always assigned
            note_audio = generate_instrument_sound(pitch_value, note_duration, instrument)
            sound = sound + note_audio

        return sound


    # Path to your image file
    image_path = image_link  # Change this to your image file path

    # Generate the sound based on the image
    duration_ms = 15000  # Total duration for the sound in milliseconds
    generated_sound = generate_sound_from_image(image_path, duration_ms)

    # Export the generated sound to a file (e.g., a WAV file)
    output_file = "generated_sound_column_average.wav"
    generated_sound.export(output_file, format="wav")



    def generate_animation_frames(image_path, column_interval=3, instrument='piano'):
        image = Image.open(image_path)
        width, height = image.size

        # Set up the output frames
        frames = []

        for x in range(0, width, column_interval):
            # Generate an image frame for the current column
            frame = image.copy()
            draw = ImageDraw.Draw(frame)
            draw.line((x, 0, x, height), fill=(255, 0, 0), width=2)  # Highlight the current column
            frames.append(np.array(frame))

        return frames

    # Path to your image file
    image_path = image_link  # Change this to your image file path

    # Generate the animation frames
    frames = generate_animation_frames(image_path, column_interval=3)

    # Path to your generated sound file
    sound_path = "generated_sound_column_average.wav"

    # Load the audio file
    audio = AudioSegment.from_wav(sound_path)

    # Set the frame rate (frames per second)
    audio_duration = len(generated_sound)
    fps = len(frames) / (audio_duration / 1000)

    # Create a video clip from the frames
    clip = ImageSequenceClip(frames, fps=fps)

    # Set the audio for the video
    clip = clip.set_audio(AudioFileClip(sound_path))

    output_video_path = "Webb6.mp4"
    clip.write_videofile(output_video_path, 
                        codec='h264',
                        remove_temp=True,
                        threads=4,
                        )