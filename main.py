from flask import Blueprint, Flask, jsonify, url_for
from flask_restful import Api, Resource, reqparse,fields, marshal_with
import numpy as np
from scipy import interpolate
from flasgger import Swagger, swag_from
import config




app = Flask(__name__)
api = Api(app)
# swagger config
app.config['SWAGGER'] = {
    'title': 'My API',
    'uiversion': 3,
    "specs_route": "/swagger/"
}
swagger = Swagger(app)
app.config.from_object(config.Config)





vlpandipr={
    "ipr":{"q_liq": [0,10,30], "p_wf": [100,90,80]},
    "vlp": {"q_liq": [0,10,20], "p_wf": [85,95,100]}
}

class Main(Resource):
    @swag_from('openapi.yaml')
    def get(self,vlpandipr_status):

        if vlpandipr_status == 'data':
            return jsonify(vlpandipr)
        if vlpandipr_status == 'result':
            x_ipr = vlpandipr['ipr']['q_liq']
            y_ipr = vlpandipr['ipr']['p_wf']
            x_vlp = vlpandipr['vlp']['q_liq']
            y_vlp = vlpandipr['vlp']['p_wf']
            ipr = interpolate.interp1d(x_ipr, y_ipr, fill_value='extrapolate')
            vlp = interpolate.interp1d(x_vlp, y_vlp, fill_value='extrapolate')
            #max_values = []
            #max_values.append(max(x_ipr))
            #max_values.append(max(x_vlp))
            xnew = np.linspace(0, max(x_ipr+x_vlp), max(x_ipr+x_vlp) * 1000 + 1)

            def myIntersection(fun1, fun2, x0):
                x_coord = []
                for i in x0:
                    if fun1(i) == fun2(i):
                        x_coord.append(i)
                    else:
                        pass
                return x_coord

            a = myIntersection(ipr, vlp, xnew)
            b = list(ipr(a))
            output_file = {"q_liq": a, "p_wf": b}
            return jsonify(output_file)
        else:
            return jsonify(vlpandipr[vlpandipr_status])

    def delete(self,vlpandipr_status):
        del vlpandipr[vlpandipr_status]
        return jsonify(vlpandipr)

    def post(self,vlpandipr_status):
        parser = reqparse.RequestParser()
        parser.add_argument("q_liq", action='append', type=int)
        parser.add_argument("p_wf", action='append', type=int)
        vlpandipr[vlpandipr_status] = parser.parse_args()
        return jsonify(vlpandipr)

    def put(self, vlpandipr_status):
        parser = reqparse.RequestParser()
        parser.add_argument("q_liq", action='append', type=int)
        parser.add_argument("p_wf", action='append', type=int)
        vlpandipr[vlpandipr_status] = parser.parse_args()
        return jsonify(vlpandipr)


api.add_resource(Main, "/api/vlpandipr/<string:vlpandipr_status>")
api.init_app(app)



if __name__ == "__main__":
    app.run(debug=True, port=3000, host="127.0.0.1")