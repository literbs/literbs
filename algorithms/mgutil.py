import time
from utility.util import keysVersion
def extractPathCompare (end, nodes, reverse=True):
    currentlyAt = end
    path = [end]
    # To avoid missing better solutions for the parent, 
    # since the parent may have been an alternative and missed 
    # the chanced to check whether it was good enough or not
    
    while currentlyAt in nodes and nodes[currentlyAt][0] != None:
        
        # Line added for update
        parent = currentlyAt
        # Line above added for update

        child = nodes[currentlyAt][0]
        
        left = (parent[0]+1,  parent[1]) 
        right = (parent[0]-1,  parent[1]) 
        top = (parent[0],  parent[1]+1) 
        bottom = (parent[0],  parent[1]-1) 
        if left in nodes:
            if left != path[len(path)-1]:
                if child != left:
                    if nodes[left][1] < nodes[child][1] and left not in path:
                        path.append(left)
                        currentlyAt = left
                        continue
        if right in nodes:
            if right != path[len(path)-1]:
                if child != right:
                    if nodes[right][1] < nodes[child][1] and right not in path:
                        path.append(right)
                        currentlyAt = right
                        continue
        if top in nodes:
            if top != path[len(path)-1]:
                if child != top:
                    if nodes[top][1] < nodes[child][1] and top not in path:
                        path.append(top)
                        currentlyAt = top
                        continue     
        if bottom in nodes:
            if bottom != path[len(path)-1]:
                if child != bottom:
                    if nodes[bottom][1] < nodes[child][1] and bottom not in path:
                        path.append(bottom)
                        currentlyAt = bottom
                        continue                                            
                        
        path.append(child)
        currentlyAt = child
        
    return path[::-1] if reverse else path


def extractPathCompareAdvanced (end, nodes, reverse=True):
    currentlyAt = end
    path = [end]
    # To avoid missing better solutions for the parent, 
    # since the parent may have been an alternative and missed 
    # the chanced to check whether it was good enough or not
    
    while currentlyAt in nodes and nodes[currentlyAt][0] != None:
        
        smallestNode = nodes[currentlyAt][0]
        smallestScore = nodes[currentlyAt][1]

        left = (currentlyAt[0]-1,  currentlyAt[1]) 
        right = (currentlyAt[0]+1,  currentlyAt[1]) 
        top = (currentlyAt[0],  currentlyAt[1]+1) 
        bottom = (currentlyAt[0],  currentlyAt[1]-1) 

        if left in nodes and left != path[len(path)-1] and nodes[left][1] < smallestScore:
            currentlyAt = left
            path.append(currentlyAt)
            continue
        if right in nodes and right != path[len(path)-1] and nodes[right][1] < smallestScore:
            currentlyAt = right
            path.append(currentlyAt)
            continue
        if top in nodes and top != path[len(path)-1] and nodes[top][1] < smallestScore:
            currentlyAt = top
            path.append(currentlyAt)
            continue
        if bottom in nodes and bottom != path[len(path)-1] and nodes[bottom][1] < smallestScore:
            currentlyAt = bottom
            path.append(currentlyAt)
            continue

        
    return path[::-1] if reverse else path

"""

One of the shortcomings of the literbs algorithm is that it can add in noise to the path
when the two instances are trying to find each other. This noise can ocasionally lead to paths
which are suboptimal as they include loops which are not ideal for real life conditions.
To mitigate this, we tweak the algorithm slightly in two places.

Pruning depends on additional data from the parent-child map used to extract the path.
Now, after recording the parent of the child, we also need to store the order in which the child was added.
The start nodes can will have the order 1, and each child after incriments the order by 1.

The second step required for pruning uses this data in the extraction step.
Initially, whilst we didn't reach the start node from the end node, we would just look at the
parent-child map to establish who the next parent is. After doing this a couple of iterations, we should get to the
start node to establish our path. This time however, we use the parent-child map like we would previously. But the parent of the
child is used as a default, not as final. Then we look at the surrounding nodes accessible to the child.
Then we compare sequentially, and if one of the optional nodes has a lower order, i.e was in the parent-child map sooner,
then we use it as the parent instead of the default.
Note, in the current implementation, this comparison is not exhaustive, i.e we are not comparing all the options, we just look for
one option which has a smaller order.

"""

