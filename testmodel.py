import tensorflow as tf
from keras.models import load_model
# Load the saved model
model = load_model('MRI_MODEL.h5')

# Load the image you want to classify
img = tf.keras.preprocessing.image.load_img('media\IM00002.jpg', target_size=(224, 224))

# Preprocess the image
x = tf.keras.preprocessing.image.img_to_array(img)
x = x / 255.0
x = tf.expand_dims(x, axis=0)

# Make a prediction
predictions = model.predict(x)
print("predictions : ",predictions)
mri_prediction = model.predict(x)
print("mri_prediction : ",mri_prediction)

# Print the predicted class
predicted_class = tf.argmax(predictions, axis=1)
mri = mri_prediction.argmax(axis = 1)
print(mri)
print(predicted_class)

