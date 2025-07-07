import asyncio
from datetime import datetime
import random
import aiofiles
import googlesearch
from rubpy import Client, filters
from rubpy.types import Update
from tcping import tcping
from TranslatorX import AsyncTranslator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Text, delete, select

# تنظیمات ضداسپم
recent_guids = set()
SPAM_TIMEOUT = 10  # زمان بلاک GUID به ثانیه

# تنظیمات دیتابیس
DATABASE_URL = "sqlite+aiosqlite:///bot.db"
engine = create_async_engine(DATABASE_URL, echo=False)
Base = declarative_base()

# مدل‌های دیتابیس
class UserInfo(Base):
    __tablename__ = 'user_info'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    guid = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    bio = Column(Text)

class Setting(Base):
    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    value = Column(Boolean)

class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    question = Column(String, unique=True)
    answer = Column(Text)

class Language(Base):
    __tablename__ = 'language'
    id = Column(Integer, primary_key=True)
    user_guid = Column(String, unique=True)
    language = Column(String, default='fa')

# مقداردهی اولیه دیتابیس
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# مقداردهی اولیه کلاینت و کامپوننت‌ها
client = Client('my-self')
async_translator = AsyncTranslator()
http_client = AsyncClient()
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# قالب پیام‌ها
MESSAGE_TEMPLATES = {
    'fa': {
        'welcome': "🌟 خوش آمدید! چگونه می‌توانم به شما کمک کنم؟",
        'ping_success': "✅ پینگ موفق! تأخیر: {latency} میلی‌ثانیه",
        'ping_failed': "❌ پینگ ناموفق. سرور ممکن است خاموش باشد.",
        'info': "📋 **اطلاعات پروفایل**\nنام کاربری: {username}\nشناسه: `{guid}`\nنام: {first_name}\nنام خانوادگی: {last_name}\nبیوگرافی:\n{bio}",
        'reset_info': "✅ اطلاعات با موفقیت بازنشانی شد.",
        'set_bio_error': "❌ خطا در به‌روزرسانی بیوگرافی: {error}",
        'set_bio_success': "✅ بیوگرافی با موفقیت به‌روزرسانی شد.",
        'get_bio_none': "ℹ️ بیوگرافی تنظیم نشده است. از `/set_bio` استفاده کنید.",
        'time': "🕒 زمان کنونی: {time}",
        'date': "📅 تاریخ کنونی: {date}",
        'translate_missing': "⚠️ لطفاً زبانی برای ترجمه مشخص کنید.",
        'translate_reply': "⚠️ لطفاً به پیامی پاسخ دهید که حاوی متن برای ترجمه باشد。",
        'calc_missing': "⚠️ لطفاً یک عبارت ریاضی وارد کنید.",
        'calc_error': "❌ خطا در محاسبه: {error}",
        'auto_edit_text': "✍️ ویرایش خودکار متن اکنون {status} است.",
        'auto_bold': "✍️ **پررنگ خودکار** اکنون {status} است.",
        'auto_italic': "✍️ __کج خودکار__ اکنون {status} است.",
        'dice': "🎲 شما عدد **{number}** را آوردید!",
        'wiki_error': "❌ خطا در دریافت خلاصه ویکی‌پدیا: {error}",
        'search_error': "❌ خطا در دریافت نتایج جستجو: {error}",
        'ping_host_error': "❌ خطا در پینگ هاست: {error}",
        'persian_date': "📅 تاریخ پارسی کنونی: {date}",
        'english_date': "📅 تاریخ میلادی کنونی: {date}",
        'typing_status': "⌨️ نشانگر تایپ اکنون {status} است.",
        'block_no_reply': "⚠️ لطفاً به پیامی پاسخ دهید تا کاربر مسدود شود.",
        'block_error': "❌ خطا در مسدود کردن کاربر: {error}",
        'block_success': "✅ کاربر `{guid}` مسدود شد.",
        'unblock_no_reply': "⚠️ لطفاً به پیامی پاسخ دهید تا کاربر رفع مسدودیت شود.",
        'unblock_error': "❌ خطا در رفع مسدودیت کاربر: {error}",
        'unblock_success': "✅ کاربر `{guid}` رفع مسدودیت شد。",
        'set_answer_missing': "⚠️ لطفاً سؤال و پاسخ را وارد کنید.",
        'set_answer_success': "✅ پاسخ برای «{question}» با موفقیت تنظیم شد。",
        'get_answer_missing': "⚠️ لطفاً سؤالی برای دریافت پاسخ وارد کنید.",
        'get_answer_none': "⚠️ پاسخی برای «{question}» یافت نشد。",
        'delete_answer_missing': "⚠️ لطفاً سؤالی برای حذف پاسخ وارد کنید.",
        'delete_answer_success': "✅ پاسخ برای «{question}» با موفقیت حذف شد。",
        'delete_answer_none': "⚠️ پاسخی برای «{question}» یافت نشد.",
        'answer_missing': "⚠️ لطفاً سؤالی برای دریافت پاسخ وارد کنید。",
        'answer_none': "⚠️ پاسخی برای «{question}» یافت نشد。",
        'clean_answers': "✅ همه پاسخ‌ها پاک شدند。",
        'ai_error': "❌ خطا در ارتباط با سرویس هوش مصنوعی.",
        'ai_no_response': "⚠️ پاسخی از هوش مصنوعی دریافت نشد。",
    },
    'en': {
        'welcome': "🌟 Welcome! How can I assist you today?",
        'ping_success': "✅ Ping successful! Latency: {latency} ms",
        'ping_failed': "❌ Ping failed. The server might be down.",
        'info': "📋 **Profile Information**\nUsername: {username}\nGUID: `{guid}`\nFirst Name: {first_name}\nLast Name: {last_name}\nBio:\n{bio}",
        'reset_info': "✅ Info reset successfully.",
        'set_bio_error': "❌ Error updating bio: {error}",
        'set_bio_success': "✅ Bio updated successfully.",
        'get_bio_none': "ℹ️ No bio set yet. Use `/set_bio` to set one.",
        'time': "🕒 Current time: {time}",
        'date': "📅 Current date: {date}",
        'translate_missing': "⚠️ Please provide a language to translate.",
        'translate_reply': "⚠️ Please reply to a message containing text to translate.",
        'calc_missing': "⚠️ Please provide a calculation expression.",
        'calc_error': "❌ Error in calculation: {error}",
        'auto_edit_text': "✍️ Auto edit text is now {status}.",
        'auto_bold': "✍️ **Auto bold** is now {status}.",
        'auto_italic': "✍️ __Auto italic__ is now {status}.",
        'dice': "🎲 You rolled a **{number}**!",
        'wiki_error': "❌ Error fetching Wikipedia summary: {error}",
        'search_error': "❌ Error fetching search results: {error}",
        'ping_host_error': "❌ Error pinging host: {error}",
        'persian_date': "📅 Current Persian date: {date}",
        'english_date': "📅 Current English date: {date}",
        'typing_status': "⌨️ Typing indicator is now {status}.",
        'block_no_reply': "⚠️ Please reply to a message to block the user.",
        'block_error': "❌ Error blocking user: {error}",
        'block_success': "✅ User `{guid}` has been blocked.",
        'unblock_no_reply': "⚠️ Please reply to a message to unblock the user.",
        'unblock_error': "❌ Error unblocking user: {error}",
        'unblock_success': "✅ User `{guid}` has been unblocked.",
        'set_answer_missing': "⚠️ Please provide a question and answer.",
        'set_answer_success': "✅ Answer for '{question}' set successfully.",
        'get_answer_missing': "⚠️ Please provide a question to get the answer for.",
        'get_answer_none': "⚠️ No answer found for '{question}'.",
        'delete_answer_missing': "⚠️ Please provide a question to delete the answer for.",
        'delete_answer_success': "✅ Answer for '{question}' deleted successfully.",
        'delete_answer_none': "⚠️ No answer found for '{question}'.",
        'answer_missing': "⚠️ Please provide a question to get the answer for.",
        'answer_none': "⚠️ No answer found for '{question}'.",
        'clean_answers': "✅ All answers have been cleared.",
        'ai_error': "❌ Error communicating with AI service.",
        'ai_no_response': "⚠️ No response from AI.",
    }
}

