import json

from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class Authorize(Resource):
    def get(self, license_key, user_ip):
        with open("keys.json") as keys_file:
            licenses_json = json.load(keys_file)

            for licence in licenses_json["licenses"]:
                if licence["key"] == license_key:  # User inputted valid key

                    if licence["ip"] == "":  # Case when key wasn't bound (fresh license)
                        result = {"status": 1, "message": "Fresh license"}

                    elif licence["ip"] == user_ip:  # Case when user access license from bound ip address
                        result = {"status": 1, "message": "Repeated login"}

                    else:  # Case when license owner tries to use license
                        result = {"status": 0, "message": "License is activated on other device"}

            try:
                if result == {"status": 1, "message": "Fresh key"}:
                    licence["ip"] = user_ip

                    updated_json = open("keys.json", "w")
                    json.dump(licenses_json, updated_json)

                return result

            except UnboundLocalError:
                result = {"status": 0, "message": "Invalid license"}

                return result


class Keys(Resource):
    def get(self):
        with open("keys.json") as keys_file:
            licenses_json = json.load(keys_file)

        return licenses_json


api.add_resource(Authorize, "/authorize/<string:license_key>/<string:user_ip>")
api.add_resource(Keys, "/keys/get")

if __name__ == "__main__":
    app.run(debug=True)