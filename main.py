from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from asst import AssistantWrapper, Response
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

api_key = os.getenv("OPENAI_API_KEY")
auth_token = os.getenv("AUTH_TOKEN")

def protect_urls(authorization):
    if not authorization or not authorization.startswith("Bearer "):
        abort(401, description="Unauthorized")

    token = authorization.split(" ")[1]
    if not validate_token(token):
        abort(401, description="Invalid token")

def validate_token(token: str) -> bool:
    # Placeholder for token validation logic
    return token == auth_token  # Replace with actual validation

@app.route('/henny', methods=['POST'])
def call_henny():
    authorization = request.headers.get('Authorization', None)
    protect_urls(authorization)
    request_data = request.get_json()
    data = request_data.get("data")
    henny = AssistantWrapper('HennyOldman', api_key)
    response = henny.ask(data)
    return jsonify(response.content)

@app.route('/DFB', methods=['POST'])
def call_dfb():
    authorization = request.headers.get('Authorization', None)
    protect_urls(authorization)
    request_data = request.get_json()
    data = request_data.get("data")
    dfb = AssistantWrapper('DFB', api_key)
    response = dfb.ask(data)
    return jsonify(response.content)

@app.route('/assistant/<name>', methods=['POST'])
def call_assistant(name):
    authorization = request.headers.get('Authorization', None)
    protect_urls(authorization)
    request_data = request.get_json()
    prompt = request_data.get("data")
    asst = AssistantWrapper(name, api_key)
    response = asst.ask(prompt)
    return jsonify(response.content)


@app.route('/')
def root():
    return "Hello"

if __name__ == '__main__':
    app.run(debug=True)
