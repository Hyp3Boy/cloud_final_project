import json
import boto3
import os


def lambda_handler(event, context):
    # Entrada (json)
    print(event)  # Revisar en CloudWatch
    body = json.loads(event["Records"][0]["body"])
    tenant_id = body["tenant_id"]
    farmacia_name = body["farmacia_name"]
    name_table = os.environ["FARMACIA_TABLE"]
    # Proceso
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(name_table)
    archivo = {
        "tenant_id": tenant_id,
        "farmacia_name": farmacia_name,
    }
    print(archivo)  # Revisar en CloudWatch
    response = table.put_item(Item=archivo)
    # Salida (json)
    return {"statusCode": 200, "response": response}
