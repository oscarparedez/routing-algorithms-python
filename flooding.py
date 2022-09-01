import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def flooding(initialNode, totalNodes, G):
    visitedNodes = []

    visitedNodes.append(initialNode)
    while len(visitedNodes) != totalNodes:
        for m in visitedNodes:
            initialNode = m
            for n in G.neighbors(initialNode):
                # print(n)
                if n not in visitedNodes:
                    visitedNodes.append(n)
                    #send message
                    # print('66666', initialNode, n)
    # pos=nx.spring_layout(G)
    # nx.draw_networkx(G,pos)
    # labels = nx.get_edge_attributes(G,'weight')
    # nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    # plt.savefig('filename.png')

    # df = nx.to_pandas_edgelist(G, nodelist=visitedNodes)
    # print(df)
    return visitedNodes

    