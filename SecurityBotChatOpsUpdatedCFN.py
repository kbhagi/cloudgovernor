import os
import boto3
import json
import requests

def lambda_handler(event, context):
    # create ssm client
    ssm = boto3.client('ssm')
    # create env var for SSM Parameter containing Slack Webhook URL
    ssm_parameter_name = os.environ['SSM_PARAMETER_NAME']
    bot_token = ""
    slack_channel_id = ""
    slack_icon_emoji = ':see_no_evil:'
    slack_user_name = 'xxxxx'
    try:
        response = ssm.get_parameter(Name=ssm_parameter_name)
        response_object = str(response['Parameter']['Value'])
        response_object_dict = json.loads(response_object)
        bot_token = response_object_dict.get('bot_token')
        slack_channel_id = response_object_dict.get("slack_channel_id")

    except Exception as e:
        print(e)

    for findings in event['detail']['findings']:
        if findings.get("Compliance").get("Status") == "FAILED":
            severityLabel = findings['Severity']['Label']
            title = findings['Title']
            awsAccountId = findings['AwsAccountId']
            for resources in findings['Resources']:
                resourceId = resources['Id']
                resourceType = resources['Type']
                resourceRegion = resources['Region']
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
                                "text": "*Resource:* " + resourceId
                            },
                            {
                                "type": "mrkdwn",
                                "text": "*Resource Type:* " + resourceType
                            }
                        ]
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": "*Region:* " + resourceRegion
                            },
                            {
                                "type": "mrkdwn",
                                "text": "*Time:* " + event.get("time")
                            }
                        ]
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": "*Account:* " + awsAccountId
                            },
                            {
                                "type": "mrkdwn",
                                "text": "*Compliance Status:* " + findings.get("Compliance").get("Status")
                            }
                        ]
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": "*Severity:* " + severityLabel
                            },
                            {
                                "type": "mrkdwn",
                                "text": "*FindingId:* " + findings.get("Id")
                            },

                        ]
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Check:* " + title
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "<" + findings.get('Remediation').get('Recommendation').get(
                                'Url') + "|*Recommendation:* " + findings.get('Remediation').get('Recommendation').get(
                                'Text') + ">"
                        }
                    }
                ]
                slack_payload = {
                    'token': bot_token,
                    'channel': slack_channel_id,
                    'text': "ElectricEye",
                    'icon_emoji': slack_icon_emoji,
                    'username': slack_user_name,
                    'blocks': json.dumps(blocks) if blocks else None
                }
                status = requests.post('https://slack.com/api/chat.postMessage', slack_payload).json()
                print(status)


        else:
            print("Compliance Status is either passed or None " + findings.get("Compliance").get(
                "Status") + " for " + findings.get("Id"))
