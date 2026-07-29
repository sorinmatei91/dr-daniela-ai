import os
import requests

from dotenv import load_dotenv

load_dotenv()


PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")


if PAGE_ACCESS_TOKEN:
    print("✅ FACEBOOK TOKEN LOADED:", PAGE_ACCESS_TOKEN[:20])
else:
    print("❌ PAGE_ACCESS_TOKEN LIPSEȘTE")


if INSTAGRAM_ACCESS_TOKEN:
    print("✅ INSTAGRAM TOKEN LOADED:", INSTAGRAM_ACCESS_TOKEN[:20])
else:
    print("❌ INSTAGRAM_ACCESS_TOKEN LIPSEȘTE")


GRAPH_URL = "https://graph.facebook.com/v25.0"
FACEBOOK_PAGE_ID = "1103317229542953"


def send_message(recipient_id, message_text):
    """
    Trimite mesaj text către utilizator în Facebook Messenger.
    """

    if not PAGE_ACCESS_TOKEN:
        print("❌ PAGE_ACCESS_TOKEN LIPSEȘTE")
        return

    url = f"{GRAPH_URL}/{FACEBOOK_PAGE_ID}/messages"

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
    )

    if response.status_code != 200:
        print("❌ FACEBOOK ERROR:")
        print(response.text)
        return

    response.raise_for_status()


def send_instagram_message(recipient_id, message_text):
    """
    Trimite mesaj text către utilizator în Instagram.
    """

    if not INSTAGRAM_ACCESS_TOKEN:
        print("❌ INSTAGRAM_ACCESS_TOKEN LIPSEȘTE")
        return

    if not recipient_id:
        print("❌ RECIPIENT ID LIPSEȘTE")
        return

    url = "https://graph.instagram.com/v24.0/me/messages"

    headers = {
        "Authorization": f"Bearer {INSTAGRAM_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "recipient": {
            "id": str(recipient_id),
        },
        "message": {
            "text": message_text,
        },
    }

    print("📤 TRIMIT MESAJ INSTAGRAM")
    print("Recipient:", recipient_id)
    print("Text:", message_text)
    print("Token încărcat:", bool(INSTAGRAM_ACCESS_TOKEN))
    print("Lungime token:", len(INSTAGRAM_ACCESS_TOKEN))

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30,
        )

        print(
            "📨 Instagram RESPONSE:",
            response.status_code,
            response.text,
        )

        if response.status_code != 200:
            print("❌ INSTAGRAM ERROR:")
            print(response.text)
            return

        response.raise_for_status()
        print("✅ Mesaj Instagram trimis cu succes")

    except requests.exceptions.Timeout:
        print("❌ Instagram request timeout")

    except requests.exceptions.RequestException as error:
        print("❌ Instagram request error:", error)
        
def send_button_message(recipient_id, text, buttons):
    """
    Trimite mesaj Facebook Messenger cu butoane URL.
    """

    if not PAGE_ACCESS_TOKEN:
        print("❌ PAGE_ACCESS_TOKEN LIPSEȘTE")
        return

    url = f"{GRAPH_URL}/{FACEBOOK_PAGE_ID}/messages"

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

    if response.status_code != 200:
        print("❌ FACEBOOK BUTTON ERROR:")
        print(response.text)
        return

    response.raise_for_status()


def send_postback_buttons(recipient_id, text, buttons):
    """
    Trimite mesaj Facebook Messenger cu butoane postback.
    """

    if not PAGE_ACCESS_TOKEN:
        print("❌ PAGE_ACCESS_TOKEN LIPSEȘTE")
        return

    url = f"{GRAPH_URL}/{FACEBOOK_PAGE_ID}/messages"

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

    if response.status_code != 200:
        print("❌ FACEBOOK POSTBACK ERROR:")
        print(response.text)
        return

    response.raise_for_status()


def send_programare_postback(recipient_id):
    """
    Trimite butonul de programare în Facebook Messenger.
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
    Configurează butonul Get Started pentru Facebook Messenger.
    """

    if not PAGE_ACCESS_TOKEN:
        print("❌ PAGE_ACCESS_TOKEN LIPSEȘTE")
        return

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

    if response.status_code != 200:
        print("❌ GET STARTED ERROR:")
        print(response.text)
        return

    response.raise_for_status()


def setup_persistent_menu():
    """
    Configurează meniul permanent pentru Facebook Messenger.
    """

    if not PAGE_ACCESS_TOKEN:
        print("❌ PAGE_ACCESS_TOKEN LIPSEȘTE")
        return

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

    if response.status_code != 200:
        print("❌ PERSISTENT MENU ERROR:")
        print(response.text)
        return

    response.raise_for_status()


if __name__ == "__main__":
    print("Configurare Messenger...")

    setup_get_started()
    setup_persistent_menu()

    print("Gata.")