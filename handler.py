import json
import boto3
from botocore.client import Config
import uuid
import os
from boto3.s3.transfer import TransferConfig


s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')

def client_upload(event, context):
    with open(event['file'], "wb") as file:
        bucket = 'image-bucket-upload'
        upload_path = '/tmp/{}'.format(file)
        response = s3_client.upload_file(file,Key=upload_path,  Bucket=bucket, Body=file)
        # bucket_name = 'client-image-upload'
        # my_bucket = s3_resource.Bucket(bucket_name)
        # file_name = 'teste'
        # object_name = 'teste.jpg'
        # response = s3_client.upload_file(file_name, bucket_name, object_name)
        return {
            "statusCode": 200,
            "body": json.dumps(response)
                }

def download_client_recognized(event, context):
    bucket_name = 'image-bucket-recognized'
    my_bucket = s3_resource.Bucket(bucket_name)
    file_array = []    
    for files in my_bucket.objects.all():
        url = s3_client.generate_presigned_url('get_object',
                                Params={
                                    'Bucket': bucket_name,
                                    'Key': files.key,
                                },                                  
                                ExpiresIn=3600)
        file_array.append(url)
        file_array.append(files.key)
    return {
        "statusCode": 200,
        "body": json.dumps(file_array)
    }

def download_client_upload(event, context):
    bucket_name =  'image-bucket-upload'
    my_bucket = s3_resource.Bucket(bucket_name)
    file_array = []    
    for files in my_bucket.objects.all():
        url = s3_client.generate_presigned_url('get_object',
                                Params={
                                    'Bucket': bucket_name,
                                    'Key': files.key,
                                },                                  
                                ExpiresIn=3600)
        file_array.append(url)
        file_array.append(files.key)
    return {
        "statusCode": 200,
        "body": json.dumps(file_array)
    }   
 
def delete_client_upload(event, context):  
        bucket_name =  event['bucket']
        file_name = event['filename']
        my_bucket = s3_resource.Bucket(bucket_name)
        response = my_bucket.delete_objects(
                            Delete={
                                'Objects': [
                                    {
                                        'Key': file_name  
                                    }
                                ]
                            }
                        )
        return {
        "statusCode": 200,
        "body": json.dumps(response)
                }   

# def delete_client_recognized(event, context):  
#         bucket_name =  event['bucket']
#         file_name = event['filename']
#         my_bucket = s3_resource.Bucket(bucket_name)
#         response = my_bucket.delete_objects(
#                             Delete={
#                                 'Objects': [
#                                     {
#                                         'Key': file_name 
#                                     }
#                                 ]
#                             }
#                         )
#         return {
#         "statusCode": 200,
#         "body": json.dumps(response)
#                 }   


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