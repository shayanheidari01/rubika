# Example usage
import asyncio
from typing import Union
from rubpy.bot import BotClient, ButtonFilter, CommandFilter, InlineMessage, Update, Keypad, KeypadRow, Button, ButtonTypeEnum, ChatKeypadTypeEnum


async def main():
    client = BotClient("your-bot-token")

    @client.on_update(CommandFilter("start"))
    async def handle_start(client: BotClient, update: Update):
        keypad = Keypad(
            rows=[
                KeypadRow(buttons=[
                    Button(id="100", type=ButtonTypeEnum.SIMPLE, button_text="Add Account"),
                    Button(id="101", type=ButtonTypeEnum.SIMPLE, button_text="Edit Account")
                ]),
                KeypadRow(buttons=[
                    Button(id="102", type=ButtonTypeEnum.SIMPLE, button_text="Remove Account")
                ])
            ],
            resize_keyboard=True,
            on_time_keyboard=False
        )
        response = await update.reply(
            text="Welcome to the bot! Choose an option:",
            inline_keypad=keypad,
            chat_keypad_type=ChatKeypadTypeEnum.NONE
        )
        #logger.info("Start command response: %s", response)

    @client.on_update(CommandFilter("test"))
    async def handle_test(client: BotClient, update: Update):
        response = await update.reply(text="accepted", chat_id=update.chat_id)
        #logger.info("Test command response: %s", response)

    @client.on_update(CommandFilter("testkeypad"))
    async def handle_testkeypad(client: BotClient, update: Update):
        keypad = Keypad(
            rows=[
                KeypadRow(buttons=[
                    Button(id="test_100", type=ButtonTypeEnum.SIMPLE, button_text="Test Button")
                ])
            ],
            resize_keyboard=True,
            on_time_keyboard=False
        )
        response = await update.reply(
            text="Testing a simple keypad:",
            inline_keypad=keypad,
            chat_keypad_type=ChatKeypadTypeEnum.NONE
        )
        #logger.info("Test keypad response: %s", response)

    @client.on_update(ButtonFilter("100"))
    async def handle_add_account(client: BotClient, update: Union[Update, InlineMessage]):
        response = await update.reply(client=client, text="You clicked Add Account!")
        #logger.info("Add account response: %s", response)

    @client.on_update(ButtonFilter("101"))
    async def handle_edit_account(client: BotClient, update: Union[Update, InlineMessage]):
        response = await update.reply(client=client, text="You clicked Edit Account!")
        #logger.info("Edit account response: %s", response)

    @client.on_update(ButtonFilter("102"))
    async def handle_remove_account(client: BotClient, update: Union[Update, InlineMessage]):
        response = await update.reply(client=client, text="You clicked Remove Account!")
        #logger.info("Remove account response: %s", response)

    @client.on_update(ButtonFilter("test_100"))
    async def handle_test_button(client: BotClient, update: Union[Update, InlineMessage]):
        response = await update.reply(client=client, text="You clicked Test Button!")
        #logger.info("Test button response: %s", response)

    # Fallback handler for unhandled updates
    @client.on_update()
    async def handle_unmatched(client: BotClient, update: Union[Update, InlineMessage]):
        update_type = "InlineMessage" if isinstance(update, InlineMessage) else update.type
        #logger.debug("Unhandled update (%s): %s", update_type, update)

    # Run with webhook
    # await client.run(webhook_url="url", path='/webhook', host="0.0.0.0", port=3000)

    # Or run with polling
    await client.run()

if __name__ == "__main__":
    asyncio.run(main())
