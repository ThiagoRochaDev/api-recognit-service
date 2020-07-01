import json
import boto3
from botocore.client import Config

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')

bucket_name = 'client-image-processing'
my_bucket = s3_resource.Bucket(bucket_name)


def download_process(event, context):   
    url = s3_client.generate_presigned_url('get_object',
                                Params={
                                    'Bucket': 'client-image-processing',
                                    'Key': 'destaque36.jpg',
                                },                                  
                                ExpiresIn=3600)


    return url

 

    