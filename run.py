# -*- coding: utf-8 -*-
from __future__ import annotations

import logging

from faceSwapper import create_app

app = create_app()

if __name__ == '__main__':
    #Setup the logger
    # file_handler = logging.FileHandler('output.log')
    # handler = logging.StreamHandler()

    # Remove any existing handlers attached by Flask
    for handler in app.logger.handlers:
        app.logger.removeHandler(handler) 

    FORMAT = "['%(asctime)s - %(levelname)7s - %(filename)21s:%(lineno)3s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)

    # Disable propagation to prevent double logging
    # app.logger.propagate = False

    # file_handler.setLevel(logging.DEBUG)
    # handler.setLevel(logging.DEBUG)
    # file_handler.setFormatter(logging.Formatter(
    #     '%(asctime)s %(levelname)s: %(message)s '
    #     '[in %(pathname)s:%(lineno)d]'
    # ))
    # handler.setFormatter(logging.Formatter(
    #    '%(asctime)s %(levelname)s: %(message)s '
    #    '[in %(pathname)s:%(lineno)d]'
    # ))
    # app.logger.addHandler(handler)
    # app.logger.addHandler(file_handler)
    # app.logger.error('first test message...')

    app.run(debug=True, use_reloader=False)
    # app.run(debug=False)
