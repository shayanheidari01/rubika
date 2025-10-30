FROM python:3.11-slim

# جلوگیری از بافر شدن خروجی و کش pip
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# مسیر کار
WORKDIR /rubika-bot

# کپی پروژه
COPY . .

# نصب ابزارها
RUN pip install --upgrade pip \
    && pip install mkdocs mkdocs-material mdx-include

# پورت پیش‌فرض MkDocs
EXPOSE 8000

# اجرای سرور MkDocs
CMD ["mkdocs", "serve", "-a", "0.0.0.0:8000"]
