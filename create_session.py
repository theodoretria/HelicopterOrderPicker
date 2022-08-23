import telethon
from telethon.sessions import StringSession

api_id = 12503964
api_hash = '7f6f3c9d695c8f1697d69f2466216d42'

with telethon.TelegramClient(StringSession(), api_id, api_hash) as client:
    session_string = client.session.save()

with open('session.txt', 'w') as f:
    f.write(session_string)