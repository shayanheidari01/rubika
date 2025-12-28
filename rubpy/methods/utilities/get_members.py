from typing import Awaitable, Callable, Dict, Optional, Tuple

import rubpy

class GetMembers:
    async def get_members(
        self: "rubpy.Client",
        object_guid: str,
        start_id: Optional[str] = None,
        search_text: Optional[str] = None,
    ) -> "rubpy.types.Update":
        """
        Get members of a group or channel.

        Args:
        - object_guid (str): The GUID of the group or channel.
        - start_id (int, optional): The starting ID for fetching members.
        - search_text (str, optional): The text to search for among members.

        Returns:
        - rubpy.types.Update: An Update object containing information about the members.

        Raises:
        - ValueError: If the object_guid does not start with 'c0' or 'g0'.
        """

        if not isinstance(object_guid, str):
            raise TypeError("object_guid must be a string")

        normalized_guid = object_guid.strip()
        if not normalized_guid:
            raise ValueError("object_guid cannot be empty")

        handler_map: Dict[str, Tuple[
            Callable[..., Awaitable["rubpy.types.Update"]],
            str,
        ]] = {
            "c0": (self.get_channel_all_members, "channel_guid"),
            "g0": (self.get_group_all_members, "group_guid"),
        }

        handler_tuple = handler_map.get(normalized_guid[:2])
        if handler_tuple is None:
            raise ValueError("Invalid object_guid. Must start with 'c0' or 'g0'.")

        handler, guid_keyword = handler_tuple

        normalized_start_id = str(start_id).strip() if start_id is not None else None
        if normalized_start_id == "":
            normalized_start_id = None

        normalized_search = None
        if isinstance(search_text, str):
            normalized_search = search_text.strip() or None

        return await handler(
            **{
                guid_keyword: normalized_guid,
                "start_id": normalized_start_id,
                "search_text": normalized_search,
            }
        )
