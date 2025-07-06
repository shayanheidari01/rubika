import asyncio
from datetime import datetime
import random
import googlesearch
from rubpy import Client, filters
from rubpy.types import Update
from tcping import tcping
from TranslatorX import AsyncTranslator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, delete, select
from sqlalchemy.sql import func

# مجموعه‌ای برای نگهداری پیام‌هایی که اخیراً پاسخ داده شدند
recent_guids = set()

# زمان بلاک شدن هر GUID (برحسب ثانیه)
SPAM_TIMEOUT = 10  # مثلاً 10 ثانیه

# Database setup
DATABASE_URL = "sqlite+aiosqlite:///bot.db"
engine = create_async_engine(DATABASE_URL, echo=False)
Base = declarative_base()

# Database models
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

# Create database tables
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Initialize client and other components
client = Client('my-self')
async_translator = AsyncTranslator()
http_client = AsyncClient()
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Message templates with formatting and emojis
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
        'translate_reply': "⚠️ لطفاً به پیامی پاسخ دهید که حاوی متن برای ترجمه باشد.",
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
        'block_username_not_found': "⚠️ کاربر `@{username}` یافت نشد.",
        'unblock_no_reply': "⚠️ لطفاً به پیامی پاسخ دهید تا کاربر رفع مسدودیت شود.",
        'unblock_error': "❌ خطا در رفع مسدودیت کاربر: {error}",
        'unblock_success': "✅ کاربر `{guid}` رفع مسدودیت شد.",
        'unblock_username_not_found': "⚠️ کاربر `@{username}` یافت نشد.",
        'set_answer_missing': "⚠️ لطفاً سؤال و پاسخ را وارد کنید.",
        'set_answer_success': "✅ پاسخ برای «{question}» با موفقیت تنظیم شد.",
        'get_answer_missing': "⚠️ لطفاً سؤالی برای دریافت پاسخ وارد کنید.",
        'get_answer_none': "⚠️ پاسخی برای «{question}» یافت نشد.",
        'delete_answer_missing': "⚠️ لطفاً سؤالی برای حذف پاسخ وارد کنید.",
        'delete_answer_success': "✅ پاسخ برای «{question}» با موفقیت حذف شد.",
        'delete_answer_none': "⚠️ پاسخی برای «{question}» یافت نشد.",
        'answer_missing': "⚠️ لطفاً سؤالی برای دریافت پاسخ وارد کنید.",
        'answer_none': "⚠️ پاسخی برای «{question}» یافت نشد.",
        'clean_answers': "✅ همه پاسخ‌ها پاک شدند.",
        'ai_error': "❌ خطا در ارتباط با سرویس هوش مصنوعی.",
        'ai_no_response': "⚠️ پاسخی از هوش مصنوعی دریافت نشد.",
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
        'block_username_not_found': "⚠️ User `@{username}` not found.",
        'unblock_no_reply': "⚠️ Please reply to a message to unblock the user.",
        'unblock_error': "❌ Error unblocking user: {error}",
        'unblock_success': "✅ User `{guid}` has been unblocked.",
        'unblock_username_not_found': "⚠️ User `@{username}` not found.",
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

# Font styling function
def format_message(message: str, bold: bool = False, italic: bool = False) -> str:
    if bold:
        return f"**{message}**"
    if italic:
        return f"__{message}__"
    return message

# Get user language
async def get_user_language(user_guid: str) -> str:
    async with AsyncSessionLocal() as session:
        result = await session.get(Language, user_guid)
        return result.language if result else 'fa'

# Set user language
async def set_user_language(user_guid: str, language: str):
    async with AsyncSessionLocal() as session:
        lang = await session.get(Language, user_guid)
        if lang:
            lang.language = language
        else:
            lang = Language(user_guid=user_guid, language=language)
            session.add(lang)
        await session.commit()

# Get setting from database
async def get_setting(key: str) -> bool:
    async with AsyncSessionLocal() as session:
        setting = await session.get(Setting, key)
        return setting.value if setting else False

