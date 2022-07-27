import json
import boto3
import os


def lambda_message(event, context):
    type_check = "crawlerName"
    source = event.get("source")
    ms = event.get("detail")
    state = ms.get("state")
    name = ""
    id = "-"
    if source == "aws.glue":
        if type_check in ms:
            name = ms.get("crawlerName")
        else:
            name = ms.get("jobName")
            id = ms.get("jobRunId")

    elif source =="aws.codepipeline":
        name = ms.get("pipeline")
        id = ms.get("execution-id")

    content = f'AWS Resource:{name}\tStage_id:{id}\tState:{state}'
    
    client = boto3.client("sns")
    response = client.publish(
        TargetArn = os.environ.get("Topic"),
        Message = content,
        MessageStructure = 'string'
    )