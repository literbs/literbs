import math
from utility.util import findRightAngleTurns, convertTo2Dp, commentResults, turnIntoKiloBytes, keysVersion, appendDataToFile, lastLineOfCSV
from timeit import default_timer as timer
from automate.efficiency import buildBlockMaze as efficiencyGrid
from automate.optimality import produceGrid as optimalityGrid
from automate.robustness import produceRandomMaze

from algorithms.sh import heuristic
from algorithms.shp import heuristic as singlePruned

from algorithms.literbs import heuristic as literbs
from algorithms.literbsPrunedWithSpacing import heuristic as literbsPrunedWithSpace
from algorithms.literbsPruned import heuristic as literbsPruned
from algorithms.literbsPythagFitness import heuristic as literbsPythagFitness
from algorithms.literbs8Options import heuristic as literbs8Options
from algorithms.literbs8Pruned import heuristic as literbs8Pruned
from algorithms.literbs8OptionsPrunedWithSpacing import heuristic as literbs8Prunedspace
from algorithms.literbs8OptionsPythagFitness import heuristic as literbs8Pythag
from algorithms.literbs8PrunedPythag import heuristic as literbs8PythagPruned

from algorithms.lee import lee_algorithm
from algorithms.a2 import astar_algorithm
from algorithms.da2 import dual_astar_algorithm

from algorithms.rrt import rrtRunner
from algorithms.jps import jps
from algorithms.bellmanford import spfa, bellmanFord

import yaml
import tracemalloc
import eventlet
eventlet.monkey_patch()

# liberbs-pythag does support socket stuff

recordHeaders = ['seed', 'density', 'gridSize', 'numberOfRightAngleTurns', 'visitSize', 'visitExcess', 'duration', 'pathSize', 'maxMemory', 'algorithm', 'message']

algorithmCodeNameMap = {
    'da2': 'Dual A star algorithm',
    'a2': 'A Star algorithm',
    'lee': 'The lee algorithm',
    'literbs': 'LiteRBS',
    'literbs-pythag': 'LiteRBS Pythag',
    'literbs-pruned': 'LiteRBS Pruned',
    'literbs-pruned-spacing': 'LiteRBS Pruned Spacing',
    'literbs-8': 'LiteRBS 8 options',
    'literbs-8-pruned': 'LiteRBS 8 Pruned',
    'literbs-8-pruned-spacing': 'LiteRBS 8 Pruned Spacing',
    'literbs-8-pythag': 'LiteRBS 8 Pythag',
    'literbs-8-pythag-pruned': 'LiteRBS 8 Pythag Pruned',
    'rrt': 'Rapidly exploring Random Tree',
    'jps': 'Jump point search algorithm',
    'bf': 'Bellman ford algorithm (optimised for grid)',
    'spfa': 'Shortest Path Faster Algorithm',
    'sh': 'LITRBS (Using 1 instance)',
    'shp': 'LITRBS (Using 1 instance) Pruned'
}

# SPECIFC_TEST_CONFIG defines the variables
# which are supported to run a single test
SPECIFC_TEST_CONFIG = {
    'mode': "", # can be: 'efficiency', or 'robustness' or 'optimality',
    'gridSize': 5, # integer, > 0
    'density': 1, # used only when mode == 'robustness'
    'seed': 0, # integer which defines the random seed, to maintain consistent graphs and runs (good for debugging)
    'socket': None, # object, which can be None if not needed, otherwise present it here
    'algorithm': "", # algorithm alias goes here, for example 'a2' for 'a start algorithm'
    'comment': False, # boolean, when true, result is commented out,
    'multiple-algorithms': [] # optional, for the runTestCasesAllAlgorithms function mainly
}

