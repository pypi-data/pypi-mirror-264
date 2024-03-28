import pickle
import networkx as nx
import pandas as pd
import os
db_folder = r'//10.120.148.123/hwDataLakeWWIP_s3/HPW-TOOLS/Tracing-tool-db'
network_parquet = os.path.join(db_folder, 'nnn_link_gdf.parquet')

edge_attr = ['linkID', 'parcels', 'Length', 'pipeDia']


def load_graphs():
    # make src folder if it does not exist
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)

    if os.path.exists(os.path.join(db_folder, 'sewer_network_graph.pickle')) and os.path.exists(
            os.path.join(db_folder, 'reversed_sewer_network_graph.pickle')):
        G, reversed_graph = load_graphs_from_pickle()
    else:
        make_graphs_pickle(network_parquet, edge_attr)
        G, reversed_graph = load_graphs_from_pickle()

    return G, reversed_graph


def load_graphs_from_pickle():
    with open(os.path.join(db_folder, 'sewer_network_graph.pickle'), 'rb') as handle:
        G = pickle.load(handle)
    with open(os.path.join(db_folder, 'reversed_sewer_network_graph.pickle'), 'rb') as handle:
        reversed_graph = pickle.load(handle)
    return G, reversed_graph




def make_graphs_pickle(network_parquet: str, edge_attr: list):
    # read the pickle file
    network_parquet_gdf = pd.read_parquet(network_parquet)

    # in column 'us_Node' and 'ds_Node', the data type is object, need to change to string
    # convert the data type to string
    network_parquet_gdf['us_Node'] = network_parquet_gdf['us_Node'].astype(str)
    network_parquet_gdf['ds_Node'] = network_parquet_gdf['ds_Node'].astype(str)


    # create a directed graph from the sewer network
    G = nx.from_pandas_edgelist(network_parquet_gdf, 'us_Node', 'ds_Node', edge_attr=edge_attr,
                                create_using=nx.DiGraph())

    # save G into a pickle file
    with open(os.path.join(db_folder, 'sewer_network_graph.pickle'), 'wb') as handle:
        pickle.dump(G, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # reverse the graph for upstream traversal
    reversed_graph = G.reverse()

    # save reversed_graph into a pickle file
    with open(os.path.join(db_folder, 'reversed_sewer_network_graph.pickle'), 'wb') as handle:
        pickle.dump(reversed_graph, handle, protocol=pickle.HIGHEST_PROTOCOL)

#
