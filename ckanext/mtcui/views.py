from flask import Blueprint


mtcui = Blueprint(
    "mtcui", __name__, url_prefix="/mtcui")


def page():
    return "Hello, mtcui!"


mtcui.add_url_rule(
    "/page", view_func=page, endpoint="page")


def get_blueprint():
    return mtcui
