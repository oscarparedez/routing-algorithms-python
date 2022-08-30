
S = set() 
G = [] # adjacency matrix
  
# give input matrix
for i in range(4): 
    listo = [0, 0, 0, 0]
      
    for j in range(4):
        listo[j] = int(input("give input"))
    G.append(listo)
      
source = int(input("give source")) 
destination = int(input("give destination")) 
Q = [] # empty queue
  
for i in range(4):
    Q.append(i)
      
d =[0, 0, 0, 0] # initialize d values
pi =[0, 0, 0, 0] # initialize pi values
  
for i in range(4):
    if(i == source):
        d[i] = 0
    else:
        d[i] = 999
for i in range(4):
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
    for y in range(4):
          
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
