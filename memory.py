MAX_MESSAGES = 6

conversations = {}


def get_conversation(user_id):
    return conversations.get(user_id, [])


def add_message(user_id, role, content):
    if user_id not in conversations:
        conversations[user_id] = []

    conversations[user_id].append(
        {
            "role": role,
            "content": content
        }
    )

    conversations[user_id] = conversations[user_id][-MAX_MESSAGES:]


def clear_conversation(user_id):
    conversations.pop(user_id, None)