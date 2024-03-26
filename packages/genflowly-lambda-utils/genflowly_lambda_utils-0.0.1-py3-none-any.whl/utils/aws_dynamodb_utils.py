import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def save_to_dynamodb(data: dict, aws_region: str, table_name: str) -> dict:
    logger.info("Received data object: %s", data)
    dynamodb = boto3.resource('dynamodb', region_name=aws_region)
    response = {}
    try:
        table = dynamodb.Table(table_name)
        print("Received item_data : %s", data)
        response = table.put_item(Item=data)  # putItem expects a dict object
        logger.info("Saved data object: %s", str(response))
    except Exception as e:
        logger.error("Save to DynamoDB failed: %s", e)
    return response


def read_from_dynamodb(table_name: str, key: dict, aws_region: str) -> dict:
    logger.info("Received request to get item: %s from table: %s", key, table_name)
    dynamodb = boto3.resource('dynamodb', region_name=aws_region)
    response = {}
    try:
        table = dynamodb.Table(table_name)
        response = table.get_item(Key=key)  # getItem expects a key
        if 'Item' in response:
            logger.info("Retrieved item: %s", str(response['Item']))
        else:
            logger.info("No item found with key: %s", key)
    except Exception as e:
        logger.error("Read from DynamoDB failed: %s", e)
    return response
