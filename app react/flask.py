from flask import Flask, request,jsonify
from flask_cors import CORS
from flask_restplus import Api, Resource, fields
import jsons
from flask_restful import reqparse
from .checker import Evaluate

app = Flask(__name__)
evaluator = Evaluate()
CORS(app)

@app.route('/check', methods=['POST'])
def login():
    #print(dir(request))
    print(request.get_json())
    #print(request.form['input'])
    j = evaluator.check(request.get_json()['data'])
    return(j)

'''@app.route('/check', methods=['OPTIONS'])
def preflight():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response'''

if __name__ == '__main__':
    app.run()






'''
app = Flask(__name__)
api = Api(app)
"""
models = api.model('Grammatik',
    {'data': fields.String(required = True,
                               description="Input")})
"""
@api.route("/")
class MainClass(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    def options(self):
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response

    #@api.expect(models)
    def post(self):
        try:
            response = jsonify({"statusCode": 200, "result": json_string})
            #print(JSON.stringify(response))
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        except Exception as error:
            return jsonify({
                "statusCode": 500})
'''