from rubpy import Client

OBJECT_GUID = '' # Enter the group or channel GUID

with Client('bot') as bot:
    has_continue = True
    next_start_id = None
    count = 1

    while has_continue:
        result = bot.get_members(OBJECT_GUID, start_id=next_start_id)
        next_start_id = result.next_start_id
        has_continue = result.has_continue
        in_chat_members = result.in_chat_members

        for in_chat_member in in_chat_members:
            print(in_chat_member)
            count += 1

    print(count)
