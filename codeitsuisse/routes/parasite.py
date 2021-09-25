import logging
import json

from flask import request, jsonify

from codeitsuisse import app

import numpy as np

logger = logging.getLogger(__name__)

@app.route('/parasite', methods=['POST'])
def parasite():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = []
    for case01 in data:
        room = case01['room']
        grid = case01['grid']
        interestedIndividuals = case01['interestedIndividuals']

        grid1, time1 = infection(grid, 'A')
        grid2, time2 = infection(grid, 'B')

        ans01 = {'room':room, 'p1':{}}
        for ind in interestedIndividuals:
            i,j = map(int, ind.split(','))
            ans01['p1'][ind] = int(time1[i,j])
        if np.sum(grid1==1)==0:
            ans01['p2'] = int(np.amax(time1))
        else:
            ans01['p2'] = -1
        if np.sum(grid2==1)==0:
            ans01['p3'] = int(np.amax(time2))
        else:
            ans01['p3'] = -1

        result.append(ans01)

    return jsonify(result)

def infection(grid, typeP):
    grid1 = np.array(grid, dtype=int)
    grid1p5 = np.array(grid, dtype=int)
    time1 = -1*np.ones(grid1.shape, dtype=int)
    m, n = grid1.shape

    t = 0
    time1[grid1==3]=t

    while True:
        changes1 = 0
        t += 1
        for i in range(m):
            for j in range(n):
                if grid1[i,j] == 3:
                    if typeP=='A':
                        ch1 = infectNeighbour1(grid1p5, time1, i, j, m, n, t)
                    elif typeP=='B':
                        ch1 = infectNeighbour2(grid1p5, time1, i, j, m, n, t)
                    else:
                        ch1 = infectNeighbour1(grid1p5, time1, i, j, m, n, t)
                    changes1 += ch1
        grid1 = grid1p5
        if changes1 == 0:
            break
    return grid1, time1

def infectNeighbour1(grid1p5, time1, i, j, m, n, t):
    changes = 0
    if not i-1<0:
        if grid1p5[i-1,j]==1:
            grid1p5[i-1,j] = 3
            time1[i-1,j] = t
            changes += 1
    if not i+1>=m:
        if grid1p5[i+1,j]==1:
            grid1p5[i+1,j] = 3
            time1[i+1,j] = t
            changes += 1
    if not j-1<0:
        if grid1p5[i,j-1]==1:
            grid1p5[i,j-1] = 3
            time1[i,j-1] = t
            changes += 1
    if not j+1>=n:
        if grid1p5[i,j+1]==1:
            grid1p5[i,j+1] = 3
            time1[i,j+1] = t
            changes += 1
    return changes

def infectNeighbour2(grid1p5, time1, i, j, m, n, t):
    changes = 0
    if not i-1<0:
        if grid1p5[i-1,j]==1:
            grid1p5[i-1,j] = 3
            time1[i-1,j] = t
            changes += 1
    if not i+1>=m:
        if grid1p5[i+1,j]==1:
            grid1p5[i+1,j] = 3
            time1[i+1,j] = t
            changes += 1
    if not j-1<0:
        if grid1p5[i,j-1]==1:
            grid1p5[i,j-1] = 3
            time1[i,j-1] = t
            changes += 1
    if not j+1>=n:
        if grid1p5[i,j+1]==1:
            grid1p5[i,j+1] = 3
            time1[i,j+1] = t
            changes += 1

    if not (i-1<0 or j-1<0):
        if grid1p5[i-1,j-1]==1:
            grid1p5[i-1,j-1] = 3
            time1[i-1,j-1] = t
            changes += 1
    if not (i-1<0 or j+1>=n):
        if grid1p5[i-1,j+1]==1:
            grid1p5[i-1,j+1] = 3
            time1[i-1,j+1] = t
            changes += 1
    if not (i+1>=m or j-1<0):
        if grid1p5[i+1,j-1]==1:
            grid1p5[i+1,j-1] = 3
            time1[i+1,j-1] = t
            changes += 1
    if not (i+1>=m or j+1>=n):
        if grid1p5[i+1,j+1]==1:
            grid1p5[i+1,j+1] = 3
            time1[i+1,j+1] = t
            changes += 1
    return changes
