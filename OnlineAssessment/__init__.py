from flask import Flask

app = Flask(__name__)


# use blueprint to route
from OnlineAssessment.core.views import core
from OnlineAssessment.error_pages.handlers import error_pages

# Register blueprint
app.register_blueprint(core)
app.register_blueprint(error_pages)