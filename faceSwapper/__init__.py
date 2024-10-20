
from flask import Flask

from faceSwapper.apis import faceSwapper_bp
from faceSwapper.routes.FaceSwapperRoute import faceSwapper_routes
from faceSwapper.commons.config import CommonConfig

def create_app():

    app = Flask(
        __name__,
        template_folder=CommonConfig.USER_INTERFACE_WEB_TEMPLATES_DIR,
        static_folder=CommonConfig.USER_INTERFACE_WEB_STATIC_DIR
    )
    app.register_blueprint(faceSwapper_bp,  url_prefix='/api/face')
    app.register_blueprint(faceSwapper_routes)

    return app
