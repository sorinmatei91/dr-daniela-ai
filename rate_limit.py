import time


MESSAGE_LIMIT = 20

WINDOW_SECONDS = 24 * 60 * 60


user_messages = {}



def can_use_ai(user_id):

    now = time.time()


    if user_id not in user_messages:

        user_messages[user_id] = []


    # eliminăm mesajele mai vechi de 24 ore

    user_messages[user_id] = [
        timestamp
        for timestamp in user_messages[user_id]
        if now - timestamp < WINDOW_SECONDS
    ]


    print(
        "🔒 RATE LIMIT:",
        user_id,
        "mesaje AI în ultimele 24h:",
        len(user_messages[user_id])
    )


    if len(user_messages[user_id]) >= MESSAGE_LIMIT:

        print(
            "⛔ LIMITA ATINSA pentru:",
            user_id
        )

        return False


    user_messages[user_id].append(now)


    print(
        "✅ Permis OpenAI pentru:",
        user_id
    )


    return True