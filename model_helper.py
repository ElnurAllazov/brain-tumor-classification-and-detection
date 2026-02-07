import io
import numpy as np
from PIL import Image
import random
import time
import os

# Classes based on the notebook: Glioma, Meningioma, No Tumor, Pituitary
CLASS_NAMES = ['Glioma', 'Meningioma', 'No Tumor', 'Pituitary']

# Model Configurations
MODELS_CONFIG = {
    'baseline': 'baseline_cnn.keras',
    'inception': 'inception_v3.keras',
    'unet': 'u_net.keras'
}

loaded_models = {}

def preprocess_image(image_bytes):
    """
    Preprocessing logic based on the notebook:
    - Resize to 128x128
    - Normalize by 255
    """
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    image = image.resize((128, 128))
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0) # Add batch dimension
    return img_array

# Loading models if tensorflow is available
try:
    import tensorflow as tf
    from tensorflow.keras import backend as K

    def f1_score(y_true, y_pred):
        def recall(y_true, y_pred):
            true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
            possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
            recall = true_positives / (possible_positives + K.epsilon())
            return recall

        def precision(y_true, y_pred):
            true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
            predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
            precision = true_positives / (predicted_positives + K.epsilon())
            return precision

        precision_val = precision(y_true, y_pred)
        recall_val = recall(y_true, y_pred)
        return 2 * ((precision_val * recall_val) / (precision_val + recall_val + K.epsilon()))

    print("--- Model Loading Status ---")
    for mid, filename in MODELS_CONFIG.items():
        if os.path.exists(filename):
            try:
                # Use custom_objects to let Keras know about your f1_score function
                loaded_models[mid] = tf.keras.models.load_model(
                    filename, 
                    custom_objects={'f1_score': f1_score}
                )
                print(f"✅ SUCCESS: Loaded model '{mid}' from {filename}")
            except Exception as e:
                print(f"❌ ERROR loading {mid}: {e}")
        else:
            print(f"ℹ️ INFO: {filename} not found, using Mock for '{mid}'")
    print("--------------------------")
except ImportError:
    print("❌ CRITICAL: TensorFlow not found! All models will use 'Mock Mode'.")
    print("👉 Solution: Run 'pip install tensorflow'")
    tf = None

def get_prediction_result(model_id, image_bytes):
    """
    Main entry point for prediction. 
    Routes to real model if loaded, otherwise raises an error.
    """
    if model_id in loaded_models:
        return predict_real(model_id, image_bytes)
    else:
        raise ValueError(f"Model '{model_id}' is not loaded. Please ensure the .keras file exists.")

def predict_real(model_id, image_bytes):
    """
    Real prediction using a specific model.
    """
    curr_model = loaded_models.get(model_id)
    if not curr_model:
        raise ValueError(f"Model '{model_id}' session not found.")
    
    try:
        # 1. Determine the expected size and preprocessing
        input_shape = curr_model.input_shape[1:3]
        target_size = (input_shape[1], input_shape[0]) if input_shape[0] is not None else (128, 128)
        
        # 2. Load and resize
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        image = image.resize(target_size)
        
        # 3. Apply scaling
        # Based on your notebook: rescale=1./255 for all models
        img_array = np.array(image) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # 4. Predict and handle multiple outputs
        raw_results = curr_model.predict(img_array)
        
        # If your model has [main_out, aux_0, aux_1], we take main_out (the first one)
        if isinstance(raw_results, list):
            predictions = raw_results[0].flatten()
        else:
            predictions = raw_results.flatten()
            
        # Map predictions to class names (always using the first 4 slots)
        probs = {CLASS_NAMES[i]: float(predictions[i]) for i in range(len(CLASS_NAMES))}
        
        # Get the best class from the main output
        best_index = np.argmax(predictions[:len(CLASS_NAMES)])
        predicted_class = CLASS_NAMES[best_index]
        confidence = float(predictions[best_index])

        return {
            "class": predicted_class,
            "confidence": confidence,
            "probabilities": probs,
            "mode": f"real ({model_id})"
        }
    except Exception as e:
        print(f"❌ ERROR during prediction with '{model_id}': {str(e)}")
        raise e
