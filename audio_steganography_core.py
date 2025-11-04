import cv2
import numpy as np
from pydub import AudioSegment
import os
import struct

# ---------- ENCODE ----------
def encode_audio_in_image(image_path, audio_path, output_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError("Image not found!")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype(np.uint8)

    temp_wav = "temp_audio.wav"
    audio = AudioSegment.from_file(audio_path)
    audio = audio.set_channels(1).set_sample_width(2).set_frame_rate(44100)
    audio.export(temp_wav, format="wav")

    
    with open(temp_wav, "rb") as f:
        audio_bytes = f.read()
    os.remove(temp_wav)

   
    length_bytes = struct.pack(">I", len(audio_bytes))  
    data = length_bytes + audio_bytes

    
    bits = ''.join(format(byte, '08b') for byte in data)

    flat = img.flatten()
    if len(bits) > len(flat):
        raise ValueError("Image not large enough for this audio file!")

    for i in range(len(bits)):
        flat[i] = (flat[i] & 0b11111110) | int(bits[i])

    stego = flat.reshape(img.shape)
    stego = cv2.cvtColor(stego, cv2.COLOR_RGB2BGR)
    cv2.imwrite(output_path, stego)
    print(f"Stego image saved as {output_path}")


# ---------- DECODE ----------
def decode_audio_from_image(stego_path, output_audio_path):
    img = cv2.imread(stego_path)
    if img is None:
        raise FileNotFoundError("Stego image not found!")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    flat = img.flatten()

    bits = [str(p & 1) for p in flat]

    
    length_bits = ''.join(bits[:32])
    audio_len = struct.unpack(">I", int(length_bits, 2).to_bytes(4, 'big'))[0]

   
    audio_bits = bits[32:32 + (audio_len * 8)]
    audio_bytes = bytes(int(''.join(audio_bits[i:i+8]), 2) for i in range(0, len(audio_bits), 8))

    temp_wav = "decoded_temp.wav"
    with open(temp_wav, "wb") as f:
        f.write(audio_bytes)

    try:
        if output_audio_path.lower().endswith(".mp3"):
            sound = AudioSegment.from_wav(temp_wav)
            sound.export(output_audio_path, format="mp3")
            os.remove(temp_wav)
        else:
            os.rename(temp_wav, output_audio_path)
    except Exception as e:
        print(" Audio conversion issue:", e)

    print(f" Audio extracted and saved as {output_audio_path}")