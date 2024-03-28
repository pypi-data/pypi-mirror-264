import aiohttp


class TikTokPostResponse:
    """
    This class represents a TikTok post response object.
    """

    def __init__(self, response_json):
        self.code = response_json["code"]
        self.msg = response_json["msg"]
        self.processed_time = response_json["processed_time"]
        self.data = response_json["data"]
        self.video_binary = response_json["video_binary"]
        self.id = self.data["id"]
        self.region = self.data["region"]
        self.title = self.data["title"]
        self.cover = self.data["cover"]
        self.origin_cover = self.data["origin_cover"]
        self.duration = self.data["duration"]
        self.play = self.data["play"]
        self.wmplay = self.data["wmplay"]
        self.music = self.data["music"]
        self.music_info = self.data["music_info"]
        self.music_id = self.music_info["id"]
        self.music_title = self.music_info["title"]
        self.music_play = self.music_info["play"]
        self.music_cover = self.music_info["cover"]
        self.music_author = self.music_info["author"]
        self.music_original = self.music_info["original"]
        self.music_duration = self.music_info["duration"]
        self.music_album = self.music_info["album"]
        self.play_count = self.data["play_count"]
        self.digg_count = self.data["digg_count"]
        self.comment_count = self.data["comment_count"]
        self.share_count = self.data["share_count"]
        self.download_count = self.data["download_count"]
        self.create_time = self.data["create_time"]
        self.author = self.data["author"]
        self.author_id = self.author["id"]
        self.author_unique_id = self.author["unique_id"]
        self.author_nickname = self.author["nickname"]
        self.author_avatar = self.author["avatar"]


class TikTok:
    """
    This class represents a TikTok object.
    """

    def __init__(self, token: str):
        """
        Initialize a TikTok object.
        """
        self.token = token

    async def getpost(self, url: str):
        """
        Download a TikTok post and its associated metadata.

        Parameters:
        - url: The URL of the TikTok post.

        Returns:
        - Response.
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    url="https://api.heal.lol/v1/tiktok/post",
                    data={"url": url},
                    headers={"Authorization": self.token},
                ) as response:
                    resp = await response.json()
                    return resp, response.status
            except aiohttp.ClientError as e:
                return e
