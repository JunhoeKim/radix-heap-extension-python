import os, sys
import random

nodeCount = 2000
# arcCountPerNode = 10
maxDistance = 100
lines = []
for i in range(nodeCount):
    # for j in range(random.randint(arcCountPerNode, arcCountPerNode)):
    for j in range(i + 1, nodeCount):
        # dist = random.randint(1, maxDistance) + maxDistance - i
        dist = random.randint(1, maxDistance)
        # dic[str(i) + " " + str(j)] = dist
        # dic[str(j) + " " + str(i))] = dist
        lines.append("a " + str(i+1) + " " + str(j+1) + " " + str(dist))
        lines.append("a " + str(j+1) + " " + str(i+1) + " " + str(dist))
        # print("a", i, random.randint(0, nodeCount), random.randint(1, maxDistance+1))

f = open(sys.argv[1], "w")
for l in lines:
    f.write(l)
    f.write("\n")
