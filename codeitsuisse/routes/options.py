import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/options', methods=['POST'])
def options():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    options = data['options']
    views = data['view']
    
    return json.dumps(1)



