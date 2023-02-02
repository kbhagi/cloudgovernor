import json
import logging
import requests

bot_token = ""
slack_channel = '#securitybot'
slack_channel_id = ''
slack_icon_emoji = ':see_no_evil:'
slack_user_name = 'xxxxx'

blocks = [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Finding"
			}
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "*Resource:*- arn:aws:s3:::xxxx..com"
				},
				{
					"type": "mrkdwn",
					"text": "*Resource Type:* AwsS3Bucket"
				}
			]
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "*Region:* AP-SOUTH-1"
				},
				{
					"type": "mrkdwn",
					"text": "*Time:* 2021-06-27T17:31:02Z"
				}
			]
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "*Account:* "
				},
				{
					"type": "mrkdwn",
					"text": "*Compliance Status:* Failing"
				}
			]
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "*Severity:* MEDIUM"
				}
			]
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Check:* [S3.6] S3 Buckets should have server access logging enabled"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "<https://docs.aws.amazon.com/AmazonS3/latest/dev/ServerLogs.html|*Recommendation:* For more information on Bucket Policies and how to configure it refer to the Amazon S3 Server Access Logging section of the Amazon Simple Storage Service Developer Guide>"
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Remediate"
					},
					"style": "primary",
					"value": 'xxxx-6355-7060-9d05-6d4696b34845'
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Suppress"
					},
					"style": "danger",
					"value": "xxxx-6355-7060-9d05-6d4696b34845"
				}
			]
		}
	]

notification_headers = {'Content-Type': 'application/json', 'token': bot_token}


payload = {
        'token': bot_token,
        'channel': slack_channel_id,
        'text': "SecurityBot",
        'icon_emoji': slack_icon_emoji,
        'username': slack_user_name,
        'blocks': json.dumps(blocks) if blocks else None
        }

def post_message_to_slack(text, blocks = None):
    return requests.post('https://slack.com/api/chat.postMessage', payload).json()

if __name__ == '__main__':
    r = post_message_to_slack("test",blocks)
    print(r)