# تابع فرمت‌بندی پیام
def format_message(message: str, bold: bool = False, italic: bool = False) -> str:
    if bold and italic:
        return f"**__{message}__**"
    elif bold:
        return f"**{message}**"
    elif italic:
        return f"__{message}__"
    return message

# توابع کمکی دیتابیس
async def get_user_language(user_guid: str) -> str:
    async with AsyncSessionLocal() as session:
        result = await session.get(Language, user_guid)
        return result.language if result else 'fa'

async def set_user_language(user_guid: str, language: str):
    async with AsyncSessionLocal() as session:
        lang = await session.get(Language, user_guid)
        if lang:
            lang.language = language
        else:
            lang = Language(user_guid=user_guid, language=language)
            session.add(lang)
        await session.commit()

async def get_setting(key: str) -> bool:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Setting).where(Setting.key == key))
        setting = result.scalar_one_or_none()
        return setting.value if setting else False

async def set_setting(key: str, value: bool):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Setting).where(Setting.key == key))
        setting = result.scalar_one_or_none()
        if setting:
            setting.value = value
        else:
            session.add(Setting(key=key, value=value))
        await session.commit()

async def get_user_info() -> dict:
    async with AsyncSessionLocal() as session:
        user = await session.get(UserInfo, 1)
        return user.__dict__ if user else {}

