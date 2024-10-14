
from flask import Flask

from faceSwapper.apis.UploadsAPI import uploadsAPI_routes
from faceSwapper.apis.SwapperAPI import swapperAPI_routes
from faceSwapper.apis.EnhancerAPI import enhancerAPI_routes
from faceSwapper.routes.FaceSwapper import faceSwapper_routes
from faceSwapper.commons.config import CommonConfig

def create_app():

    app = Flask(
        __name__,
        template_folder=CommonConfig.USER_INTERFACE_WEB_TEMPLATES_DIR,
        static_folder=CommonConfig.USER_INTERFACE_WEB_STATIC_DIR
    )
    app.register_blueprint(swapperAPI_routes)
    app.register_blueprint(uploadsAPI_routes)
    app.register_blueprint(faceSwapper_routes)
    app.register_blueprint(enhancerAPI_routes)

    return app
