import boto3
import os


sns = boto3.client('sns')

TOPIC_ARN = os.environ['TOPIC_ARN']  

def lambda_handler(event, context):
    try:
        email = event['request']['userAttributes']['email']
        print(f"Subscribing new user to SNS: {email}")
        
        response = sns.subscribe(
            TopicArn=TOPIC_ARN,
            Protocol='email',
            Endpoint=email
        )
        
        print("SNS Subscription response:", response)
        
        return event  # Always return the original event
    except Exception as e:
        print("Error subscribing to SNS:", str(e))
        return event  # Still return the event even on error
