import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ALGORITHM_CODE_NAMES = {
    'da2': 'Dual A star algorithm',
    'a2': 'A Star algorithm',
    'lee': 'Lee algorithm',
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
    'sh': 'LITRBS (1 instance)',
    'shp': 'LITRBS (1 instance) Pruned'
}

NUMERICAL_FIELDS = ['numberOfRightAngleTurns','visitSize','visitExcess','duration','pathSize','maxMemory']
GROUP_BY_FIELD = 'algorithm'
DEFAULT_FIELD_OPERATIONS = {'duration': 'convertDurationToMs'}

def summarise (path, dropFields=[], fieldOperations=DEFAULT_FIELD_OPERATIONS):
    postProcessingObjectMean, postProcessingObjectMedian, postProcessingStandardDeviationObject = retrieveTableObjects (path, dropFields, fieldOperations)
    useFullName = True
    return convertDataIntoPandasDataframe(postProcessingObjectMean, useFullName), convertDataIntoPandasDataframe(postProcessingObjectMedian, useFullName), convertDataIntoPandasDataframe(postProcessingStandardDeviationObject, useFullName)

def retrieveTableObjects (path, dropFields=[], fieldOperations=DEFAULT_FIELD_OPERATIONS):
    # retrieve all data and group items based on the associated algorithm
    allData = pd.read_csv(path)
    groups = allData.groupby([GROUP_BY_FIELD])

    # summarised data will be stored in these objects
    # which can then be used to produce the tables for display
    postProcessingObjectMean = {}
    postProcessingObjectMedian = {}
    postProcessingStandardDeviationObject = {}

    # go through each group and identify metrics
    # for each column and for each algorithm (mean, median, standard dev)
    for groupNames, numericalSections in groups:

        algorithmName = groupNames[0]
        numericalSections = numericalSections.drop(labels=[GROUP_BY_FIELD]+dropFields, axis='columns')
        columns = list(numericalSections.columns)

        for column in columns:

            columnValues = np.array(list(numericalSections[column]))

            meanValue, medianValue, standardDeviation = identifyMetrics (columnValues)

            addValueToObject(postProcessingObjectMean, algorithmName, column, meanValue)
            addValueToObject(postProcessingObjectMedian, algorithmName, column, medianValue)
            addValueToObject(postProcessingStandardDeviationObject, algorithmName, column, standardDeviation)

    return postProcessingObjectMean, postProcessingObjectMedian, postProcessingStandardDeviationObject

def convertDataIntoPandasDataframe (object, useFullName=True):
    outputObject = {}

    # for each algorithm, turn the object inside out
    for algorithmName in object:
        algorithmContents = object[algorithmName]
        appendMetricIntoObject(outputObject, 'algorithm', algorithmName)

        # algorithmContents should look like: (numberOfRightAngleTurns, visitSize, duration ....)
        for fieldName in algorithmContents:
            appendMetricIntoObject(outputObject, fieldName, algorithmContents[fieldName])

    if useFullName:
        for keyIndex in range(len(outputObject['algorithm'])):
            key = outputObject['algorithm'][keyIndex]
            if key not in ALGORITHM_CODE_NAMES:
                continue
            correspondingName = ALGORITHM_CODE_NAMES[key]
            outputObject['algorithm'][keyIndex] = correspondingName

    return pd.DataFrame(outputObject)

def appendMetricIntoObject (outputObject, fieldName, fieldValue):
    if fieldName not in outputObject:
        outputObject[fieldName] = []

    outputObject[fieldName].append(fieldValue)

def determineMedianValue (columnValues):
    data = list(columnValues)
    size = len(data)
    data.sort()
    return data[math.floor(size/2)]

def convertDurationToMs (seconds):
    return seconds * 1000

def retrieveValueOfFieldFromOperation (fieldName, fieldOperations, summarisedValue):
    operation = 'round' if fieldName in fieldOperations else fieldOperations[fieldName]

    if operation == 'round':
        return round(summarisedValue)
    if operation == 'convertDurationToMs':
        return convertDurationToMs(summarisedValue)

