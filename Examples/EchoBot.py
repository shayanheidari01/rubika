from rubpy import Client

app = Client('auth')

@app.handler
async def EchoBot(bot, message):
    if await message.of_user():
        if await message.is_text:
            await message.reply(
                await message.text()
            )


# If a new message is received and the message is of text type
# Copies the textual content of that message and replies to the same message again
