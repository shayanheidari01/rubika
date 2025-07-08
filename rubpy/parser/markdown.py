import markdownify
import re

MARKDOWN_RE = (
    r'\*\*(.*?)\*\*|`(.*?)`|__(.*?)__|--(.*?)--|~~(.*?)~~|\|\|(.*?)\|\||\[(.*?)\]\((\S+)\)'
)

class Markdown:
    def __init__(self) -> None:
        self.pattern = re.compile(MARKDOWN_RE)

    def to_markdown(self, text: str) -> str:
        return markdownify.markdownify(html=text).strip()

    def to_metadata(self, text: str) -> dict:
        meta_data_parts = []

        while True:
            for markdown in self.pattern.finditer(text):
                string = markdown.group(0)
                span = markdown.span()
                from_index = span[0]

                if string.startswith('**'):
                    text = self.pattern.sub(r'\1', text, count=1)
                    meta_data_parts.append({
                        'type': 'Bold',
                        'from_index': from_index,
                        'length': len(string) - 4,
                    })
                    break
                elif string.startswith('`'):
                    text = self.pattern.sub(r'\2', text, count=1)
                    meta_data_parts.append({
                        'type': 'Mono',
                        'from_index': from_index,
                        'length': len(string) - 4,
                    })
                    break
                elif string.startswith('__'):
                    text = self.pattern.sub(r'\3', text, count=1)
                    meta_data_parts.append({
                        'type': 'Italic',
                        'from_index': from_index,
                        'length': len(string) - 4,
                    })
                    break
                elif string.startswith('--'):
                    text = self.pattern.sub(r'\4', text, count=1)
                    meta_data_parts.append({
                        'type': 'Underline',
                        'from_index': from_index,
                        'length': len(string) - 4,
                    })
                    break
                elif string.startswith('~~'):
                    text = self.pattern.sub(r'\5', text, count=1)
                    meta_data_parts.append({
                        'type': 'Strike',
                        'from_index': from_index,
                        'length': len(string) - 4,
                    })
                    break
                elif string.startswith('||'):
                    text = self.pattern.sub(r'\6', text, count=1)
                    meta_data_parts.append({
                        'type': 'Spoiler',
                        'from_index': from_index,
                        'length': len(string) - 4,
                    })
                    break

                else:
                    text = self.pattern.sub(r'\7', text, count=1)
                    mention_text_object_type = 'hyperlink'
                    mention_type = 'MentionText'
                    mention_text_object_guid = markdown.group(8)
                    length = len(markdown.group(7))

                    if mention_text_object_guid.startswith('u'):
                        mention_text_object_type = 'User'
                    elif mention_text_object_guid.startswith('g'):
                        mention_text_object_type = 'Group'
                    elif mention_text_object_guid.startswith('c'):
                        mention_text_object_type = 'Channel'
                    else:
                        mention_type = 'Link'

                    if mention_type == 'MentionText':
                        meta_data_parts.append({
                            'type': mention_type,
                            'from_index': from_index,
                            'length': length,
                            'mention_text_object_guid': mention_text_object_guid,
                            'mention_text_object_type': mention_text_object_type
                        })
                        break

                    else:
                        meta_data_parts.append({
                            'from_index': from_index,
                            'length': length,
                            'link': {
                                'hyperlink_data': {
                                    'url': mention_text_object_guid,
                                },
                                'type': mention_text_object_type,
                            },
                            'type': mention_type,
                        })
                        break

            else:
                break

        result = {'text': text.strip()}

        if meta_data_parts:
            result['metadata'] = {'meta_data_parts': meta_data_parts}

        return result