grouping = {
    "users": {
        "Values": ["Block", "Unblock"],
        "GetUserInfo": {
            "params": {
                "user_guid": {"types": ["str", "optional"]}
            }
        },
        "SetBlockUser": {
            "params": {
                "user_guid": {"types": "str"},
                "action": {"types": ["str", "optional"], "alloweds": ["Block", "Unblock"], "default": "Block"}
            }
        },
        "DeleteUserChat": {
            "params": {
                "user_guid": {"types": "str"},
                "last_deleted_message_id": {"types": ["str", "int"], "func": "to_string"}
            }
        },
        "CheckUserUsername": {
            "params": {
                "username": {"types": "str"}
            }
        }
    },
    "chats": {
        "Values": ["Mute", "Unmute", "Typing", "Uploading", "Recording", "Text", "Hashtag"],
        "UploadAvatar": {
            "params": {
                "object_guid": {"types": "str"},
                "main_file_id":  {"types": "str"},
                "thumbnail_file_id": {"types": "str"}
            }
        },
        "DeleteAvatar": {
            "params": {
                "object_guid": {"types": "str"},
                "avatar_id": {"types": "str"}
            }
        },
        "GetAvatars": {
            "params": {
                "object_guid": {"types": "str"}
            }
        },
        "GetChats": {
            "params": {
                "start_id": {"types": ["str", "optional"]}
            }
        },
        "SeenChats": {
            "params": {
                "seen_list": {"types": "dict", "func": "to_array"}
            }
        },
        "GetChatAds": {
            "params": {
                "state": {"types": ["int", "str"], "defualt": {"func": "timestamp"}, "func": "to_number"}
            }
        },
        "SetActionChat": {
            "params": {
                "object_guid": {"types": "str"},
                "action": {"types": ["str", "optional"], "alloweds": ["Mute", "Unmute"], "default": "Mute"}
            }
        },
        "GetChatsUpdates": {
            "params": {
                "state": {"types": ["int", "str"], "defualt": {"func": "timestamp"}, "func": "to_number"}
            }
        },
        "SendChatActivity": {
            "params": {
                "object_guid": {"types": "str"},
                "activity": {"types": ["str", "optional"], "alloweds": ["Typing", "Uploading", "Recording"], "default": "Typing"}
            }
        },
        "DeleteChatHistory": {
            "params": {
                "object_guid": {"types": "str"},
                "last_message_id": {"types": ["int", "str"], "func": "to_string"}
            }
        },
        "SearchChatMessages": {
            "params": {
                "object_guid": {"types": "str"},
                "search_text": {"types": "str"},
                "type": {"types": ["str", "optional"], "alloweds": ["Text", "Hashtag"], "default": "Hashtag"}
            }
        }

    },
    "extras": {
        "Values": [],
        "SearchGlobalObjects": {
            "params": {
                "search_text": {"types": "str"}
            }
        },
        "GetAbsObjects": {
            "params": {
                "object_guids": {"types": ["str", "list"], "func": "to_array"}
            }
        },
        "GetObjectByUsername": {
            "params": {
                "username": {"types": "str"}
            }
        },
        "GetLinkFromAppUrl": {
            "params": {
                "app_url": {"types": "str"}
            }
        }
    },
    "groups": {
        "Values": ["Set", "Unset", "SetAdmin", "UnsetAdmin", "Hidden", "Visible", "AddMember", "ViewAdmins", "ViewMembers", "SendMessages", "SetAdmin", "BanMember", "ChangeInfo", "PinMessages", "SetJoinLink", "SetMemberAccess", "DeleteGlobalAllMessages"],
        "AddGroup": {
            "params": {
                "title": {"types": "str"},
                "member_guids": {"types": ["str", "list"], "func": "to_array"}
            }
        },
        "JoinGroup": {
            "params": {
                "link": {"types": "str", "cname": "hash_link", "func": "get_hash_link"}
            }
        },
        "LeaveGroup": {
            "params": {
                "group_guid": {"types": "str"}
            }
        },
        "RemoveGroup": {
            "params": {
                "group_guid": {"types": "str"}
            }
        },
        "GetGroupInfo": {
            "params": {
                "group_guid": {"types": "str"}
            }
        },
        "GetGroupLink": {
            "params": {
                "group_guid": {"types": "str"}
            }
        },
        "SetGroupLink": {
            "params": {
                "group_guid": {"types": "str"}
            }
        },
        "EditGroupInfo": {
            "updated_parameters": True,
            "params": {
                "group_guid": {"types": "str"},
                "updated_parameters": {"types": ["list"], "alloweds": ["title", "description", "slow_mode", "chat_history_for_new_members", "event_messages", "chat_reaction_setting"]},
                "title": {"types": ["str", "optional"]},
                "description": {"types": ["str", "optional"]},
                "slow_mode": {"types": ["int", "str", "optional"]},
                "event_messages": {"types": ["bool", "optional"]},
                "chat_reaction_setting": {"types": ["dict", "optional"]},
                "chat_history_for_new_members": {"types": ["str", "optional"], "alloweds": ["Hidden", "Visible"]},
            }
        },
        "SetGroupAdmin": {
            "params": {
                "group_guid": {"types": "str"},
                "member_guid": {"types": "str"},
                "access_list": {"types": ["str", "list"], "alloweds": ["SetAdmin", "BanMember", "ChangeInfo", "PinMessages", "SetJoinLink", "SetMemberAccess", "DeleteGlobalAllMessages"], "func": "to_array"},
                "action": {"types": ["str", "optional"], "alloweds": ["SetAdmin", "UnsetAdmin"], "default": "SetAdmin"}
            }
        },
        "BanGroupMember": {
            "params": {
                "group_guid": {"types": "str"},
                "member_guid": {"types": "str"},
                "action": {"types": ["str", "optional"], "alloweds": ["Set", "Unset"], "default": "Set"}
            }
        },
        "AddGroupMembers": {
            "params": {
                "group_guid": {"types": "str"},
                "member_guids": {"types": ["str", "list"], "func": "to_array"}
            }
        },
        "GetGroupAllMembers": {
            "params": {
                "group_guid": {"types": "str"},
                "search_text": {"types": ["str", "optional"], "default": ""},
                "start_id": {"types": ["str", "optional"]}
            }
        },
        "GetGroupAdminMembers": {
            "params": {
                "group_guid": {"types": "str"},
                "start_id": {"types": ["str", "optional"]}
            }
        },
        "GetGroupMentionList": {
            "params": {
                "group_guid": {"types": "str"},
                "search_mention": {"types": ["str", "optional"]}
            }
        },
        "GetGroupDefaultAccess": {
            "params": {
                "group_guid": {"types": "str"}

            }
        },
        "SetGroupDefaultAccess": {
            "params": {
                "group_guid": {"types": "str"},
                "access_list": {"types": ["str", "list"], "alloweds": ["AddMember", "ViewAdmins", "ViewMembers", "SendMessages"]}
            }
        },
        "GetBannedGroupMembers": {
            "params": {
                "group_guid": {"types": "str"},
                "start_id": {"types": ["str", "optional"]}
            }
        },
        "GroupPreviewByJoinLink": {
            "params": {
                "link": {"types": "str", "cname": "hash_link", "func": "get_hash_link"}
            }
        },
        "DeleteNoAccessGroupChat": {
            "params": {
                "group_guid": {"types": "str"}
            }
        },
        "GetGroupAdminAccessList": {
            "params": {
                "group_guid": {"types": "str"},
                "member_guid": {"types": "str"}
            }
        },
        "CreateGroupVoiceChat": {
            "params": {
                "group_guid": {"types": "str"},
            }
        },
        "SetGroupVoiceChatSetting": {
            "updated_parameters": True,
            "params": {
                "group_guid": {"types": "str"},
                "voice_chat_id": {"types": "str"},
                "title": {"types": "str"},
                "updated_parameters": {"types": ["list"], "alloweds": ["title"]}
            }
        },
        "LeaveGroupVoiceChat": {
            "params": {
                "chat_guid": {"types": "str"},
                "voice_chat_id": {"types": "str"}
            }
        },
        "GetGroupVoiceChatUpdates": {
            "params": {
                "chat_guid": {"types": "str"},
                "voice_chat_id": {"types": "str"},
                "state": {"types": "int"}
            }
        },
        "SetGroupVoiceChatState": {
            "params": {
                "chat_guid": {"types": "str"},
                "voice_chat_id": {"types": "str"},
                "activity": {"types": "str"}
            }
        },
        "SendGroupVoiceChatActivity": {
            "params": {
                "chat_guid": {"types": "str"},
                "voice_chat_id": {"types": "str"},
                "action": {"types": "str"},
                "participant_object_guid": {"types": "str"}
            }
        },
        "GetGroupVoiceChatParticipants": {
            "params": {
                "chat_guid": {"types": "str"},
                "voice_chat_id": {"types": "str"},
            }
        },
        "DiscardGroupVoiceChat": {
            "params": {
                "group_guid": {"types": "str"},
                "voice_chat_id": {"types": "str"}
            }
        }
    },
    "messages": {
        "Values": [
            "Pin","Unpin", "Text", "Gif", "File", "Image", "Voice", "Music", "Video", "FileInline", "Quiz", "Regular", "FromMin", "FromMax", "Local", "Global"], 
        "SendMessage": {
            "params": {
                "object_guid": {"types": "str"},
                "message": {
                    "types": ["dict", "Struct", "str", "optional"],
                    "ifs": {
                        "str": {"func": "to_metadata", "unpack": True},
                        "otherwise": {"cname": "sticker", "func": "to_array"}
                    }
                },
                "reply_to_message_id": {
                    "types": ["str", "int", "optional"],
                    "func": "to_string"
                },
                "file_inline": {
                    "types": ["Struct", "dict", "optional"],
                    "func": "to_array"
                },
                "type": {"types": ["str", "optional"], "alloweds": ["FileInlineCaption", "FileInline"], "default": "FileInline"},
                "rnd": {"types": ["str", "int", "optional"], "default": {"func": "random_number"}, "func": "to_string"}
            }
        },
        "EditMessage": {
            "params": {
                "object_guid": {"types": "str"},
                "message_id": {"types": ["str", "int"], "func": "to_string"},
                "text": {"types": "str", "func": "to_metadata", "unpack": True}
            }
        },
        "DeleteMessages": {
            "params": {
                "object_guid": {"types": "str"},
                "message_ids": {"types": ["int", "str", "list"], "func": "to_array"},
                "type": {"types": ["str", "optional"], "alloweds": ["Local", "Global"], "default": "Global"}
            }
        },
        "RequestSendFile": {
            "params": {
                "file_name": {"types": "str"},
                "size": {"types": ["str", "int", "float"], "func": "to_number"},
                "mime": {"types": ["str", "optional"], "heirship": ["file_name"], "func": "get_format"}
            }
        },
        "ForwardMessages": {
            "params": {
                "from_object_guid": {"types": "str"},
                "to_object_guid": {"types": "str"},
                "message_ids": {"types": ["int", "str", "list"], "func": "to_array"},
                "rnd": {"types": ["str", "int", "optional"], "default": {"func": "random_number"}, "func": "to_string"}
            }
        },
        "CreatePoll": {
            "params": {
                "object_guid": {"types": "str"},
                "question": {"types": "str",  },
                "options": {"types": "list", "minimum": 2},
                "type": {"types": ["str", "optional"], "alloweds": ["Quiz", "Regular"], "default": "Regular"},
                "is_anonymous": {"types": ["bool", "optional"]},
                "allows_multiple_answers": {"types": ["bool", "optional"]},
                "correct_option_index": {"types": ["str", "int", "optional"], "func": "to_number"},
                "explanation": {"types": ["str", "optional"]},
                "reply_to_message_id": {"types": ["int", "optional"], "default": 0},
                "rnd": {"types": ["str", "int", "optional"], "default": {"func": "random_number"}, "func": "to_string"}
            }
        },
        "VotePoll": {
            "params": {
                "poll_id": {"types": "str"},
                "selection_index": {"types": ["int", "str"], "func": "to_number"}
            }
        },
        "GetPollStatus": {
            "params": {
                "poll_id": {"types": "str"}
            }
        },
        "GetPollOptionVoters": {
            "params": {
                "poll_id": {"types": "str"},
                "selection_index": {"types": ["int", "str"], "func": "to_number"},
                "start_id": {"types": ["str", "optional"]}
            }
        },
        "SetPinMessage": {
            "params": {
                "object_guid": {"types": "str"},
                "message_id": {"types": ["str", "int"], "func": "to_string"},
                "action": {"types": ["str", "optional"], "alloweds": ["Pin", "Unpin"], "default": "Pin"}
            }
        },
        "GetMessagesUpdates": {
            "params": {
                "object_guid": {"types": "str"},
                "state": {"types": ["int", "str"], "defualt": {"func": "timestamp"}, "func": "to_number"}
            }
        },
        "SearchGlobalMessages": {
            "params": {
                "search_text": {"types": "str"},
                "type": {"types": ["str", "optional"], "alloweds": ["Text"], "default": "Text"}
            }
        },
        "ClickMessageUrl": {
            "params": {
                "object_guid": {"types": "str"},
                "message_id": {"types": ["str", "int"], "func": "to_string"},
                "link_url": {"types": "str"}
            }
        },
        "GetMessagesByID": {
            "params": {
                "object_guid": {"types": "str"},
                "message_ids": {"types": ["int", "str", "list"], "func": "to_array"}
            }
        },
        "GetMessages": {
            "params": {
                "object_guid": {"types": "str"},
                "min_id": {"types": ["str", "int"], "func": "to_number"},
                "max_id": {"types": ["str", "int"], "func": "to_number"},
                "sort": {"types": ["str", "optional"], "alloweds": ["FromMin", "FromMax"], "default": "FromMin"},
                "limit": {"types": ["str", "int"], "func": "to_number", "default": 10},
            }
        },
        "GetMessagesInterval": {
            "params": {
                "object_guid": {"types": "str"},
                "middle_message_id": {"types": ["str", "int"], "func": "to_string"},
            }
        },
        "GetMessageShareUrl": {
            "params": {
                "object_guid": {"types": "str"},
                "message_id": {"types": ["str", "int"]},
            }
        },
        "ActionOnMessageReaction": {
            "params": {
                "object_guid": {"types": "str"},
                "message_id": {"types": ["str", "int"], "func": "to_string"},
                "action": {"types": "str", "alloweds": ["Add", "Remove"], "default": "Add"},
                "reaction_id": {"types": ["str", "int", "optional"], "func": "to_string"}
            }
        }
    },
    "channels": {
        "Values": ["Join", "Remove", "Archive", "Set", "Unset"],
        "AddChannel": {
            "params": {
                "title": {"types": "str"},
                "description": {"types": ["str", "optional"]}
            }
        },
        "RemoveChannel": {
            "params": {
                "channel_guid": {"types": "str"}
            }
        },
        "GetChannelInfo": {
            "params": {
                "channel_guid": {"types": "str"}
            }
        },
        "EditChannelInfo": {
            "updated_parameters": True,
            "params": {
                "channel_guid": {"types": "str"},
                "updated_parameters": {"types": ["list"], "alloweds": ["title", "description", "channel_type", "sign_messages"]},
                "title": {"types": "str"},
                "description": {"types": ["str", "optional"]},
                "channel_type": {"types": ["str", "optional"], "alloweds": ["Public", "Private"], "default": "Public" },
                "sign_messages": {"types": ["str", "optional"]}
            }
        },
        "JoinChannelAction": {
            "params": {
                "channel_guid": {"types": "str"},
                "action": {"types": ["str", "optional"], "alloweds": ["Join", "Remove", "Archive"], "default": "Join"}
            }
        },
        "JoinChannelByLink": {
            "params": {
                "link": {"types": "str", "cname": "hash_link", "func": "get_hash_link"}
            }
        },
        "AddChannelMembers": {
            "params": {
                "channel_guid": {"types": "str"},
                "member_guids": {"types": ["str", "list"], "func": "to_array"}
            }
        },
        "BanChannelMember": {
            "params": {
                "channel_guid": {"types": "str"},
                "member_guid": {"types": "str"},
                "action": {"types": ["str", "optional"], "alloweds": ["Set", "Unset"], "default": "Set"}
            }
        },
        "CheckChannelUsername": {
            "params": {
                "username": {"types": "str"}
            }
        },
        "ChannelPreviewByJoinLink": {
            "params": {
                "link": {"types": "str", "cname": "hash_link", "func": "get_hash_link"}
            }
        },
        "GetChannelAllMembers": {
            "params": {
                "channel_guid": {"types": "str"},
                "search_text": {"types": ["str", "optional"]},
                "start_id": {"types": ["str", "optional"]}
            }
        },
        "GetChannelAdminMembers": {
            "params": {
                "channel_guid": {"types": "str"},
                "start_id": {"types": ["str", "optional"]}
            }
        },
        "UpdateChannelUsername": {
            "params": {
                "channel_guid": {"types": "str"},
                "username": {"types": "str"}
            }
        },
        "GetChannelLink": {
            "params": {
                "channel_guid": {"types": "str"}
            }
        },
        "SetChannelLink": {
            "params": {
                "channel_guid": {"types": "str"}
            }
        },
        "GetChannelAdminAccessList": {
            "params": {
                "channel_guid": {"types": "str"},
                "member_guid": {"types": "str"}
            }
        },
        "CreateChannelVoiceChat": {
            "params": {
                "channel_guid": {"types": "str"},
            }
        },
        "SetChannelVoiceChatSetting": {
            "updated_parameters": True,
            "params": {
                "channel_guid": {"types": "str"},
                "voice_chat_id": {"types": "str"},
                "title": {"types": "str"},
                "updated_parameters": {"types": ["list"], "alloweds": ["title"]}
            }
        },
        "DiscardChannelVoiceChat": {
            "params": {
                "channel_guid": {"types": "str"},
                "voice_chat_id": {"types": "str"}
            }
        }
    },
    "contacts": {
        "Values": [],
        "DeleteContact": {
            "params": {
                "user_guid": {"types": "str"}
            }
        },
        "AddAddressBook": {
            "params": {
                "phone": {"types": "str", "func": "get_phone"},
                "first_name": {"types": "str"},
                "last_name": {"types": ["str", "optional"], "default": ""}
            }
        },
        "GetContactsUpdates": {
            "params": {
                "state": {"types": ["int", "str"], "defualt": {"func": "timestamp"}, "func": "to_number"}
            }
        },
        "GetContacts": {
            "params": {
                "start_id": {"types": ["int", "str", "optional"], "func": "to_string"}
            }
        }
    },
    "settings": {
        "Values": ["Nobody", "Everybody", "MyContacts", "Bots", "Groups", "Contacts", "Channels", "NonConatcts"],
        "SetSetting": {
            "updated_parameters": True,
            "params": {
                "updated_parameters": {"types": ["list"], "alloweds": ["show_my_last_online", "show_my_phone_number", "show_my_profile_photo", "link_forward_message", "can_join_chat_by"]},
                "show_my_last_online": {"types": ["str", "optional"], "alloweds": ["Nobody", "Everybody", "MyContacts"]},
                "show_my_phone_number": {"types": ["str", "optional"], "alloweds": ["Nobody", "Everybody", "MyContacts"]},
                "show_my_profile_photo": {"types": ["str", "optional"], "alloweds": ["Everybody", "MyContacts"]},
                "link_forward_message": {"types": ["str", "optional"], "alloweds": ["Nobody", "Everybody", "MyContacts"]},
                "can_join_chat_by": {"types": ["str", "optional"], "alloweds": ["Everybody", "MyContacts"]}
            }
        },
        "AddFolder": {
            "params": {
                "cname": {"types": "str"},
                "include_chat_types": {
                    "types": ["str", "list", "optional"],
                    "alloweds": ["Bots", "Groups", "Contacts", "Channels", "NonConatcts"], "func": "to_array", "default": []},
                "exclude_chat_types": {
                    "types": ["str", "list", "optional"],
                    "alloweds": ["Bots", "Groups", "Contacts", "Channels", "NonConatcts"], "func": "to_array", "default": []},
                "include_object_guids": {"types": ["str", "list", "optional"], "func": "to_array", "default": []},
                "exclude_object_guids": {"types": ["str", "list", "optional"], "func": "to_array", "default": []}
            }
        },
        "GetFolders": {
            "params": {
                "last_state": {"types": ["int", "str"], "defualt": {"func": "timestamp"}, "func": "to_number"}
            }
        },
        "EditFolder": {
            "updated_parameters": True,
            "params": {
                "updated_parameters": {"types": ["list"], "alloweds": ["include_chat_types", "exclude_chat_types", "include_object_guids", "exclude_object_guids"]},
                "cname": {"types": "str"},
                "include_chat_types": {
                    "types": ["str", "list", "optional"],
                    "alloweds": ["Bots", "Groups", "Contacts", "Channels", "NonConatcts"], "func": "to_array", "default": []},
                "exclude_chat_types": {
                    "types": ["str", "list", "optional"],
                    "alloweds": ["Bots", "Groups", "Contacts", "Channels", "NonConatcts"], "func": "to_array", "default": []},
                "include_object_guids": {"types": ["str", "list", "optional"], "func": "to_array", "default": []},
                "exclude_object_guids": {"types": ["str", "list", "optional"], "func": "to_array", "default": []}
            }
        },
        "DeleteFolder": {
            "params": {
                "folder_id": {"types": "str"}
            }
        },
        "UpdateProfile": {
            "updated_parameters": True,
            "params": {
                "updated_parameters": {"types": ["list"], "alloweds": ["first_name", "last_name", "bio"]},
                "first_name": {"types": ["str", "optional"]},
                "last_name": {"types": ["str", "optional"]},
                "bio": {"types": ["str", "optional"]}
            }
        },
        "UpdateUsername": {
            "params": {
                "username": {"types": "str"}
            }
        },
        "GetTwoPasscodeStatus": None,
        "GetSuggestedFolders": None,
        "GetPrivacySetting": None,
        "GetBlockedUsers": None,
        "GetMySessions": None,
        "TerminateSession": {
            "params": {
                "session_key": {"types": "str"}
            }
        },
        "SetupTwoStepVerification": {
            "params": {
                "password": {"types": ["str", "int"], "func": "to_string"},
                "hint": {"types": ["str", "int"], "func": "to_string"},
                "recovery_email": {"types": "str"}
            }
        }
    },
    "stickers": {
        "Values": ["All", "Add", "Remove"],
        "GetMyStickerSets": None,
        "SearchStickers": {
            "params": {
                "search_text": {"types": ["str", "optional"], "default": ""},
                "start_id": {"types": ["str", "optional"]}
            }
        },
        "GetStickerSetByID": {
            "params": {
                "sticker_set_id": {"types": "str"}
            }
        },
        "ActionOnStickerSet": {
            "params": {
                "sticker_set_id": {"types": "str"},
                "action": {"types": ["str", "optional"], "alloweds": ["Add", "Remove"], "default": "Add"}
            }
        },
        "GetStickersByEmoji": {
            "params": {
                "emoji": {"types": "str", "cname": "emoji_character"},
                "suggest_by": {"types": ["str", "optional"], "default": "Add"}
            }
        },
        "GetStickersBySetIDs": {
            "params": {
                "sticker_set_ids": {"types": ["str", "list"], "func": "to_array"}
            }
        },
        "GetTrendStickerSets": {
            "params": {
                "start_id": {"types": ["str", "optional"]}
            }
        }

    },
    "authorisations": {
        "Values": ["SMS", "Internal"],
        "GetDCs": {
            "urls": ["https://getdcmess.iranlms.ir/", "https://getdcmess1.iranlms.ir/", "https://getdcmess2.iranlms.ir/"],
            "encrypt": False,
            "params": {
                "api_version": {"types": ["int", "str"], "func": "to_string", "default": "4"}
            }
        },
        "SignIn": {
            "tmp_session": True,
            "params": {
                "phone_code": {"types": "str"},
                "phone_number": {"types": "str", "func": "get_phone"},
                "phone_code_hash": {"types": "str"},
                "public_key": {"types": "str"},
            }
        },
        "SendCode": {
            "tmp_session": True,
            "params": {
                "phone_number": {"types": "str", "func": "get_phone"},
                "pass_key": {"types": ["str", "optional"], "default": None},
                "send_type": {"types": ["str", "optional"], "alloweds": ["SMS", "Internal"], "default": "SMS"}
            }
        },
        "RegisterDevice": {
            "params": {
                "uaer_agent": {"types": "str", "func": "get_browser", "unpack": True},
                "app_version": {"types": "str"}, 
                "lang_code": {"types": ["str", "optional"], "default": "fa"}
            }
        },
        "LoginDisableTwoStep": {
            "tmp_session": True,
            "params": {
                "phone_number": {"types": "str", "func": "get_phone"},
                "email_code": {"types": ["str", "int"], "func": "to_string"},
                "forget_password_code_hash": {"types": "str"}
            }
        }
    }
}