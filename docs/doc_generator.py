import inspect
import rubpy
from collections import defaultdict
import re

def sanitize_anchor(text):
    return re.sub(r'[^a-z0-9_]+', '-', text.lower()).strip('-')

def get_public_methods(cls):
    methods = defaultdict(list)

    for name, member in inspect.getmembers(cls):
        if name.startswith("_") or not callable(member):
            continue

        if inspect.ismethod(member) or inspect.isfunction(member):
            kind = "Static"
            if inspect.ismethod(member):
                kind = "Class" if isinstance(getattr(cls, name), classmethod) else "Instance"
            elif isinstance(getattr(cls, name), staticmethod):
                kind = "Static"

            doc = inspect.getdoc(member) or "توضیحی موجود نیست."
            signature = str(inspect.signature(member))
            methods[kind].append({
                "name": name,
                "signature": signature,
                "doc": doc
            })

    return methods

def generate_markdown(method_groups):
    markdown = [
        "# مستندات کلاس `rubpy.Client`",
        "",
        "این سند شامل لیست متدهای عمومی و مستندات آن‌ها است.",
        "",
        "---",
        "## فهرست متدها"
    ]

    for kind in ["Instance", "Class", "Static"]:
        methods = method_groups.get(kind, [])
        if not methods:
            continue
        markdown.append(f"\n**{kind} Methods:**")
        for m in sorted(methods, key=lambda x: x["name"]):
            anchor = sanitize_anchor(m["name"])
            markdown.append(f"\n- [{m['name']}](#{anchor})")

    markdown.append("\n---")

    for kind in ["Instance", "Class", "Static"]:
        methods = method_groups.get(kind, [])
        if not methods:
            continue

        markdown.append(f"\n## متدهای {kind}\n")
        for m in sorted(methods, key=lambda x: x["name"]):
            anchor = sanitize_anchor(m["name"])
            markdown.extend([
                f"<a name=\"{anchor}\"></a>",
                f"### `{m['name']}{m['signature']}`",
                "",
                f"**نوع متد:** {kind}",
                "",
                "```python",
                f"{m['name']}{m['signature']}",
                "```",
                "",
                m["doc"],
                "",
                "---"
            ])

    markdown.append("\n*مستندات به‌صورت خودکار تولید شده‌اند.*")
    return "\n".join(markdown)

if __name__ == "__main__":
    methods = get_public_methods(rubpy.types.Update)
    markdown = generate_markdown(methods)

    with open("update_methods.md", "w", encoding="utf-8") as f:
        f.write(markdown)

    print("فایل مستندات Markdown با فهرست ساده ایجاد شد.")
