from rubpy.bot import BotClient, filters
from rubpy.bot.models import Update

import os

app = BotClient(
    token="EDAAE0AXRKFAPTDLQRPPHHLBTQBCMRPRJIYFLTNSVGHLIRIJWLBECCIZCFAIJSSI")

GROUP_CHAT_IDS = ["g0GNTBv0f1cc3c3e479408a231e3d7f5"]
ADMIN_SENDER_ID = "u0IYdTF0909d724592ee14b7784d29ce"


@app.middleware()
async def logger(bot, update, call_next):
    print("🔹 Update received:", update)
    await call_next()


@app.on_start()
async def hello(bot):
    print(await bot.get_me())
    print("Bot started!")


@app.on_update(filters.chat(GROUP_CHAT_IDS) & filters.photo)
async def group_handler(client: BotClient, update: Update):
    if update.new_message.sender_id == ADMIN_SENDER_ID:
        file = None
        try:
            file = await update.download(save_as="/tmp/image.jpg")
            await update.delete()
            await client.send_file(
                chat_id=update.chat_id,
                file=file,
                text=update.new_message.text,
                type="Image",
                reply_to_message_id=update.new_message.reply_to_message_id,
                metadata=update.new_message.metadata,
            )
        except Exception as e:
            print(e)
        finally:
            os.remove(file) if file else None


@app.on_update(filters.chat(GROUP_CHAT_IDS) & filters.text)
async def group_handler(client: BotClient, update: Update):
    if update.new_message.sender_id == ADMIN_SENDER_ID:
        try:
            await update.delete()
            await client.send_message(
                chat_id=update.chat_id,
                text=update.new_message.text,
                reply_to_message_id=update.new_message.reply_to_message_id,
                metadata=update.new_message.metadata,
            )
        except Exception as e:
            print(e)


app.run(
    webhook_url="https://rpgroup.liara.run",
    path="/",
    port=8000
)