import json
import boto3


def upload(event, context):
    s3 = boto3.client('s3')
    bucket = 'client-image-upload'
    file_name = event['Records'][0]['s3']['object']['key']
    key_name = event['Records'][0]['s3']['object']['key']
    s3.upload_file(file_name, bucket, key_name)    
    
def download(event, context):  
    s3 = boto3.client('s3')
    file_name = event['Records'][0]['s3']['object']['key']
    key_name = event['Records'][0]['s3']['object']['key']
    s3.download_file('client-image-processing', file_name, key_name)



def delete(event,context):      
    s3 = boto3.client('s3')
    file_name = event['Records'][0]['s3']['object']['key']
    s3.delete_object(Bucket='client-image-processing', Key=file_name)