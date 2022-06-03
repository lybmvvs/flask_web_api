from flask import Flask, render_template, jsonify
from apispec import APISpec
from apispec_webframeworks.flask import FlaskPlugin
from apispec.ext.marshmallow import MarshmallowPlugin
from marshmallow import Schema, fields

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world!'

spec = APISpec(
    title='flask-api-swagger-doc',
    version = '1.0.0',
    openapi_version='3.0.2',
    plugins=[FlaskPlugin(), MarshmallowPlugin()]
)

@app.route('/api/swagger.json')
def create_swagger_spec():
    return jsonify(spec.to_dict())


if __name__ == "__main__":
    app.run(debug=True)