import osmnx as ox

G = ox.graph_from_place('София, Болгария', network_type='drive')
ox.save_graphml(G, 'sofia_road_network.graphml')