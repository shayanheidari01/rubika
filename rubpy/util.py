from re import finditer, sub, findall
from io import BytesIO
from pybase64 import b64encode
from mutagen.mp3 import MP3
try:
    from tinytag import TinyTag
except ModuleNotFoundError:
    TinyTag = None
try:
    from PIL import Image
except ModuleNotFoundError:
    Image = None


class Utils:
    __slots__ = ()

    def __init__(self):
        pass

    def textParser(self, text):
        try:
            pattern = r'``(.*)``|\*\*(.*)\*\*|__(.*)__|\[(.*)\]\((\S+)\)'
            conflict = 0
            meta_data_parts = []
            for markdown in finditer(pattern, text):
                span = markdown.span()
                if markdown.group(0).startswith('``'):
                    text = sub(pattern, r'\1', text, count=1)
                    meta_data_parts.append(
                        {
                            'type': 'Mono',
                            'from_index': span[0] - conflict,
                            'length': span[1] - span[0] - 2
                        }
                    )
                    conflict += 2

                elif markdown.group(0).startswith('**'):
                    text = sub(pattern, r'\2', text, count=1)
                    meta_data_parts.append(
                        {
                            'type': 'Bold',
                            'from_index': span[0] - conflict,
                            'length': span[1] - span[0] - 4
                        }
                    )
                    conflict += 4

                elif markdown.group(0).startswith('__'):
                    text = sub(pattern, r'\3', text, count=1)
                    meta_data_parts.append(
                        {
                            'type': 'Italic',
                            'from_index': span[0] - conflict,
                            'length': span[1] - span[0] - 4
                        }
                    )
                    conflict += 4

                else:
                    text = sub(pattern, r'\4', text, count=1)

                    mention_text_object_type = 'User'
                    mention_text_object_guid = markdown.group(5)
                    if mention_text_object_guid.startswith('g'):
                        mention_text_object_type = 'Group'

                    elif mention_text_object_guid.startswith('c'):
                        mention_text_object_type = 'Channel'

                    meta_data_parts.append(
                        {
                            'type': 'MentionText',
                            'from_index': span[0] - conflict,
                            'length': len(markdown.group(4)),
                            'mention_text_object_guid': mention_text_object_guid,
                            'mention_text_object_type': mention_text_object_type
                        }
                    )
                    conflict += 4 + len(mention_text_object_guid)

            result = {'text': text.replace('**', '').replace('__', '').replace('``', '')}
            if meta_data_parts:
                result['metadata'] = {
                    'meta_data_parts': meta_data_parts
                }

            return (result.get('metadata').get('meta_data_parts'), result.get('text'))

        except AttributeError:
            return ([], '')

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