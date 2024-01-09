from rubpy import Client, filters, Rubino
from rubpy.types import Updates

bot = Client('bot')
rubino = Rubino(client=bot)

@bot.on_message_updates(filters.text)
async def updates(update: Updates):
    text: str = update.raw_text

    if text.startswith('https://rubika.ir/post/'):
        post = await rubino.get_post_by_share_link(text)
        if post.has_access:
            post = post.post
            if post.file_type == 'Video':
                #await update.reaction(1)
                await bot.send_video(update.object_guid,
                                     video=post.full_file_url,
                                     reply_to_message_id=update.message_id)
            elif post.file_type == 'Picture':
                #await update.send_activity('Uploading')
                #await update.reaction(1)
                await bot.send_photo(update.object_guid,
                                     photo=post.full_file_url,
                                     reply_to_message_id=update.message_id)

bot.run()
