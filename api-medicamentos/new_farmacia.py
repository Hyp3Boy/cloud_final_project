import json
import boto3


def lambda_handler(event, context):
    # Entrada (json)
    tenant_id = event["tenant_id"]
    farmacia_name = event["farmacia_name"]
    # Proceso
    farmacia = {
        "tenant_id": tenant_id,
        "farmacia_name": farmacia_name,
    }
    # Publicar en SNS
    sns_client = boto3.client("sns")
    response_sns = sns_client.publish(
        TopicArn="arn:aws:sns:us-east-1:223794358031:NuevaFarmacia",
        Subject="Nueva Farmacia",
        Message=json.dumps(farmacia),
        MessageAttributes={
            "tenant_id": {"DataType": "String", "StringValue": tenant_id},
            "farmacia_name": {"DataType": "String", "StringValue": farmacia_name},
        },
    )
    print(response_sns)
    print("exitoso")
    # Salida (json)
    return {"statusCode": 200, "response": response_sns}
