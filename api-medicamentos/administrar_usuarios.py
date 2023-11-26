import boto3
import json
from botocore.exceptions import ClientError

dynamodb_client = boto3.client('dynamodb')
table_name = 'NombreDeTuTablaDeEmpleados'

def lambda_handler(event, context):
    try:
        if event['httpMethod'] == 'POST':
            return agregar_empleado(event)
        elif event['httpMethod'] == 'PUT':
            return actualizar_empleado(event)
        elif event['httpMethod'] == 'DELETE':
            return eliminar_empleado(event)
        elif event['httpMethod'] == 'GET':
            return obtener_empleado(event)
        else:
            return {
                'statusCode': 400,
                'body': json.dumps('Método HTTP no soportado')
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps('Error en el servidor: ' + str(e))
        }

def agregar_empleado(event):
    data = json.loads(event['body'])
    try:
        if 'employee_id' not in data or 'nombre' not in data or 'email' not in data:
            return {
                'statusCode': 400,
                'body': json.dumps('Faltan datos necesarios')
            }

        dynamodb_client.put_item(
            TableName=table_name,
            Item={
                'employee_id': {'S': data['employee_id']},
                'nombre': {'S': data['nombre']},
                'email': {'S': data['email']},
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps('Empleado agregado con éxito')
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps('Error al agregar empleado: ' + str(e))
        }

def actualizar_empleado(event):
    data = json.loads(event['body'])
    try:
        update_expression = "SET nombre = :nombre"
        expression_attribute_values = {
            ':nombre': {'S': data['nombre']}
        }

        dynamodb_client.update_item(
            TableName=table_name,
            Key={
                'employee_id': {'S': data['employee_id']}
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        return {
            'statusCode': 200,
            'body': json.dumps('Empleado actualizado con éxito')
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps('Error al actualizar empleado: ' + str(e))
        }

def eliminar_empleado(event):
    data = json.loads(event['body'])
    try:
        dynamodb_client.delete_item(
            TableName=table_name,
            Key={
                'employee_id': {'S': data['employee_id']}
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps('Empleado eliminado con éxito')
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps('Error al eliminar empleado: ' + str(e))
        }

def obtener_empleado(event):
    employee_id = event['queryStringParameters']['employee_id']
    try:
        response = dynamodb_client.get_item(
            TableName=table_name,
            Key={
                'employee_id': {'S': employee_id}
            }
        )
        if 'Item' in response:
            return {
                'statusCode': 200,
                'body': json.dumps(response['Item'])
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps('Empleado no encontrado')
            }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps('Error al obtener empleado: ' + str(e))
        }
      
