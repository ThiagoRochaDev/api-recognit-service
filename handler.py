import json
import boto3


def upload(event, context):
    s3 = boto3.client('s3')
    bucket = 'your-bucket-name'
    file_name = 'location-of-your-file'
    key_name = 'name-of-file-in-s3'
    s3.upload_file(file_name, bucket, key_name)    
    
def download(event, context):  
    s3 = boto3.client('s3')
    s3.download_file('BUCKET_NAME', 'OBJECT_NAME', 'FILE_NAME')



def delete(event,context):      
    s3 = boto3.client('s3')
    s3.delete_object(Bucket='mybucketname', Key='myfile.whatever')