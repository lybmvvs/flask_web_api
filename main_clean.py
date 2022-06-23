import json
from scipy.interpolate import interp1d
from scipy import optimize
from flask import Flask, abort
from flasgger import Swagger, SwaggerView, Schema, fields
from marshmallow.validate import OneOf


app = Flask(__name__)
swagger = Swagger(app)
app.config["SWAGGER"] = {
    "title": "VLP_IPR_api",
    "uiversion": 2,
}

class Dynamic(Schema):

    q_liq: fields.List(fields.Float, required=True)
    p_wf: fields.List(fields.Float, required=True)

    def swag_validation_function(self, data, main_def):
        self.load(data)

    def swag_validatoin_error_handler(self, err, data, main_def):
        abort(400, err)

class InputData(Schema):

    vlp: fields.Nested(Dynamic, required=True)
    ipr: fields.Nested(Dynamic, required=True)

    def swag_validation_function(self, data, main_def):
        self.load(data)

    def swag_validatoin_error_handler(self, err, data, main_def):
        abort(400, err)


class ApiView(SwaggerView):

    parameters = InputData
    responses = {
        200: {
            "description": "ВСЕ ЗБС",
            "schema": InputData,
        }
    }

    tags = ["intersection"]

    def get(body: InputData, request_type: str):

        if request_type == "data":
            return body

        else:
            vlp = interp1d(
                x=body.vlp.q_liq,
                y=body.vlp.q_liq
            )
            ipr = interp1d(
                x=body.ipr.q_liq,
                y=body.ipr.q_liq
            )

            # try:
            #     solution = optimize.brent(
            #         func=...,
            #         a=...,
            #         b=...,
            #     )
            # except ValueError:
            #     solution = optimize.minimize_scalar(
            #         fun=...,
            #         method="bounded",
            #         bounds=(
            #             ...,
            #             ...,
            #         )
            #     )
            return {"q_liq": 0, "p_wf": 1}


app.add_url_rule(
    "/api/vlpandipr/<string:request_type>",
    view_func=ApiView.as_view("api"),
    methods=["GET"],
)

if __name__ == "__main__":
    app.run(
        debug=True,
        port=3000,
    )
