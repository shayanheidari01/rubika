from re import findall
try: from PIL import Image
except ModuleNotFoundError: Image = None
from io import BytesIO
from pybase64 import b64encode
from mutagen.mp3 import MP3
try: from tinytag import TinyTag
except ModuleNotFoundError: TinyTag = None


class Utils:
    __slots__ = ()
    def __init__(self):
        pass

    def textParser(self, text,):
        results = []
        real_text = text.replace('**', '').replace('__', '').replace('``', '')

        bolds = findall(r'\*\*(.*?)\*\*', text)
        italics = findall(r'\_\_(.*?)\_\_', text)
        monos = findall(r'\`\`(.*?)\`\`', text)
        mResult = [real_text.index(i) for i in monos]
        bResult = [real_text.index(i) for i in bolds]
        iResult = [real_text.index(i) for i in italics]

        for bIndex, bWord in zip(bResult, bolds):
            results.append({
				'from_index' : bIndex,
				'length' : len(bWord),
				'type' : 'Bold'
			})

        for iIndex, iWord in zip(iResult, italics):
            results.append({
				'from_index' : iIndex,
				'length' : len(iWord),
				'type' : 'Italic'
			})

        for mIndex, mWord in zip(mResult, monos):
            results.append({
				'from_index' : mIndex,
				'length' : len(mWord),
				'type' : 'Mono'
			})

        return (results, real_text)

    def adsFinder(self, string):
        urls = findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
        if urls != []: return True
        elif '@' in string: return True
        for check in ['.ir', '.com', '.org']:
            if check in string: return True
        else:
            return False

    def is_forward(self, message):
        try:
            if 'forwarded_from' in message.keys() and message.get('forwarded_from').get('type_from') == 'Channel':
                return True
            else:
                return False
        except KeyError:
            message = message.get('message')
            if 'forwarded_from' in message.keys() and message.get('forwarded_from').get('type_from') == 'Channel':
                return True
            else:
                return False

    def getImageSize(self, image_bytes):
        if Image != None:
            image = Image.open(BytesIO(image_bytes))
            return image.size
        else:
            raise ImportWarning('Please install <pillow> and try again')

    def getThumbnail(self, image_bytes):
        if Image != None:
            image = Image.open(BytesIO(image_bytes))
            width, height = image.size
            if height > width:
                new_height = 40
                new_width  = round(new_height * width / height)
            else:
                new_width = 40
                new_height = round(new_width * height / width)
            image = image.resize((new_width, new_height), Image.ANTIALIAS)
            changed_image = BytesIO()
            image.save(changed_image, format='PNG')
            return b64encode(changed_image.getvalue())
        else:
            raise ImportWarning('Please install <pillow> and try again')

    async def get_voice_duration(self, file_bytes):
        file = BytesIO()
        file.write(file_bytes)
        file.seek(0)
        audio = MP3(file)
        return audio.info.length

    async def getVideoDuration(self, video):
        if TinyTag != None:
            duration = TinyTag.get(video).duration
            return round(duration * 1000)
        else:
            raise ImportWarning('Plaese install <TinyTag> and try again')

    async def getMusicArtist(self, music_bytes):
        return str(TinyTag.get(music_bytes).artist)

    async def getMimeFromURL(self, url):
        if '?' in url:
            return url.split('/')[-1].split('?')[0].split('.')[-1]
        elif '.' in url:
            return url.split('.')[-1]
        else:
            return '.unknown'

    async def thumb_inline(self):
        return 'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAIAAAADnC86AAAAL0lEQVR4nO3NQQ0AAAgEIPVz/Rsbw81BATpJXZiTVSwWi8VisVgsFovFYrFY/DRelEIAZd5yXa4AAAAASUVORK5CYII='