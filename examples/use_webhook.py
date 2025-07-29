import asyncio
from rubpy.bot import BotClient, filters
from rubpy.bot.models import Button, InlineMessage, Keypad, KeypadRow, Update
from rubpy.bot.enums import ButtonTypeEnum

# Replace with your actual bot token
RUBIKA_TOKEN = "bot-token"
WEBHOOK_URL = "https://example.com"  # URL وب‌هوک شما

async def main():
    bot = BotClient(token=RUBIKA_TOKEN, use_webhook=True)

    @bot.on_update(filters.commands("start"))
    async def handle_start(client: BotClient, update: Update):
        if update.new_message:
            chat_id = update.chat_id
            #logger.info(f"Sending welcome message to chat_id={chat_id}")
            response = await client.send_message(
                chat_id=chat_id,
                text="Welcome to the test bot! Use the buttons below to interact.",
                inline_keypad=Keypad(
                    rows=[
                        KeypadRow(buttons=[
                            Button(id="btn_hello", type=ButtonTypeEnum.SIMPLE, button_text="Say Hello"),
                            Button(id="btn_info", type=ButtonTypeEnum.SIMPLE, button_text="Get Info")
                        ])
                    ]
                )
            )
           # logger.debug(f"Start command response: {response}")

    @bot.on_update(filters.button("btn_hello"))
    async def handle_hello_button(client: BotClient, update: InlineMessage):
       # logger.info(f"Handling btn_hello click for chat_id={update.chat_id}")
        response = await client.send_message(
            chat_id=update.chat_id,
            text=f"✅ You clicked the 'Say Hello' button!"
        )
        #logger.debug(f"Button hello response: {response}")

    @bot.on_update(filters.button("btn_info"))
    async def handle_info_button(client: BotClient, update: InlineMessage):
       # logger.info(f"Handling btn_info click for chat_id={update.chat_id}")
        bot_info = await client.get_me()
        response = await client.send_message(
            chat_id=update.chat_id,
            text=f"ℹ️ Bot Info: {bot_info.get('username', 'Unknown')}"
        )
       # logger.debug(f"Button info response: {response}")

    @bot.on_update(filters.update_type("NewMessage"))
    async def handle_new_message(client: BotClient, update: Update):
        if update.new_message and not update.new_message.text.startswith("/"):
         #   logger.info(f"Handling new message for chat_id={update.chat_id}")
            response = await client.send_message_with_buttons(
                chat_id=update.chat_id,
                text=f"📩 Received your message: {update.new_message.text}",
                buttons=[
                    [{"id": "btn_add", "text": "Add Item"}],
                    [{"id": "btn_remove", "text": "Remove Item"}]
                ]
            )
         #   logger.debug(f"New message response: {response}")

    await bot.run(webhook_url=WEBHOOK_URL, port=8000, path='/wk')

    """
    (method) def run(
        webhook_url: str | None = None,
        path: str | None = '/webhook',
        host: str = "0.0.0.0",
        port: int = 8080
                    ) -> CoroutineType[Any, Any, None]
    
    - Run the bot, either using polling or webhook.
    """

if __name__ == "__main__":
    asyncio.run(main())
