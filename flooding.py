import networkx as nx
import matplotlib.pyplot as plt
import json
import numpy as np
import pandas as pd

visitedNodes = []

G = nx.Graph()
totalNodes = 0
with open("topologia.txt") as f:
    json_data = json.load(f)

    for i in json_data['config']:
        totalNodes+=1
        head = i
        for neighbor in json_data['config'][i]:
            G.add_edge(head, neighbor, weight = 1)

translate = {
    "A": "a@alumchat.fun",
    "B": "b@alumchat.fun",
    "C": "c@alumchat.fun",
    "D": "d@alumchat.fun",
    "E": "e@alumchat.fun",
    "F": "f@alumchat.fun",
    }

currentNode = "A"
visitedNodes.append(currentNode)
while len(visitedNodes) != totalNodes:
    for m in visitedNodes:
        currentNode = m
        for n in G.neighbors(currentNode):
            # print(n)
            if n not in visitedNodes:
                visitedNodes.append(n)
                #send message
                # print('66666', currentNode, n)

pos=nx.spring_layout(G)
nx.draw_networkx(G,pos)
labels = nx.get_edge_attributes(G,'weight')
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
plt.savefig('filename.png')

df = nx.to_pandas_edgelist(G, nodelist=visitedNodes)
print(df)