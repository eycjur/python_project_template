# ruff: noqa: E402, F401

# Note: lambdaはstageごとにサブディレクトリでデプロイされるため、その対応をしている

import os
from typing import Any

import awsgi

from src.settings import AWS_API_GATEWAY_STAGE_NAME

# dash
os.environ["DASH_URL_BASE_PATHNAME"] = f"/{AWS_API_GATEWAY_STAGE_NAME}/"

from src.presentation.dash.index import app


def handler(event: Any, context: Any) -> dict[str, Any]:
    return awsgi.response(app.server, event, context)


"""
# fastapi
from mangum import Mangum

from src.presentation.fastapi.app import app

handler = Mangum(app, api_gateway_base_path=f"/{AWS_API_GATEWAY_STAGE_NAME}")
"""

"""
# flask

from flask import Flask

from src.presentation.flask.routes import router

app = Flask(__name__, template_folder="presentation/flask/templates")
app.register_blueprint(router, url_prefix=f"/{AWS_API_GATEWAY_STAGE_NAME}")


def handler(event: Any, context: Any) -> dict[str, Any]:
    return awsgi.response(app, event, context)
"""
