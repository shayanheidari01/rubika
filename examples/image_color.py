from rubpy import Client, filters
from rubpy.types import Updates
from PIL import Image
from io import BytesIO

bot = Client('bot')

@bot.on_message_updates(filters.is_group, filters.Commands(['rgb', 'RGB']))
def make_image(update: Updates):
    try:
        hex_color = update.command[-1]
        if not hex_color.startswith('#') or len(hex_color) != 7:
            return update.reply("فرمت رنگ اشتباه است. مثال: #ff5733")

        # تبدیل رنگ به RGB
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))

        # ساخت تصویر با رنگ موردنظر
        image = Image.new('RGB', (10, 10), color=rgb)
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        buffer.seek(0)

        return update.reply_photo(buffer.read(), file_name='color.png')

    except Exception as e:
        return update.reply(f"خطا در پردازش رنگ: {e}")

bot.run()
