from rubpy import Client, handlers, models, methods
from aiohttp import ClientSession, ClientTimeout
from random import choice
from asyncio import run, sleep

my_group = "GUID"
my_filters = ('@', 'join', 'rubika.ir')
group_admins = []
silence_list = []
no_gifs = False

my_insults = (
    'کیر',
    'کص',
    'کون',
    'کس ننت',
    'کوس',
    'کوص',
    'ممه',
    'ننت',
    'بی ناموس',
    'بیناموس',
    'بیناموص',
    'بی ناموص',
    'گایید',
    'جنده',
    'جندع',
    'جیندا',
    'پستون',
    'کسکش',
    'ننه کس',
    'اوبی',
    'هرزه',
    'قحبه',
    'عنتر',
    'فاک',
    'کسعمت',
    'کصخل',
    'کسخل',
    'تخمی',
    'سکس',
    'صکص',
    'کسخول',
    'کسشر',
    'کسشعر',
)

def getAds(string: str) -> bool:
    string = string.lower()
    for filter in my_filters:
        if filter in string:
            return True
        else:
            continue
    return False

def getInsults(string: str) -> bool:
    for filter in my_insults:
        if filter in string:
            return True
        else:
            continue
    return False

async def updateAdmins(client: Client) -> None:
    global group_admins
    results = await client(methods.groups.GetGroupAdminMembers(my_group))
    results = results.to_dict().get('in_chat_members')
    for result in results:
        GUID = result.get('member_guid')
        if not GUID in group_admins:
            group_admins.append(GUID)
        else:
            continue

