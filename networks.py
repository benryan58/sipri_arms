
import json
import networkx as nx
import pandas as pd
from tqdm import tqdm
tqdm.pandas()

def get_edges(transfer):
    u = transfer.sellercod
    v = transfer.buyercod
    attr = transfer[['nrdel', 'odat', 'ldat', 'desig2', 'wcat', 'desc', 'tivdel']].to_dict()

    if isinstance(transfer.delyears, str) and "-" in transfer.delyears:
        # Split out the delivery over the specified years; this splits things
        # roughly evenly, allocating the remainder to the first year, which
        # is an _approximation_for_convenience_ and not necessarily how the 
        # actual deliveries were structured historically.
        delivery_years = [int(x.strip()) for x in transfer.delyears.split("-")]
        delivery_years = list(range(delivery_years[0], delivery_years[1]+1))
        units_per_year = transfer.nrdel // len(delivery_years)

        edges = [()] * len(delivery_years)

        for i in range(len(edges)):
            nrdel = units_per_year + (i==0) * (transfer.nrdel % len(delivery_years))
            tivdel = nrdel * transfer.tivunit
            attr_i = attr.copy()
            attr_i.update({'nrdel': nrdel, 'ldat': delivery_years[i], 'tivdel': tivdel})
            edges[i] = (u, v, attr_i)
    else:
        edges = [(u, v, attr)]

    return edges

def build_network(edge_list):
    g = nx.MultiDiGraph()

    for edge in edge_list:
        g.add_edge(edge[0], edge[1], **edge[2])

    return g


def extract_network(df, verbose=True):
    if verbose:
        all_edges = df.progress_apply(get_edges, axis=1)
    else:
        all_edges = df.apply(get_edges, axis=1)

    g = build_network([item for sublist in all_edges for item in sublist])

    return g

def write_json(g, fpath):
    data = nx.readwrite.json_graph.node_link_data(g)
    json.dump(data, fpath)

    return None

def write_network(g, fpath, type='gexf'):
    if type=='gexf':
        write_func = nx.write_gexf
    elif type=='json':
        write_func = write_json
    elif type=='pickle':
        write_func = nx.write_gpickle
    elif type=='pajek':
        write_func = nx.write_pajek
    elif type=='yaml':
        write_func = nx.write_yaml
    elif type=='gml':
        write_func = nx.write_gml
    elif type=='graphml':
        write_func = nx.write_graphml_lxml

    write_func(g, fpath)

    return None

##################
### WIP parts:
##################

def summarize(g, method='years', **kwargs):
    if method=='years':
        return summarize_years(g)
    elif method=='entities':
        return summarize_entities(g, kwargs)
    elif method=='weapon_type':
        return summarize_weapon_type(g)
    else:
        print("Unrecognized aggregation scheme")
        return g

def summarize_years(g):
    '''
    Aggregate network such that there is one edge per direction per node pair
    per year; i.e., multiple types of transfers are consolidated, resulting in 
    a sum of the `tivdel` value and a dictionary of weapons types/units
    '''
    return g

def summarize_entities(g, year_range='all'):
    '''
    Aggregate network such that there is one edge per node pair for the given 
    year range; 
    '''
    return g

def summarize_weapon_type(g):
    '''
    '''
    return g

def aggregate_geographies(g):
    '''
    '''
    return g