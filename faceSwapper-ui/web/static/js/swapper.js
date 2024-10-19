import * as commons from "./commons.js";
import * as gallery from "./gallery.js";

document.addEventListener('DOMContentLoaded', function () {
    async function swapFaces(source, target) {

        commons.showLoadingSpinner();  // Show loading before starting the process

        try {
            const sourceFile = document.getElementById(source).files[0];
            const targetFile = document.getElementById(target).files[0];
            if (!sourceFile || !targetFile) {
                commons.showMessage(`Please make sure both source and target files are present.`, false);
                return;
            }

            const sourceGalleryOrder = gallery.getImageOrder(document.getElementById(`${source}Gallery`));
            const targetGalleryOrder = gallery.getImageOrder(document.getElementById(`${target}Gallery`));
            if (sourceGalleryOrder.length === 0 || targetGalleryOrder.length === 0) {
                commons.showMessage(`Please make sure both source and target images have faces in them.`, false);
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
            const response = await fetch(apiUrlForSwap, {
                method: 'POST',
                body: formData
            });

            // Check if the response is okay before attempting to parse JSON
            if (!response.ok) {
                commons.hideLoadingSpinner();  // Hide loading after the process is done
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            if (response.status === 200) {
                // Reference to the preview container
                const swappedResult = document.getElementById('swappedResult');
                commons.showBase64Previews(result.image, swappedResult)
                commons.showMessage(`Face swap operation successful!`, true);
            } else {
                commons.showMessage(`Face swap operation failed! ${result.error}.`, false);
            }
            commons.hideLoadingSpinner();  // Hide loading after the process is done
        } catch (error) {
            commons.showMessage(`Face swap operation failed! Error: ${error.message}.`, false);
        }
        commons.hideLoadingSpinner();  // Hide loading after the process is done
    }

    // Add event listener to log the current image order for both source and target containers
    document.getElementById('swapFaces').addEventListener('click', () => {
        swapFaces('source', 'target')
    });
});