def runSingleTest (algorithm='magnetic', start=(0, 0), end=(1, 1), barriers={}, socketInformation=None, gridSize=50, comment=False, seed=None, density=None):
    originalBarriers = barriers.copy()
    path = []
    message = ''

    maxIterationsOverride = 1000000000000000

    if algorithm == 'da2':
        tracemalloc.start()
        tracemalloc.take_snapshot()
        startTime = timer()
        ( path, visits ) = dual_astar_algorithm(originalBarriers, start, end, maxIterations=maxIterationsOverride, socketInformation=socketInformation)
        endTime = timer()
        (_, maxMemory) = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        # print('actually read:', maxMemory2)

    elif algorithm == 'a2':
        tracemalloc.start()
        tracemalloc.take_snapshot()
        startTime = timer()
        ( path, visits ) = astar_algorithm(originalBarriers, start, end, maxIterations=maxIterationsOverride, socketInformation=socketInformation)
        endTime = timer()
        (_, maxMemory) = tracemalloc.get_traced_memory()
        tracemalloc.stop()

    elif algorithm == 'lee':
        tracemalloc.start()
        tracemalloc.take_snapshot()
        startTime = timer()
        ( path, visits ) = lee_algorithm(originalBarriers, start, end, maxIterations=maxIterationsOverride, socketInformation=socketInformation)
        endTime = timer()
        (_, maxMemory) = tracemalloc.get_traced_memory()
        tracemalloc.stop()

    elif algorithm == 'sh':
        tracemalloc.start()
        tracemalloc.take_snapshot()
        startTime = timer()
        ( path, visits ) = heuristic(start, end, originalBarriers, maxIterations=maxIterationsOverride, socketInformation=socketInformation)
        endTime = timer()
        (_, maxMemory) = tracemalloc.get_traced_memory()
        tracemalloc.stop()

    elif algorithm == 'shp':
        tracemalloc.start()
        tracemalloc.take_snapshot()
        startTime = timer()
        ( path, visits ) = singlePruned(start, end, originalBarriers, maxIterations=maxIterationsOverride, socketInformation=socketInformation)
        endTime = timer()
        (_, maxMemory) = tracemalloc.get_traced_memory()
        tracemalloc.stop()

    elif algorithm == 'literbs':
        tracemalloc.start()
        tracemalloc.take_snapshot()
        startTime = timer()
        ( path, visits, message ) = literbs(start, end, barriers, maxIterations=maxIterationsOverride, socketInformation=socketInformation)
        endTime = timer()
        (_, maxMemory) = tracemalloc.get_traced_memory()
        tracemalloc.stop()

    elif algorithm == 'literbs-pruned':
        tracemalloc.start()
        tracemalloc.take_snapshot()
        startTime = timer()
        ( path, visits, message ) = literbsPruned(start, end, barriers, maxIterations=maxIterationsOverride, socketInformation=socketInformation)
        endTime = timer()
        (_, maxMemory) = tracemalloc.get_traced_memory()
        tracemalloc.stop()

    elif algorithm == 'literbs-8':
        tracemalloc.start()
        tracemalloc.take_snapshot()
        startTime = timer()
        ( path, visits, message ) = literbs8Options(start, end, barriers, maxIterations=maxIterationsOverride, socketInformation=socketInformation)
        endTime = timer()
        (_, maxMemory) = tracemalloc.get_traced_memory()
        tracemalloc.stop()

    elif algorithm == 'literbs-8-pruned':
        tracemalloc.start()
        tracemalloc.take_snapshot()
        startTime = timer()
        ( path, visits, message ) = literbs8Pruned(start, end, barriers, maxIterations=maxIterationsOverride, socketInformation=socketInformation)
        endTime = timer()
        (_, maxMemory) = tracemalloc.get_traced_memory()
        tracemalloc.stop()

    elif algorithm == 'literbs-8-pythag':
        tracemalloc.start()
        tracemalloc.take_snapshot()
        startTime = timer()
        ( path, visits, message ) = literbs8Pythag(start, end, barriers, maxIterations=maxIterationsOverride, socketInformation=socketInformation)
        endTime = timer()
        (_, maxMemory) = tracemalloc.get_traced_memory()
        tracemalloc.stop()

    elif algorithm == 'literbs-8-pythag-pruned':
        tracemalloc.start()
        tracemalloc.take_snapshot()
        startTime = timer()
        ( path, visits, message ) = literbs8PythagPruned(start, end, barriers, maxIterations=maxIterationsOverride, socketInformation=socketInformation)
        endTime = timer()
        (_, maxMemory) = tracemalloc.get_traced_memory()
        tracemalloc.stop()

    elif algorithm == 'literbs-pruned-spacing':
        tracemalloc.start()
        tracemalloc.take_snapshot()
        startTime = timer()
        ( path, visits, message ) = literbsPrunedWithSpace(start, end, barriers, maxIterations=maxIterationsOverride, socketInformation=socketInformation)
        endTime = timer()
        (_, maxMemory) = tracemalloc.get_traced_memory()
        tracemalloc.stop()

    elif algorithm == 'literbs-8-pruned-spacing':
        tracemalloc.start()
        tracemalloc.take_snapshot()
        startTime = timer()
        ( path, visits, message ) = literbs8Prunedspace(start, end, barriers, maxIterations=maxIterationsOverride, socketInformation=socketInformation)
        endTime = timer()
        (_, maxMemory) = tracemalloc.get_traced_memory()
        tracemalloc.stop()

    elif algorithm == 'literbs-pythag':
        tracemalloc.start()
        tracemalloc.take_snapshot()
        startTime = timer()
        ( path, visits, message ) = literbsPythagFitness(start, end, barriers, maxIterations=maxIterationsOverride, socketInformation=socketInformation)
        endTime = timer()
        (_, maxMemory) = tracemalloc.get_traced_memory()
        tracemalloc.stop()

    elif algorithm == 'rrt':
        tracemalloc.start()
        tracemalloc.take_snapshot()
        startTime = timer()
        ( path, visits ) = rrtRunner(start, end, originalBarriers, gridSize, maxIterations=math.pow(gridSize, 5), socketInformation=socketInformation, stepSize=1)
        endTime = timer()
        (_, maxMemory) = tracemalloc.get_traced_memory()
        tracemalloc.stop()

    elif algorithm == 'jps':
        tracemalloc.start()
        tracemalloc.take_snapshot()
        startTime = timer()
        ( path, visits ) = jps(start, end, originalBarriers, gridSize, socketInformation=socketInformation)
        endTime = timer()
        (_, maxMemory) = tracemalloc.get_traced_memory()
        tracemalloc.stop()

    elif algorithm == 'spfa':
        tracemalloc.start()
        tracemalloc.take_snapshot()
        startTime = timer()
        ( path, visits ) = spfa(start, end, originalBarriers, gridSize, socketInformation=socketInformation)
        endTime = timer()
        (_, maxMemory) = tracemalloc.get_traced_memory()
        tracemalloc.stop()

    elif algorithm == 'bf':
        tracemalloc.start()
        tracemalloc.take_snapshot()
        startTime = timer()
        ( path, visits ) = bellmanFord(start, end, originalBarriers, gridSize, socketInformation=socketInformation)
        endTime = timer()
        (_, maxMemory) = tracemalloc.get_traced_memory()
        tracemalloc.stop()

    else:
        startTime = 0
        endTime = 0

    if path == -1 or path == None or ( type(path)==list and len(path) <= 1):
        if comment:
            print('path not valid for:', algorithm)
        return None

    rightAngleTurns = findRightAngleTurns(path)
    duration = endTime - startTime
    pathSize = len(path) if algorithm != 'da2' else len(path)-1

    results = {
        'maxMemory':maxMemory,
        'visitSize':len(visits),
        'message':message,
        'numberOfRightAngleTurns':rightAngleTurns,
        'visitExcess':max(0, len(visits)-len(path)),
        'pathSize':pathSize,
        'algorithm':algorithm,
        'gridSize': gridSize,
        'runTimeWithAnimation': f'{convertTo2Dp(duration*1000)} ms',
        'density': density
    }

    if socketInformation != None and 'io' in socketInformation:
        socketInformation['io'].emit('algorithm_response', { 'from':'a', 'meta': results, 'id':socketInformation.get('id') })

    results['duration'] = duration
    results['path'] = path
    results['seed'] = seed

    if comment:
        commentResults(results, algorithmCodeNameMap)

    return results

