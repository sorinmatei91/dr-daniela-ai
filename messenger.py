import os
import requests

from dotenv import load_dotenv

load_dotenv()


PAGE_ACCESS_TOKEN = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")

if PAGE_ACCESS_TOKEN:
    print("✅ TOKEN LOADED:", PAGE_ACCESS_TOKEN[:20])
else:
    print("❌ FACEBOOK_PAGE_ACCESS_TOKEN LIPSESTE")


GRAPH_URL = "https://graph.facebook.com/v25.0"



def send_message(recipient_id, message_text):
    """
    Trimite mesaj text către utilizator în Messenger.
    """

    url = f"{GRAPH_URL}/1103317229542953/messages"

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }

    payload = {
        "recipient": {
            "id": recipient_id
        },
        "messaging_type": "RESPONSE",
        "message": {
            "text": message_text
        }
    }


    print("📤 TRIMIT MESAJ FACEBOOK")
    print("Recipient:", recipient_id)
    print("Text:", message_text)
    print("Token:", PAGE_ACCESS_TOKEN[:20] if PAGE_ACCESS_TOKEN else "LIPSESTE")


    response = requests.post(
        url,
        params=params,
        json=payload,
        timeout=30
    )


    print(
        "📨 Messenger RESPONSE:",
        response.status_code,
        response.text
    ),

    if response.status_code != 200:
        print("❌ FACEBOOK ERROR:")
        print(response.text)
        return


    response.raise_for_status()



def send_button_message(recipient_id, text, buttons):
    """
    Trimite Messenger cu butoane URL.
    """

    url = f"{GRAPH_URL}/1103317229542953/messages"

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }


    payload = {
        "recipient": {
            "id": recipient_id
        },
        "messaging_type": "RESPONSE",
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": text,
                    "buttons": buttons
                }
            }
        }
    }


    response = requests.post(
        url,
        params=params,
        json=payload,
        timeout=30
    )


    print(
        "🔘 Button Messenger:",
        response.status_code,
        response.text
    )


    response.raise_for_status()



def send_postback_buttons(recipient_id, text, buttons):
    """
    Trimite Messenger cu butoane postback.
    """

    url = f"{GRAPH_URL}/1103317229542953/messages"

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }


    payload = {
        "recipient": {
            "id": recipient_id
        },
        "messaging_type": "RESPONSE",
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": text,
                    "buttons": buttons
                }
            }
        }
    }


    response = requests.post(
        url,
        params=params,
        json=payload,
        timeout=30
    )


    print(
        "🔘 Postback Messenger:",
        response.status_code,
        response.text
    )


    response.raise_for_status()



def send_programare_postback(recipient_id):

    send_postback_buttons(
        recipient_id,
        "Doriți să faceți o programare la Dr. Daniela Matei?",
        [
            {
                "type": "postback",
                "title": "📅 Vreau programare",
                "payload": "PROGRAMARE"
            }
        ]
    )



def setup_get_started():

    url = f"{GRAPH_URL}/me/messenger_profile"

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }


    payload = {
        "get_started": {
            "payload": "GET_STARTED"
        }
    }


    response = requests.post(
        url,
        params=params,
        json=payload,
        timeout=30
    )


    print(
        "🚀 Get Started:",
        response.status_code,
        response.text
    )


    response.raise_for_status()



def setup_persistent_menu():

    url = f"{GRAPH_URL}/me/messenger_profile"


    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }


    payload = {
        "persistent_menu": [
            {
                "locale": "default",
                "composer_input_disabled": False,
                "call_to_actions": [
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
            }
        ]
    }


    response = requests.post(
        url,
        params=params,
        json=payload,
        timeout=30
    )


    print(
        "📋 Persistent Menu:",
        response.status_code,
        response.text
    )


    response.raise_for_status()



if __name__ == "__main__":

    print("Configurare Messenger...")

    setup_get_started()
    setup_persistent_menu()

    print("Gata.")