def extractPath (end, nodes, reverse=True):
    currentlyAt = end
    path = [end]
    # To avoid missing better solutions for the parent, 
    # since the parent may have been an alternative and missed 
    # the chanced to check whether it was good enough or not
    
    while currentlyAt in nodes and nodes[currentlyAt][0] != None:
        
        # Line added for update
        parent = currentlyAt
        # Line above added for update

        child = nodes[currentlyAt][0]
        
        left = (parent[0]+1,  parent[1]) 
        right = (parent[0]-1,  parent[1]) 
        top = (parent[0],  parent[1]+1) 
        bottom = (parent[0],  parent[1]-1) 
        if left in nodes:
            if left != path[len(path)-1]:
                if child != left:
                    if nodes[left][1] < nodes[child][1] and left not in path:
                        path.append(left)
                        currentlyAt = left
                        continue
        if right in nodes:
            if right != path[len(path)-1]:
                if child != right:
                    if nodes[right][1] < nodes[child][1] and right not in path:
                        path.append(right)
                        currentlyAt = right
                        continue
        if top in nodes:
            if top != path[len(path)-1]:
                if child != top:
                    if nodes[top][1] < nodes[child][1] and top not in path:
                        path.append(top)
                        currentlyAt = top
                        continue     
        if bottom in nodes:
            if bottom != path[len(path)-1]:
                if child != bottom:
                    if nodes[bottom][1] < nodes[child][1] and bottom not in path:
                        path.append(bottom)
                        currentlyAt = bottom
                        continue                                            
                        
        path.append(child)
        currentlyAt = child

        # Lines below added for update
        if nodes[currentlyAt] == None:
            continue
        
        # look the left, right, top and bottom
        # disregard parent, since it will be one of those nodes
        # we will compare default node with another node that might be of interest if it exists
        
        left = (child[0]+1,  child[1]) 
        right = (child[0]-1,  child[1])
        top = (child[0],  child[1]+1) 
        bottom = (child[0],  child[1]-1) 

        if left in nodes:
            if left != parent:
                if nodes[child][0] != left:
                    if nodes[left][1] < nodes[child][1] and left not in path:
                        path.append(left)
                        currentlyAt = left
                        continue

        if right in nodes:
            if right != parent:
                if nodes[child][0] != right:
                    if nodes[right][1] < nodes[child][1] and right not in path:
                        path.append(right)
                        currentlyAt = right
                        checkParentOptions = True
                        continue

        if top in nodes:
            if top != parent:
                if nodes[child][0] != top:
                    if nodes[top][1] < nodes[child][1] and top not in path:
                        path.append(top)
                        currentlyAt = top
                        continue     

        if bottom in nodes:
            if bottom != parent:
                if nodes[child][0] != bottom:
                    if nodes[bottom][1] < nodes[child][1] and bottom not in path:
                        path.append(bottom)
                        currentlyAt = bottom
                        continue                                

        # Lines above added for update



    return path[::-1] if reverse else path


def extractPathSimple (end, nodes, reverse=True):
    currentlyAt = end
    path = [end]
    while currentlyAt in nodes and nodes[currentlyAt] != None:

        child = nodes[currentlyAt]
        path.append(child)
        currentlyAt = child


    return path[::-1] if reverse else path

def retrieveMergeNode (default, mergeOption):
    if mergeOption:
        return mergeOption
    return default

def getKeysForReserves (v):
    obj = {}
    for a in v:
        obj[a[0]] = None
    return obj

def sendData (socketInformation, currents, traces, reserves, simpleRetrace=True, mergePointAlternative=None):

    if socketInformation == None:
        return

    if 'io' not in socketInformation:
        return

    extractFunc = extractPathSimple if simpleRetrace else extractPath
    path = extractFunc(retrieveMergeNode(currents[0]['value'], mergePointAlternative), traces[0]) + extractFunc(retrieveMergeNode(currents[1]['value'], mergePointAlternative), traces[1], False)
    path = keysVersion(path)
    parentStringEdition = {**keysVersion({**traces[0], **traces[1]}), **keysVersion(getKeysForReserves(reserves[0])), **keysVersion(getKeysForReserves(reserves[1]))}

    if 'sleepDuration' in socketInformation:
        time.sleep(socketInformation['sleepDuration'])

    socketInformation['io'].emit('algorithm_response', 
        { 'meta':
            { 'algorithm': socketInformation['algo'], 'visitSize':len(traces[0]) + len(traces[1]) }, 
            'gridSize':socketInformation.get('gridSize'), 
            'id':socketInformation.get('id'), 
            'path':path, 
            'barriers':socketInformation.get('stringBarriers'), 
            'visited':parentStringEdition
        }
    )
