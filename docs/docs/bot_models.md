تمام مدل‌ها به‌صورت `dataclass` و از پایه‌ی `DictLike` ارث‌بری می‌کنند. همهٔ فیلدها `Optional` هستند تا با payloadهای ناقص یا تغییریافته(در آینده) سازگار باشند. همچنین تمامی این مدل ها از `rubpy.bot.models` در دسترس هستند.

---

## `File`

| فیلد        |             نوع | توضیحات                                                           |
| ----------- | --------------: | ----------------------------------------------------------------- |
| `file_id`   | `Optional[str]` | شناسهٔ یکتأ فایل که سرور بازمی‌گرداند                            |
| `file_name` | `Optional[str]` | نام فایل                                                          |
| `size`      | `Optional[str]` | اندازهٔ فایل (معمولاً بر حسب بایت یا رشته‌ای که API بازمی‌گرداند) |

---

## `Chat`

| فیلد         |                      نوع | توضیحات                 |
| ------------ | -----------------------: | ----------------------- |
| `chat_id`    |          `Optional[str]` | شناسهٔ چت               |
| `chat_type`  | `Optional[ChatTypeEnum]` | نوع چت                  |
| `user_id`    |          `Optional[str]` | شناسهٔ کاربر            |
| `first_name` |          `Optional[str]` | نام کاربر               |
| `last_name`  |          `Optional[str]` | نام خانوادگی کاربر      |
| `title`      |          `Optional[str]` | عنوان (برای گروه/کانال) |
| `username`   |          `Optional[str]` | نام کاربری              |

---

## `ForwardedFrom`

| فیلد             |                           نوع | توضیحات              |
| ---------------- | ----------------------------: | -------------------- |
| `type_from`      | `Optional[ForwardedFromEnum]` | نوع منبع فوروارد     |
| `message_id`     |               `Optional[str]` | شناسهٔ پیام مبدا     |
| `from_chat_id`   |               `Optional[str]` | شناسهٔ چت مبدا       |
| `from_sender_id` |               `Optional[str]` | شناسهٔ فرستندهٔ مبدا |

---

## `PaymentStatus`

| فیلد         |                           نوع | توضیحات              |
| ------------ | ----------------------------: | -------------------- |
| `payment_id` |               `Optional[str]` | شناسهٔ تراکنش/پرداخت |
| `status`     | `Optional[PaymentStatusEnum]` | وضعیت پرداخت (enum)  |

---

## `MessageTextUpdate`

| فیلد         |             نوع | توضیحات                |
| ------------ | --------------: | ---------------------- |
| `message_id` | `Optional[str]` | شناسهٔ پیام ویرایش‌شده |
| `text`       | `Optional[str]` | متن جدید پیام          |

---

## `Bot`

| فیلد            |              نوع | توضیحات               |
| --------------- | ---------------: | --------------------- |
| `bot_id`        |  `Optional[str]` | شناسهٔ ربات           |
| `bot_title`     |  `Optional[str]` | عنوان/نام ربات        |
| `avatar`        | `Optional[File]` | آواتار ربات (فایل)    |
| `description`   |  `Optional[str]` | توضیحات ربات          |
| `username`      |  `Optional[str]` | نام کاربری ربات       |
| `start_message` |  `Optional[str]` | پیام شروع (start)     |
| `share_url`     |  `Optional[str]` | URL اشتراک‌گذاری ربات |

---

## `BotCommand`

| فیلد          |             نوع | توضیحات     |
| ------------- | --------------: | ----------- |
| `command`     | `Optional[str]` | نام فرمان   |
| `description` | `Optional[str]` | توضیح فرمان |

---

## `Sticker`

| فیلد              |              نوع | توضیحات                |
| ----------------- | ---------------: | ---------------------- |
| `sticker_id`      |  `Optional[str]` | شناسهٔ استیکر          |
| `file`            | `Optional[File]` | فایل مربوط به استیکر   |
| `emoji_character` |  `Optional[str]` | ایموجی مرتبط با استیکر |

---

## `ContactMessage`

