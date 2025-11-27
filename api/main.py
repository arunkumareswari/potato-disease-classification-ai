from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf

app = FastAPI()

MODEL_PATH = r"D:\Projects\Deep Learning\Potato Disease Classification\saved_model\1"
print("Loading model from:", MODEL_PATH)

# Try loading as SavedModel
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("Model loaded successfully with tf.keras.models.load_model!")
    print(f"Model input shape: {model.input_shape}")

except Exception as e:
    print(f"Error loading with tf.keras.models.load_model: {e}")
    
    try:
        # Try loading as a SavedModel directory
        model = tf.saved_model.load(MODEL_PATH)
        print("Model loaded successfully with tf.saved_model.load!")
    except Exception as e2:
        print(f"Error loading with tf.saved_model.load: {e2}")
        raise e2

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:5500",  # VS Code Live Server
    "http://localhost:5500",   # Alternative Live Server port
    "null",                    # For file:// protocol (opening HTML directly)
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]

@app.get("/")
async def root():
    return {"message": "Potato Disease Classification API", "status": "running"}

@app.get("/ping")
async def ping():
    return {"message": "Hello, I am alive"}

def read_file_as_image(data) -> np.ndarray:
    """
    Read and preprocess image exactly as done during training
    """
    # Open image
    image = Image.open(BytesIO(data))
    
    # Convert to RGB if needed (handle PNG with alpha channel)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize to model input size (check your training code for exact size)
    image = image.resize((256, 256))
    
    # Convert to numpy array
    image = np.array(image, dtype=np.float32)
    
    return image

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Read and preprocess image
        image = read_file_as_image(await file.read())
        
        # Add batch dimension
        img_batch = np.expand_dims(image, axis=0)
        
        print(f"Image shape before prediction: {img_batch.shape}")
        print(f"Image dtype: {img_batch.dtype}")
        print(f"Image min: {img_batch.min()}, max: {img_batch.max()}")
        
        # Handle different model types
        if hasattr(model, 'predict'):
            # Keras model
            predictions = model.predict(img_batch)
        else:
            # SavedModel
            infer = model.signatures["serving_default"]
            
            # Get input key name
            input_key = list(infer.structured_input_signature[1].keys())[0]
            
            # Predict
            pred_dict = infer(**{input_key: tf.constant(img_batch, dtype=tf.float32)})
            predictions = list(pred_dict.values())[0].numpy()
        
        print(f"Raw predictions: {predictions[0]}")

        predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
        confidence = np.max(predictions[0])
        
        # Get all class probabilities
        class_confidences = {
            CLASS_NAMES[i]: float(predictions[0][i]) 
            for i in range(len(CLASS_NAMES))
        }
        
        return {
            'success': True,
            'class': predicted_class,
            'confidence': float(confidence),
            'all_predictions': class_confidences
        }
    
    except Exception as e:
        import traceback
        return {
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)