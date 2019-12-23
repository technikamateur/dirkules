from flask import Blueprint


class SemanticUI:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        blueprint = Blueprint('semanticui', __name__, template_folder='templates', static_folder='static',
                              static_url_path=app.static_url_path + '/semanticui')
        app.register_blueprint(blueprint)