| فیلد           |             نوع | توضیحات      |
| -------------- | --------------: | ------------ |
| `phone_number` | `Optional[str]` | شماره تلفن   |
| `first_name`   | `Optional[str]` | نام          |
| `last_name`    | `Optional[str]` | نام خانوادگی |

---

## `PollStatus`

| فیلد                   |                        نوع | توضیحات                        |
| ---------------------- | -------------------------: | ------------------------------ |
| `state`                | `Optional[PollStatusEnum]` | وضعیت نظرسنجی (باز/بسته و ...) |
| `selection_index`      |            `Optional[int]` | ایندکس گزینهٔ انتخاب‌شده       |
| `percent_vote_options` |      `Optional[List[int]]` | درصد آرا هر گزینه (لیست)       |
| `total_vote`           |            `Optional[int]` | مجموع آرا                      |
| `show_total_votes`     |           `Optional[bool]` | آیا مجموع آرا نمایش داده شود؟  |

---

## `Poll`

| فیلد          |                    نوع | توضیحات            |
| ------------- | ---------------------: | ------------------ |
| `question`    |        `Optional[str]` | سوال نظرسنجی       |
| `options`     |  `Optional[List[str]]` | گزینه‌ها           |
| `poll_status` | `Optional[PollStatus]` | وضعیت فعلی نظرسنجی |

---

## `Location`

| فیلد        |             نوع | توضیحات                            |
| ----------- | --------------: | ---------------------------------- |
| `longitude` | `Optional[str]` | طول جغرافیایی (رشته/عدد مطابق API) |
| `latitude`  | `Optional[str]` | عرض جغرافیایی (رشته/عدد مطابق API) |

---

## `LiveLocation`

| فیلد               |                                نوع | توضیحات                                |
| ------------------ | ---------------------------------: | -------------------------------------- |
| `start_time`       |                    `Optional[str]` | زمان شروع (timestamp / رشته مطابق API) |
| `live_period`      |                    `Optional[int]` | طول دورهٔ لایو به ثانیه                |
| `current_location` |               `Optional[Location]` | موقعیت فعلی (Location)                 |
| `user_id`          |                    `Optional[str]` | شناسهٔ کاربر ارسال‌کننده               |
| `status`           | `Optional[LiveLocationStatusEnum]` | وضعیت لایو (enum)                      |
| `last_update_time` |                    `Optional[str]` | زمان آخرین آپدیت                       |

---

## `ButtonSelectionItem`

| فیلد        |                                 نوع | توضیحات         |
| ----------- | ----------------------------------: | --------------- |
| `text`      |                     `Optional[str]` | متن آیتم انتخاب |
| `image_url` |                     `Optional[str]` | آدرس تصویر آیتم |
| `type`      | `Optional[ButtonSelectionTypeEnum]` | نوع آیتم (enum) |

---

## `ButtonSelection`

| فیلد                 |                                   نوع | توضیحات                        |
| -------------------- | ------------------------------------: | ------------------------------ |
| `selection_id`       |                       `Optional[str]` | شناسهٔ مجموعهٔ انتخاب          |
| `search_type`        |                       `Optional[str]` | نوع جستجو/فیلتر (رشتهٔ API)    |
| `get_type`           |                       `Optional[str]` | نوع واکشی آیتم‌ها              |
| `items`              | `Optional[List[ButtonSelectionItem]]` | لیست آیتم‌ها                   |
| `is_multi_selection` |                      `Optional[bool]` | آیا چندانتخابی است؟            |
| `columns_count`      |                       `Optional[str]` | تعداد ستون‌ها (رشته مطابق API) |
| `title`              |                       `Optional[str]` | عنوان مجموعهٔ انتخاب           |

---

## `ButtonCalendar`

| فیلد            |                                نوع | توضیحات                     |
| --------------- | ---------------------------------: | --------------------------- |
| `default_value` |                    `Optional[str]` | مقدار پیش‌فرض (مثلاً تاریخ) |
| `type`          | `Optional[ButtonCalendarTypeEnum]` | نوع تقویم/نمایش (enum)      |
| `min_year`      |                    `Optional[str]` | کمینهٔ سال قابل انتخاب      |
| `max_year`      |                    `Optional[str]` | بیشینهٔ سال قابل انتخاب     |
| `title`         |                    `Optional[str]` | عنوان تقویم                 |

