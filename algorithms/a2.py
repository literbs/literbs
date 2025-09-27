import heapq
import time
import math

def keysVersion (arr, appen=False):
    obj = {} if not appen else []
    for x in arr:
        if appen:
            obj.append(f'{x[0]}:{x[1]}')
        else:
            obj[f'{x[0]}:{x[1]}']=None
    return obj

def findPath (start, end, came_from):
    path = []
    current = end
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    return (path[::-1], came_from)    

def sendData (socketInformation, path, cameFrom):

    if socketInformation == None:
        return

    if 'io' not in socketInformation:
        return

    path = keysVersion(path)
    parentStringEdition = keysVersion(cameFrom)

    if 'sleepDuration' in socketInformation:
        time.sleep(socketInformation['sleepDuration'])

    socketInformation['io'].emit('algorithm_response', { 'meta':{'algorithm': socketInformation['algo'],  'visitSize':len(cameFrom) }, 'gridSize':socketInformation.get('gridSize'), 'id':socketInformation.get('id'), 'path':path, 'barriers':socketInformation.get('stringBarriers'), 'visited':parentStringEdition })

def astar_algorithm(barriers, start, end, maxIterations=1000000000, socketInformation=None):
    heap = []
    tempHeap = [] if socketInformation else None
    heapq.heappush(heap, (0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while heap and maxIterations >= 0:
        current = heapq.heappop(heap)[1]
        if current == end or current == None:
            break
        
        for neighbor in get_neighbors(barriers, current):
            new_cost = cost_so_far[current] + distance(current, neighbor)
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + distance(neighbor, end)
                heapq.heappush(heap, (priority, neighbor))
                if socketInformation:
                    tempHeap.append(neighbor)
                came_from[neighbor] = current

        sendData(socketInformation, [], came_from)

        maxIterations -= 1
        
    if end not in came_from:
        return ([], came_from)
    
    path = []
    current = end
    while current != start:
        path.append(current)
        current = came_from[current]
        sendData(socketInformation, path, came_from)        

    path.append(start)
    sendData(socketInformation, path, came_from)

    return (path[::-1], came_from)

def get_neighbors(barriers, current):
    row, col = current
    neighbors = []
    for r, c in ((row-1, col), (row, col-1), (row+1, col), (row, col+1), (row-1, col-1), (row-1, col+1), (row+1, col-1), (row+1, col+1)):
        if (r, c) in barriers:
            continue
        neighbors.append((r, c))
    return neighbors

# use euclidean distance
def distance(a, b):
    x1, y1 = a
    x2, y2 = b
    return math.sqrt ( math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2) )
