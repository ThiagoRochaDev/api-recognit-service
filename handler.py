import json
import boto3
from botocore.client import Config
import uuid
import os
from boto3.s3.transfer import TransferConfig
from itertools import takewhile, count
import base64

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')

def client_upload(event, context):
        print(event)
        img_bin = event['body']
        encoded_string = img_bin.encode('utf-8')
        image = base64.b64decode(encoded_string)
        
        bucket = 'image-bucket-uploads'
        client = event['pathParameters']['client']
        upload_path = '%s/{}'.format(event['pathParameters']['file'] + ".jpeg") % (client)
        response = s3_client.put_object(Key=upload_path,  Bucket=bucket, Body=image)
        
        return {
            "statusCode": 200,
            "headers": {
                "status": "ok",
                "Access-Control-Allow-Origin": "*"
                },
            "body": json.dumps(response)
                }


def download_client_images(event, context):
    bucket_name =  event['pathParameters']['bucket']
    my_bucket = s3_resource.Bucket(bucket_name)

    client = event['pathParameters']['client']
    file_array = []  
    count = 0  
    for files in my_bucket.objects.all():
        count+= 1 
        arr = files.key
        folder = arr.split("/")
        url = s3_client.generate_presigned_url('get_object',
                                Params={
                                    'Bucket': bucket_name,
                                    'Key': client + "/" + folder[1],
                                },                                  
                                ExpiresIn=3600)
        file_array.append(url)
        file_array.append(files.key)
    return {
        "statusCode": 200,
        "headers": {
                "status": "ok",
                "Access-Control-Allow-Origin": "*"
                },
        "body": json.dumps(file_array)
    }   
 
def delete_client_images(event, context):  
        bucket_name =  event['pathParameters']['bucket']
       
        client = event['pathParameters']['client']
        file = event['pathParameters']['file']
        my_bucket = s3_resource.Bucket(bucket_name)
        response = my_bucket.delete_objects(
                            Delete={
                                'Objects': [
                                    {
                                        'Key': client+"/"+file  
                                    }
                                ]
                            }
                        )
        return {
        "statusCode": 200,
        "headers": {
                "status": "ok",
                "Access-Control-Allow-Origin": "*"
                },
        "body": json.dumps(response)
                }   




def put_log_dynamo(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    file_name = event['Records'][0]['s3']['object']['key']

    print(str(event))
    print(str(bucket))
    print(str(file_name))

    json_object = s3_client.get_object(Bucket=bucket,Key=file_name)
    id_bd = str(uuid.uuid4())
    
    table = dynamodb.Table('Logs')
    table.put_item(Item={
        'id': id_bd,
        'file_name': file_name,
        'bucket_name': bucket,
        'event': event
        
    })