from rubpy import Client

app = Client(
    auth='auth-key',
    account_guid='account-object-guid'
)

@app.MessageUpdates
async def Downloader(bot, message):
    if await message.of_group() and await message.is_text():
        text = await message.text()
        if text.startswith('دانلود'):
            message_info = await message.show()
            message_info = message_info.get('message')
            if 'reply_to_message_id' in message_info.keys():
                print(await message.show())
                await bot.download(
                    object_guid=await message.chat_id(),
                    message_id=message_info.get('message_id'),
                    save=True
                )
                await message.reply('فایل مورد نظر دانلود و ذخیره شد')
            else:
                await message.reply('لطفا روی یک فایل ریپلای بزنید')
