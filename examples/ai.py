"""
this source code is just a sample for rubpy.BotClient
You can edit the source code whenever you want.
"""

import aiohttp
from rubpy import BotClient
from rubpy.bot import filters
from rubpy.bot.models import Update, Keypad, KeypadRow, Button
from rubpy.bot.enums import ChatKeypadTypeEnum

bot = BotClient(
    token='your-bot-token'
)

@bot.on_update(filters.commands('start'))
async def handle_start(bot, update: Update):
    keypad = Keypad(
            rows=[
                KeypadRow(buttons=[
                    Button(id="1", type="Simple", button_text="گفتگو با هوش مصنوعی ✨")
                ]),
                KeypadRow(buttons=[
                    Button(id="2", type="Simple", button_text="تولید تصویر 🌌"),
                    Button(id="3", type="Simple", button_text="پاکسازی حافظه 🗑")
                ])
            ],
            resize_keyboard=True,
            on_time_keyboard=False
        )

    await update.reply('سلام! خوش اومدی. از دکمه های زیر برای برای کار با ربات استفاده کن:',
                       chat_keypad=keypad, chat_keypad_type=ChatKeypadTypeEnum.NEW)

@bot.on_update(filters.text("گفتگو با هوش مصنوعی ✨"))
async def handle_ai(bot, update: Update):
    await update.reply('سوال یا موضوعی که میخوای در موردش باهام صحبت کنی رو بفرست ✨')

@bot.on_update(filters.text("تولید تصویر 🌌"))
async def handle_ai(bot, update: Update):
    keypad = Keypad(
            rows=[
                KeypadRow(buttons=[
                    Button(id="1", type="Simple", button_text="در حال به روزرسانی ⚠")
                ])
            ],
            resize_keyboard=True,
            on_time_keyboard=False
        )
    await update.reply('این بخش در حال به روزرسانی است.', inline_keypad=keypad)

@bot.on_update(filters.text("پاکسازی حافظه 🗑"))
async def handle_ai(bot, update: Update):
    keypad = Keypad(
            rows=[
                KeypadRow(buttons=[
                    Button(id="1", type="Simple", button_text="در حال به روزرسانی ⚠")
                ])
            ],
            resize_keyboard=True,
            on_time_keyboard=False
        )
    await update.reply('این بخش در حال به روزرسانی است.', inline_keypad=keypad)

@bot.on_update()
async def handle_ai(bot, update: Update):
    if update.new_message and update.new_message.text:
        if update.new_message.text not in ["پاکسازی حافظه 🗑", "تولید تصویر 🌌",
                                           "/start", "گفتگو با هوش مصنوعی ✨"]:
            
            msg = await update.reply('لطفا کمی صبر کنید...')
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get('https://shython-apis.liara.run/ai', params={'prompt': update.new_message.text}) as resp:
                        if resp.ok:
                            resp = await resp.json()
                
                await msg.edit_text(resp['data'])
            
            except Exception:
                await update.reply('⚠ خطایی رخ داد، مجددا تلاش کنید.')

bot.run() # You can set webhook on bot.run