async def set_user_info(info: dict):
    async with AsyncSessionLocal() as session:
        user = await session.get(UserInfo, 1)
        if user:
            for key, value in info.items():
                setattr(user, key, value)
        else:
            session.add(UserInfo(**info))
        await session.commit()

# تابع کمکی برای ارسال پیام فرمت‌شده
async def send_formatted_message(update: Update, message: str, bold: bool, italic: bool, auto_edit_text: bool = False):
    if auto_edit_text: 
        output = ''
        for char in message:
            output += char
            message = format_message(output, bold, italic)
            await update.edit(message)
            await asyncio.sleep(0.1)
    else:
        await update.edit(format_message(message, bold, italic))

# هندلرهای دستورات
async def handle_ping(update: Update, templates: dict):
    result = await tcping('messengerg2c1.iranlms.ir', 443, timeout=1)
    await update.edit(templates['ping_success'].format(latency=result['latency_ms']) if result.get('status') == 'up' else templates['ping_failed'])

async def handle_info(update: Update, templates: dict):
    my_info = await get_user_info()
    if not my_info:
        result = await client.get_me()
        my_info = {k: getattr(result.user, k) for k in ['username', 'user_guid', 'first_name', 'last_name', 'bio']}
        my_info['guid'] = my_info.pop('user_guid')
        await set_user_info(my_info)
    await update.edit(templates['info'].format(**my_info))

async def handle_reset_info(update: Update, templates: dict):
    async with AsyncSessionLocal() as session:
        await session.execute(delete(UserInfo))
        await session.commit()
    await update.edit(templates['reset_info'])

async def handle_set_bio(update: Update, templates: dict):
    new_bio = update.text[9:].strip()
    if not new_bio:
        await update.edit(templates['set_bio_error'].format(error='No bio provided'))
        return
    try:
        await client.update_profile(bio=new_bio)
        my_info = await get_user_info()
        my_info['bio'] = new_bio
        await set_user_info(my_info)
        await update.edit(templates['set_bio_success'])
    except Exception as e:
        await update.edit(templates['set_bio_error'].format(error=str(e)))

async def handle_get_bio(update: Update, templates: dict):
    my_info = await get_user_info()
    await update.edit(f"Current Bio:\n{my_info['bio']}" if my_info.get('bio') else templates['get_bio_none'])

async def handle_time(update: Update, templates: dict):
    await update.edit(templates['time'].format(time=datetime.now().strftime('%H:%M:%S')))

async def handle_date(update: Update, templates: dict):
    await update.edit(templates['date'].format(date=datetime.now().strftime('%Y-%m-%d')))

