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
    notification_parameters = os.environ['NOTIFICATION_PARAMETER']
    slack_object = {}
    teams_object = {}
    bot_token = "xxsszz"
    slack_channel = '#securitybot'
    slack_channel_id = 'xxxxxxs'
    slack_icon_emoji = ':see_no_evil:'
    slack_user_name = 'zzzzz'
    try:
        response = ssm.get_parameter(Name=notification_parameters, WithDecryption=True)
        response_object = str(response['Parameter']['Value'])
        response_object_dict = json.loads(response_object)
        slack_object = response_object_dict.get('slack_object')
        slack_hooks = slack_object.get("slack_webhooks")
        logger.info("slack_object")
        logger.info(slack_object)
        teams_object = response_object_dict.get('teams_object')
        teams_hooks = teams_object.get("teams_webhooks")
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
                                    "value": resourceId
                                },
                                {
                                    "name": "Resource Type:",
                                    "value": resourceType
                                },
                                {
                                    "name": "Region:",
                                    "value": resourceRegion
                                },
                                {
                                    "name": "Time:",
                                    "value": event.get("time")
                                },
                                {
                                    "name": "Account:",
                                    "value": awsAccountId
                                },
                                {
                                    "name": "Compliance Status:",
                                    "value": findings.get("Compliance").get("Status")
                                },
                                {
                                    "name": "Check:",
                                    "value": title
                                },
                                {
                                    "name": "FindingId:",
                                    "value": findings.get("Id")
                                },
                                {
                                    "name": "Recommendation:",
                                    "value": findings.get('Remediation').get('Recommendation').get('Text')
                                }
                            ],
                            "text": "**Findings:**"
                        }
                    ]
                }
                for hook in slack_hooks:
                    print(hook)
                    if severityLabel in slack_object.get("severity"):
                        logger.info(
                            "slack severity match found " + str(slack_object.get("severity")) + " " + severityLabel)
                        status = requests.post('https://slack.com/api/chat.postMessage', slack_payload).json()
                        logger.info(status)
                    else:
                        logger.info("severityLabel doesn't match the slack_hooks severity " + str(
                            slack_object.get("severity")) + " " + severityLabel)
                for hook in teams_hooks:
                    if severityLabel in teams_object.get("severity"):
                        logger.info(
                            "team severity match found " + str(teams_object.get("severity")) + " " + severityLabel)
                        status = requests.post(hook, json.dumps(teams_payload).encode('utf-8'))
                        logger.info(status)
                    else:
                        logger.info("severityLabel doesn't match the teams_hooks severity " + str(
                            teams_object.get("severity")) + " " + severityLabel)
        else:
            logger.info("Compliance Status is either passed or None " + findings.get("Compliance").get(
                "Status") + " for " + findings.get("Id"))
