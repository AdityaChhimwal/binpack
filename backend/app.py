import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, request, jsonify
from flask_cors import CORS
from compiler import compile_code
import json

app = Flask(__name__)
CORS(app)


@app.route("/compile", methods=["POST"])
def compile_schema():
    try:
        data = request.json
        schema = data.get("schema")

        result = compile_code(schema)

        if "error" in result:
            return jsonify(result), 400

        return jsonify({
            "generated_code": result["code"],
            "ir": result["ir"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/serialize", methods=["POST"])
def serialize_data():
    try:
        data = request.json
        schema = data.get("schema")
        json_data = data.get("data")

        result = compile_code(schema)

        if "error" in result:
            return jsonify(result), 400

        generated_code = result["code"]

        local_env = {}
        exec(generated_code, local_env)

        serialize_list = local_env["serialize_list"]

        data_list = json.loads(json_data)

        binary = serialize_list(data_list)

        json_size = len(json_data.encode("utf-8"))
        binary_size = len(binary)

        return jsonify({
            "binary_hex": binary.hex(),
            "json_size": json_size,
            "binary_size": binary_size
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)