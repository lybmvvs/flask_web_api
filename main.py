from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api()

class Main(Resource):
    def get(self):
        return {"pwf": 100, "q_liq": 50}

api.add_resource(Main, "/api/intersection")
api.init_app(app)


if __name__ == "__main__":
    app.run(debug=True, port=3000, host="127.0.0.1")