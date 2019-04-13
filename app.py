from flask import Flask

import boto3,botocore
from boto.s3.connection import S3Connection

import os
from flask import request


import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


def fetch_image(image_name):
   filePath = "static/temp.png"    
   BUCKET_NAME = "aniboy"
   KEY = "stuff/{}.jpg".format(image_name)
  #image in s3 bucket
   s3 = boto3.resource('s3')
   try:
       s3.Bucket(BUCKET_NAME).download_file(KEY, filePath)
   except botocore.exceptions.ClientError as e:
       if e.response['Error']['Code'] == "404":
           print("The object does not exist.")
       else:
           raise
   return filePath   #store in static\



@app.route('/putimage',methods=["POST"])
def putimage():
    data=request.get_json()
    print(data)
    with open('static/data.json', 'w') as outfile:
        json.dump(data, outfile)


    return 'Hello, World!'



@app.route('/getimage',methods=["GET"])
def getimage():
    image_name=request.args.get("image_name")
    file_path=fetch_image(image_name)
    print(file_path)
    return 'Hello, World!'



if __name__=="__main__":
    app.run(host="0.0.0.0",port="8080")