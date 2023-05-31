import cv2 
import numpy as np
import tensorflow as tf
from keras.models import load_model

# Load the saved model
model = load_model('F:\Githup Repos\Pulse\model.h5')

# Load the image you want to classify
image_path = "media\patients\john/ahmed\Scans/abnormal100.jpg"

# Preprocess the image
def preprocess_data(image_path):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (240, 200))
    img = img / 255.0
    img = np.expand_dims(img, axis=-1)
    return img

# Make a prediction
def predict_image(model, image_path):
    preprocessed_image = preprocess_data(image_path)
    predictions = model.predict(np.array([preprocessed_image]))
    class_labels = ['Normal', 'Myocardial Infarction', 'History of MI', 'Abnormal Heartbeat']
    predicted_label = class_labels[np.argmax(predictions)]
    return predicted_label

predicted_image = predict_image(model,image_path)
# Print the predicted class
print(predicted_image)