async def handle_translate(update: Update, templates: dict):
    to_language = update.text[11:].strip()
    if not to_language or not update.reply_message_id:
        await update.edit(templates['translate_missing'] if not to_language else templates['translate_reply'])
        return
    reply_message = await update.get_reply_message()
    response = await async_translator.Translate(reply_message.text, to_language)
    await update.edit(f"Translated text:\n\n```{response}```")

async def handle_calc(update: Update, templates: dict):
    expression = update.text[6:].strip()
    if not expression:
        await update.edit(templates['calc_missing'])
        return
    try:
        result = eval(expression, {"__builtins__": None}, {})
        await update.edit(f"Result: {result}")
    except Exception as e:
        await update.edit(templates['calc_error'].format(error=str(e)))

async def handle_auto_edit_text(update: Update, templates: dict):
    auto_edit_text = not await get_setting('auto_edit_text')
    await set_setting('auto_edit_text', auto_edit_text)
    await update.edit(templates['auto_edit_text'].format(status='فعال شده' if auto_edit_text else 'غیرفعال شده'))

async def handle_auto_bold(update: Update, templates: dict):
    auto_bold = not await get_setting('auto_bold')
    await set_setting('auto_bold', auto_bold)
    await update.edit(templates['auto_bold'].format(status='enabled' if auto_bold else 'disabled'))

async def handle_auto_italic(update: Update, templates: dict):
    auto_italic = not await get_setting('auto_italic')
    await set_setting('auto_italic', auto_italic)
    await update.edit(templates['auto_italic'].format(status='enabled' if auto_italic else 'disabled'))

async def handle_dice(update: Update, templates: dict):
    await update.edit(templates['dice'].format(number=random.randint(1, 6)))

async def handle_wikipedia(update: Update, templates: dict):
    query = update.text[11:].strip()
    if not query:
        await update.edit(templates['wiki_error'].format(error='No query provided'))
        return
    try:
        import wikipedia
        wikipedia.set_lang(await get_user_language(update.author_object_guid))
        result = wikipedia.summary(query, sentences=2)
        await update.edit(f"**Wikipedia Summary:**\n\n{result}")
    except Exception as e:
        await update.edit(templates['wiki_error'].format(error=str(e)))

async def handle_search(update: Update, templates: dict):
    query = update.text[8:].strip()
    if not query:
        await update.edit(templates['search_error'].format(error='No query provided'))
        return
    try:
        results = googlesearch.search(query, num_results=5, advanced=True)
        output = ''.join(f"{i}- [{r.title.strip()}]({r.url.strip()})\n\n" for i, r in enumerate(results, 1))
        await update.edit(f"**Google Search Results:**\n\n{output}")
    except Exception as e:
        await update.edit(templates['search_error'].format(error=str(e)))

async def handle_ping_host(update: Update, templates: dict):
    host = update.text[6:].strip()
    if not host:
        await update.edit(templates['ping_host_error'].format(error='No host provided'))
        return
    try:
        result = await tcping(host, 443, timeout=1)
        await update.edit(templates['ping_success'].format(latency=result['latency_ms']) if result.get('status') == 'up' else templates['ping_failed'])
    except Exception as e:
        await update.edit(templates['ping_host_error'].format(error=str(e)))

async def handle_persian_date(update: Update, templates: dict):
    from persiantools.jdatetime import JalaliDate
    await update.edit(templates['persian_date'].format(date=JalaliDate.today().strftime("%Y/%m/%d")))

async def handle_english_date(update: Update, templates: dict):
    from persiantools.jdatetime import JalaliDate
    gregorian_date = JalaliDate.today().to_gregorian()
    await update.edit(templates['english_date'].format(date=gregorian_date.strftime("%Y-%m-%d")))

async def handle_typing(update: Update, templates: dict, status: bool):
    await set_setting('typing', status)
    await update.edit(templates['typing_status'].format(status='enabled' if status else 'disabled'))

async def handle_block(update: Update, templates: dict):
    if not update.reply_message_id:
        await update.edit(templates['block_no_reply'])
        return
    reply_message = await update.get_reply_message()
    try:
        await update.block(reply_message.author_object_guid)
        await update.edit(templates['block_success'].format(guid=reply_message.author_object_guid))
    except Exception as e:
        await update.edit(templates['block_error'].format(error=str(e)))

