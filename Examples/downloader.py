from rubpy import Client, Methods, Message

app = Client(
    auth='auth-key',
    account_guid='account_guid',
)

@app.handler
async def Downloader(bot: Methods, message: Message):
    if await message.of_group() and await message.is_text():
        text = await message.text()
        if text == 'دانلود':
            message_options = await message.show()
            message_options = message_options.get('message')
            if 'reply_to_message_id' in message_options.keys():
                check = await bot.download(
                    object_guid=await message.chat_id(),
                    message_id=message_options.get('reply_to_message_id'),
                    save=True,
                )
                if check:
                    await message.reply('فایل مورد نظر دانلود شد.')
                else:
                    await message.reply('خطایی رخ داد!')
            else:
                await message.reply('لطفا روی یک فایل ریپلای بزنید!')
