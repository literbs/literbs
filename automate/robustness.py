import math
import random

def getBorder (d, existing={}, blockMode=True):
    # do top
    for i in range(d):
        existing[ f'-1:{i}' if not blockMode else (-1, i) ] = None

    for i in range(d):
        existing[ f'{d}:{i}' if not blockMode else (d, i) ] = None

    for i in range(-1,d+1):
        existing[ f'{i}:{-1}' if not blockMode else (i, -1) ] = None 
    for i in range(-1,d+1):
        existing[ f'{i}:{d}' if not blockMode else (i, d) ] = None                
    
    return existing

def produceRandomMaze (percentage, dimension, seedValue=None):
    if seedValue != None:
        random.seed(seedValue)
    # print('random seed here was', )
    start = (0, 0)
    end = (dimension-1, dimension-1)
    obstacleFrequency = math.floor(math.pow(dimension, 2) * percentage/100)
    obstacles = {}
    while obstacleFrequency > 0:
        cords = (random.randint(0,dimension) ,random.randint(0,dimension))
        if cords == start or cords == end or cords in obstacles:
            continue
        obstacles[cords] = None
        obstacleFrequency-=1
    if seedValue != None:
        random.seed(seedValue)
    return (start, end, getBorder(dimension, obstacles))
