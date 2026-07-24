import os
import time

from dotenv import load_dotenv
from flask import Flask, request

load_dotenv()

from memory import add_message, get_conversation
from openai_client import generate_ai_response
from messenger import (
    send_message,
    send_button_message,
    send_postback_buttons
)


app = Flask(__name__)


VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")


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





            # =================================
            # BUTOANE MESSENGER
            # =================================


            if postback:


                payload = postback.get("payload")


                print("📌 Postback primit:", payload)




                if payload == "GET_STARTED":


                    send_message(
                        sender_id,
                        "Bună ziua! Sunt Asistentul Virtual al Dr. Daniela Matei.\n\n"
                        "Vă pot ajuta cu informații despre programări, servicii medicale "
                        "și întrebări generale despre sănătatea feminină."
                    )


                    continue





                # PROGRAMARE

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
                    # CONTINUARE PARTEA 2/3


                # SERVICII

                if payload == "SERVICII":


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





                if payload == "CATEGORIE_CONSULTATII":


                    send_message(
                        sender_id,
                        "Consultații disponibile:\n\n"
                        "👩‍⚕️ Consultație ginecologică\n"
                        "🤰 Consultație de sarcină\n"
                        "🤰 Monitorizare sarcină\n\n"
                        "Pentru programare puteți alege una dintre platformele disponibile."
                    )


                    continue





                if payload == "CATEGORIE_INVESTIGATII":


                    send_message(
                        sender_id,
                        "Investigații disponibile:\n\n"
                        "🔍 Ecografie transvaginală\n"
                        "🔍 Ecografie obstetricală\n"
                        "🧪 Test Babeș-Papanicolau\n\n"
                        "Pentru detalii și programare vă pot ajuta cu platformele disponibile."
                    )


                    continue





                if payload == "CATEGORIE_CONTRACEPTIE":


                    send_message(
                        sender_id,
                        "Servicii pentru sănătatea feminină:\n\n"
                        "💊 Consiliere contraceptivă\n"
                        "🩺 Inserare sterilet\n"
                        "🌸 Consultații pentru menopauză\n\n"
                        "Pentru recomandări personalizate este necesară o consultație medicală."
                    )


                    continue





                # INTREBARE

                if payload == "INTREBARE":


                    send_message(
                        sender_id,
                        "Sigur, vă pot ajuta cu informații generale despre sănătatea feminină.\n\n"
                        "Puteți întreba, de exemplu:\n\n"
                        "• Ce presupune o consultație ginecologică?\n"
                        "• Am dureri abdominale, ce ar trebui să fac?\n"
                        "• Ce investigații sunt recomandate în sarcină?\n"
                        "• Cum mă pot programa la Dr. Daniela Matei?"
                    )


                    continue






            # =================================
            # MESAJ TEXT NORMAL
            # =================================


            user_text = message.get("text")



            if not user_text:

                continue



            user_text_lower = user_text.lower()



            # =================================
            # DETECTARE PROGRAMARE
            # =================================


            programare_keywords = [
                "programare",
                "programez",
                "vreau la medic",
                "vreau consultație",
                "vreau consultatie",
                "cum mă programez",
                "cum ma programez",
                "aș vrea o consultație",
                "as vrea o consultatie"
            ]



            if any(
                keyword in user_text_lower
                for keyword in programare_keywords
            ):


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
                # CONTINUARE PARTEA 3/3


            # =================================
            # DETECTARE UNDE CONSULTĂ MEDICUL
            # =================================


            locatie_keywords = [
                "unde consultă",
                "unde consulta",
                "unde o găsesc",
                "unde o gasesc",
                "unde lucrează",
                "unde lucreaza",
                "la ce clinică",
                "la ce clinica",
                "unde este cabinetul",
                "unde face consultații",
                "unde face consultatii",
                "locatie",
                "locație"
            ]



            if any(
                keyword in user_text_lower
                for keyword in locatie_keywords
            ):


                send_button_message(
                    sender_id,
                    "Dr. Daniela Matei oferă consultații prin următoarele platforme:",
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





            # =================================
            # OPENAI
            # =================================


            try:


                print(f"👤 Mesaj utilizator: {user_text}")



                add_message(
                    sender_id,
                    "user",
                    user_text
                )



                conversation = get_conversation(sender_id)



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
        debug=True
    )