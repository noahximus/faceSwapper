// ================================
// Commons.js functionality
// ================================

// Show message function
function showMessage(text, success = true) {
    const messageElement = document.getElementById('message');

    messageElement.textContent = text;
    messageElement.style.backgroundColor = success ? '#dff0d8' : '#f2dede'; // Light green or red
    messageElement.style.color = success ? '#3c763d' : '#a94442'; // Dark green or red
    messageElement.style.borderColor = success ? '#d6e9c6' : '#ebccd1'; // Border color based on success
    messageElement.classList.remove('hidden');
    messageElement.classList.add('visible');

    setTimeout(() => {
        messageElement.classList.remove('visible');
        messageElement.classList.add('hidden');
    }, 5000);
}

// Dynamically load external scripts
function loadExternalScript(scriptUrl) {
    const script = document.createElement('script');
    script.src = scriptUrl;
    script.type = 'text/javascript';
    script.defer = true;
    document.body.appendChild(script);
}

// ================================
// Upload.js functionality
// ================================

// Function to upload files (image/video)
async function uploadFile(inputId, uploadType) {
    const fileInput = document.getElementById(inputId);
    const file = fileInput.files[0];

    if (!file) {
        showMessage(`Please upload a ${uploadType} file (image or video).`, false);
        return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('uploadType', uploadType);

    try {
        const response = await fetch(apiUrlForUploads, {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        if (response.status === 200) {
            showMessage(`${uploadType.charAt(0).toUpperCase() + uploadType.slice(1)} uploaded successfully!`, true);
            loadImagesFromApiResult(`${uploadType}Gallery`, result.faces);
        } else {
            showMessage(`Upload failed! ${result.error}.`, false);
        }
    } catch (error) {
        showMessage(`${uploadType.charAt(0).toUpperCase() + uploadType.slice(1)} upload failed! Error: ${error.message}.`, false);
    }
}

// Show previews for images
function showPreviews(fileInput, previewContainer) {
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

// ================================
// Gallery.js functionality
// ================================

// Load images from input
function loadImagesFromInput(divId, fileInput) {
    const galleryDiv = document.getElementById(divId);
    const files = Array.from(fileInput.files);
    galleryDiv.innerHTML = ''; 

    files.forEach((file, index) => {
        const reader = new FileReader();
        reader.onload = function (event) {
            handleImageLoad(event.target.result, file.name, index, galleryDiv);
        };
        reader.readAsDataURL(file);
    });
}

function handleImageLoad(imgSrc, faceName, index, galleryDiv) {
    const img = document.createElement('img');
    img.src = imgSrc;
    img.alt = faceName;
    img.draggable = true;
    img.dataset.index = index;
    
    const imageContainer = document.createElement('div');
    imageContainer.classList.add('image-container');
    imageContainer.draggable = true;
    imageContainer.dataset.index = index;

    imageContainer.appendChild(img);
    galleryDiv.appendChild(imageContainer);
}

// ================================
// Preparation.js functionality
// ================================

document.addEventListener('DOMContentLoaded', function () {

    document.getElementById('source').addEventListener('change', function(event) {
        showPreviews(this, document.getElementById('sourcePreview'));
        uploadFile(event.target.id, 'source');
        const files = event.target.files;
        const filenameDisplay = document.getElementById('sourceFilename');
        filenameDisplay.textContent = files.length > 0 ? files[0].name : '';
    });

    document.getElementById('target').addEventListener('change', function(event) {
        showPreviews(this, document.getElementById('targetPreview'));
        uploadFile(event.target.id, 'target');
        const files = event.target.files;
        const filenameDisplay = document.getElementById('targetFilename');
        filenameDisplay.textContent = files.length > 0 ? files[0].name : '';
    });

    // Applying draggable functionality to galleries
    makeImagesDraggable('sourceGallery');
    makeImagesDraggable('targetGallery');
});

function makeImagesDraggable(containerId) {
    let draggedElement = null;

    document.getElementById(containerId).addEventListener('dragstart', (event) => {
        if (event.target.closest('.image-container')) {
            draggedElement = event.target.closest('.image-container');
            draggedElement.classList.add('dragging');
            event.dataTransfer.setData('text/plain', draggedElement.dataset.index);
        }
    });

    document.getElementById(containerId).addEventListener('dragover', (event) => {
        event.preventDefault();
        const target = event.target.closest('.image-container');
        if (target && target !== draggedElement) {
            target.style.border = '2px dashed #000';
        }
    });

    document.getElementById(containerId).addEventListener('drop', (event) => {
        event.preventDefault();
        const target = event.target.closest('.image-container');
        if (target && target !== draggedElement) {
            const draggedIndex = parseInt(draggedElement.dataset.index, 10);
            const targetIndex = parseInt(target.dataset.index, 10);

            const draggedImageSrc = draggedElement.querySelector('img').src;
            const targetImageSrc = target.querySelector('img').src;

            draggedElement.querySelector('img').src = targetImageSrc;
            target.querySelector('img').src = draggedImageSrc;

            draggedElement.dataset.index = targetIndex;
            target.dataset.index = draggedIndex;

            target.style.border = '';
            draggedElement.classList.remove('dragging');
        }
    });

    document.getElementById(containerId).addEventListener('dragend', (event) => {
        if (event.target.closest('.image-container')) {
            event.target.closest('.image-container').classList.remove('dragging');
        }
    });
}
