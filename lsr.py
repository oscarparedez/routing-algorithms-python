
import numpy
import json
S = set() 
G = [] # adjacency matrix

# Positions of nodes in matrix
dicLetters = {
    "A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8,
    "J": 9, "K": 10, "L": 11, "M": 12, "N": 13, "O": 14, "P": 15, "Q": 16, "R": 17,
    "S": 18, "T": 19, "U": 20, "V": 21, "W": 22, "X": 23, "Y": 24, "Z": 25
  }

totalNodes = 0
with open("topologia.txt") as f:
    json_data = json.load(f)
    sizeMatrix = len(json_data['config'])

    for i in json_data['config']:
        lst = [999] * sizeMatrix
        for neighbor in json_data['config'][i]:
            lst[dicLetters[neighbor]] = 1
        G.append(lst)    
print(G)
# exit()
      
source = int(input("give source")) 
destination = int(input("give destination")) 
Q = [] # empty queue
  
for i in range(sizeMatrix):
    Q.append(i)
      
d = [0] * sizeMatrix # initialize d values
pi =[0] * sizeMatrix # initialize pi values
  
for i in range(sizeMatrix):
    if(i == source):
        d[i] = 0
    else:
        d[i] = 999
for i in range(sizeMatrix):
    pi[i] = 9000
S.add(source)
  
# While items still exist in Q
while (len(Q) != 0): 
      
    # Find the minimum distance x from
    # source of all nodes in Q
    x = min(d[q] for q in Q) 
    u = 0
    for q in Q:
        if(d[q] == x):
              
            # Find the node u in Q with minimum 
            # distance x from source 
            u = q 
              
    print(u, "Is the minimum distance")
    Q.remove(u) # removed the minimum vertex
    S.add(u)
    adj = []
    for y in range(sizeMatrix):
          
        # find adjacent vertices to minimum vertex
        if(y != u and G[u][y]!= 999):     
            adj.append(y)
              
     # For each adjacent vertex, perform the update
     # of distance and pi vectors        
    for v in adj:        
        if(d[v] > (d[u] + G[u][v])):
            d[v] = d[u] + G[u][v] 
            pi[v] = u # update adjacents distance and pi
route = []
x = destination

# If destination is source, then pi[x]= 9000. 
if(pi[x] == 9000): 
    print(source)
else:
    # Find the path from destination to source
    while(pi[x]!= 9000): 
        route.append(x)
        x = pi[x]
    route.reverse() 

print(route) # Display the route
print(pi) # Display the path vector
print(d) # Display the distance of each node from source
