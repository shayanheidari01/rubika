import asyncio

from rubpy import BotClient
from rubpy.bot.enums import ChatKeypadTypeEnum
from rubpy.bot.models.button import Button
from rubpy.bot.models.keypad import Keypad
from rubpy.bot.models.keypad_row import KeypadRow

async def main():
    # مقدار توکن را از متغیر محیطی یا مقداردهی مستقیم بگیرید
    token = "your-bot-token"
    chat_id = "chat-id"  # شناسه چتی که می‌خواهید تست کنید

    client = BotClient(token=token, rate_limit=0.3, use_webhook=False)

    try:
        upload_file_result = await client.send_file(chat_id, file=r"C:\Users\ASUS\Downloads\file.zip", text='hello')
        print("✅ send file:", upload_file_result)
    except Exception as e:
        print("❌ send file:", e)

    try:
        upload_file_result = await client.send_file(chat_id, file_id=upload_file_result.file_id)
        print("✅ send file:", upload_file_result)
    except Exception as e:
        print("❌ send file:", e)

    try:
        upload_file_result = await client.send_file(chat_id, file=r"C:\Users\ASUS\Pictures\favicon.png", type='Image')
        print("✅ send image file:", upload_file_result)
    except Exception as e:
        print("❌ send image file:", e)

    try:
        updates = await client.get_updates(limit=5)
        print("✅ get_updates:", updates)
    except Exception as e:
        print("❌ get_updates:", e)

    try:
        me = await client.get_me()
        print("✅ get_me:", me)
    except Exception as e:
        print("❌ get_me:", e)

    try:
        commands = [
            {"command": "start", "description": "شروع"},
            {"command": "help", "description": "راهنما"}
        ]
        result = await client.set_commands(commands)
        print("✅ set_commands:", result)
    except Exception as e:
        print("❌ set_commands:", e)

    try:
        result = await client.get_chat(chat_id)
        print("✅ get_chat:", result)
    except Exception as e:
        print("❌ get_chat:", e)

    try:
        msg = await client.send_message(chat_id=chat_id, text="سلام از کتابخانه تستی!")
        print("✅ send_message:", msg)
        message_id = msg.message_id
        #await msg.delete()
    except Exception as e:
        print("❌ send_message:", e)
        message_id = None

    try:
        keypad = Keypad(
            rows=[
                KeypadRow(buttons=[
                    Button(id="1", type="Simple", button_text="دکمه ۱")
                ]),
                KeypadRow(buttons=[
                    Button(id="2", type="Simple", button_text="دکمه ۲"),
                    Button(id="3", type="Simple", button_text="دکمه ۳")
                ])
            ],
            resize_keyboard=True,
            on_time_keyboard=False
        )
        msg_keypad = await client.send_message(
            chat_id=chat_id,
            text="پیام با کیبورد",
            chat_keypad=keypad,
            chat_keypad_type=ChatKeypadTypeEnum.NEW
        )
        print("✅ send_message with keypad:", msg_keypad)
    except Exception as e:
        print("❌ send_message with keypad:", e)

    try:
        poll = await client.send_poll(chat_id=chat_id, question="پرسش تستی؟", options=["بله", "خیر"])
        print("✅ send_poll:", poll)
    except Exception as e:
        print("❌ send_poll:", e)

    try:
        loc = await client.send_location(chat_id=chat_id, latitude="35.7", longitude="51.4")
        print("✅ send_location:", loc)
    except Exception as e:
        print("❌ send_location:", e)

    try:
        contact = await client.send_contact(chat_id=chat_id, first_name="علی", last_name="اکبری", phone_number="09120000000")
        print("✅ send_contact:", contact)
    except Exception as e:
        print("❌ send_contact:", e)

    try:
        if message_id:
            edited = await client.edit_message_text(chat_id=chat_id, message_id=message_id, text="پیام ویرایش شده!")
            print("✅ edit_message_text:", edited)
    except Exception as e:
        print("❌ edit_message_text:", e)

    try:
        if message_id:
            keypad_edit = Keypad(
                rows=[
                    KeypadRow(buttons=[Button(id="a", type="Simple", button_text="ویرایش شد")])
                ],
                resize_keyboard=True,
                on_time_keyboard=False
            )
            edit_keypad = await client.edit_message_keypad(chat_id=chat_id, message_id=message_id, inline_keypad=keypad_edit)
            print("✅ edit_message_keypad:", edit_keypad)
    except Exception as e:
        print("❌ edit_message_keypad:", e)


    try:
        fwd = await client.forward_message(from_chat_id=chat_id, message_id=message_id, to_chat_id=chat_id)
        print("✅ forward_message:", fwd)
    except Exception as e:
        print("❌ forward_message:", e)
    
    try:
        if message_id:
            deleted = await client.delete_message(chat_id=chat_id, message_id=message_id)
            print("✅ delete_message:", deleted)
    except Exception as e:
        print("❌ delete_message:", e)

    try:
        edit_kp = await client.edit_chat_keypad(chat_id=chat_id, keypad_type=ChatKeypadTypeEnum.REMOVE)
        print("✅ edit_chat_keypad (remove):", edit_kp)
    except Exception as e:
        print("❌ edit_chat_keypad (remove):", e)

    try:
        url = "https://yourdomain.com/rubika-webhook"
        for t in ["ReceiveUpdate", "ReceiveInlineMessage"]:
            res = await client.update_bot_endpoints(url=url, endpoint_type=t)
            print(f"✅ update_bot_endpoints ({t}):", res)
    except Exception as e:
        print("❌ update_bot_endpoints:", e)

    await client.session.close()

if __name__ == "__main__":
    asyncio.run(main())