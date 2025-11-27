from google.cloud import storage
import tensorflow as tf
from PIL import Image
import numpy as np
import functions_framework
import os
import tempfile


BUCKET_NAME = "potato-disease-classification-models"
class_names = ['Early Blight', 'Late Blight', 'Healthy']

model = None


def download_blob(bucket_name, source_blob_name, destination_file_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print(f"Blob {source_blob_name} downloaded to {destination_file_name}")


@functions_framework.http
def predict(request):
    global model
    
    # Handle CORS for browser requests
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)
    
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    
    try:
        if model is None:
            # Use temp directory for cloud functions
            temp_dir = tempfile.gettempdir()
            model_path = os.path.join(temp_dir, "potatoes.h5")
            
            print(f"Downloading model to: {model_path}")
            
            download_blob(
                BUCKET_NAME,
                "models/potatoes.h5",
                model_path,
            )

            model = tf.keras.models.load_model(model_path)
            print("Model loaded successfully")
            print(f"Model input shape: {model.input_shape}")

        # Check if file is in request
        if 'file' not in request.files:
            return ({"error": "No file provided"}, 400, headers)
            
        image = request.files["file"]

        # Validate file
        if image.filename == '':
            return ({"error": "No file selected"}, 400, headers)

        # Read and preprocess image exactly as in saved_model code
        img = Image.open(image)
        
        # Convert to RGB if needed (handle PNG with alpha channel)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize to model input size
        img = img.resize((256, 256))
        
        # Convert to numpy array (NO normalization, same as saved_model code)
        image_array = np.array(img, dtype=np.float32)
        
        # Add batch dimension
        img_batch = np.expand_dims(image_array, axis=0)
        
        print(f"Image shape: {img_batch.shape}, dtype: {img_batch.dtype}")
        print(f"Image range: min={img_batch.min()}, max={img_batch.max()}")
        
        # Predict
        predictions = model.predict(img_batch)

        print("Raw predictions:", predictions[0])

        predicted_class = class_names[np.argmax(predictions[0])]
        confidence = round(100 * (np.max(predictions[0])), 2)
        
        # Get all class probabilities
        class_confidences = {
            class_names[i]: round(float(predictions[0][i]) * 100, 2)
            for i in range(len(class_names))
        }

        return ({
            'success': True,
            'class': predicted_class,
            'confidence': confidence,
        }, 200, headers)
        
    except Exception as e:
        import traceback
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        return ({"success": False, "error": str(e)}, 500, headers)