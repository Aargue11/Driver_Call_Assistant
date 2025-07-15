import os
import subprocess
from TTS.api import TTS

# Crear carpeta si no existe
os.makedirs("audio_static", exist_ok=True)

# Inicializar Coqui
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)

def generar_audio(nombre_archivo, texto):
    ruta_raw = f"audio_static/{nombre_archivo}_raw.wav"
    ruta_final = f"audio_static/{nombre_archivo}.mp3"

    # Paso 1: Generar archivo wav con Coqui
    tts.tts_to_file(text=texto, file_path=ruta_raw)

    # Paso 2: Convertir con ffmpeg a mp3 con parámetros correctos para Twilio
    subprocess.run([
        r"C:\ffmpeg\bin\ffmpeg.exe",
        "-y",
        "-i", ruta_raw,
        "-ac", "1",
        "-ar", "16000",
        "-b:a", "64k",
        "-codec:a", "libmp3lame",
        "-compression_level", "2",
        "-flags", "+bitexact",
        "-write_xing", "0",
        "-f", "mp3",
        ruta_final
    ], check=True)

    os.remove(ruta_raw)  # Eliminar wav temporal
    print(f"✅ Audio final convertido y guardado: {ruta_final}")
    return ruta_final

if __name__ == "__main__":
    generar_audio("test_offer", "Hello! This is your load offer from Dallas to Miami.")


