import matplotlib.pyplot as plt
import networkx as nx

G=nx.Graph()

# for index,cluster in clusterMap.items():
#   G.add_node(index)
#   for clusterLob in cluster:
#     if clusterLob is not index:# and index in clusterMap[clusterLob]:
#       G.add_edge(index,clusterLob,{'w':abs(3-correlationMap[index][clusterLob])})



G.add_edges_from([("a","c",{'w':1000}),("c","d",{'w':1000})])
pos=nx.spring_layout(G,iterations=50,weight='w',scale=10)
print(pos)
nx.draw(G,pos,with_labels=True)

plt.show()