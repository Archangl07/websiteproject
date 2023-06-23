import boto3

import key_config as keys


dynamodb_client = boto3.client(
    'dynamodb',
    #aws_access_key_id     = keys.ACCESS_KEY_ID,
    #aws_secret_access_key = keys.ACCESS_SECRET_KEY,
    region_name           = keys.REGION_NAME,
)
dynamodb_resource = boto3.resource(
    'dynamodb',
    #aws_access_key_id     = keys.ACCESS_KEY_ID,
    #aws_secret_access_key = keys.ACCESS_SECRET_KEY,
    region_name           = keys.REGION_NAME,
)

def create_table():
    table = dynamodb_resource.create_table(
        TableName='student',  # Name of the table
        KeySchema=[
            {
                'AttributeName': 'reg_number',
                'KeyType': 'HASH'  # HASH = partition key
            },
            {
                'AttributeName': 'email',
                'KeyType': 'RANGE'  # RANGE = sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'reg_number',  # Name of the attribute
                'AttributeType': 'S'  # S = String
            },
            {
                'AttributeName': 'email',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table

        