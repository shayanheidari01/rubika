from rubpy import Client, utils
from rubpy.types import Updates

bot = Client('bot')
groups = [] # insert the group guids

async def text_filter(update: Updates, result):
    return update.object_guid in groups and update.raw_text

async def check_is_admin(group_guid: str, user_guid: str):
    next_start_id = None
    has_continue = True

    while has_continue:
        result = await bot.get_group_admin_members(group_guid, start_id=next_start_id)
        next_start_id = result.next_start_id
        has_continue = result.has_continue

        admins = [admin.member_guid for admin in result.in_chat_members]
        if user_guid in admins:
            return True

    return False

@bot.on_message_updates(text_filter)
async def updates(update: Updates):
    text: str = update.raw_text

    if utils.is_rubika_link(text):
        if not await check_is_admin(update.object_guid, update.author_guid):
            await update.delete_messages()

    elif utils.is_username(text):
        if not await check_is_admin(update.object_guid, update.author_guid):
            await update.delete_messages()

bot.run()