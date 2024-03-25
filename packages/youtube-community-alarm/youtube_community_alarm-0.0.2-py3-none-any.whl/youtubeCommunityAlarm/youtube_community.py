import requests
import json
import re

BASE_URL = "https://www.youtube.com/"
REGEX = {
    "YT_INITIAL_DATA": "ytInitialData = ({(?:(?:.|\n)*)?});</script>",
    "HOUR_TIME_PATTERN": r'(\d+)\s*시간\s*전',
    "MINUTE_TIME_PATTERN": r'(\d+)\s*분\s*전',
}

class YoutubeCommunity:
    def __init__(self, channel_id):
        self.channel_id = channel_id

    def get_all_posts_with_time(self):
        response = requests.get(f"{BASE_URL + self.channel_id}/community")
        posts_with_time = []
        if response.status_code == 200:
            m = re.findall(REGEX["YT_INITIAL_DATA"], response.text)
            if m:
                json_data = json.loads(m[0])
            else:
                print("Regular expression did not match any content in the response text.")
                return []

            tabs = json_data['contents']['twoColumnBrowseResultsRenderer']['tabs']
            posts = []
            for tab in tabs:
                try:
                    posts = tab['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer'][
                        'contents']
                except KeyError:
                    pass

            if not posts:
                print("No posts found.")
                return
            for post in posts:
                try:
                    back_stage_post_renderer = post["backstagePostThreadRenderer"]["post"]['backstagePostRenderer']
                    text = back_stage_post_renderer["contentText"]["runs"][0]["text"]
                    time = back_stage_post_renderer["publishedTimeText"]["runs"][0]["text"]
                    posts_with_time.append((time, text))
                except KeyError:
                    continue
        else:
            print(f"[Can't get data from the channel_id: {self.channel_id}]")
            print(f"Response status code: {response.status_code}")

        return posts_with_time
