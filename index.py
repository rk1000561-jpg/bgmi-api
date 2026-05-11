from flask import Flask, request, jsonify
import requests
import json
from urllib.parse import unquote

app = Flask(__name__)


def get_token():
    try:
        s = requests.Session()

        s.get(
            "https://www.rooter.gg/",
            headers={"User-Agent": "Mozilla/5.0"}
        )

        cookie = s.cookies.get("user_auth")

        if not cookie:
            return None, None

        token = json.loads(unquote(cookie)).get("accessToken")

        return token, s

    except:
        return None, None


@app.route("/")
def home():
    uid = request.args.get("uid")

    if not uid:
        return jsonify({
            "status": False,
            "message": "UID required"
        })

    try:
        token, session = get_token()

        if not token:
            raise Exception()

        url = f"https://bazaar.rooter.io/order/getUnipinUsername?gameCode=BGMI_IN&id={uid}"

        response = session.get(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "User-Agent": "Mozilla/5.0"
            }
        )

        data = response.json()

        return jsonify({
            "status": True,
            "developer": "@R3XTRON",
            "username": data["unipinRes"]["username"],
            "uid": uid,
            "server": "BGMI",
            "region": "India"
        })

    except:
        return jsonify({
            "status": False,
            "message": "Request failed"
        })
