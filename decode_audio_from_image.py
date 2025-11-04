import cv2
import numpy as np
import wave
from pydub import AudioSegment

def decode_audio_from_image(stego_path, output_audio_path):
   
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

    
    if not bits:
        raise ValueError(" No hidden audio data found in image!")

    binary_data = ''.join(bits)
    audio_bytes = bytes(int(binary_data[i:i + 8], 2) for i in range(0, len(binary_data), 8))

    
    temp_wav = "decoded_temp.wav"
    with wave.open(temp_wav, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(44100)
        wf.writeframes(audio_bytes)

    try:
    
        if output_audio_path.lower().endswith(".mp3"):
            sound = AudioSegment.from_wav(temp_wav)
            sound.export(output_audio_path, format="mp3")
        else:
            
            import shutil
            shutil.copy(temp_wav, output_audio_path)

        print(f" Audio successfully decoded and saved as {output_audio_path}")
    except Exception as e:
        print(f" Decoding succeeded but conversion failed: {e}")
        print("Try playing decoded_temp.wav manually.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python decode_audio_from_image.py <stego_image> <output_audio>")
    else:
        decode_audio_from_image(sys.argv[1], sys.argv[2])