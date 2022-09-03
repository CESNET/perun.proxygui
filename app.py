import json

from flask import Flask, render_template, request, redirect, make_response, jsonify, session
from flask_babel import Babel, get_locale, gettext
from jwcrypto import jwk, jwt
from jwcrypto.jwk import JWKSet, JWK
import yaml

app = Flask(__name__)
babel = Babel(app)

with open("config_templates/config-template.yaml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)

if 'css_framework' not in cfg:
    cfg['css_framework'] = 'bootstrap'

app.secret_key = cfg["secret_key"]

TOKEN_ALG = cfg['token_alg']
KEY_ID = cfg['key_id']
KEYSTORE = cfg['keystore']
REDIRECT_URL = cfg['redirect_url']


def import_keys(file_path: str) -> JWKSet:
    jwk_set = jwk.JWKSet()
    with open(file_path, "r") as file:
        jwk_set.import_keyset(file.read())
    return jwk_set


def get_signing_jwk(file: str, key: str) -> JWK:
    jwk_set = import_keys(file)
    return jwk_set.get_key(key)


def verify_jwt(token):
    jwk_key = get_signing_jwk(KEYSTORE, KEY_ID)
    return jwt.JWT(jwt=token, key=jwk_key).claims


@app.context_processor
def inject_conf_var():
    return dict(cfg=cfg, lang=get_locale())


@babel.localeselector
def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'en')


@app.route('/')
def index():
    return redirect('/IsTestingSP')


@app.route('/authorization/<message>')
def authorization(message):
    message = json.load(verify_jwt(message))
    email = message.get('email')
    service = message.get('service')
    registration_url = message.get('registration_url')
    if not email or not service:
        return make_response(jsonify({gettext("fail"): gettext("Missing request parameter")}), 400)
    return render_template(
        "authorization.html",
        email=email,
        service=service,
        registration_url=registration_url,
    )


@app.route('/SPAuthorization/<message>')
def sp_authorization(message):
    message = json.load(verify_jwt(message))
    email = message.get('email')
    service = message.get('service')
    registration_url = message.get('registration_url')
    return render_template(
        "SPAuthorization.html",
        email=email,
        service=service,
        registration_url=registration_url,
    )


@app.route('/IsTestingSP')
def is_testing_sp():
    return render_template(
        "IsTestingSP.html",
        redirect_url=REDIRECT_URL
    )


if __name__ == "__main__":
    app.run(debug=True)
