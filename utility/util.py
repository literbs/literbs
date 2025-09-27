import math
import os
import csv

def keysVersion (arr, appen=False):
    obj = {} if not appen else []
    for x in arr:
        if appen:
            obj.append(f'{x[0]}:{x[1]}')
        else:
            obj[f'{x[0]}:{x[1]}']=None
    return obj

def convertTo2Dp (numb):
    return math.floor(numb*100)/100

def getAreaMeta (blockers, areaSize):
    areaMeta = {}
    for key in blockers:
        x = math.floor((key[0])/areaSize)
        y = math.floor((key[1])/areaSize)
        id = (x,y)
        if id in areaMeta:
            areaMeta[id][key] = None
        else:
            areaMeta[id] = {}
            areaMeta[id][key] = None

    return areaMeta

def turnIntoKiloBytes (bytes):
    # inKiloBytes = bytes / 1000
    return math.floor(bytes*10)/10000

def getDistance(vectorOne, vectorTwo, pythagoras=True):
    if not pythagoras:
        return abs(vectorOne[0]-vectorTwo[0]) + abs(vectorOne[1]-vectorTwo[1])  
    return math.sqrt(math.pow(vectorOne[0]-vectorTwo[0], 2) + math.pow(vectorOne[1]-vectorTwo[1], 2))

def findRightAngleTurns (path):
    numberOfTurns = 0
    for k in range(2, len(path)):
        current = path[k]
        prev = path[k-2]
        difference = (abs(current[0]-prev[0]), abs(current[1]-prev[1]))
        if difference[0] >= 1 and difference[1] >= 1:
            numberOfTurns += 1
    return numberOfTurns

def calculateAverageDistanceFromObstacles (path, obstacles):
    distances = [1, 2]
    for cord in path:
        distances.append(findClosestObstacle(cord, obstacles))
    
    # distances.sort()
    size = len(distances)
    return sum(distances)/size
    # [math.floor(size/2)]    

def encodeCord (cord, cordSplitter="::"):
    try:
        return str(cord[0])+cordSplitter+str(cord[1])
    except:
        True
        return ""

def findClosestObstacle (cord, obstacles):
    keys = list(obstacles)
    min_ = float('inf')
    for ob in keys:
        distance = getDistance(ob, cord, pythagoras=False)
        min_ = min(min_, distance)
    
    return min_

def encodeArray (arr, cordListSplitter=":::", cordSplitter="::"):
    return cordListSplitter.join( [ encodeCord(cord, cordSplitter) for cord in arr ] )     

def findRightAngleTurns (path):
    numberOfTurns = 0
    for k in range(2, len(path)):
        current = path[k]
        prev = path[k-2]
        difference = (abs(current[0]-prev[0]), abs(current[1]-prev[1]))
        if difference[0] >= 1 and difference[1] >= 1:
            numberOfTurns += 1
    return numberOfTurns    

def commentResults (results, algorithmCodeNameMap):
    print('--------------------------------------------------------------------')
    for key in results:
        if key == 'path':
            continue
        if key == 'algorithm':
            value = results[key] if key not in algorithmCodeNameMap else algorithmCodeNameMap[key]
            print(key.upper(), value)
        else:
            print(key.upper(),  str(results[key]))


def decode (node):

    try:
        first = int(node[0])
    except:
        first = -1 * int( node[0].replace('-', '') )

    try:
        second = int(node[1])
    except:
        second = -1 * int( node[1].replace('-', '') )

    return (first, second)

def appendDataToFile(filepath, columns, extraLine):

    directory = os.path.dirname(filepath)
    if directory:
        os.makedirs(directory, exist_ok=True)
    
    # Open the file in append mode
    with open(filepath, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # If this is the first time creating the file, write headers
        # You can check if the file is empty:
        if csvfile.tell() == 0:
            writer.writerow(columns)

        writer.writerow(extraLine)
        csvfile.flush()

def lastLineOfCSV(filepath, headers):
    if not os.path.isfile(filepath):
        return None

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # No lines or only one line (e.g., header)
    if len(lines) <= 1:
        return None

    lastLine = lines[-1].rstrip("\n")
    parts = lastLine.split(",")
    if len(parts) != len(headers):
        return None

    obj = {}
    for h in range(len(headers)):
        obj[headers[h]] = parts[h]
    
    return obj