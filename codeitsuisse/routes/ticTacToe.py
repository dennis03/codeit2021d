import logging
import json

from flask import request, jsonify

from codeitsuisse import app

import pprint
import requests
import sseclient

logger = logging.getLogger(__name__)

@app.route('/tic-tac-toe', methods=['POST'])
def TTT():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    battleId = data.get("battleId")
    url = 'https://cis2021-arena.herokuapp.com/tic-tac-toe/start'
    logging.info('starting')
    streamResponse = requests.get(url, params=battleId, stream=True)
    logging.info('started')
    logging.info('started',streamResponse)
    avaActions = ['NW','N','NE','W','C','E','SW','S','SE']

    client = sseclient.SSEClient(streamResponse)
    # for event in client.events():
    #     # print("got a new event from server")
    #     logging.info("evenyt data :{}".format(event.data))
    #     pprint.pprint(event.data)



    result = 0
    logging.info("My result :{}".format(result))
    return json.dumps(result)



