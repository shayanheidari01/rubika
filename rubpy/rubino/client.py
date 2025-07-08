from random import random
import os
from typing import Dict, Union

from .. import exceptions
from ..types import Update
import rubpy

class Rubino:
    DEFAULT_PLATFORM = {
        'app_name': 'Main',
        'app_version': '4.4.6',
        'platform': 'PWA',
        'package': 'web.rubika.ir',
    }

    def __init__(self, client: 'rubpy.Client') -> None:
        self.client = client
        self.url = 'https://rubino1.iranlms.ir/'

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args, **kwargs):
        return

    async def _execute_request(self, method: str, data: Dict[str, Union[int, str, bool]]) -> Update:
        result = await self.client.connection.send(
            api_version='0',
            input=data,
            method=method,
            url=self.url,
            client=self.DEFAULT_PLATFORM,
        )

        if result.get('status') == 'OK':
            return Update(result.get('data'))
        else:
            raise exceptions.ErrorAction(result.get('status_det'))

    async def _follow_unfollow_helper(self, f_type: str, followee_id: str, profile_id: str) -> dict:
        return await self._execute_request(
            'requestFollow',
            {
                'f_type': f_type,
                'followee_id': followee_id,
                'profile_id': profile_id
            })

    async def get_profile_list(self, limit: int = 10, sort: str = 'FromMax', equal: bool = False) -> dict:
        return await self._execute_request('getProfileList', {'limit': limit, 'sort': sort, 'equal': equal})

    async def follow(self, followee_id: str, profile_id: str) -> dict:
        return await self._follow_unfollow_helper('Follow', followee_id, profile_id)

    async def unfollow(self, followee_id: str, profile_id: str) -> dict:
        return await self._follow_unfollow_helper('Unfollow', followee_id, profile_id)

    async def get_my_profile_info(self, profile_id: str = None) -> dict:
        return await self._execute_request('getMyProfileInfo', {'profile_id': profile_id})

    async def create_page(self, **kwargs) -> dict:
        return await self._execute_request('createPage', {**kwargs})

    async def update_profile(self, **kwargs) -> dict:
        return await self._execute_request('updateProfile', {**kwargs})

    async def is_exist_username(self, username: str) -> dict:
        return await self._execute_request('isExistUsername', {'username': username.replace('@', '')})

    async def get_post_by_share_link(self, share_link: str, profile_id: str = None) -> dict:
        return await self._execute_request('getPostByShareLink', {'share_string': share_link.split('/')[-1], 'profile_id': profile_id})

    async def add_comment(self, text: str, post_id: str, post_profile_id: str, profile_id: str) -> dict:
        return await self._execute_request('addComment', {'content': text, 'post_id': post_id,
                                                   'post_profile_id': post_profile_id,
                                                   'rnd': int(random() * 1e10),
                                                   'profile_id': profile_id})

    async def _like_unlike_helper(self, action_type: str, post_id: str, post_profile_id: str, profile_id: str) -> dict:
        return await self._execute_request('likePostAction', {'action_type': action_type,
                                                      'post_id': post_id,
                                                      'post_profile_id': post_profile_id,
                                                      'profile_id': profile_id})

    async def like(self, post_id: str, post_profile_id: str, profile_id: str) -> dict:
        return await self._like_unlike_helper('Like', post_id, post_profile_id, profile_id)

    async def unlike(self, post_id: str, post_profile_id: str, profile_id: str) -> dict:
        return await self._like_unlike_helper('Unlike', post_id, post_profile_id, profile_id)

    async def view(self, post_id: str, post_profile_id: str) -> dict:
        return await self._execute_request('addPostViewCount', {'post_id': post_id, 'post_profile_id': post_profile_id})

    # ... (previous code)

    async def get_comments(self, post_id: str, profile_id: str, post_profile_id: str,
                           limit: int = 50, sort: str = 'FromMax', equal: bool = False) -> dict:
        return await self._execute_request('getComments', {
            'equal': equal,
            'limit': limit,
            'sort': sort,
            'post_id': post_id,
            'profile_id': profile_id,
            'post_profile_id': post_profile_id
        })

    async def get_recent_following_posts(self, profile_id: str, limit: int = 30,
                                         sort: str = 'FromMax', equal: bool = False) -> dict:
        return await self._execute_request('getRecentFollowingPosts', {
            'equal': equal,
            'limit': limit,
            'sort': sort,
            'profile_id': profile_id
        })

    async def get_profile_posts(self, target_profile_id: str, profile_id: str,
                                limit: int = 50, sort: str = 'FromMax', equal: bool = False) -> dict:
        return await self._execute_request('getRecentFollowingPosts', {
            'equal': equal,
            'limit': limit,
            'sort': sort,
            'profile_id': profile_id,
            'target_profile_id': target_profile_id
        })

    async def get_profiles_stories(self, profile_id: str, limit: int = 100) -> dict:
        return await self._execute_request('getProfilesStories', {
            'limit': limit,
            'profile_id': profile_id
        })

    async def request_upload_file(self, profile_id: str, file_name: str,
                                  file_size: int, file_type: str) -> dict:
        return await self._execute_request('requestUploadFile', {
            'file_name': file_name.split('/')[-1],
            'file_size': file_size,
            'file_type': file_type,
            'profile_id': profile_id
        })

    async def get_profile_highlights(self, profile_id: str, target_profile_id: str,
                                     limit: int = 10, sort: str = 'FromMax', equal: bool = False) -> dict:
        return await self._execute_request('getProfileHighlights', {
            'equal': equal,
            'limit': limit,
            'sort': sort,
            'target_profile_id': target_profile_id,
            'profile_id': profile_id
        })

    async def get_bookmarked_posts(self, profile_id: str,
                                   limit: int = 50, sort: str = 'FromMax', equal: bool = False) -> dict:
        return await self._execute_request('getBookmarkedPosts', {
            'equal': equal,
            'limit': limit,
            'sort': sort,
            'profile_id': profile_id
        })

    async def get_explore_posts(self, profile_id: str, limit: int = 50,
                                sort: str = 'FromMax', equal: bool = False, max_id: str = None) -> dict:
        return await self._execute_request('getExplorePosts', {
            'equal': equal,
            'limit': limit,
            'sort': sort,
            'max_id': max_id,
            'profile_id': profile_id
        })

    async def get_blocked_profiles(self, profile_id: str,
                                   limit: int = 50, sort: str = 'FromMax', equal: bool = False) -> dict:
        return await self._execute_request('getBlockedProfiles', {
            'equal': equal,
            'limit': limit,
            'sort': sort,
            'profile_id': profile_id
        })

    async def get_profile_followers(self, profile_id: str, target_profile_id: str,
                                    limit: int = 50, sort: str = 'FromMax', equal: bool = False) -> dict:
        return await self._execute_request('getProfileFollowers', {
            'equal': equal,
            'f_type': 'Follower',
            'limit': limit,
            'sort': sort,
            'target_profile_id': target_profile_id,
            'profile_id': profile_id
        })

    async def get_profile_followings(self, profile_id: str, target_profile_id: str,
                                     limit: int = 50, sort: str = 'FromMax', equal: bool = False) -> dict:
        return await self._execute_request('getProfileFollowers', {
            'equal': equal,
            'f_type': 'Following',
            'limit': limit,
            'sort': sort,
            'target_profile_id': target_profile_id,
            'profile_id': profile_id
        })

    async def get_profile_info(self, profile_id: str, target_profile_id: str) -> dict:
        return await self._execute_request('getProfileInfo', {
            'profile_id': profile_id,
            'target_profile_id': target_profile_id
        })

    async def block_profile(self, profile_id: str, blocked_id: str) -> dict:
        return await self._execute_request('setBlockProfile', {
            'action': 'Block',
            'blocked_id': blocked_id,
            'profile_id': profile_id
        })

    async def unblock_profile(self, profile_id: str, blocked_id: str) -> dict:
        return await self._execute_request('setBlockProfile', {
            'action': 'Unblock',
            'blocked_id': blocked_id,
            'profile_id': profile_id
        })

    async def get_my_archive_stories(self, profile_id: str, limit: int = 50, sort: str = 'FromMax', equal: bool = False) -> dict:
        return await self._execute_request('getMyArchiveStories', {'equal': equal, 'limit': limit, 'sort': sort, 'profile_id': profile_id})

    async def remove_page(self, profile_id: str, record_id: str) -> dict:
        return await self._execute_request('removeRecord', {'model': 'Profile', 'record_id': record_id, 'profile_id': profile_id})

    async def upload_file(self, file: str, profile_id: str, file_type: str) -> dict:
        filename, filesize = file.split('/')[-1], os.path.getsize(file)
        result = await self.request_upload_file(profile_id, filename, filesize, file_type)
        
        byte_file = open(file, 'rb').read()
        headers = {
            'auth': self.client.auth,
            'file-id': result['data']['file_id'],
            'chunk-size': str(len(byte_file)),
            'total-part': str(1),
            'part-number': str(1),
            'hash-file-request': result['data']['hash_file_request'],
        }

        async with self.client.connection.session.post(result.server_url, data=byte_file, headers=headers) as result:
            if result.ok:
                result = await result.json()
                return Update(result.get('data')), result

# ... (continue with any other methods you have)


    async def add_post(self, profile_id: str, file: str, caption: str = None, file_type: str = 'Picture') -> dict:
        result = await self.upload_file(file, profile_id, file_type)
        return await self._execute_request('addPost', {
            'rnd': int(random() * 1e6 + 1),
            'width': 720,
            'height': 720,
            'caption': caption,
            'file_id': result[1]['file_id'],
            'post_type': file_type,
            'profile_id': profile_id,
            'hash_file_receive': result[0]['hash_file_receive'],
            'thumbnail_file_id': result[1]['file_id'],
            'thumbnail_hash_file_receive': result[0]['hash_file_receive'],
            'is_multi_file': False,
        })

    async def add_picture(self, profile_id: str, file):
        pass