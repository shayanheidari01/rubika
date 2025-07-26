from rubpy import BotClient

# Create a new Client instance
app = BotClient("bot-token")


async def main():
    # Start client
    await app.start()

    # Send a message, Markdown is enabled by default
    await app.send_message("chat_id", "Hi there! I'm using **Rubpy**")

    # Close client
    await app.stop()


import asyncio
asyncio.run(main())
