# must be called as we're using zipped requirements
try:
    import unzip_requirements
except ImportError:
    pass

import boto3
import urllib.parse
import json
import random

print("Loading function")
s3 = boto3.client("s3")
textract = boto3.client("textract", region_name="us-east-1")


def extract_text(response, extract_by="LINE"):
    text = ""
    for item in response["Blocks"]:
        if item["BlockType"] == extract_by:
            text += item["Text"] + "\n"
    return text


def generate_random_code():
    random_digits = "".join(str(random.randint(0, 9)) for _ in range(9))

    result_string = f"{random_digits}"
    return result_string


def get_textract_data(bucket_name, document_key):
    print("Loading getTextractData")
    # Call Amazon Textract
    print(textract)

    response = textract.detect_document_text(
        Document={"S3Object": {"Bucket": bucket_name, "Name": document_key}}
    )

    print(json.dumps(response))

    data_dict = {}

    raw_text = extract_text(response, extract_by="LINE")

    # All the raw text in one line
    string_text = raw_text.replace("\n", " ")
    string_text = string_text.replace("\u00ae", " ")

    data_dict["INFO"] = string_text
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
        medinfo = response["INFO"]
        sns_client = boto3.client("sns")
        response_sns = sns_client.publish(
            TopicArn="arn:aws:sns:us-east-1:223794358031:NuevoMedicamento",
            Subject="Nuevo Medicamento",
            Message=json.dumps(response),
            # Add fabricant_id to Message
            MessageAttributes={
                "fabricant_id": {"DataType": "String", "StringValue": fabricant_id},
                "info": {"DataType": "String", "StringValue": medinfo},
            },
        )

        return {"statusCode": 200, "body": response_sns}

    except Exception as e:
        print(e)
        print("Error getting object {} from bucket {}. ".format(key, bucket))
        raise e