---

## `ButtonNumberPicker`

| فیلد            |             نوع | توضیحات                      |
| --------------- | --------------: | ---------------------------- |
| `min_value`     | `Optional[str]` | حداقل مقدار (رشته مطابق API) |
| `max_value`     | `Optional[str]` | حداکثر مقدار                 |
| `default_value` | `Optional[str]` | مقدار پیش‌فرض                |
| `title`         | `Optional[str]` | عنوان پیکر عددی              |

---

## `ButtonStringPicker`

| فیلد            |                   نوع | توضیحات                 |
| --------------- | --------------------: | ----------------------- |
| `items`         | `Optional[List[str]]` | لیست رشته‌ای گزینه‌ها   |
| `default_value` |       `Optional[str]` | مقدار پیش‌فرض           |
| `title`         |       `Optional[str]` | عنوان انتخاب‌گر رشته‌ای |

---

## `ButtonTextbox`

| فیلد            |                                     نوع | توضیحات                   |
| --------------- | --------------------------------------: | ------------------------- |
| `type_line`     |   `Optional[ButtonTextboxTypeLineEnum]` | نوع خط/ورودی (enum)       |
| `type_keypad`   | `Optional[ButtonTextboxTypeKeypadEnum]` | نوع کیپد (enum)           |
| `place_holder`  |                         `Optional[str]` | متن جایگزین (placeholder) |
| `title`         |                         `Optional[str]` | عنوان فیلد متنی           |
| `default_value` |                         `Optional[str]` | مقدار پیش‌فرض             |

---

## `ButtonLocation`

| فیلد                       |                                نوع | توضیحات                |
| -------------------------- | ---------------------------------: | ---------------------- |
| `default_pointer_location` |               `Optional[Location]` | محل اشاره‌گر پیش‌فرض   |
| `default_map_location`     |               `Optional[Location]` | مکان نقشه پیش‌فرض      |
| `type`                     | `Optional[ButtonLocationTypeEnum]` | نوع ورودی مکان (enum)  |
| `title`                    |                    `Optional[str]` | عنوان                  |
| `location_image_url`       |                    `Optional[str]` | تصویر/نقشه مرتبط (URL) |

---

## `AuxData`

| فیلد        |             نوع | توضیحات            |
| ----------- | --------------: | ------------------ |
| `start_id`  | `Optional[str]` | شناسهٔ شروع (کمکی) |
| `button_id` | `Optional[str]` | شناسهٔ دکمهٔ مرتبط |

---

## `JoinChannelData`

| فیلد       |              نوع | توضیحات                                                                 |
| ---------- | ---------------: | ----------------------------------------------------------------------- |
| `username` |  `Optional[str]` | نام کاربری کانال/گروه (در `__post_init__` با حذف `@` نرمال‌سازی می‌شود) |
| `ask_join` | `Optional[bool]` | آیا از کاربر درخواست ملحق شدن شود؟ (پیش‌فرض `False`)                    |

---

## `OpenChatData`

| فیلد          |                      نوع | توضیحات               |
| ------------- | -----------------------: | --------------------- |
| `object_guid` |          `Optional[str]` | شناسهٔ شیٔ (GUID)     |
| `object_type` | `Optional[ChatTypeEnum]` | نوع شی (ChatTypeEnum) |

---

## `ButtonLink`

| فیلد               |                         نوع | توضیحات                                                                                  |
| ------------------ | --------------------------: | ---------------------------------------------------------------------------------------- |
| `type`             |             `Optional[str]` | نوع لینک (رشتهٔ API)                                                                     |
| `link_url`         |             `Optional[str]` | آدرس لینک — در `__post_init__` برخی لینک‌های `rubika.ir` به deep-link نرمال‌سازی می‌شوند |
| `joinchannel_data` | `Optional[JoinChannelData]` | داده‌های join-channel مرتبط                                                              |
| `open_chat_data`   |    `Optional[OpenChatData]` | داده‌های open-chat مرتبط                                                                 |

---

## `Button`

