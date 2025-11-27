const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const previewContainer = document.getElementById('previewContainer');
const previewImage = document.getElementById('previewImage');
const predictBtn = document.getElementById('predictBtn');
const resetBtn = document.getElementById('resetBtn');
const loading = document.getElementById('loading');
const resultContainer = document.getElementById('resultContainer');
const resultTitle = document.getElementById('resultTitle');
const resultConfidence = document.getElementById('resultConfidence');
const errorDiv = document.getElementById('error');

let selectedFile = null;

// Click to upload
uploadArea.addEventListener('click', () => fileInput.click());

// File selection
fileInput.addEventListener('change', (e) => {
    handleFile(e.target.files[0]);
});

// Drag & Drop
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    handleFile(e.dataTransfer.files[0]);
});

function handleFile(file) {
    if (!file) return;

    if (!file.type.startsWith('image/')) {
        showError('Please upload a valid image file');
        return;
    }

    if (file.size > 10 * 1024 * 1024) {
        showError('File size should be less than 10MB');
        return;
    }

    selectedFile = file;
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        uploadArea.style.display = 'none';
        previewContainer.style.display = 'block';
        resultContainer.style.display = 'none';
        errorDiv.style.display = 'none';
    };
    reader.readAsDataURL(file);
}

// Predict button
predictBtn.addEventListener('click', async () => {
    if (!selectedFile) return;

    loading.style.display = 'block';
    predictBtn.disabled = true;
    resultContainer.style.display = 'none';
    errorDiv.style.display = 'none';

    try {
        const formData = new FormData();
        formData.append('file', selectedFile);

        // CHANGE THIS URL TO YOUR FASTAPI BACKEND URL
        const response = await fetch("https://us-central1-nice-azimuth-477813-r1.cloudfunctions.net/predict", {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error('Prediction failed');

        const data = await response.json();
        displayResult(data);
    } catch (error) {
        showError('Failed to connect to server. Make sure your FastAPI backend is running.');
        console.error('Error:', error);
    } finally {
        loading.style.display = 'none';
        predictBtn.disabled = false;
    }
});

// Reset button
resetBtn.addEventListener('click', () => {
    selectedFile = null;
    fileInput.value = '';
    uploadArea.style.display = 'block';
    previewContainer.style.display = 'none';
    resultContainer.style.display = 'none';
    errorDiv.style.display = 'none';
});

function displayResult(data) {
    // Check if API call was successful
    if (!data.success) {
        showError(data.error || 'Prediction failed');
        return;
    }
    
    // Extract data from your backend's response format
    const className = data.class;
    const confidence = data.confidence.toFixed(2);
    
    resultTitle.textContent = `Result: ${className}`;
    resultConfidence.textContent = `Confidence: ${confidence}%`;
    

    // Color coding based on disease type
    if (className.toLowerCase().includes('healthy')) {
        resultContainer.className = 'result-container result-healthy';
    } else {
        resultContainer.className = 'result-container result-diseased';
    }

    resultContainer.style.display = 'block';
}

function showError(message) {
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}