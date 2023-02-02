import requests
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


teams_payload = {
"@type": "MessageCard",
"@context": "http: //schema.org/extensions",
"themeColor": "0584 ED",
"summary": "Findings",
"sections": [

 {
  "facts": [
   {
    "name": "Resource:",
    "value": ""
   },
   {
    "name": "Resource Type:",
    "value": ""
   },
   {
    "name": "Region:",
    "value": ""
   },
   {
    "name": "Time:",
    "value": ""
   },
   {
    "name": "Account:",
    "value": ""
   },
   {
    "name": "Compliance Status:",
    "value": ""
   },
  ],
  "text": "Findings:"
 }

# {
#  "activityTitle": " **Resource** ",
#  "activitySubtitle": "arn:aws:s3:::exposed-bucket",
#  "markdown": True
# },
# {
#  "activityTitle": " **Resource Type:** ",
#  "activitySubtitle": "AwsS3Bucket!",
#  "markdown": True
# },
# {
#  "activityTitle": " **Region:** ",
#  "activitySubtitle": "ap-south-1",
#  "markdown": True
# },
# {
#  "activityTitle": " **Time:** ",
#  "activitySubtitle": "2021-08-07T14:08:51Z",
#  "markdown": True
# },
# {
#  "activityTitle": " **Account:** ",
#  "activitySubtitle": "xxxxxx",
#  "markdown": True
# },
# {
#  "activityTitle": " **Compliance Status:** ",
#  "activitySubtitle": "Failed",
#  "markdown": True
# }
]
}

def post_to_teams():
    hook = "https://securitybot.webhook.office.com/webhookb2/xxx@xxx-8a2f-46dd-xxxx/IncomingWebhook/xxxxa0cb/xxxxx-xx"
    status = requests.post(hook, json.dumps(teams_payload).encode('utf-8'))
    print(status)
    print(status.json())
    print(status.reason)


if __name__ == '__main__':
   post_to_teams()