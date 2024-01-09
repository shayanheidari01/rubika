# filters
- شامل 3 کلاس است که عبارتند از: `Operator`، `BaseModels`، `RegexModel`
###### می توانید از تمام ویژگی های آپدیت استفاده کنید که مهمترین آنها قبلا نوشته شده است...
### مثال ها
```python
async def custom_filter(message, result):
    return result

on_message_updates('hi' != models.raw_text())
on_message_updates(custom_filter != models.raw_text())

on_message_updates(custom_filter == models.time(func=int))

on_message_updates(filters.RegexModel(pattern=r'hi'))
```
##### چند فیلتر (AND)
```python
on_message_updates(
    (15 < filters.time(func=int) > 10)
    &
    filters.RegexModel(pattern=r'hi')
    &
    filters.is_private
)

# or

on_message_updates(
    15 < filters.time(func=int) > 10,
    filters.RegexModel(pattern=r'hi'),
    filters.is_private
)
```
##### چند فیلتر (OR)
```python
on_message_updates(
    filters.is_private
    |
    (filters.author_guid() == 'GUID')
)

# or 

on_message_updates(
    filters.is_private,
    filters.author_guid() == 'GUID',
    __any=True
)

```
