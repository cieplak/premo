from flask import Flask

from premo import resources


app = Flask(__name__)


app.add_url_rule('/resources', 'resource.create', resources.resource.create, methods=['POST'])
app.add_url_rule('/resources/<string:id>', 'resource.read', resources.resource.get, methods=['GET'])
