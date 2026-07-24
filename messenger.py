import os
import requests

from dotenv import load_dotenv

load_dotenv()


PAGE_ACCESS_TOKEN = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")

GRAPH_URL = "https://graph.facebook.com/v23.0"




def send_message(recipient_id, message_text):
    """
    Trimite mesaj text către utilizator în Messenger.
    """

    url = f"{GRAPH_URL}/me/messages"

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


    response = requests.post(
        url,
        params=params,
        json=payload,
        timeout=30
    )


    print(
        "📨 Messenger:",
        response.status_code,
        response.text
    )


    response.raise_for_status()





def send_button_message(recipient_id, text, buttons):
    """
    Trimite mesaj Messenger cu butoane URL.
    """

    url = f"{GRAPH_URL}/me/messages"

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
    Trimite mesaj Messenger cu butoane interne postback.
    """

    url = f"{GRAPH_URL}/me/messages"

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
        "🔘 Postback Buttons:",
        response.status_code,
        response.text
    )


    response.raise_for_status()





def send_programare_postback(recipient_id):
    """
    Trimite buton pentru programare.
    """

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
    """
    Configurează butonul Începe din Messenger.
    """

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
    """
    Configurează meniul permanent Messenger.
    """


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