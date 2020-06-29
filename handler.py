import json
import boto3





def upload(event, context):
    bucket =  "client-image-upload"
    file_name = event['Records'][0]['s3']['object']['key']
    s3.put_object( bucket, file_name, file_name)    
    
    
def download_process(event, context):
    s3 = boto3.client('s3')  
    bucket =  "client-image-upload"
    file_name = event['Records'][0]['s3']['object']['key']
    s3.list_objects(bucket)

def download_output(event, context):  
    bucket =  "client-image-processing"
    file_name = event['Records'][0]['s3']['object']['key']
    s3.get_object(bucket, file_name)



def delete_process(event,context):      
    bucket =  "client-image-upload"
    file_name = event['Records'][0]['s3']['object']['key']
    s3.delete_object(bucket,file_name)


def delete_output(event,context):      
    bucket =  "client-image-processing"
    file_name = event['Records'][0]['s3']['object']['key']
    s3.delete_object(bucket,file_name)