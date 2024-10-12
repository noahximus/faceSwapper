// ================================
// Show message functionality (from commons.js)
// ================================
function showMessage(text, success = true) {
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

// ================================
// Upload functionality (from upload.js)
// ================================
async function uploadFile(inputId, uploadType) {
    const fileInput = document.getElementById(inputId);
    const file = fileInput.files[0];

    if (!file) {
        showMessage(`Please upload a ${uploadType} file.`, false);
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
            showMessage(`Upload failed: ${result.error}`, false);
        }
    } catch (error) {
        showMessage(`Error uploading ${uploadType}: ${error.message}`, false);
    }
}

// ================================
// Show image previews
// ================================
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
// Gallery handling (from gallery.js)
// ================================
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
    equalizeHeightsAcrossGalleries();
}

function loadImagesFromApiResult(divId, faces) {
    console.log('loadImagesFromApiResult')
    const galleryDiv = document.getElementById(divId);  // Get the div by its ID
    galleryDiv.innerHTML = '';  // Clear any existing images in the gallery

    // Iterate over the faces array
    faces.forEach((faceBase64, index) => {
        // Create the img.src directly from base64
        const imgSrc = `data:image/jpeg;base64,${faceBase64}`;
        handleImageLoad(imgSrc, `Face ${index + 1}`, index, galleryDiv);
    });
    equalizeHeightsAcrossGalleries();
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

// ================================
// Initialization (from preparation.js)
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

    makeImagesDraggable('sourceGallery');
    makeImagesDraggable('targetGallery');
});

// Function to extract the current order of images from a given container
function getImageOrder(containerElement) {
    const order = [];
    // Query the image containers inside the provided element
    containerElement.querySelectorAll('.image-container').forEach(container => {
        // const filename = container.querySelector('.image-filename').textContent;  // Get the filename
        const index = container.dataset.index;  // Get the data-index attribute
        // const imgSrc = container.querySelector('img').src;  // Get the base64 image source
        
        // Store both filename, index, and the image src in the array
        // order.push({ 
        //     // filename: filename, 
          // 'index': index,
          // imgSrc: imgSrc 
        // });
        order.push(index);
    });
    return order;
}

function showBase64Previews(base64String, previewContainer) {
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

function equalizeHeightsAcrossGalleries() {
    const containers = document.querySelectorAll('.source-gallery .image-container, .target-gallery .image-container');
    let maxHeight = 0;

    // Reset height to auto so we can calculate the correct height
    containers.forEach(container => {
        container.style.height = 'auto';  // Reset the height
    });

    // Calculate the tallest container across both galleries
    containers.forEach(container => {
        const height = container.offsetHeight;
        if (height > maxHeight) {
            maxHeight = height;
        }
    });

    // Set all containers in both source and target galleries to the maximum height
    containers.forEach(container => {
        container.style.height = `${maxHeight}px`;
    });
}

// Run the equalizeHeightsAcrossGalleries function after the images load
window.onload = equalizeHeightsAcrossGalleries;

// Optionally, you can re-run this function if new images are added dynamically
