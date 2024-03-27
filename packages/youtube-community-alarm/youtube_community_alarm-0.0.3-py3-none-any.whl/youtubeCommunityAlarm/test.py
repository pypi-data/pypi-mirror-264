from crontab_register import CrontabRegister
from youtube_community import YoutubeCommunity


if __name__ == "__main__":
    # channel_id = "@-zg6kl"
    #
    # cr = CrontabRegister(channel_id=channel_id, time_limit_for_checking_in_hours="10")
    # cr.register_crontab()
    #
    # # posts = YoutubeCommunity(channel_id).get_all_posts_with_time()



    channel_id = "@my_channel_id"
    # Check for new posts until those posted within the last 30 minutes using a cron expression "30 * * * *"
    cr = CrontabRegister(channel_id=channel_id, time_limit_for_checking_in_minutes=30,
                              cron_expression="30 * * * *")
    cr.register_crontab()
