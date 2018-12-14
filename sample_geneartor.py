import os, sys
import random

nodeCount = 50
# arcCountPerNode = 10
maxDistance = 50

for i in range(nodeCount):
    # for j in range(random.randint(arcCountPerNode, arcCountPerNode)):
    for j in range(i + 1, nodeCount):
        dist = random.randint(1, maxDistance) + maxDistance - i
        # dic[str(i) + " " + str(j)] = dist
        # dic[str(j) + " " + str(i))] = dist
        print("a", i+1, j+1, dist)
        print("a", j+1, i+1, dist)
        # print("a", i, random.randint(0, nodeCount), random.randint(1, maxDistance+1))

