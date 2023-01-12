from rubpy import Client, Methods

app = Client(auth='your_auth')
group_guid = 'your_group_guid'

# *************
# *** Guide ***
# In line 3, enter
# the AUTH of your user account
# that is an administrator/admin in your group
# In line 4, enter your group's
# GUID and then run source to
# clear your group's blacklist
# *** Guide ***
# *************

async def Deleter(bot: Methods) -> None:
    while True:
        BannedGroupMembers = await bot.getBannedGroupMembers(group_guid=group_guid)
        in_chat_members = BannedGroupMembers.get('in_chat_members')
        if in_chat_members == []:
            exit(0)
        else:
            for member in in_chat_members:
                member_guid = member.get('member_guid')
                await bot.banGroupMember(
                    group_guid=group_guid, member_guid=member_guid, action='Unset')

app.run(Deleter)