from rubpy import Client, filters
from rubpy.types import Updates
from PIL import Image
from io import BytesIO

bot = Client('bot')

@bot.on_message_updates(filters.is_group, filters.Commands(['rgb', 'RGB']))
def make_image(update: Updates):
    color: str = update.command[-1]
    color = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
    image = Image.new('RGB', (10, 10))
    buffer = BytesIO()

    for y in range(10):
        for x in range(10):
            image.putpixel((x, y), color)

    image.save(buffer, 'PNG')
    return update.reply_photo(buffer.getvalue(), file_name='image.png')

bot.run()