async def handle_unblock(update: Update, templates: dict):
    if not update.reply_message_id:
        await update.edit(templates['unblock_no_reply'])
        return
    reply_message = await update.get_reply_message()
    try:
        await client.set_block_user(reply_message.author_object_guid, action='Unblock')
        await update.edit(templates['unblock_success'].format(guid=reply_message.author_object_guid))
    except Exception as e:
        await update.edit(templates['unblock_error'].format(error=str(e)))

async def handle_set_answer(update: Update, templates: dict):
    parts = update.text[12:].strip().split(' ', 1)
    if len(parts) < 2:
        await update.edit(templates['set_answer_missing'])
        return
    question, answer = parts
    async with AsyncSessionLocal() as session:
        existing = await session.execute(select(Answer).where(Answer.question == question))
        existing = existing.scalars().first()
        if existing:
            existing.answer = answer
        else:
            session.add(Answer(question=question, answer=answer))
        await session.commit()
        await update.edit(templates['set_answer_success'].format(question=question))

async def handle_get_answer(update: Update, templates: dict):
    question = update.text[12:].strip()
    if not question:
        await update.edit(templates['get_answer_missing'])
        return
    async with AsyncSessionLocal() as session:
        answer = await session.execute(select(Answer).where(Answer.question == question))
        answer = answer.scalars().first()
        await update.edit(f"Answer for '{question}': {answer.answer}" if answer else templates['get_answer_none'].format(question=question))

async def handle_delete_answer(update: Update, templates: dict):
    question = update.text[15:].strip()
    if not question:
        await update.edit(templates['delete_answer_missing'])
        return
    async with AsyncSessionLocal() as session:
        result = await session.execute(delete(Answer).where(Answer.question == question))
        await session.commit()
        await update.edit(templates['delete_answer_success'].format(question=question) if result.rowcount > 0 else templates['delete_answer_none'].format(question=question))

async def handle_answer(update: Update, templates: dict):
    question = update.text[8:].strip()
    if not question:
        await update.edit(templates['answer_missing'])
        return
    async with AsyncSessionLocal() as session:
        answer = await session.execute(select(Answer).where(Answer.question == question))
        answer = answer.scalars().first()
        await update.edit(f"Answer: {answer.answer}" if answer else templates['answer_none'].format(question=question))

async def handle_clean_answers(update: Update, templates: dict):
    async with AsyncSessionLocal() as session:
        await session.execute(delete(Answer))
        await session.commit()
    await update.edit(templates['clean_answers'])

async def handle_set_language(update: Update, templates: dict):
    language = update.text[13:].strip().lower()
    if language not in ['fa', 'en']:
        await update.edit("⚠️ لطفاً یک زبان معتبر (fa یا en) مشخص کنید.")
        return
    await set_user_language(update.author_object_guid, language)
    await update.edit(f"✅ زبان به {'فارسی' if language == 'fa' else 'انگلیسی'} تنظیم شد.")

async def handle_ai(update: Update, templates: dict):
    response = await http_client.get('https://chatgpt.ehsancoder-as.workers.dev/', params={'text': update.text[4:].strip()})
    if response.status_code == 200 and response.json().get('ok'):
        await update.edit(f"Ai Response:\n\n{response.json()['result']}")
    else:
        await update.edit(templates['ai_error'] if response.status_code != 200 else templates['ai_no_response'])

async def handle_status(update: Update, templates: dict):
    auto_edit_text, auto_bold, auto_italic, typing = await asyncio.gather(
        get_setting('auto_edit_text'),
        get_setting('auto_bold'),
        get_setting('auto_italic'),
        get_setting('typing')
    )
    status_message = (
        "╭━ 🎛️ 𝗦𝗬𝗦𝗧𝗘𝗠 𝗦𝗧𝗔𝗧𝗨𝗦 ━━━━\n\n"
        f"┃ ⚙️ ویرایش خودکار متن: {'✅ فعال' if auto_edit_text else '❌ غیرفعال'}\n"
        f"┃ 🅱️ **بولد** کردن متن: {'✅ فعال' if auto_bold else '❌ غیرفعال'}\n"
        f"┃ ✨ __ایتالیک__ کردن متن: {'✅ فعال' if auto_italic else '❌ غیرفعال'}\n"
        f"┃ ⌨️ حالت درحال نوشتن: {'✅ فعال' if typing else '❌ غیرفعال'}\n"
        "╰━━━━━━━━━━━━━━━━━━━━━"
    )
    await update.edit(status_message)

