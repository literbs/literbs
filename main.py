# sets the import from position throughout entire project
import argparse
import sys
from pathlib import Path
topDirectory = Path(__file__).resolve().parents[0]
sys.path.append(topDirectory)

from utility.runs import runTestCaseForAllAlgorithms, runAnimate, algorithmCodeNameMap, retrieveTestCasesFromConfig, runSingleTestCase
import socketio
import threading

from tabulate import tabulate
import socketio
import eventlet
import socketio

parser = argparse.ArgumentParser(description="Path finding comparison")
parser.add_argument("--mode", "-m", required=True, choices=["animate", "quick-compare", "record-tests", "view-code-names"], help="Mode to run script in\n. animate - opens socket io client, which can then be used to send path information onto web UI. single - runs a single test")
parser.add_argument("--grid-type", "-t", choices=["efficiency", "robustness", "optimality"], default="efficiency", help="The type of grid to work with")
parser.add_argument("--grid-size", "-s", type=int, default=5, help="The number of rows and columns of your grid")
parser.add_argument("--grid-density", "-d", type=int, default=5, help="Describes the ratio of obstacles to free space there should be in the grid, only for grid type of 'robustness'")
parser.add_argument("--grid-seed", "-e", type=int, default=None, help="Describes which random to seed to use")
parser.add_argument("--grid-algorithms", "-a", default=[], nargs="+", help=f"Defines which algorithms to run. Use the 'view-code-names' command to view options")
parser.add_argument("--test-config", "-c", help="file path to retrieve test config")

args = parser.parse_args()

if args.mode == "animate":

    print('Animate new mode in progress')
    runningData = { 'running': False }

    sio = socketio.Server(cors_allowed_origins="*")
    app = socketio.WSGIApp(sio, static_files={
        '/': {'content_type': 'text/html', 'filename': './web/compare.html'}
    })

    @sio.event
    def connect(sid, environ):
        print('connect ', sid)

    # @sio.event
    # def algorithm_response(sid, data):
    #     sio.emit('algorithm_response', data)    

    @sio.event
    def message(sid, data):
        # sio.emit('emit', data)
        if runningData['running']:
            return
        if 'nonprocessing' not in data:
            return
        runAnimate (sio, threading, runningData, data['algorithms'], data['gridSize'], data['rosbustnessLevel'], data['testType'], None if 'seedValue' not in data else data['seedValue'], 0.05 if 'delay' not in data else data['delay'])
        # print('message ', data)

    @sio.event
    def disconnect(sid):
        print('disconnect ', sid)

    if __name__ == '__main__':
        eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 5005)), app)


if args.mode == "quick-compare":
    print("\nRuning single test mode.", "algorithms to run:", args.grid_algorithms, "grid type:", args.grid_type, 'grid size:', args.grid_size, 'grid density:', args.grid_density, 'grid seed:', args.grid_seed, '\n')
    headers = ['algorithm', 'maxMemory', 'visitSize', 'numberOfRightAngleTurns', 'visitExcess', 'pathSize', 'runTimeWithAnimation']    
    rows = []

    algorithmsToRun = args.grid_algorithms
    if len(args.grid_algorithms) == 1 and args.grid_algorithms[0] == "*":
        algorithmsToRun = list(algorithmCodeNameMap)

    allResults = runTestCaseForAllAlgorithms ({
        'mode': args.grid_type, 
        'gridSize': args.grid_size,
        'density': args.grid_density,
        'seed': args.grid_seed,
        'socket': None,
        'algorithm': None,
        'comment': False,
        'multiple-algorithms': algorithmsToRun
    })

    for alg in allResults:
        response = allResults[alg]
        if response == None:
            print('failed run for', alg)
            continue

        section = []
        for h in headers:
            value = response.get(h)
            if h == 'algorithm':
                value = algorithmCodeNameMap[value]
            section.append(value)
        rows.append(section)

    headers[len(headers)-1] = 'runTimeWithoutAnimation'
    print(tabulate(rows, headers=headers, tablefmt="grid"))


if args.mode == "record-tests":
    testCases = retrieveTestCasesFromConfig(args.test_config)
    for test in testCases:
        runSingleTestCase(topDirectory, test)

if args.mode == "view-code-names":
    headers = ['code name', 'algorithm']
    rows = []
    for code in algorithmCodeNameMap:
        rows.append([code, algorithmCodeNameMap[code]])

    print(tabulate(rows, headers=headers, tablefmt="grid"))