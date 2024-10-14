import * as commons from "./commons.js";

document.addEventListener('DOMContentLoaded', function () {


    async function enhance(ids) {

        commons.showLoadingSpinner();  // Show loading before starting the process

        try {
            var images = []; // Array to hold the src values

            // Iterate over each ID in the array
            ids.forEach(function(id) {
              // Get the img element inside the div with the given ID
              var imgElement = document.querySelector(`#${id} img`);
              
              // Check if the imgElement exists and has a src attribute
              if (imgElement && imgElement.getAttribute('src')) {
                // Add the src to the formDoc array
                images.push(imgElement.getAttribute('src'));
              }
            });

            // Create FormData
            const formData = new FormData();
            formData.append('images', JSON.stringify(images));

            // Perform the fetch request
            const response = await fetch(apiUrlForEnhance, {
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
                const enhancedResult = document.getElementById('enhancedResult');
                commons.showBase64Previews(result.image, enhancedResult)
                commons.showMessage(`Enhancement operation successful!`, true);
            } else {
                commons.showMessage(`Enhancement operation failed! ${result.error}.`, false);
            }
        } catch (error) {
            commons.showMessage(`Enhancement operation failed! Error: ${error.message}.`, false);
        }
        commons.hideLoadingSpinner();  // Hide loading after the process is done
    }

    // Add event listener to log the current image order for both source and target containers
    document.getElementById('enhance').addEventListener('click', () => {
        enhance(['swappedResult', 'targetPreview', 'sourcePreview'])
    });
});

