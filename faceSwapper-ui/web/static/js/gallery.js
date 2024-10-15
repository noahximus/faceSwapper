// commons.js
import * as commons from "./commons.js";

// ================================
// Upload functionality (from upload.js)
// ================================
export async  function uploadFile(inputId, uploadType) {
    const fileInput = document.getElementById(inputId);
    const file = fileInput.files[0];

    if (!file) {
        commons.showMessage(`Please upload a ${uploadType} file.`, false);
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
            commons.showMessage(`${uploadType.charAt(0).toUpperCase() + uploadType.slice(1)} uploaded successfully!`, true);
            loadImagesFromApiResult(`${uploadType}Gallery`, result.faces);
        } else {
            showMessage(`Upload failed: ${result.error}`, false);
        }
    } catch (error) {
        showMessage(`Error uploading ${uploadType}: ${error.message}`, false);
    }
}
// ================================
// Gallery handling (from gallery.js)
// ================================
export function loadImagesFromInput(divId, fileInput) {
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

export function loadImagesFromApiResult(divId, faces) {
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

export function duplicateFace(imageElement) {
    const parentContainer = imageElement.parentElement;
    const clonedContainer = parentContainer.cloneNode(true);

    // Update the click event to ensure the new cloned image can also be duplicated
    const duplicateBtn = clonedContainer.querySelector('.duplicate-btn');
    duplicateBtn.addEventListener('click', function() {
      duplicateFace(clonedContainer.querySelector('img'));
    });

    // Update the click event to ensure the new cloned image can also be duplicated
    const deleteButton = clonedContainer.querySelector('.delete-btn');
    deleteButton.addEventListener('click', function() {
      deleteFace(clonedContainer.querySelector('img'));
    });

    const parentParentContainer = parentContainer.parentElement;
    parentParentContainer.appendChild(clonedContainer);
}

export function deleteFace(button) {
    // Get the parent container of the image, which is .image-container
    const imageContainer = button.parentElement;
    imageContainer.remove();
}

export function handleImageLoad(imgSrc, faceName, index, galleryDiv) {
    const img = document.createElement('img');
    img.src = imgSrc;
    img.alt = faceName;
    img.draggable = true;
    img.dataset.index = index;

    const imageContainer = document.createElement('div');
    imageContainer.classList.add('image-container');
    imageContainer.draggable = true;
    imageContainer.dataset.index = index;

    const duplicateButton = document.createElement('button');
    duplicateButton.classList.add('duplicate-btn');
    duplicateButton.onclick = function() {
        duplicateFace(img);
    }
    duplicateButton.innerText = '+';

    const deleteButton = document.createElement('button');
    deleteButton.classList.add('delete-btn');
    deleteButton.onclick = function() {
        deleteFace(img);
    }
    deleteButton.innerText = '-';

    const buttonContainer = document.createElement('div');
    buttonContainer.classList.add('button-container');

    buttonContainer.appendChild(duplicateButton);
    buttonContainer.appendChild(deleteButton);

    imageContainer.appendChild(img);
    imageContainer.appendChild(buttonContainer);

    galleryDiv.appendChild(imageContainer);
}

export function makeImagesDraggable(containerId) {
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
        commons.showPreviews(this, document.getElementById('sourcePreview'));
        uploadFile(event.target.id, 'source');
        const files = event.target.files;
        const filenameDisplay = document.getElementById('sourceFilename');
        filenameDisplay.textContent = files.length > 0 ? files[0].name : '';
    });

    document.getElementById('target').addEventListener('change', function(event) {
        commons.showPreviews(this, document.getElementById('targetPreview'));
        uploadFile(event.target.id, 'target');
        const files = event.target.files;
        const filenameDisplay = document.getElementById('targetFilename');
        filenameDisplay.textContent = files.length > 0 ? files[0].name : '';
    });

    makeImagesDraggable('sourceGallery');
    makeImagesDraggable('targetGallery');
});

// Function to extract the current order of images from a given container
export function getImageOrder(containerElement) {
    const order = [];
    // Query the image containers inside the provided element
    containerElement.querySelectorAll('.image-container').forEach(container => {
        const index = container.dataset.index;  // Get the data-index attribute
        order.push(index);
    });
    return order;
}
export function equalizeHeightsAcrossGalleries() {
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