# Set setting in database
async def set_setting(key: str, value: bool):
    async with AsyncSessionLocal() as session:
        setting = await session.get(Setting, key)
        if setting:
            setting.value = value
        else:
            setting = Setting(key=key, value=value)
            session.add(setting)
        await session.commit()

# Get user info from database
async def get_user_info() -> dict:
    async with AsyncSessionLocal() as session:
        user = await session.get(UserInfo, 1)
        if user:
            return {
                'username': user.username,
                'guid': user.guid,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'bio': user.bio
            }
        return {}

# Set user info in database
async def set_user_info(info: dict):
    async with AsyncSessionLocal() as session:
        user = await session.get(UserInfo, 1)
        if user:
            user.username = info.get('username')
            user.guid = info.get('guid')
            user.first_name = info.get('first_name')
            user.last_name = info.get('last_name')
            user.bio = info.get('bio')
        else:
            user = UserInfo(**info)
            session.add(user)
        await session.commit()

@client.on_message_updates(filters.is_me)
async def new_message(update: Update):
    user_guid = update.author_object_guid
    lang = await get_user_language(user_guid)
    templates = MESSAGE_TEMPLATES[lang]
    
    auto_edit_text = await get_setting('auto_edit_text')
    auto_bold = await get_setting('auto_bold')
    auto_italic = await get_setting('auto_italic')
    typing = await get_setting('typing')

    if typing:
        asyncio.create_task(update.send_activity('Typing'))

    if auto_edit_text and update.text and not update.text.startswith('/'):
        output = ''
        for part in update.text:
            output += part
            formatted = format_message(output.strip(), auto_bold, auto_italic)
            await update.edit(formatted)
            await asyncio.sleep(0.01)
    
    elif auto_bold and update.text and not update.text.startswith('/'):
        await update.edit(format_message(update.text.strip(), bold=True))
    
    elif auto_italic and update.text and not update.text.startswith('/'):
        await update.edit(format_message(update.text.strip(), italic=True))
    
    elif update.text and not update.text.startswith('/'):
        async with AsyncSessionLocal() as session:
            answer = await session.execute(
                select(Answer).where(Answer.question == update.text)
            )
            answer = answer.scalars().first()
            if answer:
                await update.edit(format_message(answer.answer, auto_bold, auto_italic))
    
    elif update.text == '/ping':
        result = await tcping('messengerg2c1.iranlms.ir', 443, timeout=1)
        if result.get('status') == 'up':
            await update.edit(templates['ping_success'].format(latency=result['latency_ms']))
        else:
            await update.edit(templates['ping_failed'])
    
    elif update.text == '/info':
        my_info = await get_user_info()
        if not my_info:
            result = await client.get_me()
            my_info = {
                'username': result.user.username,
                'guid': result.user.user_guid,
                'first_name': result.user.first_name,
                'last_name': result.user.last_name,
                'bio': result.user.bio
            }
            await set_user_info(my_info)
        
        await update.edit(templates['info'].format(**my_info))
    
    elif update.text == '/reset_info':
        async with AsyncSessionLocal() as session:
            await session.execute(delete(UserInfo))
            await session.commit()
        await update.edit(templates['reset_info'])
    
    elif update.text.startswith('/set_bio'):
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
    
    elif update.text == '/get_bio':
        my_info = await get_user_info()
        if not my_info or not my_info.get('bio'):
            await update.edit(templates['get_bio_none'])
        else:
            await update.edit(f"Current Bio:\n{my_info['bio']}")
    
    elif update.text == '/live_time':
        for _ in range(10):
            current_time = datetime.now().strftime('%H:%M:%S')
            message = await update.edit(templates['time'].format(time=current_time))
            message.client = client
            await message.edit(templates['time'].format(time=current_time))
            await asyncio.sleep(1)
    
    elif update.text == '/time':
        current_time = datetime.now().strftime('%H:%M:%S')
        await update.edit(templates['time'].format(time=current_time))
    
    elif update.text == '/date':
        current_date = datetime.now().strftime('%Y-%m-%d')
        await update.edit(templates['date'].format(date=current_date))
    
    elif update.text.startswith('/translate '):
        to_language = update.text[11:].strip()
        if not to_language:
            await update.edit(templates['translate_missing'])
            return

        if not update.reply_message_id:
            await update.edit(templates['translate_reply'])
            return

        reply_message = await update.get_reply_message()
        response = await async_translator.Translate(reply_message.text, to_language)
        await update.edit(f"Translated text:\n\n```{response}```")
    
    elif update.text.startswith('/calc'):
        try:
            expression = update.text[6:].strip()
            if not expression:
                await update.edit(templates['calc_missing'])
                return
            result = eval(expression, {"__builtins__": None}, {})
            await update.edit(f"Result: {result}")
        except Exception as e:
            await update.edit(templates['calc_error'].format(error=str(e)))
    
    elif update.text == '/auto_edit_text':
        auto_edit_text = not auto_edit_text
        await set_setting('auto_edit_text', auto_edit_text)
        status = 'enabled' if auto_edit_text else 'disabled'
        await update.edit(templates['auto_edit_text'].format(status=status))
    
    elif update.text == '/auto_bold':
        auto_bold = not auto_bold
        await set_setting('auto_bold', auto_bold)
        status = 'enabled' if auto_bold else 'disabled'
        await update.edit(templates['auto_bold'].format(status=status))
    
    elif update.text == '/auto_italic':
        auto_italic = not auto_italic
        await set_setting('auto_italic', auto_italic)
        status = 'enabled' if auto_italic else 'disabled'
        await update.edit(templates['auto_italic'].format(status=status))
    
    elif update.text == '/dice':
        dice_roll = random.randint(1, 6)
        await update.edit(templates['dice'].format(number=dice_roll))
    
    elif update.text.startswith('/wikipedia'):
        query = update.text[11:].strip()
        if not query:
            await update.edit(templates['wiki_error'].format(error='No query provided'))
            return

        try:
            import wikipedia
            wikipedia.set_lang(lang)
            result = wikipedia.summary(query[2:].strip() if lang == 'fa' else query, sentences=2)
            await update.edit(f"**Wikipedia Summary:**\n\n{result}")
        except Exception as e:
            await update.edit(templates['wiki_error'].format(error=str(e)))
    
    elif update.text.startswith('/search'):
        query = update.text[8:].strip()
        if not query:
            await update.edit(templates['search_error'].format(error='No query provided'))
            return

        try:
            results = googlesearch.search(query, num_results=5, advanced=True)
            output, count = '', 1
            for result in results:
                output += f"{count}- [{result.title.strip()}]({result.url.strip()})\n\n"
                count += 1
            await update.edit(f"**Google Search Results:**\n\n{output}")
        except Exception as e:
            await update.edit(templates['search_error'].format(error=str(e)))
    
    elif update.text.startswith('/ping '):
        host = update.text[6:].strip()
        if not host:
            await update.edit(templates['ping_host_error'].format(error='No host provided'))
            return

        try:
            result = await tcping(host, 443, timeout=1)
            if result.get('status') == 'up':
                await update.edit(templates['ping_success'].format(latency=result['latency_ms']))
            else:
                await update.edit(templates['ping_failed'])
        except Exception as e:
            await update.edit(templates['ping_host_error'].format(error=str(e)))
    
    elif update.text.startswith('/persian_date'):
        from persiantools.jdatetime import JalaliDate
        jalali_date = JalaliDate.today()
        await update.edit(templates['persian_date'].format(date=jalali_date.strftime("%Y/%m/%d")))
    
    elif update.text.startswith('/english_date'):
        from persiantools.jdatetime import JalaliDate
        jalali_date = JalaliDate.today()
        gregorian_date = jalali_date.to_gregorian()
        await update.edit(templates['english_date'].format(date=gregorian_date.strftime("%Y-%m-%d")))
    
    elif update.text.startswith('/typing on'):
        await set_setting('typing', True)
        await update.edit(templates['typing_status'].format(status='enabled'))
    
    elif update.text.startswith('/typing off'):
        await set_setting('typing', False)
        await update.edit(templates['typing_status'].format(status='disabled'))
    
    elif update.text == '/block':
        if not update.reply_message_id:
            await update.edit(templates['block_no_reply'])
            return
        
        reply_message = await update.get_reply_message()
        if reply_message.author_object_guid:
            try:
                await update.block(reply_message.author_object_guid)
                await update.edit(templates['block_success'].format(guid=reply_message.author_object_guid))
            except Exception as e:
                await update.edit(templates['block_error'].format(error=str(e)))
        else:
            await update.edit(templates['block_no_reply'])
    
    elif update.text.startswith('/block @'):
        username = update.text[8:].strip()
        if not username:
            await update.edit(templates['block_error'].format(error='No username provided'))
            return
        
        try:
            user = await client.get_object_by_username(username)
            if user.exist and user.type == 'User':
                await update.block(user.user.user_guid)
                await update.edit(templates['block_success'].format(guid=user.user.user_guid))
            else:
                await update.edit(templates['block_username_not_found'].format(username=username))
        except Exception as e:
            await update.edit(templates['block_error'].format(error=str(e)))
    
    elif update.text == '/unblock':
        if not update.reply_message_id:
            await update.edit(templates['unblock_no_reply'])
            return
        
        reply_message = await update.get_reply_message()
        if reply_message.author_object_guid:
            try:
                await client.set_block_user(reply_message.author_object_guid, action='Unblock')
                await update.edit(templates['unblock_success'].format(guid=reply_message.author_object_guid))
            except Exception as e:
                await update.edit(templates['unblock_error'].format(error=str(e)))
        else:
            await update.edit(templates['unblock_no_reply'])
    
    elif update.text.startswith('/unblock @'):
        username = update.text[10:].strip()
        if not username:
            await update.edit(templates['unblock_error'].format(error='No username provided'))
            return
        
        try:
            user = await client.get_object_by_username(username)
            if user.exist and user.type == 'User':
                await client.set_block_user(user.user.user_guid, action='Unblock')
                await update.edit(templates['unblock_success'].format(guid=user.user.user_guid))
            else:
                await update.edit(templates['unblock_username_not_found'].format(username=username))
        except Exception as e:
            await update.edit(templates['unblock_error'].format(error=str(e)))
    
    elif update.text.startswith('/set_answer '):
        parts = update.text[12:].strip().split(' ', 1)
        if len(parts) < 2:
            await update.edit(templates['set_answer_missing'])
            return
        
        question, answer = parts
        async with AsyncSessionLocal() as session:
            existing_answer = await session.execute(
                select(Answer).where(Answer.question == question)
            )
            existing_answer = existing_answer.scalars().first()
            if existing_answer:
                existing_answer.answer = answer
            else:
                new_answer = Answer(question=question, answer=answer)
                session.add(new_answer)
            await session.commit()
            await update.edit(templates['set_answer_success'].format(question=question))
    
    elif update.text.startswith('/get_answer '):
        question = update.text[12:].strip()
        if not question:
            await update.edit(templates['get_answer_missing'])
            return
        
        async with AsyncSessionLocal() as session:
            answer = await session.execute(
                select(Answer).where(Answer.question == question)
            )
            answer = answer.scalars().first()
            if answer:
                await update.edit(f"Answer for '{question}': {answer.answer}")
            else:
                await update.edit(templates['get_answer_none'].format(question=question))
    
    elif update.text.startswith('/delete_answer '):
        question = update.text[15:].strip()
        if not question:
            await update.edit(templates['delete_answer_missing'])
            return
        
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                delete(Answer).where(Answer.question == question)
            )
            await session.commit()
            if result.rowcount > 0:
                await update.edit(templates['delete_answer_success'].format(question=question))
            else:
                await update.edit(templates['delete_answer_none'].format(question=question))
    
    elif update.text.startswith('/answer '):
        question = update.text[8:].strip()
        if not question:
            await update.edit(templates['answer_missing'])
            return
        
        async with AsyncSessionLocal() as session:
            answer = await session.execute(
                select(Answer).where(Answer.question == question)
            )
            answer = answer.scalars().first()
            if answer:
                await update.edit(f"Answer: {answer.answer}")
            else:
                await update.edit(templates['answer_none'].format(question=question))
    
    elif update.text == '/clean_answers':
        async with AsyncSessionLocal() as session:
            await session.execute(delete(Answer))
            await session.commit()
        await update.edit(templates['clean_answers'])
    
    elif update.text.startswith('/set_language '):
        language = update.text[13:].strip().lower()
        if language not in ['fa', 'en']:
            await update.edit("⚠️ Please specify a valid language (fa or en).")
            return
        await set_user_language(user_guid, language)
        await update.edit(f"✅ Language set to {'Persian' if language == 'fa' else 'English'}.")
    
    elif update.text.startswith('/ai'):
        response = await http_client.get('https://chatgpt.ehsancoder-as.workers.dev/', params={'text': update.text[4:].strip()})
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                await update.edit(f"Ai Response:\n\n{data['result']}")
            else:
                await update.edit(templates['ai_no_response'])
        else:
            await update.edit(templates['ai_error'])
    
    elif update.text == '/help':
        help_text = (
            "Available Commands:\n"
            "/ping - Check if the bot is alive.\n"
            "/info - Get your profile information.\n"
            "/reset_info - Reset your profile information.\n"
            "/set_bio <new_bio> - Set a new bio for your profile.\n"
            "/get_bio - Get your current bio.\n"
            "/live_time - Show the current live time with updates.\n"
            "/time - Show the current time.\n"
            "/date - Show the current date.\n"
            "/translate <language> - Translate the replied message to the specified language.\n"
            "/calc <expression> - Calculate a mathematical expression.\n"
            "/auto_edit_text - Toggle auto editing of text messages.\n"
            "/auto_bold - Toggle auto bold formatting of text messages.\n"
            "/auto_italic - Toggle auto italic formatting of text messages.\n"
            "/dice - Roll a dice (1-6).\n"
            "/wikipedia <query> - Get a summary from Wikipedia for the given query.\n"
            "/search <query> - Search Google for the given query and return results.\n"
            "/ping <host> - Ping a specified host and return latency.\n"
            "/persian_date - Show the current Persian date.\n"
            "/english_date - Show the current English date.\n"
            "/typing on/off - Enable or disable typing indicator in messages.\n"
            "/block/unblock [@username] or reply to a message to block/unblock users.\n"
            "/set_answer <question> <answer> - Set an answer for a specific question.\n"
            "/get_answer <question> - Get the answer for a specific question.\n"
            "/delete_answer <question> - Delete the answer for a specific question.\n"
            "/answer <question> - Get an answer for a specific question from predefined answers.\n"
            "/clean_answers - Clear all predefined answers.\n"
            "/set_language <fa|en> - Set the bot language (Persian or English).\n"
            "/ai <text> - Get a response from AI based on the provided text.\n\n",
            "Powered by Shayan Heidari:\nhttps://github.com/shayanheidari01/rubika/tree/master/examples/self"
        )
        await update.edit(format_message(help_text, auto_bold, auto_italic))

@client.on_message_updates(filters.regex('^سلام'))
async def handle_hello(update: Update):
    guid = update.object_guid

    # اگر قبلاً این GUID پردازش شده و هنوز توی set هست، اسپم محسوب می‌شه
    if guid in recent_guids:
        return  # نادیده بگیر

    # اضافه کردن GUID به لیست ضداسپم
    recent_guids.add(guid)

    # حذف GUID بعد از SPAM_TIMEOUT ثانیه
    asyncio.create_task(remove_guid_after_delay(guid))

    # انیمیشن ایموجی
    for i in range(30):
        emoji = random.choice([
            "🩷", "❤️", "🧡", "💛", "💚", "🩵", "💙", "💜",
            "🖤", "🩶", "🤍", "🤎", "❤️‍🔥", "❤️‍🩹", "❣",
            "💕", "💞", "💓", "💗", "💖", "💘", "💝", "♥️"
        ])
        await update.edit(f'سلام {emoji}')
        await asyncio.sleep(0.5)

# تابع برای حذف GUID بعد از مدتی
async def remove_guid_after_delay(guid: str):
    await asyncio.sleep(SPAM_TIMEOUT)
    recent_guids.discard(guid)

client.run(init_db())