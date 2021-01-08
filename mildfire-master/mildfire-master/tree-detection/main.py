import requests
import json
import treemarker

from flask import escape, jsonify

def get_risk(request):

    request_args = request.args
    lat = float(request_args.get('lat'))
    lng = float(request_args.get('lng'))

    arr = treemarker.get_predictions(lat, lng)

    return jsonify(trees=arr)