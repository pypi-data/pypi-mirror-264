# Youtube Community Alarm

Python3 Interface for Scheduling Crontab to Retrieve YouTube Community Posts and Send Notifications


## Quickstart
```bash
pip install youtube-community-alarm
```


```python
>>> from crontab_register import CrontabRegister

>>> channel_id = "@my_channel_id"
>>> cr = CrontabRegister(channel_id=channel_id)
>>> cr.register_crontab()
```

Check if the crontab is registered by running the following command:

```bash
crontab -l

# Output
# 0 */10 * * * /usr/bin/python3 /path/youtube_community_alarm.py --channel_id @my_channel_id /path/log.log 2>&1
```

## Crontab Error Case

If you encounter errors from the crontab, you can refer to [this troubleshooting guide](https://23log.tistory.com/171)






