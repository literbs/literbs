import time
from algorithms.mgutil import extractPath

"""
    mgp4 = mg4 + pruning
"""

queue = []
visitedTrace = {}
obstacles = {}

def inBucket (cords, visited):
    return cords in visited

def filterOptions(cords):
    if inBucket(cords, visitedTrace):
        return False
    if inBucket(cords, obstacles):
        return False
    return True

def keysVersion (arr, appen=False):
    obj = {} if not appen else []
    for x in arr:
        if appen:
            obj.append(f'{x[0]}:{x[1]}')
        else:
            obj[f'{x[0]}:{x[1]}']=None
    return obj

# def extractPath (end, nodes):
#     currentlyAt = end
#     path = [end]
#     while currentlyAt in nodes and nodes[currentlyAt] != None:
#         path.append(nodes[currentlyAt])
#         currentlyAt = nodes[currentlyAt]

#     return path[::-1]

def heuristic(start, end, barriers, maxIterations = 1000000000, socketInformation=None): #function for something else
    global obstacles
    global queue
    global visitedTrace
    global queue
    
    queue = []
    reserves = []

    obstacles = barriers
    queue.append(start)
    current = start
    visitedTrace = {start:(None, 0)}
    reserves = []

    while queue and current != end and maxIterations >= 0:
        current = queue.pop(len(queue)-1) 
        options = [
          (current[0]-1, current[1]),  # top
          (current[0], current[1]+1),  # right
          (current[0]+1, current[1]),  # bottom
          (current[0], current[1]-1),  # left
        ]

        options = list(filter(filterOptions, options))

        if not len(options) and len(reserves):
            # trying to find a new route
            (parent, nextRes, count) = reserves.pop(0)
            visitedTrace[nextRes] = (parent, count)
            queue.append(nextRes) 
            continue
        if len(queue):
            continue
        elif not len(options): 
            if current == end:
                # We have reached the end but haven't properly acknowledged it
                continue          
            # visitedTrace[nextRes] = parent
            return ([], {})         

        bestFitness = float('inf')
        bestCord = None

        for opt in options:
            fitness = abs(opt[0] - end[0]) + abs(opt[1] - end[1])
            if fitness < bestFitness:
                bestFitness = fitness
                bestCord = opt
        
        visitedTrace[bestCord] = (current, visitedTrace[current][1]+1 )
        queue.append(bestCord)

        for opt in options:
            if opt != bestCord:
                reserves.append((current, opt, visitedTrace[current][1]+1))

        if socketInformation != None and 'io' in socketInformation:
            if 'sleepDuration' in socketInformation:
                time.sleep(socketInformation['sleepDuration'])
            path = extractPath(current, visitedTrace)
            socketInformation['io'].emit('algorithm_response', { 'meta':{'algorithm':'Single instance Lee (Pruned)', 'iterationCount':maxIterations}, 'gridSize':socketInformation.get('gridSize'), 'id':socketInformation.get('id'), 'barriers':socketInformation.get('stringBarriers'), 'path':{ f'{x[0]}:{x[1]}':None for x in path }, 'visited': { f'{x[0]}:{x[1]}':None for x in visitedTrace } })

            
        maxIterations -= 1

    if maxIterations <= 0:
        return ([], [])

    path = extractPath(end, visitedTrace)
    if socketInformation != None and 'io' in socketInformation:
        socketInformation['io'].emit('algorithm_response', { 'meta':{'algorithm':'Single instance Lee (Pruned)', 'iterationCount':maxIterations}, 'gridSize':socketInformation.get('gridSize'), 'id':socketInformation.get('id'), 'barriers':socketInformation.get('stringBarriers'), 'path':{ f'{x[0]}:{x[1]}':None for x in path }, 'visited': { f'{x[0]}:{x[1]}':None for x in visitedTrace } })

    return (path, list(visitedTrace)+reserves)