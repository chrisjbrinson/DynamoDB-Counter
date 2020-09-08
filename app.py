import json
import boto3
import os

# Initialize dynamodb boto3 object
dynamodb = boto3.resource('dynamodb')
# Set dynamodb table name variable from env
ddbTableName = os.environ['databaseName']
table = dynamodb.Table(ddbTableName)

def lambda_handler(event, context):
    # Update item in table or add if doesn't exist 
    
    ddbResponse = table.update_item(
        Key={
            'id': 'Counter'
        },
        UpdateExpression='SET numberOfViews = numberOfViews + :value',
        ExpressionAttributeValues={
            ':value': 1
        },
        ReturnValues="UPDATED_NEW"
    )
    
    
    # Format dynamodb response into variable
    responseBody = ddbResponse
    responseBody["Attributes"]["numberOfViews"] = int(responseBody["Attributes"]["numberOfViews"])
    responseBody = json.dumps(ddbResponse["Attributes"]["numberOfViews"])
    
    
    # Create api response object
    apiResponse = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Credentails" : True
        },
        "body": responseBody
    }

    # Return api response object
    return apiResponse