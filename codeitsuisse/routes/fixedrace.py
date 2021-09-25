import logging
import json

from flask import request, jsonify

from codeitsuisse import app

from collections import defaultdict
import random

logger = logging.getLogger(__name__)

scores = defaultdict(lambda: 0)

@app.route('/fixedrace', methods=['POST'])
def fixedrace():
    str1 = request.data
    logging.info("data sent for evaluation {}".format(str1))
    if str1[:5] == b'##set':
        _, name, strS = str1.split(b',')
        scores[name] = int(strS)
        return b'done ' + str1
    elif str1[:7] == b'##reset':
        scores.clear()
        return b'done ' + str1
    elif str1[:6] == b'##show':
        ss = {k: v for k, v in sorted(scores.items(), key=lambda item: -item[1])}
        # print(ss)
        return str(ss)
    else:
        names1 = str1.split(b',')
        guess = guessRank(names1)
        return b','.join(guess)


def guessRank(names1):
    scores1 = []
    for name in names1:
        scores1.append(scores[name])
    ss1 = sorted(set(scores1))[::-1]
    guess = []
    for ss1e in ss1:
        g1 = [names1[i] for i in range(len(names1)) if scores1[i]==ss1e]
        random.shuffle(g1)
        guess += g1
    return guess

