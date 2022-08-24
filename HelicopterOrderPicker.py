import telethon
from telethon.sessions import StringSession
from telethon import events
import os
from time import time
import shutil
import re
import asyncio


async def main():
    api_id = 12503964
    api_hash = '7f6f3c9d695c8f1697d69f2466216d42'

    with open('session.txt', 'r') as f:
        string_session = f.read()

    client = telethon.TelegramClient(StringSession(string_session), api_id, api_hash)
    me = client.get_me()
    await client.start()
    helicopter_order_picker_id = -1001611765239
    svolota_id = -1001762078325
    helicopter_id = '@RunAsHelicopter'
    helicopter_message_templates = [
        'статистика', 'теорвер', 'матстат',
        'ймовірністні', 'статистика',
        'python', 'вероятности',
        'ймовірності', 'ймовирности',
        'теор вер', 'мат стат', 'ймовірностей'
    ]
    messages_dir = 'messages'

    try:
        os.mkdir(messages_dir)
    except FileExistsError:
        pass

    async def save_messages(client, message):
        for dir_path in os.listdir(messages_dir):
            delete_old_messages(os.path.join(messages_dir, dir_path))

        dir_name = f'{message.id}'
        dir_path = os.path.join(messages_dir, dir_name)
        os.mkdir(dir_path)
        await client.download_media(message, os.path.join(dir_path, f'media_{message.id}'))
        with open(os.path.join(dir_path, f'message_{message.id}.txt', ), 'w', encoding="utf-8") as f:
            f.write(f'{message.peer_id}: {message.message}')

    def find_deleted_message(deleted_id):
        for message_dir in os.listdir(messages_dir):

            if int(message_dir) == deleted_id:
                message_dir_path = os.path.join(messages_dir, message_dir)
                if len(os.listdir(message_dir_path)) >= 2:
                    media, message = os.listdir(message_dir_path)
                    return os.path.join(message_dir_path, media), os.path.join(message_dir_path, message)
                else:
                    return None, os.path.join(message_dir_path, os.listdir(message_dir_path)[0])
        return None, None

    def is_message_for_me(message, templtate):
        return any([re.search(template, message.lower()) for template in helicopter_message_templates])

    def delete_old_messages(dir_path):
        dir_time = os.path.getmtime(dir_path)
        life_time_min = int((time() - dir_time) / 60)
        if life_time_min > 60:
            shutil.rmtree(dir_path)

    @client.on(events.NewMessage())
    async def save_message_handler(event: telethon.events.newmessage.NewMessage.Event):

        await save_messages(client, event.message)

    @client.on(events.MessageDeleted())
    async def send_deleted_message(event: telethon.events.MessageDeleted.Event):
        # await client.send_message('me', event)
        media, message = find_deleted_message(event.deleted_id)
        try:
            if message:
                with open(message, 'r', encoding="utf-8") as f:
                    await client.send_message(svolota_id, f.read())
        except:
            pass
        if media:
            await client.send_file(svolota_id, media)

    @client.on(events.NewMessage(
        chats=[helicopter_id], func=lambda e: is_message_for_me(e.message.message, helicopter_message_templates)))
    async def helicopter_order_handler(event: telethon.events.newmessage.NewMessage.Event):
        # await client.send_message(helicopter_order_picker_id, event.message)
        await client.forward_messages(helicopter_order_picker_id, event.message)
    await client.run_until_disconnected()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()

