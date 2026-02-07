document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const dropZoneContent = document.querySelector('.drop-zone-content');
    const previewContainer = document.getElementById('preview-container');
    const imagePreview = document.getElementById('image-preview');
    const removeBtn = document.getElementById('remove-btn');
    const analyzeBtn = document.getElementById('analyze-btn');
    const resultSection = document.getElementById('result-section');
    const analyzeBtnText = analyzeBtn.querySelector('.btn-text');
    const loader = analyzeBtn.querySelector('.loader');

    let selectedFile = null;

    // Trigger file input
    dropZone.addEventListener('click', () => {
        if (!selectedFile) fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });

    // Drag and Drop
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.remove('dragover');
        });
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        handleFiles(e.dataTransfer.files);
    });

    function handleFiles(files) {
        if (files.length > 0) {
            const file = files[0];
            if (file.type.startsWith('image/')) {
                selectedFile = file;
                const reader = new FileReader();
                reader.onload = (e) => {
                    imagePreview.src = e.target.result;
                    dropZoneContent.classList.add('hidden');
                    previewContainer.classList.remove('hidden');
                    analyzeBtn.classList.remove('disabled');
                    analyzeBtn.disabled = false;
                };
                reader.readAsDataURL(file);
            }
        }
    }

    removeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        selectedFile = null;
        fileInput.value = '';
        dropZoneContent.classList.remove('hidden');
        previewContainer.classList.add('hidden');
        analyzeBtn.classList.add('disabled');
        analyzeBtn.disabled = true;
        resultSection.classList.add('hidden');
    });

    analyzeBtn.addEventListener('click', async () => {
        if (!selectedFile) return;

        // UI State: Loading
        analyzeBtn.disabled = true;
        analyzeBtnText.textContent = 'Analysing MRI Scan...';
        loader.classList.remove('hidden');
        resultSection.classList.add('hidden');

        const selectedModel = document.querySelector('input[name="model"]:checked').value;
        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('model_id', selectedModel);

        try {
            const response = await fetch('http://localhost:8000/predict', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error('Analysis failed');

            const result = await response.json();
            displayResults(result);
        } catch (error) {
            console.error(error);
            alert('Error during analysis. Please ensure the backend is running.');
        } finally {
            analyzeBtn.disabled = false;
            analyzeBtnText.textContent = 'Initiate Analysis';
            loader.classList.add('hidden');
        }
    });

    function displayResults(data) {
        resultSection.classList.remove('hidden');

        // Update Prediction Text
        const predictionText = document.getElementById('prediction-text');
        const confidenceTag = document.getElementById('confidence-tag');

        predictionText.textContent = data.class === 'No Tumor' ? 'No Tumor Detected' : `${data.class} Detected`;
        confidenceTag.textContent = `${(data.confidence * 100).toFixed(1)}% Confidence`;

        // Update Probability Bars
        updateBar('glioma', data.probabilities['Glioma']);
        updateBar('meningioma', data.probabilities['Meningioma']);
        updateBar('pituitary', data.probabilities['Pituitary']);
        updateBar('normal', data.probabilities['No Tumor']);

        // Scroll to results
        resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function updateBar(id, value) {
        const bar = document.getElementById(`bar-${id}`);
        const valText = bar.parentElement.previousElementSibling.querySelector('.val');
        const percentage = (value * 100).toFixed(1);
        bar.style.width = `${percentage}%`;
        valText.textContent = `${percentage}%`;
    }
});
