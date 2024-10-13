
document.addEventListener('DOMContentLoaded', function () {

    function waitFor(milliseconds) {
        return new Promise(resolve => setTimeout(resolve, milliseconds));
    }

    async function swapFaces(source, target) {

        try {
            const sourceFile = document.getElementById(source).files[0];
            const targetFile = document.getElementById(target).files[0];
            if (!sourceFile || !targetFile) {
                showMessage(`Please make sure both source and target files are present.`, false);
                return;
            }

            const sourceGalleryOrder = getImageOrder(document.getElementById(`${source}Gallery`));
            const targetGalleryOrder = getImageOrder(document.getElementById(`${target}Gallery`));
            if (sourceGalleryOrder.length === 0 || targetGalleryOrder.length === 0) {
                showMessage(`Please make sure both source and target images have faces in them.`, false);
                return;
            }

            // Create FormData
            const formData = new FormData();
            formData.append('sourceFile', sourceFile);
            formData.append('sourceFileName', sourceFile.name); // source file name (additional)
            formData.append('sourceGalleryOrder', JSON.stringify(sourceGalleryOrder));  // Convert array to JSON string
            formData.append('targetFile', targetFile);
            formData.append('targetFileName', targetFile.name); // target file name (additional)
            formData.append('targetGalleryOrder', JSON.stringify(targetGalleryOrder));  // Convert array to JSON string

            // Perform the fetch request
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
        swapFaces('source', 'target')
    });
});

