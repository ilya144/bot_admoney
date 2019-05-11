from instagram_private_api import Client
import requests
import json


class InstagramParser:
    def __init__(self):
        self.api = Client(username="vip_smm_inst", password="vipsmm777")#(username="_yana_sun1_", password="instaprogo")

    def __get_media_id(self, media_url):
        response = requests.get(media_url+"?__a=1")
        try:
            parsed_data = json.loads(response.content)
        except:
            raise Exception("Invalid media url")
        media_id = parsed_data["graphql"]["shortcode_media"]["id"]
        return media_id

    def _get_id_by_username(self, username):
        user_id = self.api.username_info(username)['user']['pk']
        return user_id

    def check_like(self, media_url, username) -> bool:
        media_id = self.__get_media_id(media_url)
        likers = self.api.media_likers(media_id)['users']
        return username in [liker['username'] for liker in likers]

    def check_comment(self, media_url, username) -> bool:
        media_id = self.__get_media_id(media_url)
        comments = self.api.media_comments(media_id)['comments']
        commentators = set([comment['user']['username'] for comment in comments])
        return username in commentators

    def check_follow_by(self, target, username) -> bool:
        """
        :param target: username of user, which following by another user
        :param username: that's 'another' user
        :return: True if username found in followers
        """
        user_id = self._get_id_by_username(target)
        fetched_user = self.api.user_followers(user_id, self.api.generate_uuid(), query=username)['users']
        return username in [user['username'] for user in fetched_user]


if __name__ == "__main__":#mercedesbenz - login
    x = InstagramParser()
    print(x.check_like('https://www.instagram.com/p/BxEH_Yco8th/', 'vip_smm_inst'))
    print(x.check_comment('https://www.instagram.com/p/BxFDKGjJKx6/', 'vip_smm_inst'))
    print(x.check_follow_by('vip_smm_inst', 'maximatech_worldshop'))
