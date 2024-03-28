import networkx as nx
from collections import deque
import pickle
from typing import Tuple, Set, Dict
import os
import pandas as pd


db_folder = r'//10.120.148.123/hwDataLakeWWIP_s3/HPW-TOOLS/Tracing-tool-db'
network_parquet = os.path.join(db_folder, 'nnn_link_gdf.parquet')


def _map_unitID_MHNUM() -> pd.DataFrame:

    # Read in the data
    man_df = pd.read_parquet(os.path.join(db_folder, 'Manholes.parquet'))
    columns = ['MH_NUMBER', 'UNIT_ID']
    MH_UNITID_map = man_df[columns]

    # Drop any rows with missing values
    MH_UNITID_map_copy = MH_UNITID_map.dropna()

    return MH_UNITID_map_copy


def tracing_with_node_short_distance(graph: nx.Graph, start_node: str, direction: str, distance: int = None) -> Tuple[
    Dict[str, float], pd.DataFrame]:
    """
    Find all links in the specified direction for a given node using BFS.
    :param graph: directed graph of the network
    :param start_node: the node from which to start the search
    :param direction: the direction of the search, either 'upstream' or 'downstream'
    :param distance: the maximum distance to search
    :return: two dictionaries with nodes and edges with their distances from the start node
    """
    print('Tracing has started...')
    print('Please be patient, this may take a while if the search distance is large.')
    queue = deque([(start_node, 0)])
    visited = {start_node: 0}
    edges = pd.DataFrame(columns=['edgeID', 'distance', 'linkID'])

    while queue:
        current_node, current_distance = queue.popleft()
        if distance is not None and current_distance > distance:
            continue
        if direction == 'upstream':
            neighbors = graph.pred[current_node]
        elif direction == 'downstream':
            neighbors = graph.succ[current_node]
        else:
            raise ValueError('Invalid direction. Must be "upstream" or "downstream"')

        for neighbor in neighbors:
            if neighbor not in visited:
                edge = (neighbor, current_node) if direction == 'upstream' else (current_node, neighbor)
                edge_distance = current_distance + graph.edges[edge]['Length']
                visited[neighbor] = edge_distance
                link_id = graph.edges[edge]['linkID']
                if distance is None or edge_distance <= distance:
                    edges.loc[len(edges)] = {'edgeID': edge, 'distance': edge_distance, 'linkID': link_id}
                    queue.append((neighbor, edge_distance))
                else:
                    continue

    return visited, edges


def tracing_with_node(graph: nx.Graph, start_node, direction: str, distance: int = None) -> Tuple[Dict[str, float], pd.DataFrame]:
    """
    Find all links in the specified direction for a given node using BFS.
    :param graph:
    :param start_node:
    :param direction:
    :param distance:
    :return:
    """

    unitID_MHNUM_dict = _map_unitID_MHNUM()

    #convert start_node from ufid to mh_num
    if start_node in unitID_MHNUM_dict['UNIT_ID'].values:
        start_node = unitID_MHNUM_dict.set_index('UNIT_ID')['MH_NUMBER'].to_dict()[start_node]
    elif start_node in unitID_MHNUM_dict['MH_NUMBER'].values:
        pass
    else:
        raise ValueError(f'Node {start_node} not found in the graph')

    # network_parquet_gdf['us_Node'] = network_parquet_gdf['us_Node'].map(map_dict.set_index('MH_NUMBER')['UNIT_ID'].to_dict())
    # network_parquet_gdf['ds_Node'] = network_parquet_gdf['ds_Node'].map(map_dict.set_index('MH_NUMBER')['UNIT_ID'].to_dict())

    if distance:
        if distance < 2000:
            return tracing_with_node_short_distance(graph, start_node, direction, distance)

    # Reverse the graph if tracing upstream
    if direction == 'upstream':
        graph = graph.reverse()

    # Perform BFS in the specified direction
    bfs_edges = list(nx.bfs_edges(graph, start_node))
    node_distances = nx.single_source_dijkstra_path_length(graph, start_node, weight='Length')

    # Filter edges based on distance condition
    if distance is not None:
        bfs_edges = [edge for edge in bfs_edges if node_distances[edge[1]] <= distance]
        node_distances = {node: distance_node for node, distance_node in node_distances.items() if distance_node <= distance}

    edges_df = pd.DataFrame([(edge, node_distances[edge[1]], graph.edges[edge]['linkID']) for edge in bfs_edges],
                            columns=['edgeID', 'distance', 'linkID'])

    # Reverse the edges if tracing upstream
    if direction == 'upstream':
        edges_df['edgeID'] = edges_df['edgeID'].apply(lambda x: (x[1], x[0]))

    # convert nodes_instances to ufid
    unitID_MHNUM_dict = unitID_MHNUM_dict.set_index('MH_NUMBER')['UNIT_ID'].to_dict()

    # Mark nodes that don't exist in unitID_MHNUM_dict as "non"
    node_distances_marked = {node: distance if node in unitID_MHNUM_dict else 'nan' for node, distance in
                             node_distances.items()}

    # Remove nodes marked as "non"
    node_distances_filtered = {node: distance for node, distance in node_distances_marked.items() if distance != 'nan'}

    # convert nodes_instances to ufid
    node_distances_filtered = {unitID_MHNUM_dict[node]: distance for node, distance in node_distances_filtered.items()}


    return node_distances_filtered, edges_df

