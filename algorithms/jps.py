import heapq
import math
import time
import eventlet
eventlet.monkey_patch()
DIRECTIONS = [
    (0, 1), (1, 0), (0, -1), (-1, 0),
    (1, 1), (-1, 1), (-1, -1), (1, -1)
]

def heuristic(a, b):
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return dx + dy + (math.sqrt(2) - 2) * min(dx, dy)

def isBlocker (node, obstacles, gridDimensions={'x':0, 'y':0}):
    if node in obstacles:
        return True
    if node[0] < 0 or node[0] > gridDimensions['x']:
        return True
    if node[1] < 0 or node[1] > gridDimensions['y']:
        return True    
    return False

def addVectorToNode (node, vector):
    return (node[0]+vector[0], node[1]+vector[1])

def addVectorToNodeAndIsBlocker (node, vector, obstacles, gridDimensions):
    newNode = addVectorToNode(node, vector)
    return newNode, isBlocker(newNode, obstacles, gridDimensions)

def getHorizontalForcedDirections (directionX):
    return ((directionX, -1),(directionX, 1))

def getVerticalForcedDirections (directionY):
    return ( (-1, directionY), (1, directionY))

# we only care about orthogonals in this case
def getDiagonalForcedDirections (directionX, directionY):
    return ( (directionX, 0), (0, directionY) )

def jump (current, direction, goal, obstacles, gridDimensions):
    
    # ensure next point is reachable
    potentialJumptPoint, nextNodeisBlocker = addVectorToNodeAndIsBlocker(current, direction, obstacles, gridDimensions)
    if nextNodeisBlocker:
        return None
    # print('checking jump from', current, potentialJumptPoint)
    if potentialJumptPoint == goal:
        return potentialJumptPoint
    
    forcedDirectionsToCheck = []
    diagonalMovement = False

    # if direction flow is horizontal, 
    # check to see if we have any forced neighburs
    # if we do, return the current position as this is now a jump point
    if direction[0] != 0 and direction[1] != 0:
        # print('getting diagonal block movements')
        diagonalMovement = True
        forcedDirectionsToCheck = getDiagonalForcedDirections(direction[0], direction[1])
    else:
        if direction[0] != 0 and direction[1] == 0:
            # print('getting horizontal block movements')
            forcedDirectionsToCheck = getHorizontalForcedDirections(direction[0])
        elif direction[1] != 0 and direction[0] == 0:
            # print('getting vertical block movements')
            forcedDirectionsToCheck = getVerticalForcedDirections(direction[1])

    for checkDirection in forcedDirectionsToCheck:
        _, isForcedNeighbour = addVectorToNodeAndIsBlocker(current, checkDirection, obstacles, gridDimensions)       
        # print('first forced block check:', convertedNode, 'based on', checkDirection, 'is forced:', isForcedNeighbour)
        # if convertedNode[0] < 0 or convertedNode[0] > gridDimensions['x'] or convertedNode[1] < 0 or convertedNode[1] > gridDimensions['y']:
        #     continue
        if isForcedNeighbour:
            return potentialJumptPoint
    
    if diagonalMovement:
        futureDiagonalBlockers = jump(potentialJumptPoint, direction, goal, obstacles, gridDimensions)
        if futureDiagonalBlockers:
            return potentialJumptPoint        
        futureHorizontalBlockers = jump(potentialJumptPoint, (direction[0], 0), goal, obstacles, gridDimensions)
        if futureHorizontalBlockers:
            return potentialJumptPoint
        futureVerticalBlockers = jump(potentialJumptPoint, (0, direction[1]), goal, obstacles, gridDimensions)
        if futureVerticalBlockers:
            return potentialJumptPoint
    
    # potentialJumptPoint is no longer a jump point, 
    # its valid and we can explore it further
    validNode = potentialJumptPoint
    returnedResponse = jump(validNode, direction, goal, obstacles, gridDimensions)
    if not returnedResponse:
        # print("failure here, so returning for", potentialJumptPoint, "which has parent", current)
        return potentialJumptPoint

    return returnedResponse

def getHorizontalSuccessors (directionX):
    return (
        (directionX, -1),
        (directionX, 0),
        (directionX, 1),
    )

