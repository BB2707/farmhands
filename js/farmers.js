document.addEventListener('DOMContentLoaded', () => {
    // Get references to all the necessary HTML elements
    const imageUpload = document.getElementById('imageUpload');
    const imagePreview = document.getElementById('imagePreview');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const analysisResult = document.getElementById('analysisResult');
    const plantType = document.getElementById('plantType');
    const plantCondition = document.getElementById('plantCondition');

    // The URL of your local Flask backend API
    const API_URL = 'http://127.0.0.1:5000/predict';

    let uploadedFile = null;

    // Listen for when the user selects a file
    imageUpload.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            uploadedFile = file; // Store the file object

            // Use FileReader to read the selected file and display a preview
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview.src = e.target.result;
            };
            reader.readAsDataURL(file);

            // Enable the "Analyze" button and hide old results
            analyzeBtn.disabled = false;
            analysisResult.style.display = 'none';
        }
    });

    // Listen for clicks on the "Analyze" button
    analyzeBtn.addEventListener('click', () => {
        if (!uploadedFile) {
            alert("Please choose an image first.");
            return;
        }

        // --- Start of API Call Logic ---
        analysisResult.style.display = 'none';
        analyzeBtn.textContent = 'Analyzing...';
        analyzeBtn.disabled = true;

        // Use FormData to send the file in the request
        const formData = new FormData();
        formData.append('file', uploadedFile);

        // Use the fetch API to send the image to the Python backend
        fetch(API_URL, {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                // If server responds with an error, show it
                return response.json().then(err => { throw new Error(err.error || 'Server error') });
            }
            return response.json();
        })
        .then(data => {
            // Success! Display the prediction from the server
            const parts = data.prediction.split(' - ');
            const type = parts[0] || 'Unknown';
            const condition = parts[1] || 'N/A';
            
            plantType.textContent = type;
            plantCondition.textContent = `${condition} (${data.confidence})`;

            // Determine status color based on keywords
            plantCondition.className = ''; // Clear old classes
            if (condition.toLowerCase().includes('healthy')) {
                plantCondition.classList.add('status-good');
            } else {
                plantCondition.classList.add('status-danger');
            }
            
            analysisResult.style.display = 'block';
        })
        .catch(error => {
            // Handle errors (e.g., server not running, network issue)
            console.error('Error:', error);
            plantType.textContent = "Analysis Failed";
            plantCondition.textContent = error.message;
            plantCondition.className = '';
            plantCondition.classList.add('status-danger');
            analysisResult.style.display = 'block';
        })
        .finally(() => {
            // Always reset the button after the request is complete
            analyzeBtn.textContent = 'Analyze Plant';
            analyzeBtn.disabled = false;
        });
    });
});

