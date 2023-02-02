import sys
import logging
import pymysql
import json

# rds settings
rds_host = "xxxx.rds.amazonaws.com:3306/xxxx"
name = "xxxxx"
password = "xxxx"
db_name = "xxxxx"
# logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
try:
    conn = pymysql.connect(host="xxxxxx.rds.amazonaws.com", port=3306, user="xxxxx", passwd="xxxx", db="xxxx")
except:
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()
logger.info("SUCCESS: Connection to RDS mysql instance succeeded")


def lambda_handler(event, context):
    data = {
            'Id': event['id'],
            'Title': event['detail']['findings'][0]['Title'],
            'Description': event['detail']['findings'][0]['Description'],
            'Severity': event['detail']['findings'][0]['Severity']['Label'],
            'WorkflowStatus': event['detail']['findings'][0]['Workflow']['Status'],
            'Status': event['detail']['findings'][0]['Compliance']['Status'],
            'CreatedAt': event['detail']['findings'][0]['CreatedAt'],
            'Source': event['source'],
            'AccountNumber': event['account']
            }
    with conn.cursor() as cur:
        sql = "INSERT INTO `findings` (`Id`, `Title`, `Description`, `Severity`, `WorkflowStatus`, `Status`, `CreatedAt`, `Source`, `AccountNumber`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(sql, (data['Id'], data['Title'], data['Description'], data['Severity'], data['WorkflowStatus'], data['Status'], data['CreatedAt'], data['Source'], data['AccountNumber']))
        conn.commit()

    return {
        'statusCode': 200,
        'body': data,
    }

if __name__ == '__main__':
    status = lambda_handler({},{})
    print(status)