async def main():
    async with ClientSession(timeout=ClientTimeout(5)) as CS:
        async with Client(session='MyBot') as client:
            await updateAdmins(client)
            @client.on(handlers.MessageUpdates(models.is_group()))
            async def updates(update):
                if update.object_guid == my_group:
                    if not update.author_guid in group_admins and 'forwarded_from' in update.to_dict().get('message').keys():
                        await update.delete_messages()
                        print('Delete A Forward.')

                    if update.raw_text != None:
                        if not update.author_guid in group_admins and getAds(update.raw_text):
                            await update.delete_messages()
                            print('Delete A Link.')

                        elif getInsults(update.raw_text):
                            await update.delete_messages()
                            print('Delete A Insult.')

                        elif update.author_guid in group_admins and update.raw_text == '!open':
                            result = await client(methods.groups.SetGroupDefaultAccess(my_group, ['SendMessages']))
                            await update.reply('گروه باز شد.')

                        elif update.author_guid in group_admins and update.raw_text == '!close':
                            result = await client(methods.groups.SetGroupDefaultAccess(my_group, []))
                            await update.reply('گروه بسته شد.')

                        elif update.author_guid in group_admins and update.raw_text == 'قفل گیف':
                            global no_gifs
                            no_gifs = True
                            await update.reply('گیف قفل شد.')

                        elif update.raw_text == 'قیمت ارز':
                            string = ''
                            async with CS.get('https://api.codebazan.ir/arz/?type=arz') as response:
                                response = await response.json()
                                if response.get('Ok'):
                                    results = response.get('Result')
                                    for result in results:
                                        try:
                                            string += ''.join(['● ', result.get('name'), '\n', '• قیمت: ', result.get('price'), ' ریال','\n', '• به روزرسانی: ', result.get('update'), '\n\n'])
                                        except TypeError:
                                            continue
                                    await update.reply(string)

                        elif update.raw_text == 'دانستنی':
                            async with CS.post('http://api.codebazan.ir/danestani/') as response:
                                await update.reply(await response.text())

                        elif update.raw_text == 'جوک':
                            path = choice(['jok', 'jok/khatere', 'jok/pa-na-pa', 'jok/alaki-masalan'])
                            async with CS.post(f'http://api.codebazan.ir/{path}/') as response:
                                await update.reply(await response.text())

                        elif update.raw_text == 'ذکر امروز':
                            async with CS.post('http://api.codebazan.ir/zekr/') as response:
                                await update.reply(await response.text())

                        elif update.raw_text == 'حدیث':
                            async with CS.post('http://api.codebazan.ir/hadis/') as response:
                                await update.reply(await response.text())

                        elif update.author_guid in group_admins and update.raw_text == 'باز کردن گیف':
                            no_gifs = False
                            await update.reply('قفل گیف رفع شد.')

                        elif update.author_guid in group_admins and update.raw_text.startswith('سکوت'):
                            if update.reply_message_id != None:
                                try:
                                    result = await client(methods.messages.GetMessagesByID(my_group, [update.reply_message_id]))
                                    result = result.to_dict().get('messages')[0]
                                    if not result.get('author_object_guid') in group_admins:
                                        global silence_list
                                        silence_list.append(result.get('author_object_guid'))
                                        await update.reply('کاربر مورد نظر در حالت سکوت قرار گرفت.')
                                    else:
                                        await update.reply('کاربر مورد نظر در گروه ادمین است.')
                                except IndexError:
                                    await update.reply('ظاهرا پیامی که روی آن ریپلای کرده اید پاک شده است.')
                            elif update.text.startswith('سکوت @'):
                                username = update.text.split('@')[-1]
                                if username != '':
                                    result = await client(methods.extras.GetObjectByUsername(username.lower()))
                                    result = result.to_dict()
                                    if result.get('exist'):
                                        if result.get('type') == 'User':
                                            user_guid = result.get('user').get('user_guid')
                                            if not user_guid in group_admins:
                                                #global silence_list
                                                silence_list.append(user_guid)
                                                await update.reply('کاربر مورد نظر در حالت سکوت قرار گرفت.')
                                            else:
                                                await update.reply('کاربر مورد نظر در گروه ادمین است.')
                                        else:
                                            await update.reply('کاربر مورد نظر کاربر عادی نیست.')
                                    else:
                                        await update.reply('آیدی مورد نظر اشتباه است.')
                                else:
                                    await update.reply('آیدی مورد نظر اشتباه است.')
                            else:
                                await update.reply('روی یک کاربر ریپلای بزنید.')

                        elif update.author_guid in group_admins and update.raw_text.startswith('لیست سکوت خالی'):
                            if silence_list == []:
                                await update.reply('لیست سکوت خالی است.')
                            else:
                                silence_list = []
                                await update.reply('لیست سکوت خالی شد.')

                        elif update.raw_text == 'لینک':
                            result = await client(methods.groups.GetGroupLink(my_group))
                            result = result.to_dict().get('join_link')
                            await update.reply(f'لینک گروه:\n{result}')

                        elif update.author_guid in group_admins and update.text == '!update-admins':
                            reply = await update.reply('در حال به روزرسانی لیست ادمین ها...')
                            await updateAdmins(client)
                            await sleep(2)
                            await reply.edit('به روزرسانی لیست ادمین ها انجام شد.')

                        elif update.author_guid in group_admins and update.text.startswith('!ban'):
                            if update.reply_message_id != None:
                                try:
                                    result = await client(methods.messages.GetMessagesByID(my_group, [update.reply_message_id]))
                                    result = result.to_dict().get('messages')[0]
                                    if not result.get('author_object_guid') in group_admins:
                                        result = await client(methods.groups.BanGroupMember(my_group, result.get('author_object_guid')))
                                        await update.reply('کاربر مورد نظر از گروه حذف شد.')
                                    else:
                                        await update.reply('کاربر مورد نظر در گروه ادمین است.')
                                except IndexError:
                                    await update.reply('ظاهرا پیامی که روی آن ریپلای کرده اید پاک شده است.')
                            elif update.text.startswith('!ban @'):
                                username = update.text.split('@')[-1]
                                if username != '':
                                    result = await client(methods.extras.GetObjectByUsername(username.lower()))
                                    result = result.to_dict()
                                    if result.get('exist'):
                                        if result.get('type') == 'User':
                                            user_guid = result.get('user').get('user_guid')
                                            if not user_guid in group_admins:
                                                result = await client(methods.groups.BanGroupMember(my_group, user_guid))
                                                await update.reply('کاربر مورد نظر از گروه حذف شد.')
                                            else:
                                                await update.reply('کاربر مورد نظر در گروه ادمین است.')
                                        else:
                                            await update.reply('کاربر مورد نظر کاربر عادی نیست.')
                                    else:
                                        await update.reply('آیدی مورد نظر اشتباه است.')
                                else:
                                    await update.reply('آیدی مورد نظر اشتباه است.')
                            else:
                                await update.reply('روی یک کاربر ریپلای بزنید.')

            @client.on(handlers.MessageUpdates(models.is_group()))
            async def updates(update):
                if update.object_guid == my_group:
                    if update.author_guid in silence_list:
                        await update.delete_messages()
                    else:
                        if no_gifs:
                            if not update.author_guid in group_admins:
                                result = await client(methods.messages.GetMessagesByID(my_group, [update.message_id]))
                                result = result.to_dict().get('messages')[0]
                                if result.get('type') == 'FileInline' and result.get('file_inline').get('type') == 'Gif':
                                    await update.delete_messages()
                                    print('Delete A Gif.')

            await client.run_until_disconnected()

run(main())
