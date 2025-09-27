from collections import deque
from algorithms.a2 import sendData, get_neighbors

def keysVersion (arr, appen=False):
    obj = {} if not appen else []
    for x in arr:
        if appen:
            obj.append(f'{x[0]}:{x[1]}')
        else:
            obj[f'{x[0]}:{x[1]}']=None
    return obj

def lee_algorithm(grid, start, end, maxIterations=1000000000, socketInformation=None):
    queue = deque()
    queue.append(start)
    visited = [start]
    distance = {start: 0}
    path = [end]
    
    while queue and maxIterations>=0:
        current = queue.popleft()
        if current == end:
            break
        for neighbor in get_neighbors(grid, current):
            if neighbor not in visited:
                visited.append(neighbor)
                queue.append(neighbor)
                distance[neighbor] = distance[current] + 1
        maxIterations -= 1

        sendData(socketInformation, [], visited)
                
    if end not in distance:
        return ([], visited)
    
    while path[-1] != start:
        current = path[-1]
        neighbors = get_neighbors(grid, current)
        neighbor_distances = [distance.get(n, float('inf')) for n in neighbors]
        min_distance = min(neighbor_distances)
        if min_distance == float('inf'):
            return ([], visited)
        min_neighbors = [n for i, n in enumerate(neighbors) if neighbor_distances[i] == min_distance]
        path.append(min_neighbors[0])

    sendData(socketInformation, path, visited)
        
    return (path[::-1], visited)
