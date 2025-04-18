import json
import boto3
import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('BuoyData')

s3 = boto3.client('s3')
bucket_name = 'oes-buoy-storage-bilal'

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

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Data stored successfully'})
    }
