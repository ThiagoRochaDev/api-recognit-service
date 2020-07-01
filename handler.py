import json
import boto3
from botocore.client import Config

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')

bucket_name = 'client-image-processing'
my_bucket = s3_resource.Bucket(bucket_name)


def download_recognized(event, context):
    file_array = []    
    for files in my_bucket.objects.all():
        url = s3_client.generate_presigned_url('get_object',
                                Params={
                                    'Bucket': 'client-image-processing',
                                    'Key': files.key,
                                },                                  
                                ExpiresIn=3600)
        file_array.append(url)
    return {
        "statusCode": 200,
        "body": json.dumps(file_array)
    }

   

        
 


    