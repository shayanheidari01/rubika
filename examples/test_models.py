from rubpy.bot.models import Update, Message


update = Update(type='NewMessage', chat_id='b0...', new_message=Message(message_id='874387239487428'))

print(update.new_message.message_id)
print(update.get('new_message').get('message_id'))
print(update['new_message']['message_id'])
