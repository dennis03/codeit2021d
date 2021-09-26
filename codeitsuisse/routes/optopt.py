import logging
import json

from flask import request, jsonify

from codeitsuisse import app

import numpy as np
import scipy

logger = logging.getLogger(__name__)

@app.route('/optopt', methods=['POST'])
def optopt():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    options = data['options']
    views = data['view']

    # pdf1 = calPDF(views)


    result = [100]
    return jsonify(result)

def calPDF(views):
    means = [v['mean'] for v in views]
    vars = [v['var'] for v in views]
    mins = [v['min'] for v in views]
    maxs = [v['max'] for v in views]
    weights = [v['weight'] for v in views]

    size = 10000
    minA = np.amin(mins)
    maxB = np.amax(maxs)
    X = np.linspace(minA, maxB, size)
    pdf1 = np.zeros(X.shape)
    for k in np.arange(size):
        x = X[k]
        # for i in range(len(views)):
        #     pdf1[k] +=




