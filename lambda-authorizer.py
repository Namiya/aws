import json
import jwt
import os

# Replace this with your actual secret key
SECRET_KEY = os.environ['SECRET_KEY']

def lambda_handler(event, context):
    # Get the token from the request headers
    token = event['headers']['Authorization']

    # Verify the JWT token
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.exceptions.DecodeError:
        return {
            'statusCode': 401,
            'body': json.dumps('Invalid token')
        }

    # Return an "Allow" policy if the token is valid
    return {
        'principalId': decoded_token['user_id'],
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': 'execute-api:Invoke',
                    'Effect': 'Allow',
                    'Resource': event['methodArn']
                }
            ]
        }
    }
