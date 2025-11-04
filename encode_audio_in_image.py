import cv2
import numpy as np
from pydub import AudioSegment
import wave

def encode_audio_in_image(image_path, audio_path, output_path):
    # Load the image properly (ithe unit8 asla pahije)
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f" Image not found: {image_path}")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = np.array(img, dtype=np.uint8)

    # audio conversion (dont del this function.. conversion karta)
    audio = AudioSegment.from_file(audio_path)
    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(44100)
    audio_bytes = audio.raw_data

    # Convert bytes to bits
    binary_data = ''.join(format(byte, '08b') for byte in audio_bytes)
    binary_data += '1111111111111110'  # EOF marker

    flat_img = img.flatten()

    if len(binary_data) > len(flat_img):
        raise ValueError(" Image not large enough to hold audio data.")

    
    for i in range(len(binary_data)):
        pixel_value = int(flat_img[i])
        flat_img[i] = np.uint8((pixel_value & ~1) | int(binary_data[i]))

    # save the stego image
    stego_img = flat_img.reshape(img.shape)
    stego_img = cv2.cvtColor(stego_img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(output_path, stego_img)
    print(f" Stego image saved as {output_path}")

def decode_audio_from_image(stego_path, output_audio_path):
    import wave

    img = cv2.imread(stego_path)
    if img is None:
        raise FileNotFoundError(f" Stego image not found: {stego_path}")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = np.array(img, dtype=np.uint8)

    flat_img = img.flatten()
    bits = []

    for value in flat_img:
        bits.append(str(value & 1))
        if ''.join(bits[-16:]) == '1111111111111110':
            bits = bits[:-16]
            break

    audio_bytes = bytes(int(''.join(bits[i:i + 8]), 2) for i in range(0, len(bits), 8))

    with wave.open(output_audio_path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(44100)
        wf.writeframes(audio_bytes)

    print(f" Audio extracted and saved as {output_audio_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python encode_audio_in_image.py <image> <audio> <output_image>")
    else:
        encode_audio_in_image(sys.argv[1], sys.argv[2], sys.argv[3])