
# faceSwapper

faceSwapper is a Python-based web application for swapping faces in images. The project allows users to upload images, select faces, and swap faces between images. Users can also duplicate and delete faces directly from the gallery.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Gallery Management](#gallery-management)
- [Face Processing](#face-processing)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Face Swapping**: Upload images, detect faces, and swap faces between the images.
- **Image Enhancement**: Enhance face images before processing.
- **Duplicate Faces**: Duplicate selected faces in the gallery for reuse.
- **Delete Faces**: Remove unwanted faces from the gallery.
- **Responsive UI**: User-friendly interface with responsive design.
- **Loading Indicator**: Visual feedback during image processing.

## Installation

To install and run the project locally, follow these steps:

### Prerequisites

- Python 3.x
- Flask
- OpenCV (cv2)
- NumPy

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/noahximus/faceSwapper.git
    cd faceSwapper
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:

    ```bash
    python run.py
    ```

4. Open a web browser and go to `http://127.0.0.1:5000`.

## Usage

1. **Choose Images**: Click on choose files to add images to the gallery.
2. **Pair Faces**: After selecting source and target images, pair each face from source image to target image.
3. **Duplicate Faces**: Use the **Duplicate +** button to make copies of selected faces for reuse.
4. **Delete Faces**: Remove unwanted faces from the gallery by clicking the **Delete -** button.
5. **Swap Faces**: Use the **Swap** button to swap faces between the source and target images.
6. **Enhance Images**: Enhance the faces after swapping using the available controls.

### Gallery Management

- **Duplicate Faces**: Each face in the gallery has a **Duplicate +** button next to it. Clicking this button duplicates the face and adds it to the gallery for reuse in future swaps.
- **Delete Faces**: A **Delete -** button is provided next to each face in the gallery, allowing users to remove faces they no longer need.

### Example of Buttons Layout:
- **Duplicate**: Creates a copy of the selected face.
- **Delete**: Removes the selected face.

Buttons are displayed in a column layout for easy interaction. The gap between the buttons is minimized for a cleaner UI.

## Face Processing

### Image Enhancement

After swapping faces, users can enhance the quality of face images. The system allows for real-time processing, and users can see a loading spinner while the images are being processed.

### Face Swapping

Once images are selected and faces are detected, users can select source and target faces to swap. The system uses OpenCV for image manipulation, ensuring high-quality face swaps.

## API Endpoints

The app provides the following API endpoints:

- **/faceSwap**: Processes face swapping between selected images.
- **/enhance**: Processes face enhancement.

Example usage:

```bash
POST /faceSwap
Content-Type: application/json

{
    "source_image": "source_image_url",
    "target_image": "target_image_url"
}
```

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