def tracing_with_link(graph: nx.Graph, start_link, direction: str, distance: int = None) -> Tuple[
    Dict[str, float], pd.DataFrame]:

    start_link = [edge for edge in graph.edges if graph.edges[edge]['linkID'] == start_link]
    if not start_link:
        raise ValueError(f'Link {start_link} not found in the graph')

    start_link = start_link[0]
    start_node = start_link[0] if direction == 'upstream' else start_link[1]
    return tracing_with_node(graph, start_node, direction, distance)


def tracing_between_nodes(graph: nx.Graph, start, end) -> Tuple[
    Dict[str, float], pd.DataFrame]:

    unitID_MHNUM_dict = _map_unitID_MHNUM()

    #convert start_node from ufid to mh_num
    if start in unitID_MHNUM_dict['UNIT_ID'].values:
        start = unitID_MHNUM_dict.set_index('UNIT_ID')['MH_NUMBER'].to_dict()[start]
    elif start in unitID_MHNUM_dict['MH_NUMBER'].values:
        pass
    else:
        raise ValueError(f'Node {start} not found in the graph')

    #convert end_node from ufid to mh_num
    if end in unitID_MHNUM_dict['UNIT_ID'].values:
        end = unitID_MHNUM_dict.set_index('UNIT_ID')['MH_NUMBER'].to_dict()[end]
    elif end in unitID_MHNUM_dict['MH_NUMBER'].values:
        pass
    else:
        raise ValueError(f'Node {end} not found in the graph')


    # Get all simple paths between start_node and end_node
    all_paths = list(nx.all_simple_paths(graph, start, end))

    if not all_paths:
        raise ValueError(f'No paths found between {start} and {end}')

    # Initialize a list to hold all edges in all paths
    all_edges = pd.DataFrame(columns=['edgeID', 'distance', 'linkID'])
    all_nodes = {}

    # Iterate over all paths to extract the edges and find the distance from the start_node
    for path in all_paths:
        distance = 0
        for i in range(len(path) - 1):
            edge = (path[i], path[i + 1])
            all_nodes[path[i]] = distance
            distance += graph.edges[edge]['Length']
            link_id = graph.edges[edge]['linkID']
            all_nodes[path[i + 1]] = distance
            all_edges.loc[len(all_edges)] = {'edgeID': edge, 'distance': distance, 'linkID': link_id}

    return all_nodes, all_edges


def tracing_between_links(graph: nx.Graph, start_link, end_link) -> Tuple[
    Dict[str, float], pd.DataFrame]:

    start_link = [edge for edge in graph.edges if graph.edges[edge]['linkID'] == start_link]
    if not start_link:
        raise ValueError(f'Link {start_link} not found in the graph')
    end_link = [edge for edge in graph.edges if graph.edges[edge]['linkID'] == end_link]
    if not end_link:
        raise ValueError(f'Link {end_link} not found in the graph')

    start_link = start_link[0]
    end_link = end_link[0]

    start_node = start_link[0]
    end_node = end_link[1]
    return tracing_between_nodes(graph, start_node, end_node)





