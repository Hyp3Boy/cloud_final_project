import boto3
import json
from datetime import datetime

dynamodb_client = boto3.client('dynamodb')
table_name = 'RegistroEntradaSalida'

def lambda_handler(event, context):
    try:
        data = json.loads(event['body'])
        employee_id = data['employee_id']
        tipo_registro = data['tipo_registro'] 
    except KeyError:
        return {'statusCode': 400, 'body': json.dumps('Faltan datos necesarios')}

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        dynamodb_client.put_item(
            TableName=table_name,
            Item={
                'employee_id': {'S': employee_id},
                'timestamp': {'S': timestamp},
                'tipo_registro': {'S': tipo_registro}
            }
        )
        return {'statusCode': 200, 'body': json.dumps(f'Registro de {tipo_registro} exitoso para el empleado {employee_id}')}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps('Error al registrar en DynamoDB: ' + str(e))}
