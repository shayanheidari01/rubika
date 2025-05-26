from rubpy import Client

OBJECT_GUID = ''  # GUID گروه یا کانال موردنظر

with Client('get_all_members') as bot:
    has_continue = True
    next_start_id = None
    total_members = 0

    while has_continue:
        response = bot.get_members(OBJECT_GUID, start_id=next_start_id)

        if not response:
            break  # اگر پاسخ خالی بود، حلقه متوقف شود

        next_start_id = response.next_start_id
        has_continue = response.has_continue
        members = response.in_chat_members or []

        for member in members:
            print(member)
            total_members += 1

    print("Total members:", total_members)
