from flask import Blueprint
from flask_restx import Api
from faceSwapper.apis.SwapperAPI import swapperAPI_routes  # Import the routes from your API file
from faceSwapper.apis.EnhancerAPI import enhancerAPI_routes  # Import the routes from your API file
from faceSwapper.apis.ExtractorAPI import extractorAPI_routes
from faceSwapper.apis.UploaderAPI import uploaderAPI_routes

# Create the blueprint for the face swapping module
faceSwapper_bp = Blueprint('faceSwapper', __name__)

# Create the API object for this blueprint
api = Api(faceSwapper_bp,
          title='Face Swapper API',
          version='1.0',
          description='API for face swapping')

# Add the namespace to the API
api.add_namespace(swapperAPI_routes)
api.add_namespace(enhancerAPI_routes)
api.add_namespace(extractorAPI_routes)
api.add_namespace(uploaderAPI_routes)
