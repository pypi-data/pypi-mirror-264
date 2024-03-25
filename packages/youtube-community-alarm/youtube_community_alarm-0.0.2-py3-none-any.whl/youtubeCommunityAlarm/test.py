from crontab_register import CrontabRegister
from youtube_community import YoutubeCommunity


if __name__ == "__main__":
    channel_id = "@-zg6kl"

    cr = CrontabRegister(channel_id=channel_id, time_interval_in_hours="10")
    cr.register_crontab()

    # posts = YoutubeCommunity(channel_id).get_all_posts_with_time()

