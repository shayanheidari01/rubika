from rubpy import Client, exceptions

app = Client(auth='auth-key')
group_guid = "group_guid"

sleeped, group_admins = False, []

async def getGroupAdmins(bot):
    global group_admins
    group_admins = await bot.getGroupAdminMembers(
        group_guid=group_guid,
        get_admin_guids=True,
    )
app.run(getGroupAdmins)

async def deleteMessage(bot, message_id):
	try:
		await bot.deleteMessages(group_guid, [message_id])
	except exceptions.InvaildAuth:
		return await app.sendMessage(group_guid, 'لطفا ربات را در گروه ادمین کنید')

async def Banner(bot, message):
    try:
        object_guid, message_id = await message.chat_id(), await message.id()
        text = await message.text()
        if '@' in text:
            text = text[6:].replace('@', '')
            user_guid_for_remove = await bot.getObjectByUsername(text)
            if user_guid_for_remove.get('exist') and user_guid_for_remove.get('type') == 'User':
                user_guid_for_remove = user_guid_for_remove.get('user').get('user_guid')
                if not user_guid_for_remove in group_admins:
                    await bot.banGroupMember(object_guid, user_guid_for_remove)
                    await message.reply('کاربر مورد نظر از گروه حذف شد.')
                else:
                    await message.reply('کاربر مورد نظر ادمین گروه میباشد')
            else:
                await message.reply('احتمالا کاربری با این آیدی وجود ندارد')

        else:
            message_info = await bot.getMessagesByID(object_guid, [message_id])
            message_info = message_info.get('messages')[0]
            if 'reply_to_message_id' in message_info.keys():
                user_guid = await bot.getMessagesByID(object_guid, [message_info.get('reply_to_message_id')])
                user_guid = user_guid.get('messages')[0].get('author_object_guid')
                if not user_guid in group_admins:
                    await bot.banGroupMember(object_guid, user_guid)
                    await message.reply('کاربر مورد نظر از گروه حذف شد.')
                else:
                    await message.reply('کاربر مورد نظر ادمین گروه میباشد')
            else:
                await message.reply("لطفا روی پیام شخص مورد نظر ریپلای بزنید.")

    except exceptions.InvaildAuth:
        await message.reply('لطفا ربات را در گروه ادمین کنید')

    except exceptions.InvalidInput:
        pass

@app.handler
async def GroupManagement(bot, message):
    global sleeped, group_admins
    if await message.of_group((group_guid)):
        m_type = await message.type() # get message type, Example -> Text
        if not sleeped:
            if m_type == 'Text':
                text = await message.text()
                if text.startswith('افزودن ') and await message.author_object_guid(group_admins):
                    try:
                        username = text.split('@')
                        try:
                            if username[1] != '':
                                user_guid = await bot.getObjectByUsername(username[1])
                                if user_guid.get('exist') and user_guid.get('type') == 'User':
                                    user_guid = user_guid.get('user').get('user_guid')
                                    await bot.addGroupMembers(group_guid, [user_guid])
                                    await message.reply('کاربر مورد نظر افزوده شد')
                                else:
                                    await message.reply('احتمالا آیدی شما اشتباه است')
                            else:
                                await message.reply(
                                    'لطفا آیدی کاربر را به درستی وارد نمایید')
                        except IndexError:
                            await message.reply(
                                'لطفا آیدی کاربر را به درستی وارد نمایید')
                    except exceptions.InvalidInput:
                        pass

                elif await message.hasAds() and not await message.author_object_guid(group_admins):
                    await deleteMessage(bot, await message.id())

                elif await message.is_forward() and not await message.author_object_guid(group_admins):
                    await deleteMessage(bot, await message.id())

                elif text.lower() in ('/sleep', '!sleep') and await message.author_object_guid(group_admins):
                    sleeped = True
                    await message.reply(
                        'ربات به خواب فرو رفت!\nتوجه: در این حالت ربات هیچ کاری انجام نمیدهد.')

                elif text.startswith('اخراج') and await message.author_object_guid(group_admins):
                    await Banner(bot, message=message)

                elif text in ('/lock', '!lock') and await message.author_object_guid(group_admins):
                    await bot.setGroupDefaultAccess(group_guid, [])
                    await message.reply('گروه قفل شد')

                elif text in ('/unlock', '!unlock') and await message.author_object_guid(group_admins):
                    await bot.setGroupDefaultAccess(group_guid, ['SendMessages'])
                    await message.reply('گروه باز شد')

                elif text in ('!update-admins-list', '/update-admins-list') and await message.author_object_guid(group_admins):
                    group_admins = await bot.getGroupAdminMembers(
                        group_guid=group_guid,
                        get_admin_guids=True,
                    )
                    await message.reply('لیست ادمین های گروه به روزرسانی شد')

            elif m_type == 'FileInline': # Check Message Type
                if await message.is_forward() and not await message.author_object_guid(group_admins):
                    await deleteMessage(bot, await message.id())

            elif m_type == 'FileInlineCaption':
                if await message.is_forward() and not await message.author_object_guid(group_admins):
                    await deleteMessage(bot, await message.id())

        else:
            if m_type == 'Text':
                text = await message.text()
                if text in ('/wakeup', '!wakeup') and await message.author_object_guid(group_admins):
                    sleeped = False
                    await message.reply('ربات بیدار شد')