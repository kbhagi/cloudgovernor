import os
import boto3
import json
import requests
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info("event")
    logger.info(event)
    ssm = boto3.client('ssm')
    slack_secrets = os.environ['SLACK_SECRETS']
    slack_object = {}
    bot_token = "xxxxxxxx"
    slack_channel_id = 'xxxxxxxxs'
    slack_icon_emoji = ':see_no_evil:'
    slack_user_name = 'DRBOT'
    try:
        response = ssm.get_parameter(Name=slack_secrets, WithDecryption=True)
        response_object = str(response['Parameter']['Value'])
        response_object_dict = json.loads(response_object)
        slack_object = response_object_dict.get('bot_token')
        slack_hooks = slack_object.get("slack_webhooks")
        logger.info("slack_object")
        logger.info(slack_object)

    except Exception as e:
        logger.exception(e)

    for findings in event['detail']['findings']:
        logger.info("findings")
        logger.info(findings)
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
                                "value": str(event.get("id"))
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Suppress"
                                },
                                "style": "danger",
                                "value": str(event.get("id"))
                            }
                        ]
                    }
                ]
                slack_payload = {
                    'token': bot_token,
                    'channel': slack_channel_id,
                    'text': "SecurityBot",
                    'icon_emoji': slack_icon_emoji,
                    'username': slack_user_name,
                    'blocks': json.dumps(blocks) if blocks else None
                }
                status = requests.post('https://slack.com/api/chat.postMessage', slack_payload).json()
                logger.info(status)

        else:
            logger.info("Compliance Status is either passed or None " + findings.get("Compliance").get(
                "Status") + " for " + findings.get("Id"))
