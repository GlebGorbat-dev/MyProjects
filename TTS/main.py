import argparse
from pydub import AudioSegment
import os
import librosa
import soundfile as sf
import numpy as np
import scipy.signal
from gtts import gTTS


def generate_gtts(text, output_path="tts.wav", lang="en"):
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save("temp.mp3")

    # Конвертируем в WAV (если нужно для дальнейшей обработки)
    sound = AudioSegment.from_mp3("temp.mp3")
    sound.export(output_path, format="wav")
    os.remove("temp.mp3")

def gentle_vocode(input_path, output_path, room_size=0.1, high_shelf_db=3.0, pitch_shift_steps=0):
    # Загружаем оригинал
    y, sr = librosa.load(input_path, sr=None)

    # Лёгкий pitch shift (по умолчанию 0 = нет изменения)
    if pitch_shift_steps != 0:
        y = librosa.effects.pitch_shift(y, sr=sr, n_steps=pitch_shift_steps)

    # Лёгкая реверберация: короткий импульс + затухание
    impulse = np.exp(-np.linspace(0, 3, int(sr * room_size)))  # экспоненциальное затухание
    impulse /= np.sum(impulse)  # нормализация
    y_reverb = scipy.signal.fftconvolve(y, impulse, mode='full')[:len(y)]
    y_blend = 0.85 * y + 0.15 * y_reverb  # очень мягкий эффект помещения

    # Фильтр для лёгкой эквализации (сделать звук чуть “теплее”)
    sos = scipy.signal.iirfilter(
        N=2,
        Wn=3000,
        rs=high_shelf_db,
        btype='lowpass',
        ftype='cheby2',
        fs=sr,
        output='sos'
    )
    y_final = scipy.signal.sosfilt(sos, y_blend)

    # Нормализация
    y_final /= np.max(np.abs(y_final) + 1e-6)

    # Сохраняем
    sf.write(output_path, y_final, sr)

def mix_with_music(voice_path, music_path, output_path, voice_level, music_level):
    voice = AudioSegment.from_wav(voice_path) + voice_level
    music = AudioSegment.from_file(music_path) + music_level
    combined = voice.overlay(music, loop=True)
    combined.export(output_path, format="mp3")

def main():
    parser = argparse.ArgumentParser(description="TTS overlay with music using xtts_v2")
    parser.add_argument("--text", help="Text to convert to speech")
    parser.add_argument("--text-file", help="Path to text file")
    parser.add_argument("--language", default="en", help="TTS language (en, ru, fr, de...)")
    parser.add_argument("--music-path", default="background.mp3", help="Background music file (mp3/wav)")
    parser.add_argument("--volume", type=int, default=0, help="Voice volume adjustment in dB")
    parser.add_argument("--music-volume", type=int, default=-12, help="Music volume adjustment in dB")

    args = parser.parse_args()

    if args.text_file and os.path.exists(args.text_file):
        with open(args.text_file, "r", encoding="utf-8") as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        raise ValueError("Provide either --text or --text-file")

    if not os.path.exists(args.music_path):
        raise FileNotFoundError(f"Background music not found: {args.music_path}")

    generate_gtts(text=text, output_path="tts.wav", lang=args.language)
    gentle_vocode("tts.wav", "vocoded.wav")
    mix_with_music("vocoded.wav", args.music_path, "final_mix.mp3", args.volume, args.music_volume)

    print("✅ Аудио успешно создано: final_mix.mp3")

if __name__ == "__main__":
    main()
