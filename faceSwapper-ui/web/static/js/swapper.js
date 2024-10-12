
async function swapFaces(source, sourceGallery, target, targetGallery) {

    try {

        const sourceFile = document.getElementById(source).files[0];
        const targetFile = document.getElementById(target).files[0];
        if (!sourceFile || !targetFile) {
            showMessage(`Please make sure both source and target files are present.`, false);
            return;
        }

        // const sourceGalleryFaces = getImageOrder(sourceGallery);
        // const targetGalleryFaces = getImageOrder(targetGallery);

        const sourceGalleryOrder = getImageOrder(document.getElementById(sourceGallery));
        const targetGalleryOrder = getImageOrder(document.getElementById(targetGallery));
        if (sourceGalleryOrder.length === 0 || targetGalleryOrder.length === 0) {
            showMessage(`Please make sure both source and target images have faces in them.`, false);
            return;
        }

        const formData = new FormData();
        formData.append('sourceFile', sourceFile);
        formData.append('sourceGalleryOrder', JSON.stringify(sourceGalleryOrder));  // Convert array to JSON string
        // formData.append('sourceGalleryFaces', sourceGalleryFaces);  // Convert array to JSON string
        formData.append('targetFile', targetFile);
        formData.append('targetGalleryOrder', JSON.stringify(targetGalleryOrder));  // Convert array to JSON string
        // formData.append('targetGalleryFaces', targetGalleryFaces);  // Convert array to JSON string

        const response = await fetch(apiUrlForFaceSwap, {
            method: 'POST',
            body: formData
        });

        // Check if the response is okay before attempting to parse JSON
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        if (response.status === 200) {

            // Reference to the preview container
            const resultsPreview = document.getElementById('resultsPreview');

            showBase64Previews(result.swapped_image, resultsPreview)

            showMessage(`Face swap operation successful!`, true);
        } else {
            showMessage(`Face swap operation failed! ${result.error}.`, false);
        }
    } catch (error) {
        showMessage(`Face swap operation failed! Error: ${error.message}.`, false);
    }
}

// Add event listener to log the current image order for both source and target containers
document.getElementById('swapFaces').addEventListener('click', () => {
    swapFaces('source', 'sourceGallery', 'target', 'targetGallery')
});


