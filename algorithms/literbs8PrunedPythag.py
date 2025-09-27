import math
from algorithms.mgutil import extractPath, sendData

queue = ([], [])
obstacles = {}
traces = ({}, {})
reserves = ([], [])

def inBucket (cords, visited):
    return cords in visited

def filterOptions(cords, visited, obstacles):
    if inBucket(cords, visited):
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

def prunePoint (nodes, path, currentlyAt, obstacles):
    currentPrune = currentlyAt['value']
    child = nodes[currentPrune]
    allOptions = [
        child,
        (currentPrune[0]+1, currentPrune[1]),
        (currentPrune[0]-1, currentPrune[1]),
        (currentPrune[0], currentPrune[1]+1),
        (currentPrune[0], currentPrune[1]-1),
        (currentPrune[0]+1, currentPrune[1]+1),
        (currentPrune[0]-1, currentPrune[1]-1),
        (currentPrune[0]+1, currentPrune[1]-1),
        (currentPrune[0]-1, currentPrune[1]+1),
    ]

    appropiateOptions = []

    for option in allOptions:
        if option not in nodes:
            continue
        if option in path:
            continue

        appropiateOptions.append(option)

    if not len(appropiateOptions):
        path.append(nodes[currentPrune][0])
        currentlyAt['value'] = nodes[currentPrune][0]
    else:
        bestOption = None
        bestFitness = float('inf')
        for opt in appropiateOptions:
            if (nodes[opt][1]) < bestFitness:
                bestOption = opt
                bestFitness = nodes[opt][1]

        path.append(bestOption)
        currentlyAt['value'] = bestOption

def getExtraOptions(current, visited, barriers):
    row, col = current
    neighbors = []
    for r, c in ((row-1, col), (row, col-1), (row+1, col), (row, col+1), (row-1, col-1), (row-1, col+1), (row+1, col-1), (row+1, col+1)):
        if not filterOptions((r, c), visited, barriers):
            continue
        neighbors.append((r, c))
    return neighbors

# def runSingleIteration (currentInfo, queue, reserves, visitedTrace, visited, vistedNext, end, obstacles):
def runSingleIteration (currentInfo, queue, reserves, visitedTrace, vistedNext, end, obstacles):
    currentInfo['value'] = queue.pop(0) 
    current = currentInfo['value']
    options = getExtraOptions(current, visitedTrace, obstacles)

    if not len(options) and len(reserves):
        # this is when we know we have rerouted since we are no longer taking the best option
        (parent, nextRes, count) = reserves.pop(0)
        # visited.append(nextRes)
        visitedTrace[nextRes] = (parent, count)
        queue.append(nextRes)
        if nextRes in vistedNext:
            return nextRes
        return 1

    if not len(options) and len(queue):
        return 2          
    elif not len(options):
        # print('No path possible!')
        return -1   

    bestFitness = float('inf')
    bestCord = None

    for opt in options:
        fitness = distanceApart(opt, end)
        if fitness < bestFitness:
            bestFitness = fitness
            bestCord = opt

    # visited.append(bestCord)
    visitedTrace[bestCord] = (current, visitedTrace[current][1]+1 )
    if bestCord in vistedNext:
        return bestCord
    queue.append(bestCord)

    for opt in options:
        if opt != bestCord:
            reserves.append((current, opt, visitedTrace[current][1]+1))    

    return True
def distanceApart (cordA, cordB):
    return math.sqrt ( math.pow(cordA[0] - cordB[0], 2) + math.pow(cordA[1] - cordB[1], 2) ) 

def convertTracesIntoSingleObj (traces):
    return { f'{x[0]}:{x[1]}':None for x in list(traces[0]) + list(traces[1]) }

def heuristic(start, end, barriers, maxIterations=1000000000, socketInformation=None):
    global obstacles
    obstacles = barriers
    queue = ([start], [end])
    traces = ({start:(None, 0)}, {end:(None, 0)})
    reserves = ([], [])
    currents = [{'value':start}, {'value':end}]
    index = 0
    mergePoint = None
    restarts = 0
    inRange = False # Variable not used during original testing, only to check the MERGEINTRAIL vs MERGEDIRECT count
    while maxIterations >= 0 and len(queue[0]) and len(queue[1]) and distanceApart(currents[0]['value'], currents[1]['value']) > 1:
        try:
            nextIndex = (index+1) % 2
            status = runSingleIteration (currents[index], queue[index], reserves[index], traces[index], traces[nextIndex], currents[nextIndex]['value'], obstacles)
            if status == 1:
                restarts+=1
            if status == -1:
                return ([], [], "")
            if type(status) == tuple:
                
                if distanceApart(currents[0]['value'], currents[1]['value']) <= 2:
                    inRange = True
                    
                mergePoint = status
                break
            
            sendData(socketInformation, currents, traces, reserves, False)

            index = nextIndex
            maxIterations -= 1
        except:
            return ([], [], "")

    if maxIterations <= 0:
        return ([], [], "PASSED-MAX-ITERATIONS")

    if mergePoint != None:
        p1 = extractPath(mergePoint, traces[0])
        p2 = extractPath(mergePoint, traces[1], False)
        path = p1 + p2[1:] 

        sendData(socketInformation, currents, traces, reserves, False, mergePoint)

        return (path, list(traces[0])+list(traces[1])+reserves[0]+reserves[1], f"{'MERGEINTRAIL' if not inRange else 'MERGEDIRECT'} R:{restarts}")

    path = extractPath(currents[0]['value'], traces[0]) + extractPath(currents[1]['value'], traces[1], False)

    sendData(socketInformation, currents, traces, reserves, False)

    return (path, list(traces[0])+list(traces[1])+reserves[0]+reserves[1], f"MERGEDIRECT R:{restarts}")
    
