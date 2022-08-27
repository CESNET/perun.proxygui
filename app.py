import json

from flask import Flask, render_template, request, redirect, make_response, jsonify
from flask_babel import Babel, get_locale, gettext
from jwcrypto import jwk, jwt
from jwcrypto.jwk import JWKSet, JWK
import yaml

app = Flask(__name__)
babel = Babel(app)

with open("config_templates/config-template.yaml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)

CSS_FRAMEWORK = cfg.get('css_framework', 'bootstrap')
MUNI_FACULTY = cfg.get('MUNI_faculty', None)


TOKEN_ALG = cfg['token_alg']
KEY_ID = cfg['key_id']
KEYSTORE = cfg['keystore']
FOOTER = cfg.get('footer', None)
LANGUAGES = cfg.get('languages', None)
LOGO = cfg.get('logo', None)
NAME = cfg.get('name', None)


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


@babel.localeselector
def select_locale():
    return request.accept_languages.best_match(["en", "cs"])


@app.route('/')
def index():
    return redirect('/IsTestingSP?language=en')


@app.route('/authorization/<message>')
def authorization(message):
    message = json.load(verify_jwt(message))
    email = message.get('email')
    service = message.get('service')
    if not email or not service:
        return make_response(jsonify({"fail": "Missing request parameter"}), 400)
    return render_template(
        "authorization.html",
        email=email,
        service=service,
        css_framework=CSS_FRAMEWORK,
        faculty=MUNI_FACULTY,
        locale=get_locale()
    )


@app.route('/SPAuthorization/<message>')
def sp_authorization(message):
    message = json.load(verify_jwt(message))
    registration_url = message.get('registration_url')
    return render_template(
        "SPAuthorization.html",
        registration_url=registration_url,
        css_framework=CSS_FRAMEWORK,
        faculty=MUNI_FACULTY,
        locale=get_locale()
    )


@app.route('/IsTestingSP')
def is_testing_sp():
    language = request.args.get('language', get_locale())
    return render_template(
        "IsTestingSP.html",
        css_framework=CSS_FRAMEWORK,
        faculty=MUNI_FACULTY,
        locale=language,
        footer=FOOTER,
        sections=FOOTER['sections'],
        format=FOOTER['format'],
        current_section=FOOTER['sections'][str(language)],
        languages=LANGUAGES,
        current_language=LANGUAGES[str(language)],
        logo=LOGO,
        name=NAME,
        queryParams=dict()
    )


if __name__ == "__main__":
    app.run(debug=True)
