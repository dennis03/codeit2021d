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
        ans01['p4'] = int(calEnergy(grid1))
        result.append(ans01)
    return jsonify(result)

def calEnergy(grid):
    grid1 = np.copy(grid)
    grid1[grid1==2] = 0
    m, n = grid1.shape

    healthies = np.argwhere(grid1==1)
    healthies = [tuple(h.tolist()) for h in healthies]
    # print(healthies)

    e1 = 0
    while len(healthies)>0:
        energies = []
        paths = []
        for h in healthies:
            e, p = findEnergy1(h, grid1, m, n)
            energies.append(e)
            paths.append(p)
        e1 += np.amin(energies)
        healthies.pop(np.argmin(energies))
        for pt in paths[np.argmin(energies)]:
            grid1[pt[0],pt[1]] = 3
        # print(grid1)
    # print(e1)
    return e1


def findEnergy1(h, grid1, m, n):
    visited = {}
    queue1 = [h]
    visited[h] = (0,[h])
    while len(queue1)>0:
        h1 = queue1.pop(0)
        i,j = h1[0],h1[1]
        e = visited[h1][0]
        path = visited[h1][1]
        if not i-1<0:
            if grid1[i-1,j] == 3:
                break
            if ((i-1,j) not in visited):
                queue1.append((i-1,j))
                visited[(i-1,j)] = (e+1,path+[(i-1,j)])
        if not i+1>=m:
            if grid1[i+1,j] == 3:
                break
            if ((i+1,j) not in visited):
                queue1.append((i+1,j))
                visited[(i+1,j)] = (e+1,path+[(i+1,j)])
        if not j-1<0:
            if grid1[i,j-1] == 3:
                break
            if ((i,j-1) not in visited):
                queue1.append((i,j-1))
                visited[(i,j-1)] = (e+1,path+[(i,j-1)])
        if not j+1>=n:
            if grid1[i,j+1] == 3:
                break
            if ((i,j+1) not in visited):
                queue1.append((i,j+1))
                visited[(i,j+1)] = (e+1,path+[(i,j+1)])
    # print(visited)
    return e, path



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
                    changes1 += ch1
        grid1 = np.copy(grid1p5)
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

if __name__ == "__main__":
    h = (2,0)
    grid1 = np.array([
      [0, 3, 2],
      [0, 1, 1],
      [1, 0, 0]
    ])
    grid1 = np.array([
        [3, 1, 0, 1, 1],
        [1, 1, 1, 1, 0],
        [1, 1, 1, 1, 0]])
    grid1, time1 = infection(grid1, 'A')
    # calEnergy(grid1)
    # findEnergy1(h, grid1, 3, 3)
    # print(grid1)
    # print(time1)