import re
from typing import Dict, List, Any

import markdownify

# الگوی عبارات منظم برای شناسایی نشانه‌گذاری‌های Markdown
MARKDOWN_RE = re.compile(
    r'```([\s\S]*?)```|\*\*(.*?)\*\*|`(.*?)`|__(.*?)__|--(.*?)--|~~(.*?)~~|\|\|(.*?)\|\||\[(.*?)\]\((\S+)\)',
    flags=re.DOTALL
)

# نگاشت نوع نشانه‌گذاری به گروه مربوطه در الگوی رجکس
MARKDOWN_TYPES = {
    '```': ('Pre', 1),
    '**': ('Bold', 2),
    '`': ('Mono', 3),
    '__': ('Italic', 4),
    '--': ('Underline', 5),
    '~~': ('Strike', 6),
    '||': ('Spoiler', 7),
    '[': ('Link', 8)
}

def java_like_length(text: str) -> int:
    """
    محاسبه طول رشته بر اساس واحدهای UTF-16 (شبیه جاوا).

    پارامترها:
    - text: رشته ورودی.

    خروجی:
    تعداد واحدهای کاراکتر UTF-16.
    """
    return len(text.encode('utf-16-be')) // 2

class Markdown:
    """کلاس برای پردازش و استخراج متادیتا از متن Markdown با رفتار شبیه جاوا."""

    def to_markdown(self, text: str) -> str:
        """
        Convert HTML to Markdown.

        Args:
            - text (str): HTML text.

        Returns:
            - str: Markdown text.
        """
        return markdownify.markdownify(html=text).strip()

    def to_metadata(self, text: str) -> Dict[str, Any]:
        """
        استخراج متادیتا از متن Markdown با محاسبه شاخص‌ها به سبک جاوا.

        پارامترها:
        - text: متن Markdown.

        خروجی:
        دیکشنری حاوی متن ساده و متادیتا (در صورت وجود).
        """
        meta_data_parts: List[Dict[str, Any]] = []
        current_text = text
        offset = 0  # برای ردیابی تغییرات شاخص‌ها در واحدهای UTF-16
        char_offset = 0  # برای ردیابی تغییرات شاخص‌ها در واحدهای کاراکتر پایتون

        matches = list(MARKDOWN_RE.finditer(text))
        for match in matches:
            group = match.group(0)
            start, end = match.span()
            adjusted_start = java_like_length(text[:start]) - offset
            adjusted_char_start = start - char_offset

            # شناسایی نوع نشانه‌گذاری
            for prefix, (md_type, group_idx) in MARKDOWN_TYPES.items():
                if group.startswith(prefix):
                    content = match.group(group_idx)
                    content_length = java_like_length(content)  # طول محتوای خالص در UTF-16
                    meta_data_part = {
                        'type': md_type,
                        'from_index': adjusted_start,
                        'length': content_length
                    }

                    if md_type == 'Pre':
                        # استخراج زبان برای بلوک کد
                        lines = content.split('\n', 1)
                        language = lines[0].strip() if lines[0].strip() else ''
                        meta_data_part['language'] = language
                    elif md_type == 'Link':
                        # پردازش لینک‌ها و منشن‌ها
                        url = match.group(9)
                        mention_types = {'u': 'User', 'g': 'Group', 'c': 'Channel'}
                        mention_type = mention_types.get(url[0], 'hyperlink')

                        if mention_type == 'hyperlink':
                            meta_data_part['link'] = {'type': mention_type, 'hyperlink_data': {'url': url}}
                        else:
                            meta_data_part['type'] = 'MentionText'
                            meta_data_part['mention_text_object_guid'] = url
                            meta_data_part['mention_text_object_type'] = mention_type

                    meta_data_parts.append(meta_data_part)

                    # جایگزینی نشانه‌گذاری با متن خالص و به‌روزرسانی متن و آفست
                    markup_length = java_like_length(group)  # طول کل نشانه‌گذاری در UTF-16
                    char_markup_length = end - start  # طول کل نشانه‌گذاری در کاراکترهای پایتون
                    current_text = current_text[:adjusted_char_start] + content + current_text[end - char_offset:]
                    offset += markup_length - content_length
                    char_offset += char_markup_length - len(content)
                    break

        result = {'text': current_text.strip()}
        if meta_data_parts:
            result['metadata'] = {'meta_data_parts': meta_data_parts}
        
        return result