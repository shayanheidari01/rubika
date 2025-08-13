"""
this source code is just a sample for rubpy.BotClient
You can edit the source code whenever you want.
"""

from rubpy import BotClient
from rubpy.bot import filters
from rubpy.bot.models import (
    ButtonLink,
    JoinChannelData,
    Update,
    Keypad,
    KeypadRow,
    Button,
)
from rubpy.bot.enums import ButtonLinkTypeEnum, ButtonTypeEnum

bot = BotClient(
    token="your-bot-token"
)


@bot.on_update(filters.commands("start"))
async def handle_start(bot, update: Update):
    keypad = Keypad(
        rows=[
            KeypadRow(
                buttons=[
                    Button(
                        id="1",
                        type=ButtonTypeEnum.LINK,
                        button_text="عضویت اجباری",
                        button_link=ButtonLink(
                            type=ButtonLinkTypeEnum.JoinChannel,
                            joinchannel_data=JoinChannelData(
                                username="rubikapy", ask_join=True
                            ),  # اگر ask_join برابر False باشد کاربر مستقیما بدون پرسش عضو کانال میشود.,
                        ),
                    )
                ]
            ),
            KeypadRow(
                buttons=[
                    Button(
                        id="2",
                        type=ButtonTypeEnum.LINK,
                        button_text="باز کردن لینک",
                        button_link=ButtonLink(
                            type=ButtonLinkTypeEnum.URL,
                            link_url="https://shayan-heidari.ir/",
                        ),
                    ),
                ]
            ),
        ],
        resize_keyboard=True,
        on_time_keyboard=False,
    )

    await update.reply(
        "سلام! خوش اومدی. از دکمه های زیر برای برای کار با ربات استفاده کن:",
        inline_keypad=keypad,
    )


bot.run()