async def handle_help(update: Update, templates: dict):
    #auto_bold, auto_italic = await get_setting('auto_bold'), await get_setting('auto_italic')
    async with aiofiles.open('help.txt', 'r', encoding='utf-8') as f:
        help_text = await f.read()
    await update.edit(format_message(help_text, False, False))

# هندلر اصلی پیام‌ها
@client.on_message_updates(filters.is_me)
async def new_message(update: Update):
    user_guid = update.author_object_guid
    lang = await get_user_language(user_guid)
    templates = MESSAGE_TEMPLATES[lang]
    auto_edit_text, auto_bold, auto_italic, typing = [await get_setting(k) for k in ['auto_edit_text', 'auto_bold', 'auto_italic', 'typing']]

    if typing:
        asyncio.create_task(update.send_activity('Typing'))

    if update.text and not update.text.startswith('/'):
        async with AsyncSessionLocal() as session:
            answer = await session.execute(select(Answer).where(Answer.question == update.text))
            answer = answer.scalars().first()
            if answer:
                await send_formatted_message(update, answer.answer, auto_bold, auto_italic)
                return
        if auto_edit_text:
            await send_formatted_message(update, update.text.strip(), auto_bold, auto_italic, auto_edit_text)
        return

    command_handlers = {
        'ping': handle_ping,
        'info': handle_info,
        'reset_info': handle_reset_info,
        'set_bio': handle_set_bio,
        'get_bio': handle_get_bio,
        'time': handle_time,
        'date': handle_date,
        'translate': handle_translate,
        'calc': handle_calc,
        'auto_edit_text': handle_auto_edit_text,
        'auto_bold': handle_auto_bold,
        'auto_italic': handle_auto_italic,
        'dice': handle_dice,
        'wikipedia': handle_wikipedia,
        'search': handle_search,
        'persian_date': handle_persian_date,
        'english_date': handle_english_date,
        'typing on': lambda u, t: handle_typing(u, t, True),
        'typing off': lambda u, t: handle_typing(u, t, False),
        'block': handle_block,
        'unblock': handle_unblock,
        'set_answer': handle_set_answer,
        'get_answer': handle_get_answer,
        'delete_answer': handle_delete_answer,
        'answer': handle_answer,
        'clean_answers': handle_clean_answers,
        'set_language': handle_set_language,
        'ai': handle_ai,
        'help': handle_help,
        'status': handle_status
    }

    command = update.text.split()[0][1:] if update.text else ''
    handler = next((v for k, v in command_handlers.items() if update.text.startswith(f'/{k}')), None)
    if handler:
        await handler(update, templates)
    elif update.text:
        await update.edit("⚠️ دستور ناشناخته. از /help برای مشاهده دستورات استفاده کنید.")

# هندلر سلام
@client.on_message_updates(filters.regex('^سلام'))
async def handle_hello(update: Update):
    guid = update.object_guid
    if guid in recent_guids:
        return
    recent_guids.add(guid)
    asyncio.create_task(remove_guid_after_delay(guid))
    message = None
    for _ in range(30):
        emoji = random.choice(["🩷", "❤️", "🧡", "💛", "💚", "🩵", "💙", "💜"])
        if update.is_me:
            await update.edit(f'سلام {emoji}')
        elif message is None:
            message = await update.reply(f'سلام {emoji}')
            message.client = client
        else:
            await message.edit(f'سلام {emoji}')
        await asyncio.sleep(0.5)

async def remove_guid_after_delay(guid: str):
    await asyncio.sleep(SPAM_TIMEOUT)
    recent_guids.discard(guid)

# اجرا
client.run(init_db())