| فیلد                   |                            نوع | توضیحات                     |
| ---------------------- | -----------------------------: | --------------------------- |
| `id`                   |                `Optional[str]` | شناسهٔ دکمه                 |
| `type`                 |     `Optional[ButtonTypeEnum]` | نوع دکمه (enum)             |
| `button_text`          |                `Optional[str]` | متن دکمه                    |
| `button_selection`     |    `Optional[ButtonSelection]` | دادهٔ انتخاب (در صورت وجود) |
| `button_calendar`      |     `Optional[ButtonCalendar]` | تقویم تعبیه‌شده             |
| `button_number_picker` | `Optional[ButtonNumberPicker]` | پیکر عددی                   |
| `button_string_picker` | `Optional[ButtonStringPicker]` | پیکر رشته‌ای                |
| `button_location`      |     `Optional[ButtonLocation]` | ورودی مکان                  |
| `button_textbox`       |      `Optional[ButtonTextbox]` | ورودی متنی                  |
| `button_link`          |         `Optional[ButtonLink]` | لینک/عملیات مرتبط           |

---

## `KeypadRow`

| فیلد      |                      نوع | توضیحات                 |
| --------- | -----------------------: | ----------------------- |
| `buttons` | `Optional[List[Button]]` | لیست دکمه‌ها در یک ردیف |

---

## `Keypad`

| فیلد               |                         نوع | توضیحات                         |
| ------------------ | --------------------------: | ------------------------------- |
| `rows`             | `Optional[List[KeypadRow]]` | ردیف‌های کیپد                   |
| `resize_keyboard`  |            `Optional[bool]` | آیا کیبورد قابل تغییر سایز است؟ |
| `on_time_keyboard` |            `Optional[bool]` | آیا کیبورد موقت/زمانی است؟      |

---

## `MessageKeypadUpdate`

| فیلد            |                نوع | توضیحات                      |
| --------------- | -----------------: | ---------------------------- |
| `message_id`    |    `Optional[str]` | شناسهٔ پیام مورد به‌روزرسانی |
| `inline_keypad` | `Optional[Keypad]` | کیپد جدید اینلاین            |

---

## `MessageId`

| فیلد             |                           نوع | توضیحات                            |
| ---------------- | ----------------------------: | ---------------------------------- |
| `message_id`     |               `Optional[str]` | شناسهٔ پیام قدیمی                  |
| `new_message_id` |               `Optional[str]` | شناسهٔ پیام جدید (در صورت replace) |
| `file_id`        |               `Optional[str]` | شناسهٔ فایل مرتبط                  |
| `chat_id`        |               `Optional[str]` | شناسهٔ چت پیام                     |
| `client`         | `Optional["rubpy.BotClient"]` | ارجاع به کلاینت برای انجام عملیات  |

**متدها (async)**

* `delete()` — حذف پیام (فراخوانی `client.delete_message(chat_id, message_id or new_message_id)`)
* `edit_text(new_text: str)` — ویرایش متن پیام (فراخوانی `client.edit_message_text(chat_id, message_id or new_message_id, new_text)`)

> توجه: برای کارکرد متدها، `client` باید ست شده باشد.

---

## `Message`

| فیلد                  |                           نوع | توضیحات                                     |
| --------------------- | ----------------------------: | ------------------------------------------- |
| `message_id`          |         `Optional[MessageId]` | شناسهٔ پیام (MessageId)                     |
| `text`                |               `Optional[str]` | متن پیام                                    |
| `time`                |               `Optional[int]` | timestamp پیام                              |
| `is_edited`           |              `Optional[bool]` | آیا پیام ویرایش شده؟                        |
| `sender_type`         | `Optional[MessageSenderEnum]` | نوع فرستنده (enum)                          |
| `sender_id`           |               `Optional[str]` | شناسهٔ فرستنده                              |
| `aux_data`            |           `Optional[AuxData]` | داده‌های کمکی مرتبط                         |
| `file`                |              `Optional[File]` | فایل پیوستی (در صورت وجود)                  |
| `reply_to_message_id` |               `Optional[str]` | شناسهٔ پیام که این پیام به آن پاسخ داده شده |
| `forwarded_from`      |     `Optional[ForwardedFrom]` | اطلاعات فوروارد                             |
| `forwarded_no_link`   |               `Optional[str]` | نسخهٔ فوروارد بدون لینک (رشتهٔ API)         |
| `location`            |          `Optional[Location]` | اطلاعات مکان (در صورت وجود)                 |
| `sticker`             |           `Optional[Sticker]` | استیکر (در صورت وجود)                       |
| `contact_message`     |    `Optional[ContactMessage]` | کانتکت (در صورت وجود)                       |
| `poll`                |              `Optional[Poll]` | نظرسنجی (در صورت وجود)                      |
| `live_location`       |      `Optional[LiveLocation]` | موقعیت زنده (در صورت وجود)                  |

