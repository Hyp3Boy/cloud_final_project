import json
import boto3
import os


def lambda_handler(event, context):
    # Entrada (json)
    print(event)  # Revisar en CloudWatch
    body = json.loads(event["Records"][0]["body"])
    Message = json.loads(body["Message"])
    nombre_tabla = os.environ["TABLE_NAME"]
    
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(nombre_tabla)
    archivo = {
        "fabricant_id": Message["fabricant_id"],
        "info": Message["info"],
    }
    print(archivo)  # Revisar en CloudWatch
    response = table.put_item(Item=archivo)
    # Salida (json)
    return {"statusCode": 200, "response": response}
