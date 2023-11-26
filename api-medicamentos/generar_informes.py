import boto3
import json
from datetime import datetime

dynamodb_client = boto3.client('dynamodb')
table_name = 'RegistroEntradaSalida'

def lambda_handler(event, context):
    try:
        fecha_inicio = event['queryStringParameters']['fecha_inicio']
        fecha_fin = event['queryStringParameters']['fecha_fin']
    except KeyError:
        return {'statusCode': 400, 'body': json.dumps('Parámetros de fecha requeridos')}

    registros = obtener_registros(fecha_inicio, fecha_fin)
    informe = procesar_registros(registros)

    return {
        'statusCode': 200,
        'body': json.dumps({'informe': informe})
    }

def obtener_registros(fecha_inicio, fecha_fin):
    try:
        response = dynamodb_client.scan(
            TableName=table_name,
            FilterExpression="timestamp BETWEEN :fecha_inicio AND :fecha_fin",
            ExpressionAttributeValues={
                ':fecha_inicio': {'S': fecha_inicio + "T00:00:00"},
                ':fecha_fin': {'S': fecha_fin + "T23:59:59"}
            }
        )
        return response['Items']
    except ClientError as e:
        print(e)
        return []

def procesar_registros(registros):
    informe = {}
    for registro in registros:
        employee_id = registro['employee_id']['S']
        timestamp = datetime.strptime(registro['timestamp']['S'], '%Y-%m-%dT%H:%M:%S')

        if employee_id not in informe:
            informe[employee_id] = {'horas_trabajadas': 0, 'registros': []}

        informe[employee_id]['registros'].append(timestamp)

    for emp_id, datos in informe.items():
        sorted_timestamps = sorted(datos['registros'])
        total_horas = sumar_horas(sorted_timestamps)
        informe[emp_id]['horas_trabajadas'] = total_horas
        del informe[emp_id]['registros']  

    return informe

def sumar_horas(timestamps):
    total_horas = 0
    for i in range(0, len(timestamps), 2):
        entrada = timestamps[i]
        salida = timestamps[i + 1] if i + 1 < len(timestamps) else entrada
        total_horas += (salida - entrada).total_seconds() / 3600
    return total_horas
