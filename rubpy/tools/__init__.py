from re import findall
from io import BytesIO
from pybase64 import b64encode
try: from PIL import Image
except ModuleNotFoundError: Image = None


class Tools(object):
	def __init__(self): pass

	def analyzeString(self, text):
		Results = []
		realText = text.replace('**', '').replace('__', '').replace('``', '')

		bolds = findall(r'\*\*(.*?)\*\*', text)
		italics = findall(r'\_\_(.*?)\_\_', text)
		monos = findall(r'\`\`(.*?)\`\`', text)

		for results in bolds:
			bResult = [realText.index(i) for i in bolds]
			for bIndex, bWord in zip(bResult, bolds):
				Results.append({'from_index': bIndex, 'length': len(bWord), 'type': 'Bold'})

		for results in italics:
			iResult = [realText.index(i) for i in italics]
			for iIndex, iWord in zip(iResult, italics):
				Results.append({'from_index': iIndex, 'length': len(iWord), 'type': 'Italic'})

		for results in monos:
			mResult = [realText.index(i) for i in monos]
			for mIndex, mWord in zip(mResult, monos):
				Results.append({'from_index': mIndex, 'length': len(mWord), 'type': 'Mono'})

		return {'metadata': Results, 'string': realText}

	def adsFinder(self, string):
		urls = findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
		if urls != []: return True
		elif '@' in string: return True
		for check in ['.ir', '.com', '.org']:
			if check in string: return True
		else:
			return False

	def is_forward(self, message):
		if 'forwarded_from' in message.keys() and message.get('forwarded_from').get('type_from') == 'Channel': return True

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