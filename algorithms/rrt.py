import random
import math
import matplotlib.pyplot as plt
import time
import sys

def getRandomPoint(limit):
    return random.uniform(0, limit)

def getRandomPosition(x_limit, y_limit):
    x = getRandomPoint(x_limit)
    y = getRandomPoint(y_limit)
    return (x, y)

def findPath (parents, start, end):
    path = []
    current = end
    while current != start:
        path.append(current)
        if current not in parents:
            return path
        current = parents[current]
    path.append(start)
    return path[::-1]

def convertTreeToUniqueList (tree):
    obj = {}
    for node in tree:
        obj[f"{node[0]}:{node[1]}"] = None
    return obj

def nodeIsValid (parents, node, obstacles, xLimit, yLimit):
    if node in obstacles:
        return False
    if node[0] > xLimit or node[1] > yLimit:
        return False
    if node in parents:
        return False
    return True

def sendData (socketInformation, parents, startNode, goalNode):

    if socketInformation == None:
        return

    if 'io' not in socketInformation:
        return

    path = findPath(parents, startNode, goalNode) if goalNode else []
    path = convertTreeToUniqueList(path)

    parentStringEdition = convertTreeToUniqueList(parents)

    if 'sleepDuration' in socketInformation:
        time.sleep(socketInformation['sleepDuration'])

    socketInformation['io'].emit('algorithm_response', { 'meta':{'algorithm':'RRT',  'visitSize':len(parents) }, 'gridSize':socketInformation.get('gridSize'), 'id':socketInformation.get('id'), 'path':path, 'barriers':socketInformation.get('stringBarriers'), 'visited':parentStringEdition })


def distanceApart (cordA, cordB):
    return abs(cordA[0]-cordB[0]) + abs(cordA[1]-cordB[1])

def findNearestParent (parents, startNode, node):
    maxDistance = distanceApart(startNode, node)
    closestNode = startNode

    for parent in parents:
        distance = distanceApart(parent, node)
        if distance < maxDistance:
            closestNode = parent
            maxDistance = distance

    return closestNode

def projectNextPoint (parent, randomisedChild, stepSize):
    horizontal = randomisedChild[0] - parent[0]
    vertical = randomisedChild[1] - parent[1]

    theta = 0 if vertical == 0 else math.atan(horizontal/vertical)
    correspondingH = round(parent[0] + math.cos(theta) * stepSize)
    correspondingV = round(parent[1] + math.sin(theta) * stepSize)
    return (correspondingH, correspondingV)

# ignoring this function as we will make step size 1 for tests, otherwise tests
# will take longer than necessary to run - as rrt may not converge within maxIterations
# which would cause tests to restart - prolonging tests longer than needed. But if you are okay with this
# then feel free to add it back in, also need to uncomment lines 111 and 112 (assuming no changes to the file)
# def obstacleInWay (parent, child, maxStepSize, parentBlock, obstacles, gridSize):
#     i = 1
#     nextChild = parent
#     # move 1 node at a time, in the path direction, ensuring the next node is not an obstacle
#     while i <= maxStepSize and nextChild != child:
#         nextChild = projectNextPoint (parent, child, i)
#         if not nodeIsValid(parentBlock, nextChild, obstacles, gridSize, gridSize):
#             return True
#         i+=1
#     return False

def rrt (parentBlock, start, end, obstacles, gridSize, maxIterations=1000000000, socketInformation=None, stepSize=1):

    while maxIterations >= 0:
        maxIterations-=1
        newRandomPosition = getRandomPosition(gridSize, gridSize)

        parentNode = findNearestParent(parentBlock, start, newRandomPosition)
        shortenedRandomPosition = projectNextPoint(parentNode, newRandomPosition, stepSize)

        if not nodeIsValid(parentBlock, shortenedRandomPosition, obstacles, gridSize, gridSize):
            continue

        # if obstacleInWay (parentNode, shortenedRandomPosition, stepSize, parentBlock, obstacles, gridSize):
        #     continue

        parentBlock[shortenedRandomPosition] = parentNode
        sendData(socketInformation, parentBlock, start, shortenedRandomPosition)
        if shortenedRandomPosition == end:
            break

    return {}, end


def rrtRunner (start, end, obstacles, gridSize, maxIterations, socketInformation=None, stepSize=1):
    parentBlock = {}
    rrt(parentBlock, start, end, obstacles, gridSize, maxIterations, socketInformation, stepSize)
    path = findPath (parentBlock, start, end)
    return path, parentBlock