def determineBarrierInfo (options={}):
    if options['mode'] == "robustness":
        return produceRandomMaze(options['density'], options['gridSize'], options['seed'])
    elif options['mode'] == "efficiency":
        return efficiencyGrid(options['gridSize'], options['seed'])
    else:
        return optimalityGrid(options['gridSize'], options['seed'])


# runSpecificTest runs a specific test based
# on certain options
def runASpecificTest (options={}, knownBarrierInfo=None):

    if knownBarrierInfo:
        start, end, barriers = knownBarrierInfo
    else:
        start, end, barriers = determineBarrierInfo(options)

    return runSingleTest (options['algorithm'], start, end, barriers, options['socket'], options['gridSize'], options['comment'], options['seed'], options['density'])

# runAnimate is a helper function which lets us animate runs for multiple algorithms for demo purposes
def runAnimate (sio, threading, runningData, algorithms=[], gridSize=50, rosbustnessLevel=20, testType='robustness', seedValue=None, delay=0.05):

    print('Triggered by socket to run algorithms in parallel...')

    runningData['running'] = True

    runOptions = {
        'mode': testType,
        'gridSize': gridSize,
        'density': rosbustnessLevel,
        'seed': seedValue,
        'socket': None,
        'algorithm': "",
        'comment': False,
    }

    (start, end, barriers) = determineBarrierInfo(runOptions)
    stringBarriers = keysVersion(barriers, False)
    greenlets = []

    for i in range(len(algorithms)):
        algo = algorithms[i]
        socketInfo = { 'algo':algo, 'id':i, 'io':sio, 'sleepDuration':delay/1000, 'stringBarriers':stringBarriers, 'gridSize':gridSize }
        runOptions['socket'] = socketInfo
        runOptions['algorithm'] = algo

        def runner (data):
            runASpecificTest(data, (start, end, barriers))

        greenlets.append(eventlet.spawn(runner, runOptions.copy()))

    for g in greenlets:
        g.wait()

    for i in range(len(algorithms)):
        algo = algorithms[i]
        runOptions['socket'] = None
        runOptions['algorithm'] = algo

        results = runASpecificTest(runOptions, (start, end, barriers))

        if results == None:
            continue

        sio.emit('algorithm_response', { 'meta':{ 'maxMemory': str(turnIntoKiloBytes(results['maxMemory'])) + ' kb' , 'real run time':str( convertTo2Dp(results['duration']*1000) ) + 'milli-seconds' }, 'id':i })

    runningData['running'] = False

