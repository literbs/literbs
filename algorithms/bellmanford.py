# bellman ford optimisation -> spfa
import time
from collections import deque

def getPath (gridMap, start, end):

    path = []
    current = end
    while current != start and current != None:
        path.append(current)
        current = gridMap[current][0]
    
    path.append(start)
    return path
    

def isBlocker (node, obstacles, gridSize):
    if node[0] < 0 or node[0] > gridSize or node[1] < 0 or node[1] > gridSize:
        return True
    return node in obstacles

def convertTreeToUniqueList (tree):
    obj = {}
    for node in tree:
        obj[f"{node[0]}:{node[1]}"] = None
    return obj

def sendData (socketInformation, gridMap, start, end):

    if socketInformation == None:
        return

    if 'io' not in socketInformation:
        return

    path = getPath(gridMap, start, end)
    path = convertTreeToUniqueList(path)

    parentStringEdition = convertTreeToUniqueList(gridMap)

    if 'sleepDuration' in socketInformation:
        time.sleep(socketInformation['sleepDuration'])

    socketInformation['io'].emit('algorithm_response', { 'from':'c', 'meta':{'algorithm':'SPFA',  'visitSize':len(gridMap) }, 'gridSize':socketInformation.get('gridSize'), 'id':socketInformation.get('id'), 'path':path, 'barriers':socketInformation.get('stringBarriers'), 'visited':parentStringEdition })

def getNeighbours (node, obstacles, gridSize):
    originals = (
        (node[0]+1, node[1]),
        (node[0]-1, node[1]),
        (node[0], node[1]+1),
        (node[0], node[1]-1),
        
        (node[0]-1, node[1]-1),
        (node[0]-1, node[1]+1),
        (node[0]+1, node[1]-1),
        (node[0]+1, node[1]+1),
    )

    filteredItems = []
    for opt in originals:
        if not isBlocker(opt, obstacles, gridSize):
            filteredItems.append(opt)

    return filteredItems

def updateGridWithLatest (gridMap, parentNode, neighbours, remainingNodes):
    _, bestGrandParentScore = gridMap[parentNode]
    if bestGrandParentScore == None:
        return
    for neighbour in neighbours:
        _, previousBestScore = gridMap[neighbour]
        newScore = bestGrandParentScore + 1
        if previousBestScore == None or newScore < previousBestScore:
            gridMap[neighbour] = (parentNode, newScore)
        if previousBestScore == None:
            remainingNodes['remaining'] -= 1
        pass

def updateGridWithLatestSPFA (gridMap, parentNode, neighbours, priorityQueue):
    _, bestGrandParentScore = gridMap[parentNode]
    if bestGrandParentScore == None:
        return
    for neighbour in neighbours:
        _, previousBestScore = gridMap[neighbour]
        newScore = bestGrandParentScore + 1
        if previousBestScore == None or newScore < previousBestScore:
            gridMap[neighbour] = (parentNode, newScore)
            priorityQueue.append(neighbour)

        pass    

def bellmanFord(start, end, obstacles, gridSize, socketInformation=None):
    
    gridMap = {}
    # initialise the grid
    for x in range(gridSize+1):
        for y in range(gridSize+1):
            node = (x, y)
            if isBlocker(node, obstacles, gridSize):
                continue
            bestParent = None
            bestDistance = None
            gridMap[node] = (bestParent, bestDistance)

    gridMap[start] = (None, 0)
    remainingNodes = { 'remaining': len(gridMap)-1 }

    numberOfRuns = (gridSize * gridSize) -1

    # ensuring we do not exceed the max number of runs also means
    # we deal with the case when there is a block and we do not exceed the number of runs
    while remainingNodes['remaining'] > 0 and numberOfRuns > 0:
        for node in gridMap:
            neighbours = getNeighbours(node, obstacles, gridSize)
            updateGridWithLatest (gridMap, node, neighbours, remainingNodes)
        sendData (socketInformation, gridMap, start, end)
        numberOfRuns -= 1

    return getPath(gridMap, start, end), gridMap

def spfa(start, end, obstacles, gridSize, socketInformation=None):
    
    gridMap = {}
    # initialise the grid, excluding the obstacles
    for x in range(gridSize+1):
        for y in range(gridSize+1):
            node = (x, y)
            if isBlocker(node, obstacles, gridSize):
                continue
            bestParent = None
            bestDistance = None
            gridMap[node] = (bestParent, bestDistance)

    gridMap[start] = (None, 0)

    priorityQueue = deque()
    priorityQueue.append(start)
    # ensuring we do not exceed the max number of runs also means
    # we deal with the case when there is a block and we do not exceed the number of runs
    while len(priorityQueue) > 0:
        nextNode = priorityQueue.popleft()
        neighbours = getNeighbours(nextNode, obstacles, gridSize)
        updateGridWithLatestSPFA (gridMap, nextNode, neighbours, priorityQueue)

    sendData (socketInformation, gridMap, start, end)

    return getPath(gridMap, start, end), gridMap