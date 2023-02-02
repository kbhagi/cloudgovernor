import boto3
import os

def lambda_handler(event, context):
    # boto3 clients
    securityhub = boto3.client('securityhub')
    s3client = boto3.client('s3control')
    s3_resource = boto3.resource("s3")
    # create env vars
    remedidationName = 'S3_PrivateACL_Playbook'
    response_dict = { "s3": "", "securityhub": "", "FindingId": "" }
    # parse Account from SecHub Finding
    s3BucketName = event.get("s3BucketName")
    findingId = event.get("findingId")
    accountId = event.get("accountId")
    accountId = str(accountId)
    try:

        bucket_policy = s3_resource.BucketPolicy(s3BucketName)
        delete_response = bucket_policy.delete(
            ExpectedBucketOwner=accountId
        )
        response = s3client.put_public_access_block(
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            },
            AccountId=accountId
        )
        response_dict["s3"] = delete_response
        try:
            shub_response = securityhub.update_findings(
                Filters={'Id': [{'Value': findingId,'Comparison': 'EQUALS'}]},
                Note={'Text': 'A bucket policy that allowed public read and write access has been removed. The finding was archived. The bucket and account level access policies should be reviewed for any other instance of public or other unauthorized access being granted.','UpdatedBy': remedidationName},
                RecordState='ARCHIVED'
            )
            response_dict["securityhub"] = shub_response
            response_dict["FindingId"] = findingId
            return response_dict
        except Exception as e:
            raise e
    except Exception as e:
        raise e