def retrieveTestCasesFromConfig (path):

    if type(path) != str or len(path) == 0:
        print("No path to record config")
        return []

    with open(path, 'r', encoding='utf-8') as file:
        try:
            data = yaml.safe_load(file)
            tests = data.get('tests')
            if type(tests) != list:
                print('Ensure there is a "test" section')
                return []
            return tests
        except Exception as e:
            print("error occured:")
            print(e)
            return []

def runTestCaseForAllAlgorithms (runOptions):

    (start, end, barriers) = determineBarrierInfo(runOptions)
    algorithms = runOptions.get('multiple-algorithms')

    algorithmsToRun = []
    algorithmResults = {}

    for i in range(len(algorithms)):
        algo = algorithms[i]
        def runner (data, algo):
            data['algorithm'] = algo
            response = runASpecificTest(data, (start, end, barriers))
            algorithmResults[data['algorithm']] = response

        algorithmsToRun.append(eventlet.spawn(runner, runOptions.copy(), algo))

    for g in algorithmsToRun:
        g.wait()

    return algorithmResults

def validateTestCaseInput (testCase):
    name = testCase.get('name')

    if type(testCase.get('numberOfIterations')) != int:
        return f"for: '{name}', numberOfIterations not defined"

    if type(testCase.get('gridSize')) != int:
        return f"for: '{name}', gridSize not defined"

    if type(name) != str or len(name) == 0:
        return f"for: '{name}', give test a name, so we know which file to save it to" + name

    testType = testCase.get('type')
    if testType not in ["efficiency", "robustness", "optimality"]:
        return f"for: '{name}', unknown test type"

    if testType == "robustness":
        density = testCase.get('densityStart')
        if type(density) != int or density < 0:
            return f"for: '{name}', density must be defined and must be more than 0"

        densityIncriment = testCase.get('densityIncriment')
        if type(densityIncriment) != int or densityIncriment < 0:
            return f"for: '{name}', densityIncriment must be defined and must be more than 0"

        densityIncrimentAfter = testCase.get('densityIncrimentAfter')
        if type(densityIncrimentAfter) != int or densityIncrimentAfter < 0:
            return f"for: '{name}', densityIncrimentAfter must be defined and must be more than 0"

    return None

