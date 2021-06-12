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
        "Detail" : "Bacterial spot of tomato is a potentially devastating disease that, in severe cases, can lead to unmarketable fruit and even plant death.  Bacterial spot can occur wherever tomatoes are grown, but is found most frequently in warm, wet climates, as well as in greenhouses.  The disease is often an issue in Wisconsin.",
        "Treatment" : "A plant with bacterial spot cannot be cured.  Remove symptomatic plants from the field or greenhouse to prevent the spread of bacteria to healthy plants.  Burn, bury or hot compost the affected plants and DO NOT eat symptomatic fruit.  Although bacterial spot pathogens are not human pathogens, the fruit blemishes that they cause can provide entry points for human pathogens that could cause illness.",
    },
    1 : {
        "Name" : "Tomato_Early_blight",
        "Detail" : "Early blight is a fungal disease caused by Alternaria solani. It can occur at any time during the growing season. High humidity and temperatures above 75°F cause it to spread rapidly. The fungus overwinters in the soil, and spores can be spread by wind, water, insects, and even on your clothes or shoes. If you catch an outbreak early enough, you may be able to save your crop. The tomatoes are still edible, particularly if the disease is mostly confined to the foliage.",
        "Treatment" : "Rotate Your Crops, When you harvest a bumper crop one year, it is so tempting to plant in the same spot the following season. However, if tomatoes are the crop in question, restrain yourself! You increase the chance of developing an early blight infection if you grow tomato plants in the same place in consecutive years. Wait at least two years before planting in the same location again, since the spores can persist in the soil and any partially decomposed plants for a year to follow.",
    },
    2 : {
        "Name" : "Tomato_Late_blight",
        "Detail" : "Phytophthora infestans, the pathogen that causes tomato late blight, needs tissue to survive. Sporangia from an infected plant are carried through the air, sometimes several miles, and once they land on a suitable host, germination is almost immediate. Tomato late blight needs only a few hours to take hold. All it wants is a little free moisture on the leaves from rain, fog, or morning dew.",
        "Treatment" : "Sanitation is the first step in controlling tomato late blight. Clean up all debris and fallen fruit from the garden area. This is particularly essential in warmer areas where extended freezing is unlikely and the late blight tomato disease may overwinter in the fallen fruit. Currently, there are no strains of tomato available that are resistant to late tomato blight, so plants should be inspected at least twice a week. Since late blight symptoms are more likely to occur during wet conditions, more care should be taken during those times.",
    },
    3 : {
        'Name' : "Tomato_Leaf_Mold",
        "Detail" : "Leaf mold of tomato is caused by pathogen Passalora fulva. It is found throughout the world, predominantly on tomatoes grown where the relative humidity is high, particularly in plastic greenhouses. Occasionally, if conditions are just right, leaf mold of tomato can be a problem on field grown fruit.",
        "Treatment" : "The pathogen P. fulfa can survive on infected plant debris or in the soil, although the initial source of the disease is often infected seed. The disease is spread by rain and wind, on tools and clothing, and via insect activity. High relative humidity (greater that 85%) combined with high temperatures encourages the spread of the disease. With that in mind, if growing tomatoes in a greenhouse, maintain night temps higher than outside temperatures.",
    },
    4 : {
        'Name' : "Tomato_Septoria_leaf_spot",
        "Detail" : "Septoria on tomato leaves manifests as water spots that are 1/16 to 1/4 inch (0.15-0.5 cm.) wide. As the spots mature, they have brown edges and lighter tan centers and become septoria leaf cankers. A magnifying glass would confirm the presence of small black fruiting bodies in the center of the spots. These fruiting bodies will ripen and explode and spread more fungal spores. The disease doesn’t leave marks on the stems or fruit but does spread upward to younger foliage.",
        "Treatment" : "Treating septoria leaf spot disease after it appears is achieved with fungicides. The chemicals need to be applied on a seven- to ten-day schedule to be effective. Spraying begins after blossom drop when the first fruits are visible. The most commonly used chemicals are maneb and chlorothalonil, but there are other options available to the home gardener. Potassium bicarbonate, ziram and copper products are a few other sprays useful against the fungus. Consult the label carefully for instructions on rate and method of application.",
    },
    5 : {
        'Name' : "Tomato_Spider_mites_Two_spotted_spider_mite",
        "Detail" : "Tiny spider mites are difficult to see with the naked eye, but the pests cause serious problems when they suck the juices from a tomato plant (Lycopersicon esculentum). An infested tomato plant displays tiny spots on the leaves. If left untreated, the pests spin cottony webs on the foliage; eventually, the leaves turn brown or yellow and drop from the plant. Keep tomato plants properly watered and fertilized because healthy plants are resistant to damage by mites and other pests.",
        "Treatment" : "Water tomato plants regularly and don't allow the soil to become bone dry. Water the surrounding area because mites thrive in hot, dry, dusty conditions. Direct a strong stream of water at the affected leaves as soon as you notice evidence of mites on the leaves and then repeat at least twice every week. Often, the water dislodges the mites and prevents a heavy infestation.Remove webs from tomato leaves with a damp cloth. Eliminating the webs removes the protective cover and prevents mites from laying eggs.",
    },
    6 : {
        'Name' : "Tomato__Target_Spot",
        "Detail" : "Target spot of tomato is caused by the fungal pathogen Corynespora cassiicola. The disease occurs on field-grown tomatoes in tropical and subtropical regions of the world. Target spot was first observed on tomatoes in the U.S. in Immokalee, Florida in 1967. The disease distribution in the U.S. is limited to the southeastern region, most predominantly in the southern parts of Florida. However, the disease also occurs on tomatoes grown in greenhouse and high tunnel production systems in other areas of North America.",
        "Treatment" : "Cultural practices for target spot management include improving airflow through the canopy by wider plant spacing and avoiding over-fertilizing with nitrogen, which can cause overly lush canopy formation. Pruning suckers and older leaves in the lower canopy can also increase airflow and reduce leaf wetness. Avoid planting tomatoes near old plantings. Inspect seedlings for target spot symptoms before transplanting. Manage weeds, which may serve as alternate hosts, and avoid the use of overhead irrigation. Destroy crop residues shortly after the final harvest, and rotate away from tomato and other known hosts for at least three years.",
    },
    7 : {
        'Name' : "Tomato__Tomato_YellowLeaf__Curl_Virus",
        "Detail" : "This is one of more than a dozen plant viruses that can infect tomatoes in both the home garden and commercial production fields in Florida. In contrast to the other viruses, the impact of TYLCV can be quite severe - virtually eliminating fruit production when plants are infected at an early age. The virus is physically spread plant-to-plant by the silverleaf whitefly. These insects can acquire this virus in 15-30 minutes during a feeding period on an infected plant. These infective whiteflies can then retain the virus for 10-12 days and introduce it into any number of healthy tomatoes during feeding periods. After this 10-12 day period, these infective whiteflies must reacquire this virus by feeding upon an infected plant again.",
        "Treatment" : "Symptomatic plants should be carefully covered by a clear or black plastic bag and tied at the stem at soil line. Cut off the plant below the bag and allow bag with plant and whiteflies to desiccate to death on the soil surface for 1-2 days prior to placing the plant in the trash. Do not cut the plant off or pull it out of the garden and toss it on the compost! The goal is to remove the plant reservoir of virus from the garden and to trap the existing virus-bearing whiteflies so they do not disperse onto other tomatoes.",
    },
    8 : {
        'Name' : "Tomato__Tomato_mosaic_virus",
        "Detail" : "Mosaic virus overwinters on perennial weeds and is spread by insects that feed on them. Aphids, leafhoppers, whiteflies and cucumber beetles are common garden pests that can transmit this disease. Soil, seed, starter pots and containers can be infected and pass the virus to the plant. Cuttings or divisions from infected plants will also carry the virus.",
        "Treatment" : "There are no cures for viral diseases such as mosaic once a plant is infected. As a result, every effort should be made to prevent the disease from entering your garden. Fungicides will NOT treat this viral disease, Plant resistant varieties when available or purchase transplants from a reputable source, Do NOT save seed from infected crops, Avoid working in the garden during damp conditions (viruses are easily spread when plants are wet).",
    },
    9 : {
        'Name' : "Tomato_healthy",
        "Detail" : "A healthy tomato plant has softly fuzzed, medium-green leaves. If the leaves of your plant have brown or black patches, holes, chewed edges or fuzzy mold growing on them, make a note of that before perusing the list of problems.",
        "Treatment" : "-",
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