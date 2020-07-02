import json
import boto3
from botocore.client import Config

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')


def download_client_recognized(event, context):
    bucket_name = 'client-image-processing'
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
    bucket_name = 'client-image-upload'
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
        bucket_name = 'client-image-upload'
        my_bucket = s3_resource.Bucket(bucket_name)
        response = my_bucket.delete_objects(
                            Delete={
                                'Objects': [
                                    {
                                        'Key': "download.jpg"  
                                    }
                                ]
                            }
                        )
        return {
        "statusCode": 200,
        "body": json.dumps(response)
                }   



def delete_client_recognized(event, context):  
        bucket_name = 'client-image-processing'
        my_bucket = s3_resource.Bucket(bucket_name)
        response = my_bucket.delete_objects(
                            Delete={
                                'Objects': [
                                    {
                                        'Key': "download.jpg"  
                                    }
                                ]
                            }
                        )
        return {
        "statusCode": 200,
        "body": json.dumps(response)
                }   