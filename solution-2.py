# %%
# IMPORTING NECESSARY LIBRARIES
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import math



# SETTING UP GRAPH SIZE
plt.figure(figsize=(20,10))




# CONSTANTS DECLARATION
CONST_KM_PER_LITRE = 20
CONST_KM_PER_DEG = 110.500




# DATA PREPARATION
df_coor = pd.read_csv('./dataset/dataset_lat-long_jatim-processed.csv') # dataset for positions and coordinates
df_jobs = pd.read_csv('./dataset/Dataset-barang-angkut-processed.csv') # dataset for job list
df_edgelist = pd.read_csv('./dataset/edgelist.csv')




# DATA PROCESSING
# GENERATING SEMI-ACCURATE ROAD MAPPING
def generate_edge_list(df):
    edges = []
    
    for i in range(len(df)):
        edges.append((df['source'][i], df['target'][i]))
    return edges

# COMPUTING EUCLIDIAN DISTANCE BETWEEN TWO COORDINATES POINTS
def compute_euclidian_distance(A, B):
    x1 = A[0] 
    x2 = B[0] 
    y1 = A[1]
    y2 = B[1]

    distance = math.sqrt((abs(x1 - x2) ** 2) + (abs(y1 - y2) ** 2))
    return distance

# CONVERTING LAT-LNG TO KM FOR FUEL CONSIDERATION
def convert_latlong_to_km(value):
    return math.floor(value * CONST_KM_PER_DEG)

# COMPUTING THE MINIMUM SOLAR REQUIRED FOR A GIVEN INITIAL AND GOAL 
def compute_solar_required(initial, goal, G):
    shortest_path = nx.shortest_path(G, source = initial, target =  goal)
    total_distance = 0

    for i in range(len(shortest_path) - 1):
        total_distance += G[shortest_path[i]][shortest_path[i + 1]]
    
    return math.ceil(total_distance / CONST_KM_PER_LITRE)

# GENERATING NODES POSITION FOR ACCURATE MAPPING OF EAST JAVA 
def generate_nodes_position(df):
    pos = {}
    
    for i in range(len(df)):
        pos[df['Daerah'][i]] = (df['Longitude'][i], df['Latitude'][i])

    return pos




# GRAPH PROCESSING

# ADDING WEIGHT TO THE GRAPH FOR SHORTEST_PATH CONSIDERATION
def assign_edge_weight(G, positions):
    for edge in G.edges:
        euc_distance = compute_euclidian_distance(positions[edge[0]], positions[edge[1]])
        converted_distance = convert_latlong_to_km(euc_distance)
        G[edge[0]][edge[1]]['distance'] = converted_distance

# GENERATING EDGE LABEL FOR BETTER VISUAL: REQUIRES EDGE WEIGHT TO BE COMPUTED FIRST
def generate_edge_label(G):
    distance_label = {}

    for edge in G.edges:
        distance_label[edge] = G[edge[0]][edge[1]]['distance']
    
    return distance_label


G = nx.Graph()
edges = generate_edge_list(df_edgelist)
pos = generate_nodes_position(df_coor)
G.add_edges_from(edges)
assign_edge_weight(G, positions=pos)
edge_label = generate_edge_label(G)
nx.draw(G, pos=pos, with_labels=True, font_size=8)
nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_label)

# %%



