import os
import boto3
import json
import requests

def lambda_handler(event, context):
    # create ssm client
    ssm = boto3.client('ssm')
    # create env var for SSM Parameter containing Slack Webhook URL
    ssm_parameter_name = os.environ['MS_TEAMS_WEBHOOK_PARAMETER']
    teams_webhook = ""
    try:
        response = ssm.get_parameter(Name=ssm_parameter_name)
        response_object = str(response['Parameter']['Value'])
        response_object_dict = json.loads(response_object)
        teams_webhook = response_object_dict.get('teams_webhook')

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
                                },
                                {
                                    "name": "Severity:",
                                    "value": severityLabel
                                }
                            ],
                            "text": "**Findings:**"
                                }
                            ]
                        }

                status = requests.post(teams_webhook, json.dumps(teams_payload).encode('utf-8'))
                print(status)

        else:
            print("Compliance Status is either passed or None " + findings.get("Compliance").get(
                "Status") + " for " + findings.get("Id"))