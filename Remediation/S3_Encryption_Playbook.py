import boto3
import os

def lambda_handler(event, context):
    # boto3 clients
    sts = boto3.client('sts')
    securityhub = boto3.client('securityhub')
    # create env vars
    awsRegion = os.environ['AWS_REGION']
    lambdaFunctionName = os.environ['AWS_LAMBDA_FUNCTION_NAME']
    masterAccountId = sts.get_caller_identity()['Account']
    # parse ASFF
    securityHubEvent = (event['detail']['findings'])
    for findings in securityHubEvent:
        # parse finding ID
        findingId =str(findings['Id'])
        # parse Account from SecHub Finding
        findingOwner = str(findings['AwsAccountId'])
        for resources in findings['Resources']:
            resourceId = str(resources['Id'])
            s3BucketName = resourceId.replace('arn:aws:s3:::', '')
            if findingOwner != masterAccountId:
                memberAcct = sts.assume_role(RoleArn='arn:aws:iam::' + findingOwner + ':role/XA-ElectricEye-Response',RoleSessionName='x_acct_sechub')
                # retrieve creds from member account
                xAcctAccessKey = memberAcct['Credentials']['AccessKeyId']
                xAcctSecretKey = memberAcct['Credentials']['SecretAccessKey']
                xAcctSeshToken = memberAcct['Credentials']['SessionToken']
                # create service client using the assumed role credentials
                s3 = boto3.client('s3',aws_access_key_id=xAcctAccessKey,aws_secret_access_key=xAcctSecretKey,aws_session_token=xAcctSeshToken)
                try:
                    # apply bucket encryption
                    response = s3.put_bucket_encryption(
                        Bucket=s3BucketName,
                        ServerSideEncryptionConfiguration={ 'Rules': [ { 'ApplyServerSideEncryptionByDefault': { 'SSEAlgorithm': 'AES256' } } ] }
                    )
                    try:
                        response = securityhub.update_findings(
                            Filters={'Id': [{'Value': findingId,'Comparison': 'EQUALS'}]},
                            Note={'Text': 'SSE-S3 AES-256 encryption was applied to the bucket and the finding was archived. If data in this bucket is highly sensitive consider creating a KMS CMK for encryption instead.','UpdatedBy': lambdaFunctionName},
                            RecordState='ARCHIVED'
                        )
                        print(response)
                    except Exception as e:
                        raise e
                except Exception as e:
                    raise e
            else:
                try:
                    s3 = boto3.client('s3')
                    # apply bucket encryption
                    response = s3.put_bucket_encryption(
                        Bucket=s3BucketName,
                        ServerSideEncryptionConfiguration={ 'Rules': [ { 'ApplyServerSideEncryptionByDefault': { 'SSEAlgorithm': 'AES256' } } ] }
                    )
                    try:
                        response = securityhub.update_findings(
                            Filters={'Id': [{'Value': findingId,'Comparison': 'EQUALS'}]},
                            Note={'Text': 'SSE-S3 AES-256 encryption was applied to the bucket and the finding was archived. If data in this bucket is highly sensitive consider creating a KMS CMK for encryption instead.','UpdatedBy': lambdaFunctionName},
                            RecordState='ARCHIVED'
                        )
                        return response
                    except Exception as e:
                        raise e
                except Exception as e:
                    raise e