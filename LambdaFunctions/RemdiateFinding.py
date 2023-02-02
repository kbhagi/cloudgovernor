import json
import urllib
import os
import sys
import logging
import pymysql
import boto3
import traceback
import time

host = os.environ['host']
port = int(os.environ['port'])
user = os.environ['user']
passwd = os.environ['passwd']
db = os.environ['db']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ssm_client = boto3.client('ssm')
s3_client = boto3.client('s3')
securityhub = boto3.client("securityhub")




def get_finding_type_and_Id(**kwargs):
    event = kwargs.get("event")
    records = event.get("Records")
    print("records")
    print(records)
    record = records[0].get('Sns')
    x_form_encoded_body = record.get("Message")
    decoded_body = urllib.parse.unquote(x_form_encoded_body)
    print("decoded_body")
    print(decoded_body)
    decoded_body_list = decoded_body.replace("=", ":")
    print("decoded_body_list")
    print(decoded_body_list)
    list_string = decoded_body_list.split("payload:")
    list_object = json.loads(list_string[1])
    actions = list_object.get("actions")
    finding_Id = actions[0].get("value")
    action_type = actions[0].get("text").get("text")
    print("finding_Id, action_type")
    return finding_Id, action_type


def get_finding_details(**kwargs):
    Findings = {}
    finding_Id = kwargs.get("finding_Id")
    print("finding_Id")
    print(finding_Id)
    try:
        connection = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
        connection.autocommit(True)
    except Exception as exp:
           exception_type, exception_value, exception_traceback = sys.exc_info()
           traceback_string = traceback.format_exception(exception_type, exception_value, exception_traceback)
           err_msg = json.dumps({
                "errorType": exception_type.__name__,
                "errorMessage": str(exception_value),
                "stackTrace": traceback_string
                    })
           logger.error(err_msg)
    logger.info("SUCCESS: Connection to RDS mysql instance succeeded at get_finding_details")
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
         query = """Select Title,ResourceArn,FindingId FROM findings WHERE Id = %s""";
         cursor.execute(query, finding_Id)
         for row in cursor:
             print(row['Title'], row['ResourceArn'])
             Findings['Title'] = row['Title']
             Findings['ResourceArn'] = row['ResourceArn']
             Findings['FindingId'] = row['FindingId']
    if connection:
       connection.close()
    print("Findings dictionary")
    print(Findings)
    return Findings


def fetch_remediation(**kwargs):
    remediation_dict = {}
    title = kwargs.get("finding_title")
    print("title", title)
    try:
        connection = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
        connection.autocommit(True)
    except Exception as exp:
        exception_type, exception_value, exception_traceback = sys.exc_info()
        traceback_string = traceback.format_exception(exception_type, exception_value, exception_traceback)
        err_msg = json.dumps({
            "errorType": exception_type.__name__,
            "errorMessage": str(exception_value),
            "stackTrace": traceback_string
        })
        logger.error(err_msg)
        sys.exit()
    logger.info("SUCCESS: Connection to RDS mysql instance succeeded at get_finding_details")
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql_query = "Select DocumentName,Bucket, ObjectKey, AutomationAssumeRole, Arguments, AccountId FROM remediation WHERE Title='%s'";
        print("fetch_remediation sql_query")
        value = cursor.execute(sql_query % title)
        print(value)
        for row in cursor:
            print(row['DocumentName'], row['Bucket'], row['ObjectKey'], row['AutomationAssumeRole'])
            remediation_dict['DocumentName'] = row['DocumentName']
            remediation_dict['Bucket'] = row['Bucket']
            remediation_dict['ObjectKey'] = row['ObjectKey']
            remediation_dict['AutomationAssumeRole'] = row['AutomationAssumeRole']
            remediation_dict['Arguments'] = row['Arguments']
            remediation_dict["AccountId"] = row["AccountId"]
    if connection:
       connection.close()
    print("Remediation Dict")
    print(remediation_dict)
    return remediation_dict


def start_automation_execution(**kwargs):
    client = kwargs.get('ssm_client')
    ssm_automation_parameters = kwargs.get("ssm_automation_parameters")
    automation_assume_role = ssm_automation_parameters.get("AutomationAssumeRole")
    automation_document_name = ssm_automation_parameters.get("DocumentName")
    customer_script_argument = json.dumps(kwargs.get("customer_script_argument"))
    presignedurl = kwargs.get("presignedurl")
    script_execution = client.start_automation_execution(
        DocumentName=automation_document_name,
        Parameters={
            'AutomationAssumeRole': [
                automation_assume_role,
            ],
            'Arguments': [
                customer_script_argument,
            ],
            'PreSignedUrl': [
                presignedurl,
            ]
        }
    )
    print(script_execution)
    return script_execution


def find_values_for_arguments_keys(**kwargs):
    customer_script_arguments = kwargs.get("customer_script_argument")
    customer_arguments_dict = json.loads(customer_script_arguments)
    remediation_title = kwargs.get("finding_title")
    resource_arn = kwargs.get("resource_arn")
    if remediation_title == "[S3.4] S3 Bucket Policies should not allow public access to the bucket":
        s3bucket_name = resource_arn.replace('arn:aws:s3:::', '')
        customer_arguments_dict["s3BucketName"] = s3bucket_name
        customer_arguments_dict["findingId"] = kwargs.get("finding_Id")
        customer_arguments_dict["accountId"] = kwargs.get("accountId")
    print(customer_arguments_dict)
    return customer_arguments_dict
    # { "s3BucketName": "", "findingId": "" }


def generate_presigned_url(**kwargs):
    s3_client = kwargs.get("s3_client")
    bucket_name = kwargs.get("bucket_name")
    object_name = kwargs.get("object_name")
    expiration = 300
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except Exception as e:
        logging.info(e)
        return None

    # The response contains the presigned URL
    print("PreSignedURL")
    print(response)
    return response


