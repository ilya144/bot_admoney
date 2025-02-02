import vk_api
import requests
import json
import re


class VKParser:
    def __init__(self):
        self.auth_url = "https://oauth.vk.com/authorize?" \
                        "client_id=6959665&display=page&" \
                        "redirect_uri=https://oauth.vk.com/blank.html" \
                        "&response_type=token&v=5.95"

        self.email = ""#"gggmocha000777@mail.ru"
        self.password = ""#"kolxoz1488"

        self.token = "26bc0b4526bc0b4526bc0b456e26d63974226bc26bc0b457a7c9e0e5f7465ade086ee59"
        self.token_auth = "168892987e834182cd2eecfc78413ffe5eacd8f7d18fee0a8bb0ce98ef4457f0cc9e4faa5df16ce223a6b"

    def _refresh_auth_token(self) -> str:
        # TODO вход в вк через requests
        # https://oauth.vk.com/authorize?client_id=6959665&display=page&redirect_uri=http://vk.com&response_type=code&v=5.95
        # payload = {'email': self.email, 'password': self.password}
        # response = session.get(self.auth_url, allow_redirects=True, headers=head)
        # <input type="hidden" name="ip_h" value="[a-zA-Z0-9]*"\s?/?> re pattern
        s = requests.Session()

        first_response = s.get('https://vk.com/')
        html = first_response.text

        #ip_h_raw = re.search(r'name="ip_h" value="[a-zA-Z0-9]*"', html).group()
        #lg_h_raw = re.search(r'name="lg_h" value="[a-zA-Z0-9]*"', html).group()
        #to_raw = re.search(r'name="to" value="[a-zA-Z0-9]*"', html).group()
        #ip_h = ip_h_raw.lstrip('name="ip_h" value=').strip('"')
        #lg_h = lg_h_raw.lstrip('name="lg_h" value=').strip('"')
        #to = to_raw.lstrip('name="to" value=').strip('"')


        s.headers.update({
            'User-agent': 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) '
                          'Gecko/20100101 Firefox/52.0'
        })
        payload = {
            "act": "login",
            'role': 'al_frame',
            "_origin": "https://vk.com",
            "utf8": "1",
            "email": self.email,
            "pass": self.password,
            #"to": to,
            #"soft": "1",
            #"expire": "",
            #"ip_h": ip_h,
            #"lg_h": lg_h
        }
        print(payload)
        url = "https://login.vk.com/"
        print(s.headers)
        print(s.cookies)

        r = s.post(url, data=payload)
        print(r.text)
        #with open("vk.html", "w") as f:f.write(r.text)
        #r2 = s.get(self.auth_url, cookies=s.cookies)

        #print(r.text)
        #print(r2.text)


    def _get_user_id(self, username) -> str:
        response = requests.get("https://api.vk.com/method/users.get"
                                f"?user_ids={username}&v=5.52"
                                f"&access_token={self.token}")
        user_id = json.loads(response.content)['response'][0]['id']
        return user_id

    def _get_group_id(self, group_ids):
        response = requests.get("https://api.vk.com/method/groups.getById"
                                f"?group_ids={group_ids}&v=5.52"
                                f"&access_token={self.token}")

        group_id = json.loads(response.content)['response'][0]['id']
        return group_id

    def _isLiked(self, post_url, user_id) -> dict:
        owner_id, item_id = post_url.split('_')
        response = requests.get("https://api.vk.com/method/likes.isLiked"
                                f"?owner_id={owner_id}"
                                f"&item_id={item_id}&type=post"
                                f"&user_id={user_id}&v=5.52"
                                f"&access_token={self.token_auth}")
        return json.loads(response.content)

    def check_like(self, post_url, user_id) -> bool:
        response = self._isLiked(post_url, user_id)
        liked = response['response']['liked']
        return bool(liked)

    def check_repost(self, post_url, user_id):
        response = self._isLiked(post_url, user_id)
        copied = response['response']['copied']
        return bool(copied)

    def check_comment(self, post_url, user_id) -> bool:
        owner_id, post_id = post_url.split('_')
        response = requests.get("https://api.vk.com/method/wall.getComments"
                                f"?owner_id={owner_id}"
                                f"&post_id={post_id}&v=5.52"
                                f"&access_token={self.token}"
                                f"&count=100")
        fetched_json = json.loads(response.content)
        comments = fetched_json["response"]["items"]
        for comment in comments:
            if comment["from_id"] == user_id:
                return True
        else:
            return False

    def check_follow_by(self, group_id, user_id) -> bool:
        response = requests.get("https://api.vk.com/method/groups.isMember"
                                f"?group_id={group_id}"
                                f"&user_id={user_id}&v=5.52"
                                f"&access_token={self.token_auth}"
                                f"&extended=1")
        isMember = json.loads(response.content)['response']['member']
        return bool(isMember)

    def check_post_url(self, post_url) -> bool:
        post_ids = post_url.split("wall")[1]
        response = requests.get("https://api.vk.com/method/wall.getById"
                                f"?posts={post_ids}&v=5.52"
                                f"&access_token={self.token}")

        try:
            post_id = json.loads(response.content)['response'][0]['id']
        except:
            return False

        return True

    def check_username(self, username):
        try:
            user_id = self._get_user_id(username)
            return user_id
        except:
            raise Exception("User not found")

    def check_group_url(self, group_url):
        try:
            group_id = self._get_group_id(group_url)
        except:
            return False
        if group_id:
            return True


if __name__ == '__main__':

    parser = VKParser()
    # print(parser._get_user_id("id387340775"))
    # print(parser._get_group_id("linuxclub7777"))
    print(parser.check_post_url("https://vk.com/linuxclub?w=wall-121871413249_49989"))
    # a = vk_api.VkApi(parser.email,parser.password)
    # a._vk_login()


    # parser._refresh_auth_token()

