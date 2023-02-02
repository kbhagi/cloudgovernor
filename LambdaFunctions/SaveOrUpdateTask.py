import sys
import json
import urllib
import logging
import os
import pymysql
import boto3
import requests
host = os.environ['host']
port = int(os.environ['port'])
user = os.environ['user']
passwd = os.environ['passwd']
db = os.environ['db']
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ssm_client = boto3.client("ssm")

bot_token = "xxxxx"
slack_channel = '#securitybot'
slack_channel_id = 'xxxxx'
slack_icon_emoji = ':see_no_evil:'
slack_user_name = 'DRBOT'
def post_to_slack(**kwargs):
    message = kwargs.get("message")
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Result"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": message
            }

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


def get_task_details(**kwargs):
    event = kwargs.get("event")
    records = event.get("Records")
    print("records")
    print(records)
    record = records[0].get('Sns')
    x_form_encoded_body = record.get("Message")
    decoded_body = json.loads(urllib.parse.unquote(x_form_encoded_body))
    subject = record.get("Subject")
    print("decoded_body")
    print(decoded_body)
    return decoded_body, subject


def get_automation_status(**kwargs):
    ssm = kwargs.get("ssm_client")
    executionId = kwargs.get("ExecutionId")
    response = ssm.describe_automation_executions(
        Filters=[
            {
                'Key': 'ExecutionId',
                'Values': [
                    executionId,
                ]
            },
        ]
    )
    status = response.get("AutomationExecutionMetadataList")[0].get("AutomationExecutionStatus");
    return status


def lambda_handler(event, context):
    print(event)
    task_details, task_type = get_task_details(event=event)
    if task_type == 'save_task':
        print("----------------inside save_task------------------")
        print("task_details at save_task")
        print(task_details)
        try:
            connection = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
            connection.autocommit(True)
        except Exception:
            exception_type, exception_value, exception_traceback = sys.exc_info()
            traceback_string = traceback.format_exception(exception_type, exception_value, exception_traceback)
            err_msg = json.dumps({
                "errorType": exception_type.__name__,
                "errorMessage": str(exception_value),
                "stackTrace": traceback_string
            })
            logger.error(err_msg)
            sys.exit()
        logger.info("SUCCESS: Connection to RDS mysql instance succeeded at suppress_finding")

        with connection.cursor() as cursor:
            sql = "INSERT INTO `Tasks` (`TaskId`, `TaskStatus`, `TaskType`, `DateTime`, `FindingId`) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (
                task_details['TaskId'], task_details["TaskStatus"], task_details["TaskType"], task_details["DateTime"],
                task_details["FindingId"]))
            connection.commit()
        if connection:
            connection.close()
        print("TaskType at save_task", task_details.get("TaskType"))
        if task_details.get("TaskType") == "Suppression":
            message = "*" + task_details.get("FindingId") + "*" + " has been suppressed"
            post_to_slack(message=message)
    elif task_type == 'update_task':
        print("----------------inside update_task------------------")
        print("task_details at update_task")
        print(task_details)
        executionId = task_details.get("context").get("automation:EXECUTION_ID")
        FindingId = task_details.get("response").get("FindingId")
        print("executionId")
        print(executionId)
        status = get_automation_status(ssm_client=ssm_client, ExecutionId=executionId)
        try:
            connection = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
            connection.autocommit(True)
        except Exception:
            exception_type, exception_value, exception_traceback = sys.exc_info()
            traceback_string = traceback.format_exception(exception_type, exception_value, exception_traceback)
            err_msg = json.dumps({
                "errorType": exception_type.__name__,
                "errorMessage": str(exception_value),
                "stackTrace": traceback_string
            })
            logger.error(err_msg)
        logger.info("SUCCESS: Connection to RDS mysql instance succeeded at suppress_finding")
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql_query = """UPDATE Tasks SET TaskStatus = %s WHERE TaskId= %s""";
            data = (status, executionId)
            value = cursor.execute(sql_query, data)
            connection.commit()
            print(value)
        if connection:
            connection.close()
        message = "*" + FindingId + "*" + " has been remediated"
        post_to_slack(message=message)



if __name__ == '__main__':
    FindingId = "arn:aws:s3:::xxxx.xxxxxx.com/s3-bucket-policy-allows-public-access-check"
    message = "*" + FindingId + "*" + " has been remediated"
    post_to_slack(message=message)
