from keras.models import load_model
from collections import deque
import pickle
import cv2
import numpy as np
from django.core.files.storage import default_storage

def predict(grain_image):
    img_name = default_storage.save(grain_image.name,grain_image)
    img_url= default_storage.path(img_name)
    mean = np.array([123.68, 116.779, 103.939], dtype="float32")

    # Read image and normalize
    img = cv2.imread(img_url)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224)).astype("float32")
    img = img.reshape(1,224,224,3) 
    img -= mean

    # Load model, LB and predict
    Q = deque(maxlen=128)
    model = load_model("crop_diease_detection_model2.h5")
    lb = pickle.loads(open("label","rb").read())
    preds = model.predict(np.expand_dims(img,axis=0)[0])[0]
    Q.append(preds)
    results = np.array(Q).mean(axis=0)
    idx = np.argmax(results)
    label = lb.classes_[idx]
    return label




# predict_diease()