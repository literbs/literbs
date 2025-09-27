import heapq
from algorithms.a2 import sendData, get_neighbors, distance

def findPath (start, end, came_from):
    path = []
    current = end
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    return (path[::-1], came_from)    

def dual_astar_algorithm(grid, start, end, maxIterations=1000000000, socketInformation=None):
    heaps = ([], [])
    
    tempHeap = [] if socketInformation else None

    destinations = (end, start)

    heapq.heappush(heaps[0], (0, start))
    heapq.heappush(heaps[1], (0, end))

    came_from = ({}, {})
    cost_so_far = ({}, {})

    came_from[0][start] = None
    cost_so_far[0][start] = 0

    came_from[1][end] = None
    cost_so_far[1][end] = 0    
    
    index = 0

    conjoinedPoint = None

    while (heaps[0] or heaps[1]) and conjoinedPoint == None and maxIterations >= 0:
        nextIndex = (index + 1 ) % 2
        current = heapq.heappop(heaps[index])[1] if len(heaps[index]) else None
        if current == destinations[index] or current == None:
            break
        
        for neighbor in get_neighbors(grid, current):
            new_cost = cost_so_far[index][current] + distance(current, neighbor)
            if neighbor not in cost_so_far[index] or new_cost < cost_so_far[index][neighbor]:
                cost_so_far[index][neighbor] = new_cost
                priority = new_cost + distance(neighbor, destinations[index])
                heapq.heappush(heaps[index], (priority, neighbor))
                
                if socketInformation:
                    tempHeap.append(neighbor)

                if neighbor in came_from[nextIndex]:
                    conjoinedPoint = neighbor

                came_from[index][neighbor] = current
        
        sendData(socketInformation, [], list(came_from[0]) + list(came_from[1]))

        maxIterations -= 1
        index = nextIndex

    if conjoinedPoint==None and end not in came_from:
        return ([], came_from[0])
    
    path = []
    if conjoinedPoint != None:
        pathA = []        
        pathB = []        
        current = conjoinedPoint
        while current != start:
            pathA.append(current)
            current = came_from[0][current]
        current = conjoinedPoint
        while current != end:
            pathB.append(current)
            current = came_from[1][current]

        pathA.append(start)
        pathB.append(end)
        path = pathA[::-1] + pathB

        sendData(socketInformation, path, list(came_from[0]) + list(came_from[1]))
        return (path, { x:None for x in list(came_from[0])+list(came_from[1]) })

    else:

        current = end
        while current != start:
            path.append(current)
            current = came_from[index][current]

            sendData(socketInformation, path, list(came_from[0]) + list(came_from[1]))            

    path.append(start)
    sendData(socketInformation, path, list(came_from[0]) + list(came_from[1]))

    return (path[::-1], {**came_from[0], **came_from[1]})