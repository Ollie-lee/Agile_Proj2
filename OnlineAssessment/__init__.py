from flask import Flask

app = Flask(__name__)


from OnlineAssessment.core.views import core

# Register the apps
app.register_blueprint(core)