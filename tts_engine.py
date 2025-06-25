import os
from TTS.api import TTS

# Crear carpeta para audios si no existe
os.makedirs("static/audio", exist_ok=True)

# Cargar modelo
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)

def generar_audio(nombre_archivo, texto):
    ruta = f"static/audio/{nombre_archivo}.wav"
    tts.tts_to_file(text=texto, file_path=ruta)
    return ruta  # Devuelve la ruta para usarla en Twilio o para subir

# Ejemplo de uso
if __name__ == "__main__":
    texto = "Hello John, this is your load offer from Dallas to Miami. We pay up to 1500 dollars."
    generar_audio("john_dallas_miami", texto)
    print("✅ Audio generado en static/audio/")

