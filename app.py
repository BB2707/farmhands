import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io

# --- Load Keras Model ---
try:
    import tensorflow as tf
    from tensorflow import keras
    model = keras.models.load_model('plant_disease_model.h5')
    class_names = [
        'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
        'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
        'Corn_(maize)___Cercoppora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_',
        'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot',
        'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
        'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
        'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight',
        'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy',
        'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy',
        'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold',
        'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite',
        'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
        'Tomato___healthy'
    ]
except (ImportError, IOError) as e:
    print("Warning: TensorFlow/Keras model not loaded. The /predict endpoint will not work.")
    print(f"Error details: {e}")
    model = None
    class_names = []


# --- Flask App Initialization ---
app = Flask(__name__)
CORS(app)


# --- API Endpoints ---

@app.route('/predict', methods=['POST'])
def predict():
    if model is None: 
        return jsonify({'error': 'Model is not loaded'}), 500
    if 'file' not in request.files: 
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '': 
        return jsonify({'error': 'No selected file'}), 400
        
    try:
        img = Image.open(io.BytesIO(file.read())).convert('RGB')
        img = img.resize((224, 224))
        img_array = keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0
        
        predictions = model.predict(img_array)
        
        predicted_class_index = np.argmax(predictions[0])
        predicted_class_name = class_names[predicted_class_index].replace('___', ' - ').replace('_', ' ')
        confidence = float(np.max(predictions[0])) * 100
        
        return jsonify({'prediction': predicted_class_name, 'confidence': f"{confidence:.2f}%"})
        
    except Exception as e:
        return jsonify({'error': f'Error processing image: {e}'}), 500

# --- Main Execution ---
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')