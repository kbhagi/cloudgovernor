UPDATE BotInsights.remediation SET Title = '[S3.4] S3 Bucket Policies should not allow public access to the bucket', Description = 'Put private ACL on a bucket to remove public read or write access ', DocumentName = 'KB-AWS-ExecuteScript', Bucket = 'sbotplaybooks', Arguments = '{ "s3BucketName": "", "findingId": "" }', ObjectKey = 'S3_PrivateACL_Playbook.py', AutomationAssumeRole = 'arn:aws:iam::AccId:role/StoreBotInsightsLambda', AccountId = AccId WHERE Id = '9c166897-2336-43ab-a0cb-ce26a14ad466';