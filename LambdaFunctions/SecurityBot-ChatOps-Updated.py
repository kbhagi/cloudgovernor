import boto3
import json
import requests
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    event = {
        'version': '0',
        'id': '67aazzb0-6355-7060-9d05-6d4696b34845',
        'detail-type': 'Security Hub Findings - Imported',
        'source': 'aws.securityhub',
        'account': 'xxxxx',
        'time': '2021-06-27T17:31:02Z',
        'region': 'ap-south-1',
        'resources': [
            'arn:aws:securityhub:ap-south-1:xxxxx:product/xxxxx/default/arn:aws:s3:::xxxxx.xxxxxxx.com/s3-bucket-server-access-logging-check'
        ],
        'detail': {
            'findings': [
                {
                    'ProductArn': 'arn:aws:securityhub:ap-south-1:xxxxx:product/xxxxx/default',
                    'Types': [
                        'Software and Configuration Checks/AWS Security Best Practices'
                    ],
                    'Description': 'S3 bucket xxxxx.xxxxxxx.com does not have server access logging enabled. Refer to the remediation instructions to remediate this behavior',
                    'Compliance': {
                        'Status': 'FAILED',
                        'RelatedRequirements': [
                            'NIST CSF DE.AE-3',
                            'NIST SP 800-53 AU-6',
                            'NIST SP 800-53 CA-7',
                            'NIST SP 800-53 IR-4',
                            'NIST SP 800-53 IR-5',
                            'NIST SP 800-53 IR-8',
                            'NIST SP 800-53 SI-4',
                            'AICPA TSC CC7.2',
                            'ISO 27001:2013 A.12.4.1',
                            'ISO 27001:2013 A.16.1.7'
                        ]
                    },
                    'ProductName': 'Default',
                    'FirstObservedAt': '2021-06-27T17:30:57.033086+00:00',
                    'CreatedAt': '2021-06-26T18:05:27.082693+00:00',
                    'CompanyName': 'Personal',
                    'FindingProviderFields': {
                        'Types': [
                            'Software and Configuration Checks/AWS Security Best Practices'
                        ],
                        'Confidence': 99,
                        'Severity': {
                            'Normalized': 40,
                            'Label': 'MEDIUM'
                        }
                    },
                    'Confidence': 99,
                    'ProductFields': {
                        'Product Name': 'xxxxSecurityBot',
                        'aws/securityhub/FindingId': 'arn:aws:securityhub:ap-south-1:xxxxx:product/xxxxx/default/arn:aws:s3:::xxxxx.xxxxxxx.com/s3-bucket-server-access-logging-check',
                        'aws/securityhub/ProductName': 'Default',
                        'aws/securityhub/CompanyName': 'Personal'
                    },
                    'Remediation': {
                        'Recommendation': {
                            'Text': 'For more information on Bucket Policies and how to configure it refer to the Amazon S3 Server Access Logging section of the Amazon Simple Storage Service Developer Guide',
                            'Url': 'https://docs.aws.amazon.com/AmazonS3/latest/dev/ServerLogs.html'
                        }
                    },
                    'SchemaVersion': '2018-10-08',
                    'GeneratorId': 'arn:aws:s3:::xxxxx.xxxxxxx.com',
                    'RecordState': 'ACTIVE',
                    'Title': '[S3.6] S3 Buckets should have server access logging enabled',
                    'Workflow': {
                        'Status': 'NEW'
                    },
                    'Severity': {
                        'Normalized': 40,
                        'Label': 'MEDIUM'
                    },
                    'UpdatedAt': '2021-06-27T17:30:57.033086+00:00',
                    'WorkflowState': 'NEW',
                    'AwsAccountId': 'xxxxx',
                    'Region': 'ap-south-1',
                    'Id': 'arn:aws:s3:::xxxxx.xxxxxxx.com/s3-bucket-server-access-logging-check',
                    'Resources': [
                        {
                            'Partition': 'aws',
                            'Type': 'AwsS3Bucket',
                            'Region': 'ap-south-1',
                            'Id': 'arn:aws:s3:::xxxxx.xxxxxxx.com'
                        }
                    ]
                }
            ]
        }
    }
    logger.info("event")
    logger.info(event)
    ssm_client = boto3.Session(profile_name="default")
    ssm = ssm_client.client('ssm')
    slack_secrets = 'slack_secrets' #os.environ['NOTIFICATION_PARAMETER']
    bot_token = ""
    slack_channel_id = ''
    slack_icon_emoji = ':see_no_evil:'
    slack_user_name = 'DRBOT'
    try:
        response = ssm.get_parameter(Name=slack_secrets, WithDecryption=True)
        response_object = str(response['Parameter']['Value'])
        response_object_dict = json.loads(response_object)
        bot_token = response_object_dict.get('bot_token')
        slack_channel_id = response_object_dict.get("slack_channel_id")
        slack_user_name = response_object_dict.get("slack_user_name")
        logger.info("bot_token")
        logger.info(bot_token)
        logger.info("slack_channel_id")
        logger.info(slack_channel_id)
        logger.info("slack_user_name")
        logger.info(slack_user_name)

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
                #logger.info(status)

        else:
            logger.info("Compliance Status is either passed or None " + findings.get("Compliance").get(
                "Status") + " for " + findings.get("Id"))


if __name__ == '__main__':
    lambda_handler({},{})
