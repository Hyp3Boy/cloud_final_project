# must be called as we're using zipped requirements
try:
    import unzip_requirements
except ImportError:
    pass

import boto3
import urllib.parse
import json
import trp.trp2 as t2
import random

print("Loading function")
s3 = boto3.client("s3")
textract = boto3.client("textract", region_name="us-east-1")


def generate_random_code():
    random_digits = "".join(str(random.randint(0, 9)) for _ in range(9))

    result_string = f"{random_digits}"
    return result_string


def get_textract_data(bucket_name, document_key):
    print("Loading getTextractData")
    # Call Amazon Textract
    print(textract)
    response = textract.analyze_document(
        Document={"S3Object": {"Bucket": bucket_name, "Name": document_key}},
        FeatureTypes=["LAYOUT"],
    )

    d = t2.TDocumentSchema().load(response)
    page = d.pages[0]

    data_dict = {}

    data_dict["NAME"] = page.page_layout.titles[0].text

    data_dict["CODIGO"] = generate_random_code()

    return data_dict


def lambda_handler(event, context):
    # Get the object from the event and show its content type
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(
        event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
    )
    fabricant_id = key.split("/")[0]  # Path: fabricant_id/medicamento.jpg
    print(bucket, key)
    print(json.dumps(event))

    try:
        response = get_textract_data(bucket, key)
        medname = response["NAME"]
        sns_client = boto3.client("sns")
        response_sns = sns_client.publish(
            TopicArn="arn:aws:sns:us-east-1:223794358031:NuevoMedicamento",
            Subject="Nuevo Medicamento",
            Message=json.dumps(response),
            MessageAttributes={
                "fabricant_id": {"DataType": "String", "StringValue": fabricant_id},
                "name": {"DataType": "String", "StringValue": medname},
            },
        )

        return {"statusCode": 200, "body": response_sns}

    except Exception as e:
        print(e)
        print("Error getting object {} from bucket {}. ".format(key, bucket))
        raise e
