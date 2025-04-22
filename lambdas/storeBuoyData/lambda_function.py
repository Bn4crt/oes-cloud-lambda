#test again

import json
import boto3
import datetime
from decimal import Decimal

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('BuoyData')

s3 = boto3.client('s3')
bucket_name = 'oes-buoy-storage-bilal'

sns = boto3.client('sns')
sns_topic_arn = 'arn:aws:sns:eu-north-1:123456789012:BuoyAlerts'


def lambda_handler(event, context):
    try:
        data = json.loads(event['body'])
    except KeyError:
        data = event  # fallback for curl/Postman direct calls

    buoy_id = data.get('buoy_id')
    temperature = Decimal(str(data.get('temperature')))
    wave_height = Decimal(str(data.get('wave_height')))
    timestamp = datetime.datetime.utcnow().isoformat()

    # Save to DynamoDB
    table.put_item(Item={
        'buoy_id': buoy_id,
        'timestamp': timestamp,
        'temperature': temperature,
        'wave_height': wave_height
    })

    # Save to S3
    file_name = f"{buoy_id}_{timestamp}.json"
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=json.dumps(data))

    # 🔔 Send critical alert if wave_height > 3.0
    if wave_height > Decimal("3.0"):
        alert_message = f"🌊 ALERT!\nBuoy: {buoy_id}\nWave height is critically high: {wave_height} meters\nTimestamp: {timestamp}"
        sns.publish(
            TopicArn=sns_topic_arn,
            Message=alert_message,
            Subject='🚨 Critical Ocean Alert: High Waves Detected'
        )

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Data stored and alert triggered if needed'})
    }