def getVerticalSuccessors (directionY):
    return (
        (-1, directionY),
        (0, directionY),
        (1, directionY),
    )

def getDiagonalSuccessors (directionX, directionY):
    return (      
        (-1, directionY),
        (0, directionY),
        (1, directionY),
        (directionX, -1),
        (directionX, 0),
        (directionX, 1),
    )

def determineMovementDirection (current, parent):
    
    # get a sense of the direction
    xDiff = current[0] - parent[0]
    yDiff = current[1] - parent[1]
    
    # standardise values so we only work 
    # with with either 0, 1, or -1
    if xDiff != 0:
        xDiff = xDiff / abs(xDiff)
    if yDiff != 0:
        yDiff = yDiff / abs(yDiff)        
    
    # values returned as floats,
    # so use 'int' cast to convert to int
    return int(xDiff), int(yDiff)

# getSuccessors determines directions which should be treated as candidates
def getSuccessors (current, parent, obstacles, gridDimensions):

    if parent == None:
        return DIRECTIONS

    movementDirectionVector = determineMovementDirection (current, parent)

    successors = []
    tempSuccessors = None

    # manage horizontal, vertical, and diagonal
    if movementDirectionVector[0] != 0 and movementDirectionVector[1] == 0:
        tempSuccessors = getHorizontalSuccessors(movementDirectionVector[0])
    elif movementDirectionVector[1] != 0 and movementDirectionVector[0] == 0:
        tempSuccessors = getVerticalSuccessors(movementDirectionVector[1])
    else:
        tempSuccessors = getDiagonalSuccessors (movementDirectionVector[0], movementDirectionVector[1])

    # filter out vectors which would lead us to blocked nodes
    for vector in tempSuccessors:
        _, isBlocker = addVectorToNodeAndIsBlocker(current, vector, obstacles, gridDimensions)
        if not isBlocker:
            successors.append(vector)

    if len(successors) == 0:
        return DIRECTIONS

    return successors

def getPath(parentNodes, current):
    path = [current]
    while current in parentNodes:
        current = parentNodes[current]
        path.append(current)
    return path[::-1]

def convertTreeToUniqueList (tree):
    obj = {}
    for node in tree:
        obj[f"{node[0]}:{node[1]}"] = None
    return obj

def sendData (socketInformation, cameFrom, startNode):

    if socketInformation == None:
        return

    if 'io' not in socketInformation:
        return

    path = getPath(cameFrom, startNode)
    path = convertTreeToUniqueList(path)

    parentStringEdition = convertTreeToUniqueList(cameFrom)

    if 'sleepDuration' in socketInformation:
        # eventlet.sleep(0.5)
        time.sleep(socketInformation['sleepDuration'])

    socketInformation['io'].emit('algorithm_response', { 'meta':{'algorithm':'JPS',  'visitSize':len(cameFrom) }, 'gridSize':socketInformation.get('gridSize'), 'id':socketInformation.get('id'), 'path':path, 'barriers':socketInformation.get('stringBarriers'), 'visited':parentStringEdition })

def jps(start, goal, obstacles, gridSize, socketInformation=None):
    heap = []
    heapq.heappush(heap, (heuristic(start, goal), 0, start, None))
    came_from = {}
    cost_so_far = {start: 0}
    gridDimensions={'x':gridSize, 'y':gridSize}
    while heap:
        _, cost, current, parent = heapq.heappop(heap)
        sendData (socketInformation, came_from, current)

        if current == goal:
            return getPath(came_from, current), came_from

        directions = getSuccessors (current, parent, obstacles, gridDimensions)
        
        for dx, dy in directions:
            jp = jump(current, (dx, dy), goal, obstacles, gridDimensions)
            if jp:
                # new_cost = cost_so_far[current] + math.hypot(jp[0] - current[0], jp[1] - current[1])
                new_cost = cost_so_far[current] + heuristic(jp, current)
                if jp not in cost_so_far or new_cost < cost_so_far[jp]:
                    cost_so_far[jp] = new_cost
                    priority = new_cost + heuristic(jp, goal)
                    heapq.heappush(heap, (priority, new_cost, jp, current))
                    came_from[jp] = current        

    return None, came_from  # No path found
