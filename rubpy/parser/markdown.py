import markdownify
import re

MARKDOWN_RE = re.compile(r'\*\*(.*?)\*\*|`(.*?)`|__(.*?)__|--(.*?)--|~~(.*?)~~|\|\|(.*?)\|\||\[(.*?)\]\((\S+)\)')

def get_repl(group: str):
    if group.startswith('**'):
        return r'\1'
    elif group.startswith('```'):
        return r'\2'
    elif group.startswith('__'):
        return r'\3'
    elif group.startswith('--'):
        return r'\4'
    elif group.startswith('~~'):
        return r'\5'
    elif group.startswith('||'):
        return r'\6'
    else:
        return r'\7'


class Markdown:
    def __init__(self) -> None:
        pass

    def to_markdown(self, text: str) -> str:
        """
        Convert HTML to Markdown.

        Args:
            - text (str): HTML text.

        Returns:
            - str: Markdown text.
        """
        return markdownify.markdownify(html=text).strip()

    def to_metadata(self, text: str) -> dict:
        """
        Extract metadata from Markdown text.

        Args:
            - text (str): Markdown text.

        Returns:
            - Dict[str, Any]: Dictionary containing 'text' and 'metadata' keys.
        """
        meta_data_parts = []
        text = text.replace('```', '')

        while True:
            for find in MARKDOWN_RE.finditer(text):
                group = find.group()
                span = find.span()
                text: str = MARKDOWN_RE.sub(get_repl(group), text, count=1)

                if group.startswith('**'):
                    meta_data_parts.append({'type': 'Bold', 'from_index': span[0], 'length': len(group) - 4})
                    break

                elif group.startswith('`'):
                    meta_data_parts.append({'type': 'Mono', 'from_index': span[0], 'length': len(group) - 2})
                    break

                elif group.startswith('__'):
                    meta_data_parts.append({'type': 'Italic', 'from_index': span[0], 'length': len(group) - 4})
                    break

                elif group.startswith('--'):
                    meta_data_parts.append({'type': 'Underline', 'from_index': span[0], 'length': len(group) - 4})
                    break

                elif group.startswith('~~'):
                    meta_data_parts.append({'type': 'Strike', 'from_index': span[0], 'length': len(group) - 4})
                    break

                elif group.startswith('||'):
                    meta_data_parts.append({'type': 'Spoiler', 'from_index': span[0], 'length': len(group) - 4})
                    break

                else:
                    length, url = len(find.group(7)), find.group(8)

                    if url.startswith('u'):
                        mention_text_object_type = 'User'
                    elif url.startswith('g'):
                        mention_text_object_type = 'Group'
                    elif url.startswith('c'):
                        mention_text_object_type = 'Channel'
                    else:
                        mention_text_object_type = 'hyperlink'

                    meta_data_part = {'type': 'Link' if mention_text_object_type == 'hyperlink' else 'MentionText', 'from_index': span[0], 'length': length}
                    if mention_text_object_type == 'hyperlink':
                        meta_data_part['link'] = dict(type=mention_text_object_type, hyperlink_data=dict(url=url))

                    else:
                        meta_data_part['mention_text_object_guid'] = url
                        meta_data_part['mention_text_object_type'] = mention_text_object_type

                    meta_data_parts.append(meta_data_part)
                    break

            else:
                break

        result = {'text': text.strip()}

        if meta_data_parts:
            result['metadata'] = {'meta_data_parts': meta_data_parts}

        return result