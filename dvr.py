import networkx as nx
import matplotlib.pyplot as plt
import json
import numpy as np
import pandas as pd
import random
from operator import attrgetter

G = nx.Graph()

with open("topologia.txt") as f:
    json_data = json.load(f)

    for i in json_data['config']:
        head = i
        for neighbor in json_data['config'][i]:
            randomWeight = random.randint(1, 3)
            G.add_edge(head, neighbor, weight = randomWeight)

currentNode = "A"
targetNode = "E"
bellmanFordResults = []
for n in G.neighbors(currentNode):
    weight = G.get_edge_data(currentNode, n)['weight']
    neighborShortestPath = nx.shortest_path(G, n, targetNode)
    # print(neighborShortestPath)
    sum = 0
    for edge in range(len(neighborShortestPath) - 1):
        sum += G.get_edge_data(neighborShortestPath[edge], neighborShortestPath[edge + 1])['weight']

    bellmanFordResults.append({"source": n, "target": targetNode, "result": weight + sum, "path": neighborShortestPath})

# print(bellmanFordResults)

print(min(bellmanFordResults, key=lambda x: x['result']))

pos=nx.spring_layout(G)
nx.draw_networkx(G,pos)
labels = nx.get_edge_attributes(G,'weight')
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
plt.savefig('dvr.png')
