import aiofiles
import aiohttp
import inspect
import os
from typing import Dict, Union
from random import random

from . import thumbnail
from ..types import Update
from .. import exceptions
import rubpy

class Rubino:
    DEFAULT_PLATFORM = {
        'app_name': 'Main',
        'app_version': '4.4.9',
        'platform': 'PWA',
        'package': 'web.rubika.ir',
    }

    def __init__(self, client: "rubpy.Client") -> None:
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
            raise exceptions(result.get('status'))(result.get('status_det')) #exceptions.ErrorAction(result.get('status_det'))

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
                                  file_size: int, file_type: str) -> Update:
        return await self._execute_request('requestUploadFile', {
            'file_name': file_name,
            'file_size': str(file_size),
            'file_type': file_type,
            'profile_id': profile_id,
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

    async def upload_file(self, file, profile_id: str, file_type: str, file_name: str = None, chunk: int = 1048576,
                          callback=None, *args, **kwargs):
        """
        Upload a file to Rubika.

        Parameters:
        - file: File path or bytes.
        - mime: MIME type of the file.
        - file_name: Name of the file.
        - chunk: Chunk size for uploading.
        - callback: Progress callback.

        Returns:
        Results object.
        """
        if isinstance(file, str):
            if not os.path.exists(file):
                raise ValueError('File not found in the given path')

            if file_name is None:
                file_name = os.path.basename(file)

            async with aiofiles.open(file, 'rb+') as file:
                file = await file.read()

        elif not isinstance(file, bytes):
            raise TypeError('File argument must be a file path or bytes')

        if file_name is None:
            raise ValueError('File name is not set')

        result = await self.request_upload_file(profile_id, file_name, len(file), file_type)

        id = result.file_id
        index = 0
        count_retry = 0
        max_retring = 3
        total = int(len(file) / chunk + 1)
        upload_url = result.server_url
        hash_file_request = result.hash_file_request

        while index < total:
            if count_retry == max_retring:
                break

            data = file[index * chunk: index * chunk + chunk]
            try:
                response = await self.client.connection.session.post(
                    upload_url,
                    headers={
                        'auth': self.client.auth,
                        'file-id': id,
                        'total-part': str(total),
                        'part-number': str(index + 1),
                        'chunk-size': str(len(data)),
                        'hash-file-request': hash_file_request
                    },
                    data=data,
                    proxy=self.client.proxy,
                )
                response = await response.json()

                if response.get('status') != 'OK':
                    result = await self.request_upload_file(profile_id, file_name, len(file), file_type)
                    id = result.file_id
                    index = 0
                    total = int(len(file) / chunk + 1)
                    upload_url = result.server_url
                    hash_file_request = result.hash_file_request
                    count_retry += 1

                if callable(callback):
                    try:
                        if inspect.iscoroutinefunction(callback):
                            await callback(len(file), index * chunk)

                        else:
                            callback(len(file), index * chunk)

                    except exceptions.CancelledError:
                        return None

                    except Exception:
                        pass

                index += 1

            except Exception:
                pass

        status = response['status']
        status_det = response['status_det']

        if status == 'OK' and status_det == 'OK':
            response.update(result.original_update)
            return Update(response)

        raise exceptions(status_det)(response, request=response)

    async def add_post(self, profile_id: str, post: str, post_type: str, caption: str = None, file_name: str = None):
        if isinstance(post, str):
            if not os.path.exists(post):
                raise ValueError('File not found in the given path')

            if file_name is None:
                file_name = os.path.basename(post)

            async with aiofiles.open(post, 'rb+') as post:
                post = await post.read()

        elif not isinstance(post, bytes):
            raise TypeError('File argument must be a file path or bytes')

        data = {
            'rnd': int(random() * 1e6 + 1),
            'width': 720,
            'height': 720,
            'caption': caption,
            'post_type': post_type,
            'profile_id': profile_id,
            'is_multi_file': False,
        }

        result = await self.upload_file(post, profile_id, post_type, file_name)
        data['file_id'] = result.file_id
        data['hash_file_receive'] = result.hash_file_receive
        data['thumbnail_file_id'] = result.file_id
        data['thumbnail_hash_file_receive'] = result.hash_file_receive

        if post_type == 'Video':
            thumb = thumbnail.MediaThumbnail.from_video(post)

            if isinstance(thumb, thumbnail.ResultMedia):
                result_upload_thumb = await self.upload_file(thumb.image, profile_id, 'Picture', 'thumbnail.jpg')
                data['thumbnail_file_id'] = result_upload_thumb.file_id
                data['thumbnail_hash_file_receive'] = result_upload_thumb.hash_file_receive
                data['snapshot_file_id'] = result_upload_thumb.file_id
                data['snapshot_hash_file_receive'] = result_upload_thumb.hash_file_receive
                data['duration'] = str(thumb.seconds)

        return await self._execute_request(method='addPost', data=data)

    async def add_picture(self, profile_id: str, picture: str, caption: str = None, file_name: str = None):
        return await self.add_post(profile_id=profile_id, post=picture, post_type='Picture', caption=caption, file_name=file_name)

    async def add_video(self, profile_id: str, video: str, caption: str = None, file_name: str = None):
        return await self.add_post(profile_id=profile_id, post=video, post_type='Video', caption=caption, file_name=file_name)