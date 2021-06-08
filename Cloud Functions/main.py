from google.cloud import storage
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image
from io import BytesIO
import base64
import numpy as np
import tensorflow as tf
from flask import jsonify
#import json

def get_model(bucket_name,source_file,destination):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_file)
    blob.download_to_filename(destination)
# Best model 500, Old model 224
# PIXELS = 224
PIXELS = 500
IMAGE_SIZE = (PIXELS, PIXELS)
MODEL_NAME = 'Best_Model_Tuning_Hyperparameter_Training_Layer_Atas.h5'
# MODEL_NAME = 'temp_model.h5'
MODEL_PATH = '/tmp/{}'.format(MODEL_NAME)

model = None



DESCRIPTION = {
    0 : {
        "Name" : "Tomato_Bacterial_spot",
        "Detail" : "Ini detailnya",
        "Treatment" : "Ini treatmentnya",
    },
    1 : {
        "Name" : "Tomato_Early_blight",
        "Detail" : "Ini detailnya",
        "Treatment" : "Ini treatmentnya",
    },
    2 : {
        "Treatment" : "Ini treatmentnya",
        "Name" : "Tomato_Late_blight",
        "Detail" : "Ini detailnya",
    },
    3 : {
        'Name' : "Tomato_Leaf_Mold",
        "Detail" : "Ini detailnya",
        "Treatment" : "Ini treatmentnya",
    },
    4 : {
        'Name' : "Tomato_Septoria_leaf_spot",
        "Detail" : "Ini detailnya",
        "Treatment" : "Ini treatmentnya",
    },
    5 : {
        'Name' : "Tomato_Spider_mites_Two_spotted_spider_mite",
        "Detail" : "Ini detailnya",
        "Treatment" : "Ini treatmentnya",
    },
    6 : {
        'Name' : "Tomato__Target_Spot",
        "Detail" : "Ini detailnya",
        "Treatment" : "Ini treatmentnya",
    },
    7 : {
        'Name' : "Tomato__Tomato_YellowLeaf__Curl_Virus",
        "Detail" : "Ini detailnya",
        "Treatment" : "Ini treatmentnya",
    },
    8 : {
        'Name' : "Tomato__Tomato_mosaic_virus",
        "Detail" : "Ini detailnya",
        "Treatment" : "Ini treatmentnya",
    },
    9 : {
        'Name' : "Tomato_healthy",
        "Detail" : "Ini detailnya",
        "Treatment" : "Ini treatmentnya",
    }
}


def detail(predict, conf):
    result = DESCRIPTION[predict].copy()
    result["Confidence"] = str(conf)
    return result

def preprocess_image(image):
    image = tf.image.resize(image, IMAGE_SIZE ) / 255.0
    image = tf.expand_dims(image, 0)
    return image

def open_image_as_base64(base64Image):
    image = Image.open(BytesIO(base64.b64decode(base64Image)))
    return image

def open_image(file):
    image = Image.open(file)
    return image

def api_tomato(request):
    global model
    # Only Load once
    if model == None:
        get_model('tomato-bucket',MODEL_NAME, MODEL_PATH)
        model = load_model(MODEL_PATH)

    if request.files.get('image'):
        # print("Image")
        file_image = request.files['image']
        image = open_image(file_image)
    else:
        # print("Base64")
        file_base64 = request.form['image']
        image = open_image_as_base64(file_base64)

    image = np.asarray(image)
    image = preprocess_image(image)
    prob = model.predict(image)
    predict = np.argmax(prob[0])
    result = detail(predict, prob[0][predict])
    response = jsonify([result])
    return response