def runSingleTestCase (topDirectory, testCase):

    validateMessage = validateTestCaseInput(testCase)
    if validateMessage:
        print(validateMessage)
        return

    name = testCase.get('name')
    seed = testCase.get('initialSeed')
    seedIncriment = testCase.get('seedIncriment')
    testType = testCase.get('type')
    numberOfIterations = testCase.get('numberOfIterations')
    gridSize = testCase.get('gridSize')
    density = testCase.get('densityStart')
    densityIncriment = testCase.get('densityIncriment')
    densityIncrimentAfter = testCase.get('densityIncrimentAfter')
    algorithms = testCase.get('multiple-algorithms')
    skip = testCase.get('skip')

    if seed == None or seedIncriment == None:
        seed = None
        seedIncriment = None

    if skip:
        print('skipped test case with name:', name)
        return

    if type(algorithms) != list:
        algorithms = list(algorithmCodeNameMap)


    isRobustness = testType == "robustness"
    extension = "_1" if isRobustness else ""
    dataPathStore = f'{topDirectory}/results/{name}{extension}.csv'
    lastLine = lastLineOfCSV(dataPathStore, recordHeaders)
    editions = 1

    # defines the number of excess failures we can except
    toleranceRemaining = 100000
    failures = 0

    i = 0
    iWithoutTolerations = 0
    try:
        if lastLine != None:
            lastSeed = int(lastLine.get('seed'))
            if lastSeed != "None":
                i = int((lastSeed - seed) / seedIncriment)
                seed = lastSeed + seedIncriment
                density = int(density.get('density'))
            print('restarting test from seed:', seed, 'and the', i, 'iteration')
    except:
        pass

    while i < numberOfIterations:
        i+=1
        iWithoutTolerations+=1
        if iWithoutTolerations % 100 == 0:
            print('progress:', iWithoutTolerations, "/", numberOfIterations+failures, "tolerations remaining:", toleranceRemaining)
        response = runTestCaseForAllAlgorithms({
            'mode': testType,
            'gridSize': gridSize,
            'density': density,
            'seed': seed,
            'socket': None,
            'algorithm': "",
            'comment': False,
            'multiple-algorithms': algorithms
        })

        sections = []
        foundErrors = False
        for alg in response:
            algData = response[alg]
            if algData == None:
                foundErrors = True
                print('skipping round:', 'iteration:', i, 'seed:', seed, 'as algorithm', alg, 'failed')
                break
            rowData = []
            for column in recordHeaders:
                rowData.append(f'{algData.get(column)}')
            sections.append(rowData)

        if seedIncriment != None:
            seed += seedIncriment

        wentBack = False
        if not foundErrors:
            for s in sections:
                appendDataToFile(dataPathStore, recordHeaders, s)
        elif toleranceRemaining > 0:
            # add another iteration
            i-=1
            wentBack = True
            toleranceRemaining-=1
            failures+=1

        if not wentBack and isRobustness and (i % densityIncrimentAfter == 0):
            editions += 1
            density += densityIncriment
            dataPathStore = f"{topDirectory}/results/{name}{f'_{editions}'}.csv"