def addValueToObject (object, algorithmName, columnName, value):
    if algorithmName not in object:
        object[algorithmName] = {}
    object[algorithmName][columnName] = value

def identifyMetrics (columnValues):
    size = len(columnValues)
    meanValue = sum(columnValues) / size
    medianValue = determineMedianValue(columnValues)
    standardDeviation = np.std(columnValues)
    return (meanValue, medianValue, standardDeviation)

def appendMetricToRobustnessParent (parentObject, algorithm, metricField, metricValue):

    if algorithm not in parentObject:
        parentObject[algorithm] = {}
    if metricField not in parentObject[algorithm]:
        parentObject[algorithm][metricField] = []

    parentObject[algorithm][metricField].append(metricValue)

def condenseRobustnessTables (pathPrefix, range_=(1, 31), useMetric='mean', dropFields=[], useFullName=True):

    parentObject = {}

    for i in range(range_[0], range_[1]):
        mean, median, std = retrieveTableObjects (f'{pathPrefix}_{i}.csv', dropFields)
        useObject = None
        if useMetric == 'mean':
            useObject = mean
        elif useMetric == 'median':
            useObject = median
        else:
            useObject = std

        for algorithm in useObject:
            for metricField in useObject[algorithm]:
                appendMetricToRobustnessParent (parentObject, algorithm, metricField, useObject[algorithm][metricField])

    if useFullName:
        deleteKeys = []
        appendVals = []
        for key in parentObject:
            if key not in ALGORITHM_CODE_NAMES:
                continue
            correspondingName = ALGORITHM_CODE_NAMES[key]
            appendVals.append((correspondingName, parentObject[key]))
            deleteKeys.append(key)

        for i in range(len(appendVals)):
            key, value = appendVals[i]
            parentObject[key] = value

        for keyToDelete in deleteKeys:
            del parentObject[keyToDelete]

    return parentObject

def mapCodeNameToFullName (values):
    newv = []
    for v in values:
        if v not in ALGORITHM_CODE_NAMES:
            newv.append(v)
        else:
            newv.append(ALGORITHM_CODE_NAMES[v])
    return newv

def drawGraph (index, metric, tables, include=[]):
    plt.figure(index)

    for alg in tables:

        plt.rcParams["figure.figsize"] = (20,5)
        plt.rcParams['font.size'] = 18

        if alg not in include:
            continue

        plt.plot([x for x in range(1, 31)], tables[alg][metric], label = alg )

    plt.xlabel("Ratio of Obstacles to Total nodes in percentages (%)")
    plt.title(f'{metric} with respect to noise')
    plt.ylabel(metric)
    plt.legend()
    plt.grid(True)

def retrieveMergeTypeCount (path, algorithmKey):
    # retrieve all data and group items based on the associated algorithm
    allData = pd.read_csv(path)
    messageFieldValues = list(allData[allData.algorithm == algorithmKey]['message'])
    sections = { 'trail': 0, 'direct': 0 }
    for val in messageFieldValues:
        if 'MERGEINTRAIL' in val:
            sections['trail']+=1
        elif 'MERGEDIRECT' in val:
            sections['direct']+=1

    return sections

def retrieveMergeTypeCountForAll (pathPrefix, algorithmKey, range_=(1, 31),):

    sectionValues = {}

    for i in range(range_[0], range_[1]):
        sections = retrieveMergeTypeCount(f'{pathPrefix}_{i}.csv', algorithmKey)
        for s in sections:
            if s not in sectionValues:
                sectionValues[s] = []
            sectionValues[s].append(sections[s])

    return sectionValues

def drawMergeInfo (mergeInfo):
    for s in mergeInfo:

        plt.rcParams["figure.figsize"] = (20,5)
        plt.rcParams['font.size'] = 18

        plt.plot([x for x in range(1, 31)], mergeInfo[s], label = s)

    plt.xlabel("Density")
    plt.title(f'Merge in trail vs Merge direct')
    plt.ylabel("count")
    plt.legend()
    plt.grid(True)
