# FaceSwapper

FaceSwapper is a Python-based application that allows users to swap faces in images using advanced deep learning models. It leverages libraries such as OpenCV for computer vision, ONNX for model inference, and InsightFace for face recognition and alignment.

## Features
- Real-time face swapping in images.
- Utilizes pre-trained deep learning models for face detection and alignment.
- Supports FastAPI for web-based interaction.
- Flexible and scalable design to handle different face-swapping use cases.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/noahximus/faceSwapper.git
    cd faceSwapper
    ```

2. **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For Linux/macOS
    # For Windows, use `venv\\Scripts\\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the FastAPI server**:
    ```bash
    uvicorn main:app --reload
    ```

2. **Access the application**:
    Open your browser and go to `http://127.0.0.1:8000`.

3. **API Endpoints**:
    - `/upload`: Upload an image and specify the source and target face for swapping.
    - `/swap`: Perform the face swapping on the uploaded image.

## Dependencies
- fastapi
- uvicorn
- pydantic
- python-multipart
- pillow
- numpy
- opencv-python
- insightface
- onnxruntime

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- The ONNX Runtime for model inference.
- InsightFace for face recognition and alignment.
- The Python and FastAPI communities for their open-source contributions.
