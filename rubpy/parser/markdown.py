import re
from typing import Dict, List, Any

import markdownify

MARKDOWN_RE = re.compile(
    r"(?:^(?:> ?[^\n]*\n?)+)|```([\s\S]*?)```|\*\*([^\n*]+?)\*\*|`([^\n`]+?)`|__([^\n_]+?)__|--([^\n-]+?)--|~~([^\n~]+?)~~|\|\|([^\n|]+?)\|\||\[([^\]]+?)\]\((\S+)\)",
    flags=re.DOTALL | re.MULTILINE,
)

MARKDOWN_TYPES = {
    ">": ("Quote", None),
    "```": ("Pre", 1),
    "**": ("Bold", 2),
    "`": ("Mono", 3),
    "__": ("Italic", 4),
    "--": ("Underline", 5),
    "~~": ("Strike", 6),
    "||": ("Spoiler", 7),
    "[": ("Link", 8),
}

MENTION_PREFIX_TYPES = {"u": "User", "g": "Group", "c": "Channel", "b": "Bot"}

MARKDOWN_TYPE_SEQUENCE = tuple(MARKDOWN_TYPES.items())


def _build_utf16_prefix_lengths(text: str) -> List[int]:
    prefix_lengths = [0]
    total = 0
    append = prefix_lengths.append
    for char in text:
        total += 2 if ord(char) > 0xFFFF else 1
        append(total)
    return prefix_lengths


class Markdown:
    def to_markdown(self, text: str) -> str:
        return markdownify.markdownify(html=text).strip()

    def to_metadata(self, text: str) -> Dict[str, Any]:
        meta_data_parts: List[Dict[str, Any]] = []
        current_text = text
        offset = 0
        char_offset = 0
        utf16_prefix = _build_utf16_prefix_lengths(text)

        for match in MARKDOWN_RE.finditer(text):
            group = match.group(0)
            start, end = match.span()
            adjusted_start = utf16_prefix[start] - offset
            adjusted_char_start = start - char_offset

            for prefix, (md_type, group_idx) in MARKDOWN_TYPE_SEQUENCE:
                if group.startswith(prefix):
                    if md_type == "Quote":
                        quote_lines = group.split('\n')
                        content_lines = []
                        for line in quote_lines:
                            if line.startswith('> '):
                                content_lines.append(line[2:])
                            elif line.startswith('>'):
                                content_lines.append(line[1:])
                            else:
                                content_lines.append(line)
                        content = '\n'.join(content_lines)
                        content_length = len(content.encode("utf-16-be")) // 2
                        char_content_length = len(content)
                        
                        inner_metadata = self.to_metadata(content)
                        content = inner_metadata["text"]
                        content_length = len(content.encode("utf-16-be")) // 2
                        char_content_length = len(content)
                        
                        if "metadata" in inner_metadata:
                            for part in inner_metadata["metadata"]["meta_data_parts"]:
                                part["from_index"] += adjusted_start
                                meta_data_parts.append(part)
                    else:
                        group_start = match.start(group_idx)
                        group_end = match.end(group_idx)
                        if group_start == -1 or group_end == -1:
                            content = ""
                            content_length = 0
                            char_content_length = 0
                        else:
                            content = match.group(group_idx) or ""
                            content_length = utf16_prefix[group_end] - utf16_prefix[group_start]
                            char_content_length = group_end - group_start
                            
                            if md_type not in ("Pre", "Link"):
                                inner_metadata = self.to_metadata(content)
                                content = inner_metadata["text"]
                                content_length = len(content.encode("utf-16-be")) // 2
                                char_content_length = len(content)
                                
                                if "metadata" in inner_metadata:
                                    for part in inner_metadata["metadata"]["meta_data_parts"]:
                                        part["from_index"] += adjusted_start
                                        meta_data_parts.append(part)
                    
                    meta_data_part = {
                        "type": md_type,
                        "from_index": adjusted_start,
                        "length": content_length,
                    }

                    if md_type == "Pre":
                        lines = content.split("\n", 1)
                        language = lines[0].strip() if lines[0].strip() else ""
                        meta_data_part["language"] = language
                    elif md_type == "Link":
                        url = match.group(9)
                        mention_type = MENTION_PREFIX_TYPES.get(url[0], "hyperlink")

                        if mention_type == "hyperlink":
                            meta_data_part["link_url"] = url
                            meta_data_part["link"] = {
                                "type": mention_type,
                                "hyperlink_data": {"url": url},
                            }
                        else:
                            meta_data_part["type"] = "MentionText"
                            meta_data_part["mention_text_object_guid"] = url
                            meta_data_part["mention_text_user_id"] = url
                            meta_data_part["mention_text_object_type"] = mention_type

                    meta_data_parts.append(meta_data_part)

                    markup_length = utf16_prefix[end] - utf16_prefix[start]
                    char_markup_length = end - start
                    current_text = (
                        current_text[:adjusted_char_start]
                        + content
                        + current_text[end - char_offset :]
                    )
                    offset += markup_length - content_length
                    char_offset += char_markup_length - char_content_length
                    break

        result = {"text": current_text.strip()}
        if meta_data_parts:
            result["metadata"] = {"meta_data_parts": meta_data_parts}

        return result