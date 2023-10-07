import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine
from PIL import Image

# Function to map grayscale values to pitch
def grayscale_to_pitch(value):
    pitch_value = value / 255.0  # Normalize to [0, 1]
    return pitch_value

# Function to map RGB values to pitch
def rgb_to_pitch(red, green, blue):
    pitch_value = (red + green + blue) / 10
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

    # Generate a piano-like sound (sine wave with a piano-like decay)
    audio = Sine(frequency).to_audio_segment(duration=duration_ms)
    if audio:
        audio = audio.fade_out(int(duration_ms * 0.98))  # Apply a fade-out effect
    return audio


# Function to generate sound by averaging RGB values of columns
def generate_sound_from_image(image_path, duration_ms, instrument='piano'):
    image = Image.open(image_path)
    width, height = image.size

    # Calculate the duration for each note
    note_duration = int(duration_ms / width)

    sound = 0  # Initial silent audio

    for x in range(width):
        total_r, total_g, total_b = 0, 0, 0

        for y in range(height):
            if image.mode == 'RGB':
                r, g, b = image.getpixel((x, y))
            elif image.mode == 'L':
                # Grayscale image, use grayscale value for all channels
                grayscale_value = image.getpixel((x, y))
                r, g, b = grayscale_value, grayscale_value, grayscale_value

            total_r += r
            total_g += g
            total_b += b

        avg_r = total_r // height
        avg_g = total_g // height
        avg_b = total_b // height

        if image.mode == 'RGB':
            pitch_value = rgb_to_pitch(avg_r, avg_g, avg_b)
        elif image.mode == 'L':
            pitch_value = grayscale_to_pitch(avg_r)

        note_audio = generate_instrument_sound(pitch_value, note_duration, instrument)
        sound = sound + note_audio

    return sound



# Path to your image file
image_path = "./Generating/testing.jpg"  # Change this to your image file path

# Generate the sound based on the image
duration_ms = 20000  # Total duration for the sound in milliseconds
generated_sound = generate_sound_from_image(image_path, duration_ms)

# Export the generated sound to a file (e.g., a WAV file)
output_file = "generated_sound_column_average.wav"
generated_sound.export(output_file, format="wav")
