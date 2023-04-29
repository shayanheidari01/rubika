from rubpy import Client, Message, handlers, models
from asyncio import run, create_task
from asyncio import sleep as aiosleep
import openai

groups = ["GUID"]
openai.api_key = "openai-token"

async def sendResultOfChatGPT(message: Message, text: str) -> bool:
	await aiosleep(3)
	try:
		result = openai.ChatCompletion.create(
		  model="gpt-3.5-turbo",
		  messages=[{"role": "user", "content": text}])
		result = result.get('choices')[0].get('message').get('content')
		await message.reply(result)
	except:
		await message.reply('خطایی رخ داد.')

async def main():
	async with Client(session="MyBot") as client:
		@client.on(handlers.MessageUpdates(models.is_group))
		async def updates(message: Message):
			if message.object_guid in groups:
				text: str = message.raw_text
				if text != None:
					if text.startswith('//'):
						text = text[2:].strip()
						create_task(sendResultOfChatGPT(message, text))
		await client.run_until_disconnected()

run(main())