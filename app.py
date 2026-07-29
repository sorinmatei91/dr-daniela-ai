import os
import time

from dotenv import load_dotenv
from flask import Flask, request

load_dotenv()


from memory import add_message, get_conversation
from openai_client import generate_ai_response
from rate_limit import can_use_ai


from messenger import (
    send_message,
    send_button_message,
    send_postback_buttons,
    send_programare_postback
)


from intents import (
    detect_programare,
    detect_locatie,
    detect_servicii,
    detect_urgent_symptoms
)


app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return {
        "status": "ok",
        "service": "Dr Daniela AI Messenger Bot"
    }, 200


VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")


with open("system_prompt.txt", "r", encoding="utf-8") as file:
    SYSTEM_PROMPT = file.read()


with open("knowledge/cabinet.txt", "r", encoding="utf-8") as file:
    CABINET_INFO = file.read()



@app.get("/")
def home():

    return "Asistentul Dr. Daniela Matei este pornit."



@app.get("/webhook")
def verify_webhook():

    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")


    if mode == "subscribe" and token == VERIFY_TOKEN:

        print("Webhook verificat cu succes.")

        return challenge, 200


    return "Verificare eșuată.", 403
@app.post("/webhook")
def receive_message():

    total_start = time.perf_counter()


    data = request.get_json(silent=True) or {}


    print("\n==============================")
    print("Mesaj primit de la Meta:")
    print(data)
    print("==============================")


    if data.get("object") != "page":

        return "EVENT_RECEIVED", 200



    for entry in data.get("entry", []):

        for event in entry.get("messaging", []):


            sender_id = event.get("sender", {}).get("id")


            message = event.get("message", {})


            postback = event.get("postback")



            if message.get("is_echo"):

                continue



            if not sender_id:

                continue




            # ==============================
            # BUTOANE MESSENGER
            # ==============================


            if postback:


                payload = postback.get("payload")


                print("📌 Postback primit:", payload)



                if payload == "GET_STARTED":


                    send_postback_buttons(
                        sender_id,
                        "Bună ziua! Sunt Asistentul Virtual al Dr. Daniela Matei.\n\n",
                                [
            {
                "type": "postback",
                "title": "📅 Programare consultație",
                "payload": "PROGRAMARE"
            },
            {
                "type": "postback",
                "title": "👩‍⚕️ Servicii medicale",
                "payload": "SERVICII"
            },
            {
                "type": "postback",
                "title": "💬 Pune o întrebare",
                "payload": "INTREBARE"
            }
        ]
    
                    )


                    continue





                if payload == "PROGRAMARE":


                    send_button_message(
                        sender_id,
                        "Pentru programare la Dr. Daniela Matei, alegeți platforma dorită:",
                        [
                            {
                                "type": "web_url",
                                "url": "https://www.gralmedical.ro/medici/daniela-cosmina-matei",
                                "title": "🏥 GRAL Medical"
                            },
                            {
                                "type": "web_url",
                                "url": "https://www.reginamaria.ro/medici/dr-matei-daniela-cosmina",
                                "title": "🏥 Regina Maria"
                            },
                            {
                                "type": "web_url",
                                "url": "https://www.medic.chat/doctors/gch6So2Aas4zsHE79",
                                "title": "💻 Medic Chat"
                            }
                        ]
                    )


                    continue



                if payload == "CATEGORIE_CONSULTATII":


                    send_message(
                        sender_id,
                        "Consultații disponibile:\n\n"
                        "👩‍⚕️ Consultație ginecologică\n"
                        "🤰 Consultație de sarcină\n"
                        "🤰 Monitorizare sarcină"
                    )


                    send_programare_postback(sender_id)


                    continue





                if payload == "CATEGORIE_INVESTIGATII":


                    send_message(
                        sender_id,
                        "Investigații disponibile:\n\n"
                        "🔍 Ecografie transvaginală\n"
                        "🔍 Ecografie obstetricală\n"
                        "🧪 Test Babeș-Papanicolau"
                    )


                    send_programare_postback(sender_id)


                    continue





                if payload == "CATEGORIE_CONTRACEPTIE":


                    send_message(
                        sender_id,
                        "Servicii pentru sănătatea feminină:\n\n"
                        "💊 Consiliere contraceptivă\n"
                        "🩺 Inserare sterilet\n"
                        "🌸 Consultații pentru menopauză"
                    )


                    send_programare_postback(sender_id)


                    continue
                

            # ==============================
            # MESAJ TEXT NORMAL
            # ==============================


            user_text = message.get("text")



            if not user_text:

                continue
                        # ==============================
            # RASPUNSURI SIMPLE FARA AI
            # ==============================

            simple_messages = {

                "salut":
                "Bună ziua! Sunt Asistentul Virtual al Dr. Daniela Matei. Vă pot ajuta cu informații despre servicii medicale, programări și întrebări generale despre sănătatea feminină.",

                "buna":
                "Bună ziua! Sunt Asistentul Virtual al Dr. Daniela Matei. Vă pot ajuta cu informații despre servicii medicale, programări și întrebări generale despre sănătatea feminină.",

                "bună":
                "Bună ziua! Sunt Asistentul Virtual al Dr. Daniela Matei. Vă pot ajuta cu informații despre servicii medicale, programări și întrebări generale despre sănătatea feminină.",

                "multumesc":
                "Cu drag! Dacă aveți întrebări despre servicii medicale sau programări, vă pot ajuta.",

                "mulțumesc":
                "Cu drag! Dacă aveți întrebări despre servicii medicale sau programări, vă pot ajuta.",

                "mersi":
                "Cu drag! Sunt aici dacă aveți nevoie de informații despre consultații sau programări.",

                "ok":
                "Dacă aveți nevoie de alte informații despre serviciile Dr. Daniela Matei, vă pot ajuta."
            }


            if user_text.lower().strip() in simple_messages:


                send_message(
                    sender_id,
                    simple_messages[user_text.lower().strip()]
                )


                continue



            user_text_lower = user_text.lower()



            # ==============================
            # PROGRAMARE
            # ==============================


            if detect_programare(user_text):


                send_button_message(
                    sender_id,
                    "Pentru programare la Dr. Daniela Matei, alegeți platforma dorită:",
                    [
                        {
                            "type": "web_url",
                            "url": "https://www.gralmedical.ro/medici/daniela-cosmina-matei",
                            "title": "🏥 GRAL Medical"
                        },
                        {
                            "type": "web_url",
                            "url": "https://www.reginamaria.ro/medici/dr-matei-daniela-cosmina",
                            "title": "🏥 Regina Maria"
                        },
                        {
                            "type": "web_url",
                            "url": "https://www.medic.chat/doctors/gch6So2Aas4zsHE79",
                            "title": "💻 Medic Chat"
                        }
                    ]
                )


                continue





            # ==============================
            # SIMPTOME URGENTE
            # ==============================


            if detect_urgent_symptoms(user_text):


                add_message(
                    sender_id,
                    "user",
                    user_text
                )


                conversation = get_conversation(sender_id)
                if not can_use_ai(sender_id):

                    send_message(
                        sender_id,
                        "Vă mulțumesc pentru mesaj. Pentru a putea ajuta cât mai multe persoane, conversația automată are o limită temporară. Pentru programări sau informații suplimentare puteți folosi opțiunile disponibile."
                    )

                    continue


                print(
                    f"🧠 Mesaje trimise către OpenAI: {len(conversation)}"
                )


                ai_response = generate_ai_response(
                    SYSTEM_PROMPT
                    + "\n\nINFORMAȚII CABINET:\n"
                    + CABINET_INFO,
                    conversation
                )


                add_message(
                    sender_id,
                    "assistant",
                    ai_response
                )


                send_message(
                    sender_id,
                    ai_response
                )


                continue





            # ==============================
            # LOCATIE
            # ==============================


            if detect_locatie(user_text):


                send_message(
                    sender_id,
                    "Dr. Daniela Matei oferă consultații în locațiile disponibile prin platformele de programare."
                )


                send_programare_postback(sender_id)


                continue





            # ==============================
            # SERVICII
            # ==============================


            if detect_servicii(user_text):


                send_postback_buttons(
                    sender_id,
                    "Ce informații doriți despre serviciile medicale?",
                    [
                        {
                            "type": "postback",
                            "title": "🤰 Sarcină & consult",
                            "payload": "CATEGORIE_CONSULTATII"
                        },
                        {
                            "type": "postback",
                            "title": "🔍 Investigații",
                            "payload": "CATEGORIE_INVESTIGATII"
                        },
                        {
                            "type": "postback",
                            "title": "💊 Contracepție",
                            "payload": "CATEGORIE_CONTRACEPTIE"
                        }
                    ]
                )


                continue





            # ==============================
            # OPENAI
            # ==============================


            try:


                print(f"👤 Mesaj utilizator: {user_text}")


                add_message(
                    sender_id,
                    "user",
                    user_text
                )


                conversation = get_conversation(sender_id)

                if not can_use_ai(sender_id):

                    send_message(
        sender_id,
        "Vă mulțumesc pentru mesaj. Pentru a putea ajuta cât mai multe persoane, conversația automată are o limită temporară. Pentru programare sau informații suplimentare puteți folosi opțiunile disponibile."
    )
                    continue
       

                print(
                    f"🧠 Mesaje trimise către OpenAI: {len(conversation)}"
                )


                openai_start = time.perf_counter()


                ai_response = generate_ai_response(
                    SYSTEM_PROMPT
                    + "\n\nINFORMAȚII CABINET:\n"
                    + CABINET_INFO,
                    conversation
                )


                openai_duration = time.perf_counter() - openai_start


                print(
                    f"🤖 OpenAI: {openai_duration:.2f} sec"
                )


                add_message(
                    sender_id,
                    "assistant",
                    ai_response
                )


                send_message(
                    sender_id,
                    ai_response
                )


                total_duration = time.perf_counter() - total_start


                print(
                    f"⏱️ Total: {total_duration:.2f} sec"
                )


                print("==============================\n")



            except Exception as error:


                print(
                    f"❌ Eroare {type(error).__name__}: {error}"
                )


                send_message(
                    sender_id,
                    "Îmi pare rău, momentan nu pot răspunde. Vă rog să încercați din nou."
                )



    return "EVENT_RECEIVED", 200





if __name__ == "__main__":


    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )