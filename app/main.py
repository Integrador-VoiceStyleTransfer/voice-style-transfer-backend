from fastapi import FastAPI,Form,UploadFile,File
from pydantic import BaseModel
from botocore.exceptions import NoCredentialsError
import boto3
import requests
import os
import array


app = FastAPI()




@app.get("/")
def read_root():
    return {"Welcome": "Voice-Style-Transfer-Backend"}


@app.post("/convert/")
async def convert(*, target_id: int = Form(...), model_id: int = Form(...), content_file : UploadFile = File(...)):
    

    
    #Subir archivo a AWS y obtener url de ubicación
    boo_response,msg,url_s3 = upload_file_to_AWS(content_file)
    #Llamer al worker celery mandandole la ubicación del archivo a convertir y recibiendo un id del trabajo
    

    
    

    #Llamer al worker celery mandandole la ubicación del archivo a convertir y recibiendo un id del trabajo
    #Descargar el archivo 
    #url_s3 ='https://vst-content.s3.amazonaws.com/all/jose_10.wav'
    
    request_wav = requests.get(url_s3)
    with open("content_sounds/"+content_file.filename, 'wb') as f:
        f.write(request_wav.content)
    
    
    path_local_content = "content_sounds/"+content_file.filename

    #Run el convert

    command ="python ./model_convert/test.py -m ./model_convert/model_3_spanish_speakers.pkl"+ " -s "+path_local_content+" -t "+str(target_id)

    os.system(command)


    
    path_local_target = "conversions/"+content_file.filename.split(".")[0]+"_to_"+"t"+str(target_id)+".wav"

    name_file = path_local_target.split("/")[1]

    byte_array = array.array('B')
    target_file =  open(path_local_target,"rb") 
    byte_array.fromstring(target_file.read())
    target_file.close()

    #Subimos la conversion a S3 
    boo_response_target,msg_target,url_s3_target = upload_file_to_AWS(byte_array,name_file,bucket_name="vst-target",URL="https://vst-target.s3.amazonaws.com/all/",tipo_File=True)
    
    #Borramos el Content y Target File local
    os.remove(path_local_content)
    os.remove(path_local_target)


    #Retornamo el enlace de la conversión
    response ={"target_url":url_s3_target,"content_url":url_s3,"model_id":model_id,"msg_content":msg,"msg_target":msg_target}

    return response


def upload_file_to_AWS(local_file,name="",bucket_name='vst-content',URL='https://vst-content.s3.amazonaws.com/all/',tipo_File=False):
    ##AQUI CREDENCIALES

    s3_client = boto3.client('s3',aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
    try:

        if(tipo_File == False):
            s3_response = s3_client.put_object(Bucket=bucket_name,ACL='public-read-write',Key="all/"+local_file.filename,Body=local_file.file,ContentType=local_file.content_type)
            url_file = URL+local_file.filename 
        else:
            file_name = name
            print("****************",file_name)
            s3_response = s3_client.put_object(Body=local_file.tobytes(),Bucket=bucket_name,Key="all/"+file_name,ContentType = 'audio/x-wav',ACL='public-read-write')

            #s3_response = s3_client.put_object(Bucket=bucket_name,ACL='public-read-write',Key="all/"+file_name,Body=local_file)
            url_file = URL+ file_name

        msg = 'Upload Succesfull'
        return True,msg,url_file
    except FileNotFoundError:
        error_msg = "The file was not found"
        return False,error_msg,''
    except NoCredentialsError:
        error_msg="Credentials not available"
        return False,error_msg,''
    

