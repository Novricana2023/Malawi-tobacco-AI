import numpy as np
from tensorflow.keras.preprocessing import image
import tensorflow as tf

# These global variables should be defined in your Streamlit app or passed accordingly
IMG_HEIGHT = 224
IMG_WIDTH = 224
CLASS_NAMES = ['Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy']

def preprocess_image(image_path):
    img = image.load_img(image_path, target_size=(IMG_HEIGHT, IMG_WIDTH))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    # Rescale pixel values from [0, 255] to [-1, 1] as expected by MobileNetV2
    img_array = (img_array / 127.5) - 1
    return img_array

def predict_disease(model, image_path, class_names):
    processed_image = preprocess_image(image_path)
    predictions = model.predict(processed_image)
    class_probabilities = dict(zip(class_names, predictions[0]))
    predicted_class_index = np.argmax(predictions[0])
    predicted_class_name = class_names[predicted_class_index]
    confidence = predictions[0][predicted_class_index]
    return predicted_class_name, confidence, class_probabilities
