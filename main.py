import os
import pandas as pd
from dotenv import load_dotenv
from twilio.rest import Client
from tts_engine import generar_audio
from git import Repo

# Config
load_dotenv()
twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
client = Client(twilio_sid, twilio_token)

drivers_df = pd.read_excel("drivers.xlsx")

print("Enter Load Information:")
pickup = input("Pickup Location: ")
delivery = input("Delivery Location: ")
window_time = input("Delivery Window Time: ")
miles = input("Total Miles: ")
actual_payment = input("Actual Payment: ")
max_payment = input("Maximum Payment: ")

# Git auto-commit
def commit_audio(filepath):
    repo = Repo(".")
    repo.git.add(filepath)
    repo.index.commit(f"Add audio {filepath}")
    origin = repo.remote(name='origin')
    origin.push()
    print(f"✅ Subido a GitHub: {filepath}")

# Script estático
def generar_script(driver_name, vehicle_type):
    return (
        f"Hello {driver_name}, this is a quick load offer for your {vehicle_type}."
        f"The pickup is in {pickup} and the delivery is in {delivery}."
        f"The window for delivery is {window_time}, and it’s about {miles} miles."
        f"We are offering ${actual_payment}, but it is negotiable up to ${max_payment}."
        f"If oyu are interested please say Yes, otherwise say No. Thanks!"
    )

# Loop de llamadas
for index, row in drivers_df.iterrows():
    name = row['Name']
    phone = row['Phone']
    vehicle = row['Vehicle']
    filename = f"{name.lower().replace(' ', '_')}_{pickup.lower()}_{delivery.lower()}"

    print(f"\n🎙️ Generando audio para {name}...")
    texto = generar_script(name, vehicle)
    audio_path = generar_audio(filename, texto)

    commit_audio(audio_path)

    audio_url = f"https://gpt-audio-bot.onrender.com/audio/{filename}.mp3"

    print(f"📞 Llamando a {name} con audio: {audio_url}")
    call = client.calls.create(
        twiml=f'<Response><Play>{audio_url}</Play></Response>',
        to=phone,
        from_=twilio_number
    )
    print(f"📲 Llamada enviada a {name}, SID: {call.sid}")
