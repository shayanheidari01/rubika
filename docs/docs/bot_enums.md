در ماژول `rubpy.bot.enums` مجموعه‌ای از Enumها تعریف شده که در مدل‌ها و منطق بات استفاده می‌شوند.

---

## فهرست Enumها و اعضای آن‌ها

### `ChatTypeEnum`
| عضو | مقدار |
|---|---:|
| `USER` | `"User"` |
| `BOT` | `"Bot"` |
| `GROUP` | `"Group"` |
| `CHANNEL` | `"Channel"` |

**توضیح:** نمایانگر نوع چت — کاربر عادی، ربات، گروه یا کانال.

---

### `ForwardedFromEnum`
| عضو | مقدار |
|---|---:|
| `USER` | `"User"` |
| `CHANNEL` | `"Channel"` |
| `BOT` | `"Bot"` |

**توضیح:** مشخص‌کنندهٔ منبع یک پیام فورواردشده.

---

### `PaymentStatusEnum`
| عضو | مقدار |
|---|---:|
| `Paid` | `"Paid"` |
| `NotPaid` | `"NotPaid"` |

**توضیح:** وضعیت پرداخت (پرداخت شده یا نشده).

---

### `PollStatusEnum`
| عضو | مقدار |
|---|---:|
| `OPEN` | `"Open"` |
| `CLOSED` | `"Closed"` |

**توضیح:** وضعیت نظرسنجی.

---

### `LiveLocationStatusEnum`
| عضو | مقدار |
|---|---:|
| `STOPPED` | `"Stopped"` |
| `LIVE` | `"Live"` |

**توضیح:** وضعیت موقعیت زنده (قطع/فعال).

---

### `ButtonSelectionTypeEnum`
| عضو | مقدار |
|---|---:|
| `TextOnly` | `"TextOnly"` |
| `TextImgThu` | `"TextImgThu"` |
| `TextImgBig` | `"TextImgBig"` |

**توضیح:** نحوهٔ نمایش آیتم‌های انتخاب (فقط متن، تصویر کوچک+متن، تصویر بزرگ+متن).

---

### `ButtonSelectionSearchEnum`
| عضو | مقدار |
|---|---:|
| `NONE` | `"None"` |
| `Local` | `"Local"` |
| `Api` | `"Api"` |

**توضیح:** منشأ جستجو برای آیتم‌های انتخاب (بدون جستجو، محلی، یا از API).

---

### `ButtonSelectionGetEnum`
| عضو | مقدار |
|---|---:|
| `Local` | `"Local"` |
| `Api` | `"Api"` |

**توضیح:** روش واکشی آیتم‌ها (محلی یا از API).

---

### `ButtonCalendarTypeEnum`
| عضو | مقدار |
|---|---:|
| `DatePersian` | `"DatePersian"` |
| `DateGregorian` | `"DateGregorian"` |

**توضیح:** نوع تقویم مورد استفاده در ButtonCalendar.

---

### `ButtonTextboxTypeKeypadEnum`
| عضو | مقدار |
|---|---:|
| `STRING` | `"String"` |
| `NUMBER` | `"Number"` |

**توضیح:** نوع کیپد برای ورودی متنی: رشته یا عدد.

---

### `ButtonTextboxTypeLineEnum`
| عضو | مقدار |
|---|---:|
| `SingleLine` | `"SingleLine"` |
| `MultiLine` | `"MultiLine"` |

**توضیح:** تک‌خطی یا چندخطی بودن ورودی متنی.

---

### `ButtonLocationTypeEnum`
| عضو | مقدار |
|---|---:|
| `PICKER` | `"Picker"` |
| `VIEW` | `"View"` |

**توضیح:** حالت نمایش/تعامل نقشه (انتخاب نقطه یا مشاهده).

---

### `ButtonTypeEnum`
| عضو | مقدار |
|---|---:|
| `SIMPLE` | `"Simple"` |
| `SELECTION` | `"Selection"` |
| `CALENDAR` | `"Calendar"` |
| `NumberPicker` | `"NumberPicker"` |
| `StringPicker` | `"StringPicker"` |
| `LOCATION` | `"Location"` |
| `PAYMENT` | `"Payment"` |
| `CameraImage` | `"CameraImage"` |
| `CameraVideo` | `"CameraVideo"` |
| `GalleryImage` | `"GalleryImage"` |
| `GalleryVideo` | `"GalleryVideo"` |
| `FILE` | `"File"` |
| `AUDIO` | `"Audio"` |
| `RecordAudio` | `"RecordAudio"` |
| `MyPhoneNumber` | `"MyPhoneNumber"` |
| `MyLocation` | `"MyLocation"` |
| `Textbox` | `"Textbox"` |
| `LINK` | `"Link"` |
| `AskMyPhoneNumber` | `"AskMyPhoneNumber"` |
| `AskLocation` | `"AskLocation"` |
| `BARCODE` | `"Barcode"` |

**توضیح:** انواع مختلف دکمه‌ها که در کیپدها پشتیبانی می‌شود.

---

### `ButtonLinkTypeEnum`
| عضو | مقدار |
|---|---:|
| `URL` | `"url"` |
| `JoinChannel` | `"joinchannel"` |

**توضیح:** نوع لینک‌های قابل استفاده در دکمه‌ها.

---

### `MessageSenderEnum`
| عضو | مقدار |
|---|---:|
| `USER` | `"User"` |
| `BOT` | `"Bot"` |

**توضیح:** نوع فرستندهٔ پیام.

---

### `UpdateTypeEnum`
| عضو | مقدار |
|---|---:|
| `UpdatedMessage` | `"UpdatedMessage"` |
| `NewMessage` | `"NewMessage"` |
| `RemovedMessage` | `"RemovedMessage"` |
| `StartedBot` | `"StartedBot"` |
| `StoppedBot` | `"StoppedBot"` |
| `UpdatedPayment` | `"UpdatedPayment"` |

**توضیح:** انواع رویدادهای آپدیت که API می‌تواند ارسال کند.

---

### `ChatKeypadTypeEnum`
| عضو | مقدار |
|---|---:|
| `NONE` | `"None"` |
| `NEW` | `"New"` |
| `REMOVE` | `"Remove"` |

**توضیح:** نوع عملیات بر روی کیپد چت (هیچ، جدید، حذف).

---

### `UpdateEndpointTypeEnum`
| عضو | مقدار |
|---|---:|
| `ReceiveUpdate` | `"ReceiveUpdate"` |
| `ReceiveInlineMessage` | `"ReceiveInlineMessage"` |
| `ReceiveQuery` | `"ReceiveQuery"` |
| `GetSelectionItem` | `"GetSelectionItem"` |
| `SearchSelectionItems` | `"SearchSelectionItems"` |

**توضیح:** انواع endpointهایی که بات می‌تواند برای webhook ثبت کند.

---

## نمونۀ استفاده

```python
from rubpy.bot.enums import ChatTypeEnum, UpdateTypeEnum

# مقایسه با مقدار دریافتی از API (رشته‌ای)
if chat.chat_type == ChatTypeEnum.USER:
    print("This is a user chat")

# گرفتن مقدار متنی برای ارسال به API
payload = {"chat_keypad_type": ChatKeypadTypeEnum.NEW}

# استفاده در بررسی نوع آپدیت
if update.type == UpdateTypeEnum.NewMessage:
    # handle new message
    pass
```