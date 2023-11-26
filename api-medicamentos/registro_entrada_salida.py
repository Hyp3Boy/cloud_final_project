import boto3
from datetime import datetime

def lambda_handler(event, context):
    rekognition_client = boto3.client('rekognition')
    dynamodb_client = boto3.client('dynamodb')

    image_data = event['image_data']

    try:
        response = rekognition_client.search_faces_by_image(
            CollectionId='tu_coleccion_de_rekognition',
            Image={'Bytes': image_data}
        )
    except Exception as e:
        print(e)
        return {'statusCode': 500, 'body': 'Error en el reconocimiento facial'}

    employee_id = response['FaceMatches'][0]['Face']['ExternalImageId']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        dynamodb_client.put_item(
            TableName='tu_tabla_dynamodb',
            Item={
                'employee_id': {'S': employee_id},
                'timestamp': {'S': timestamp}
            }
        )
    except Exception as e:
        print(e)
        return {'statusCode': 500, 'body': 'Error al registrar en DynamoDB'}

    return {'statusCode': 200, 'body': 'Registro exitoso'}
