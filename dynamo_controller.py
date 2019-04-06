from datetime import datetime

import boto3

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("Djf-WebDev-Cache")


def fetch_current_status():
    response = table.get_item(Key={"cacheItem": "suspense"})

    item = response["Item"]
    print(item)
    return item


def place_suspense_status(is_suspended):
    table.put_item(Item={"cacheItem": "suspense", "isSuspended": is_suspended})


def fetch_an_item():
    begin = datetime.now()

    the_item = fetch_current_status()

    end = datetime.now()
    duration = end - begin
    print(f"The fetch item took {duration} to execute")

    return the_item


if __name__ == "__main__":
    place_suspense_status(False)
    fetch_an_item()