def confirm_finding_exists(**kwargs):
    Findings = {}
    Id = kwargs.get("Id")
    print("Id at confirm_finding_exists")
    print(Id)
    try:
        connection = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
        connection.autocommit(True)
    except Exception as exp:
        exception_type, exception_value, exception_traceback = sys.exc_info()
        traceback_string = traceback.format_exception(exception_type, exception_value, exception_traceback)
        err_msg = json.dumps({
            "errorType": exception_type.__name__,
            "errorMessage": str(exception_value),
            "stackTrace": traceback_string
        })
        logger.error(err_msg)
        sys.exit()
    logger.info("SUCCESS: Connection to RDS mysql instance succeeded at confirm_finding_exists")
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
         query = """Select FindingId FROM findings WHERE Id = %s""";
         cursor.execute(query, Id)
         for row in cursor:
             print(row['FindingId'])
             Findings['FindingId'] = row['FindingId']
    if connection:
       connection.close()
    print("Findings dictionary")
    print(Findings)
    return Findings


def suppress_finding(**kwargs):
    Id = kwargs.get("Id")
    finding_Id = kwargs.get("finding_Id")
    finding_details = confirm_finding_exists(Id=Id)
    suppressionName = "human user"
    SecurityHubResponse = {"RequestId" : "", "HTTPStatusCode": 0, "DateTime": ""}
    try:
        connection = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
        connection.autocommit(True)
    except Exception as exp:
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
    if finding_details:
       with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            print("FindingId at suppress_finding ",finding_Id)
            query = """UPDATE findings SET WorkflowStatus = %s WHERE Id = %s""";
            data = ("Suppressed", Id)
            value = cursor.execute(query, data)
            print("suppress value")
            print(value)
            connection.commit()
       if connection:
          connection.close()
       response = securityhub.update_findings(
       Filters={'Id': [{'Value': finding_Id,'Comparison': 'EQUALS'}]},
                Note={'Text': finding_Id + " has been suppressed",'UpdatedBy': suppressionName},
                RecordState='ARCHIVED'
            )
       SecurityHubResponse["RequestId"] = response.get("ResponseMetadata").get("RequestId")
       SecurityHubResponse["HTTPStatusCode"] = response.get("ResponseMetadata").get("HTTPStatusCode")
       SecurityHubResponse["DateTime"] = response.get("ResponseMetadata").get("HTTPHeaders").get('date')
       return SecurityHubResponse
    else:
        print("No finding_Id found for the passed value")

def publish_task(**kwargs):
    sns=boto3.client("sns", region_name="ap-south-1")
    response = sns.publish(
        TopicArn='arn:aws:sns:ap-south-1:xxsxxxxxx:Topic',
        Message=json.dumps({"default": json.dumps(kwargs.get("message"))}),
        Subject=kwargs.get("task_type"),
        MessageStructure='json'
    )
    print(response)


def lambda_handler(event, context):
    print(event)
    Findings = {}
    StoreMessage= {"TaskId": "", "FindingId": "", "TaskType": "", "DateTime": "" }
    # TODO implement
    Id, action_type = get_finding_type_and_Id(event=event)
    print("lambda handler")
    print(Id, action_type)
    findings_dict = get_finding_details(finding_Id=Id)
    if action_type == 'Remediate':
        finding_title = findings_dict.get("Title")
        print("finding_title", finding_title)
        finding_Id = findings_dict.get("FindingId")
        resource_arn = findings_dict.get("ResourceArn")
        remediation_dict = fetch_remediation(finding_title=finding_title)
        customer_script_argument = remediation_dict.get("Arguments")
        presigned_url = generate_presigned_url(s3_client=s3_client, bucket_name=remediation_dict.get("Bucket"),
                                               object_name=remediation_dict.get("ObjectKey"))
        customer_script_argument_updated = find_values_for_arguments_keys(finding_title=finding_title,
                                                                          customer_script_argument=customer_script_argument,
                                                                          finding_Id=finding_Id,
                                                                          resource_arn=resource_arn, accountId=remediation_dict.get("AccountId"))
        Response = start_automation_execution(ssm_client=ssm_client, ssm_automation_parameters=remediation_dict,
                                   presignedurl=presigned_url,
                                   customer_script_argument=customer_script_argument_updated)
        StoreMessage["TaskId"] = Response.get("AutomationExecutionId")
        StoreMessage["FindingId"] = finding_Id
        StoreMessage["Topic"] = "Success" if Response.get("ResponseMetadata").get("HTTPStatusCode") == 200 else "Failure"
        StoreMessage["TaskType"]="Remediation"
        StoreMessage["DateTime"]= Response.get("ResponseMetadata").get('HTTPHeaders').get("date")
        publish_task(task_type="save_task", message=StoreMessage)
        return
    elif action_type == 'Suppress':
         print("Suppress")
         findings_dict = get_finding_details(finding_Id=Id)
         finding_Id = findings_dict.get("FindingId")
         ResponseDict = suppress_finding(Id=Id, finding_Id=finding_Id)
         print("ResponseDict at RemediateFinding lambda_handler")
         print(ResponseDict)
         StoreMessage["TaskId"] = ResponseDict.get("RequestId")
         StoreMessage["FindingId"] = finding_Id
         StoreMessage["Topic"] = "Success" if ResponseDict.get("HTTPStatusCode") == 200 else "Failure"
         StoreMessage["TaskType"] = "Suppression"
         StoreMessage["DateTime"] = ResponseDict.get("DateTime")
         publish_task(task_type="save_task", message=StoreMessage)