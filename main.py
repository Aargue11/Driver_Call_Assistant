import os
import pandas as pd
from dotenv import load_dotenv
from twilio.rest import Client
from tts_engine import generar_audio
from git import Repo
import subprocess

# Config
load_dotenv()
twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
client = Client(twilio_sid, twilio_token)

drivers_df = pd.read_excel("drivers.xlsx")

# Función para limpiar nombres de archivo
def clean(text):
    return (
        text.lower()
        .replace(' ', '_')
        .replace(',', '')
        .replace('.', '')
        .replace(':', '')
        .replace(';', '')
        .replace('?', '')
        .replace('!', '')
        .replace('á', 'a')
        .replace('é', 'e')
        .replace('í', 'i')
        .replace('ó', 'o')
        .replace('ú', 'u')
    )

print("Enter Load Information:")
pickup = clean(input("Pickup Location: "))
delivery = clean(input("Delivery Location: "))
PU_window_time = input("Pickup Window Time: ")
DEL_window_time = input("Delivery Window Time: ")
miles = input("Total Miles: ")
actual_payment = input("Actual Payment: ")
max_payment = input("Maximum Payment: ")

# Función deploy a Netlify
def deploy_netlify():
    print("🚀 Haciendo deploy a Netlify automático...")
    token = os.getenv("NETLIFY_AUTH_TOKEN")
    subprocess.run([
        r"C:\Users\Alejandro Argüello G\AppData\Roaming\npm\netlify.cmd",
        "deploy",
        "--prod",
        "--dir=audio_static",
        f"--auth={token}"
    ], check=True)
    print("✅ Deploy completado correctamente y listo para Twilio!")

# Loop de llamadas
for index, row in drivers_df.iterrows():
    name = row['Name']
    phone = row['Phone']
    vehicle = row['Vehicle']

    filename = f"{clean(name)}_{pickup}_{delivery}"

    print(f"\n🎙️ Generando audio para {name}...")
    texto = (
        f"Hello {name}, this is a quick load offer for your {vehicle}. "
        f"The pickup is in {pickup}, and the delivery is in {delivery}. The trip is about {miles} miles. "
        f"The pickup time is from {PU_window_time}, and the delivery time is from {DEL_window_time}. "
        f"We are offering {actual_payment} dollars, but it is negotiable up to {max_payment} dollars. "
        f"If you are interested, please say YES; otherwise, say NO. Thanks!"
    )

    # Generar audio y guardar en carpeta audio_static
    audio_path = generar_audio(filename, texto)

    # Commit opcional (si quieres seguir usando GitHub)
    # repo = Repo(".")
    # repo.git.add(audio_path)
    # repo.index.commit(f"Add audio {audio_path}")
    # origin = repo.remote(name='origin')
    # origin.push()
    # print(f"✅ Subido a GitHub: {audio_path}")

# 🚀 Deploy Netlify después de generar todos los audios
deploy_netlify()

# 🔥 Hacer llamadas Twilio usando Netlify
for index, row in drivers_df.iterrows():
    name = row['Name']
    phone = row['Phone']

    filename = f"{clean(name)}_{pickup}_{delivery}"
    audio_url = f"https://dcassistant.netlify.app/{filename}.mp3"

    print(f"📞 Llamando a {name} con audio: {audio_url}")
    call = client.calls.create(
        twiml=f'<Response><Play>{audio_url}</Play></Response>',
        to=phone,
        from_=twilio_number
    )
    print(f"📲 Llamada enviada a {name}, SID: {call.sid}")
