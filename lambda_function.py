import json
from datetime import datetime

import boto3
from aws_xray_sdk.core import patch_all

patch_all()

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("Djf-WebDev-Cache")


def fetch_current_status():
    response = table.get_item(Key={"cacheItem": "suspense"})

    item = response["Item"]
    print(item)
    return item


def fetch_an_item():
    begin = datetime.now()

    the_item = fetch_current_status()

    end = datetime.now()
    duration = end - begin
    print(f"The fetch item took {duration} to execute")

    return the_item


def unexpected_response():
    return {
        "statusCode": 500,
        "body": json.dumps({"status": "error", "message": "unexpected", "data": None}),
    }


def lambda_handler(event, context):
    try:
        suspension_cache = fetch_an_item()
    except Exception as e:
        print(str(e))
        return unexpected_response

    if not suspension_cache["isSuspended"]:
        return {
            "statusCode": 200,
            "body": json.dumps(
                {"status": "success", "data": {"isComputeWorking": True}}
            ),
        }
    elif suspension_cache["isSuspended"]:
        return {
            "statusCode": 503,
            "body": json.dumps(
                {"status": "error", "message": "Operations suspended", "data": None}
            ),
        }
    else:
        return unexpected_response()
