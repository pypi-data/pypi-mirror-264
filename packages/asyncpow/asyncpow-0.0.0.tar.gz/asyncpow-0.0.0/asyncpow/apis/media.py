"""
 AsyncPOW - https://github.com/totaldebug/asyncpow

 Copyright (c) 2024 Steven Marks, Total Debug

 Permission is hereby granted, free of charge, to any person obtaining a copy of
 this software and associated documentation files (the "Software"), to deal in
 the Software without restriction, including without limitation the rights to
 use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 the Software, and to permit persons to whom the Software is furnished to do so,
 subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 """

from typing import Optional

from aiohttp import ClientSession, hdrs
from yarl import URL

from asyncpow.models.common import SortOptions
from asyncpow.models.media import MediaFilterOptions, MediaModel, MediaModel2, MediaStatusOptions
from asyncpow.utils.http import request


class Media:
    """
    Class to interact with media-related endpoints.

    Initialize the Media object with the base URL, API key, and session.
    """

    def __init__(self, base_url: URL, api_key: str, session: ClientSession) -> None:
        """
        Initialize the MediaAPI object with the base URL and API key.

        Args:
            base_url (str): The base URL for the media API.
            api_key (str): The API key for authentication.
            session (ClientSession): HTTP Session

        Returns:
            None
        """
        self.media_url = base_url.joinpath("media")
        self.api_key = api_key
        self.session = session

    async def get_media(
        self,
        take: int = 20,
        skip: int = 0,
        filter: MediaFilterOptions = MediaFilterOptions.AVAILABLE,
        sort: SortOptions = SortOptions.ADDED,
    ) -> MediaModel:
        """
        Get media items based on specified parameters.

        Args:
            take (int): The number of items to retrieve (default is 20).
            skip (int): The number of items to skip (default is 0).
            filter (MediaFilterOptions): The filter option for media items (default is MediaFilterOptions.AVAILABLE).
            sort (SortOptions): The sorting option for media items (default is SortOptions.ADDED).

        Returns:
            MediaModel: The media model object retrieved based on the parameters.
        """

        url = self.media_url.with_query(
            {"take": take, "skip": skip, "filter": str(filter), "sort": str(sort)}
        )
        headers = {"X-Api-Key": self.api_key}
        return await request(self.session, url, headers=headers)

    async def post_media_status(
        self, mediaId: int, status: MediaStatusOptions, is4k: Optional[bool] = None
    ) -> MediaModel2:
        """
        Update the status of a media item with optional 4k flag.

        Args:
            mediaId (int): The ID of the media item.
            status (MediaStatusOptions): The status to set for the media item.
            is4k (Optional[bool]): Optional flag indicating 4k status.

        Returns:
            MediaModel2: The model object representing the updated media item.
        """

        url = self.media_url.joinpath(str(mediaId), str(status))
        data = {"is4k": is4k} if is4k else {}
        headers = {"X-Api-Key": self.api_key}
        return await request(self.session, url, method="POST", data=data, headers=headers)

    async def delete_media(self, mediaId: int):
        """
        Delete a media item by its ID.

        Args:
            mediaId (int): The ID of the media item to delete.

        Returns:
            None
        """

        url = self.media_url.joinpath(str(mediaId))
        headers = {"X-Api-Key": self.api_key}
        await request(self.session, url, method=hdrs.METH_DELETE, headers=headers)
