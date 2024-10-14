
    // ================================
    // Show message functionality (from commons.js)
    // ================================
    export function showMessage(text, success = true) {
        const messageElement = document.getElementById('message');
        messageElement.textContent = text;
        messageElement.style.backgroundColor = success ? '#dff0d8' : '#f2dede'; // Green or red
        messageElement.style.color = success ? '#3c763d' : '#a94442'; // Text color based on success
        messageElement.classList.remove('hidden');
        messageElement.classList.add('visible');

        setTimeout(() => {
            messageElement.classList.remove('visible');
            messageElement.classList.add('hidden');
        }, 5000);
    }

    export function waitFor(milliseconds) {
        return new Promise(resolve => setTimeout(resolve, milliseconds));
    }

    // ================================
    // Show image previews
    // ================================
    export function showPreviews(fileInput, previewContainer) {
        const files = Array.from(fileInput.files);
        previewContainer.innerHTML = ''; // Clear previous previews

        files.forEach((file) => {
            const reader = new FileReader();
            reader.onload = function (event) {
                const img = document.createElement('img');
                img.src = event.target.result;
                img.style.margin = '5px';
                previewContainer.appendChild(img);
            };
            reader.readAsDataURL(file);
        });
    }

    export function showBase64Previews(base64String, previewContainer) {
        previewContainer.innerHTML = ''; // Clear existing previews

        // base64Images.forEach((base64String) => {
        const img = document.createElement('img');
        img.src = base64String;  // Set the image source to the base64 string
        // img.style.margin = '5px'; // Add some margin between images
        img.style.maxWidth = '100vp'; // Optional: Limit the size of the preview images
        // img.style.maxHeight = '150px'; 
        previewContainer.appendChild(img); // Append the preview image to the container
        // });
    }

    // Show the loading spinner
    export function showLoadingSpinner() {
      document.getElementById('loadingSpinner').style.display = 'block';
    }

    // Hide the loading spinner
    export function hideLoadingSpinner() {
      document.getElementById('loadingSpinner').style.display = 'none';
    }