---

## `Update`

| فیلد                 |                           نوع | توضیحات                                     |
| -------------------- | ----------------------------: | ------------------------------------------- |
| `type`               |    `Optional[UpdateTypeEnum]` | نوع آپدیت (پیام جدید، ویرایش، حذف و ...)    |
| `chat_id`            |               `Optional[str]` | شناسهٔ چت مرتبط با آپدیت                    |
| `removed_message_id` |               `Optional[str]` | شناسهٔ پیام حذف‌شده (در صورت وجود)          |
| `new_message`        |           `Optional[Message]` | پیام جدید (در رویداد پیام جدید)             |
| `updated_message`    |           `Optional[Message]` | پیام به‌روزرسانی‌شده (در ویرایش)            |
| `updated_payment`    |     `Optional[PaymentStatus]` | به‌روزرسانی وضعیت پرداخت (در رویداد پرداخت) |
| `client`             | `Optional["rubpy.BotClient"]` | ارجاع به کلاینت برای انجام عملیات           |

**متدهای کاربردی (همه async)**

* `reply(text, chat_keypad=None, inline_keypad=None, disable_notification=False, chat_keypad_type=ChatKeypadTypeEnum.NONE, chat_id=None) -> MessageId`
  ارسال متن (فراخوانی `client.send_message`) — به‌صورت خودکار `reply_to_message_id` را از `self.new_message.message_id` می‌گیرد (در صورت وجود).

* `reply_file(...), reply_photo(...), reply_video(...), reply_voice(...), reply_music(...), reply_gif(...)`
  شورت‌کات‌های ارسال فایل با نوع مشخص (فراخوانی `client.send_file` با پارامتر `type`).

* `delete(chat_id=None, message_id=None)` — حذف پیام (فراخوانی `client.delete_message`).

* `download(file_id=None, save_as=None, progress=None, chunk_size=65536, as_bytes=False) -> Union[str, bytes, None]`
  دانلود فایل با امکان ذخیره یا بازگرداندن بایت‌ها (فراخوانی `client.download_file`).

> همهٔ متدها ابتدا بررسی می‌کنند که `self.client` ست شده باشد و در غیر این صورت `ValueError` پرتاب می‌شود.

---

## `InlineMessage`

| فیلد         |                           نوع | توضیحات                                   |
| ------------ | ----------------------------: | ----------------------------------------- |
| `sender_id`  |               `Optional[str]` | شناسهٔ فرستندهٔ اینلاین                   |
| `text`       |               `Optional[str]` | متن                                       |
| `file`       |              `Optional[File]` | فایل پیوست (در صورت وجود)                 |
| `location`   |          `Optional[Location]` | مکان (در صورت وجود)                       |
| `aux_data`   |           `Optional[AuxData]` | دادهٔ کمکی                                |
| `message_id` |               `Optional[str]` | شناسهٔ پیام اینلاین                       |
| `chat_id`    |               `Optional[str]` | شناسهٔ چت/کاربری که پیام را دریافت می‌کند |
| `client`     | `Optional["rubpy.BotClient"]` | ارجاع به کلاینت                           |

**متدهای مشابه `Update` (async)**
`reply`, `reply_file`, `reply_photo`, `reply_voice`, `reply_music`, `reply_gif`, `reply_video`, `delete` — همان کارکرد `Update` را دارند ولی روی `self.chat_id`/`self.message_id` اجرا می‌شوند.
