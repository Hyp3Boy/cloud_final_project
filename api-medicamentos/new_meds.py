import json
import boto3
import os


def lambda_handler(event, context):
    # Entrada (json)
    print(event)  # Revisar en CloudWatch
    # body = json.loads(event["Records"][0]["Sns"])
    # print(body)  # Revisar en CloudWatch
    fabricant_id = event["Records"][0]["Sns"]['MessageAttributes']['fabricant_id']['Value']
    info = event["Records"][0]["Sns"]['MessageAttributes']['info']['Value']
    nombre_tabla = os.environ["TABLE_NAME"]

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(nombre_tabla)
    archivo = {"fabricant_id": fabricant_id, "info": info}
    print(archivo)  # Revisar en CloudWatch
    response = table.put_item(Item=archivo)
    # Salida (json)
    return {"statusCode": 200, "response": response}
