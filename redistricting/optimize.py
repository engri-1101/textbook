import numpy as np
from scipy.stats import t
from ortools.linear_solver import pywraplp as OR

def make_bdm(leaf_nodes, n_blocks=None):
    """
    Generate the block district matrix given by a sample trees leaf nodes.
    Args:
        leaf_nodes: SHPNode list, output of the generation routine
        n_blocks: (int) number of blocks in the state

    Returns: (np.array) n x d matrix where a_ij = 1 when block i appears in district j.

    """
    districts = [d['area'] for d in leaf_nodes]
    if n_blocks is None:
        n_blocks = max([max(d) for d in districts]) + 1
    block_district_matrix = np.zeros((n_blocks, len(districts)))
    for ix, d in enumerate(districts):
        block_district_matrix[d, ix] = 1
    return block_district_matrix


def make_master(k, block_district_matrix, costs,
                relax=False, opt_type='abs_val', solver='CBC'):
    """
    Constructs the master selection problem.
    Args:
        k: (int) the number of districts in a plan
        block_district_matrix: (np.array) binary matrix a_ij = 1 if block i is in district j
        costs: (np.array) cost coefficients of districts
        relax: (bool) construct relaxed linear master problem
        opt_type: (str) {"minimize", "maximize", "abs_val"

    Returns: (Gurobi.model, (dict) of master selection problem variables)

    """
    n_blocks, n_columns = block_district_matrix.shape
    
    # define the model
    if solver=='CBC':
        m = OR.Solver('master', OR.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    elif solver=='gurobi':
        m = OR.Solver('master', OR.Solver.GUROBI_MIXED_INTEGER_PROGRAMMING)
    else:
        raise ValueError('Invalid solver')

    # decision variables
    x = {} # x_i is 1 iff district i is used, 0 otherwise
    D = range(n_columns)
    for j in D:
        if relax:
            x[j] = m.NumVar(0, 1, name="x(%s)" % j)
        else:
            x[j] = m.IntVar(0, 1, name="x(%s)" % j)

    # objective function
    if opt_type == 'minimize':
        m.Minimize(sum(costs[j] * x[j] for j in D))
    elif opt_type == 'maximize':
        m.Maximize(sum(costs[j] * x[j] for j in D))
    elif opt_type == 'abs_val':
        w = m.NumVar(-k, k, name="w")
        m.Add(sum(costs[j] * x[j] for j in D) <= w, name='absval_pos')
        m.Add(sum(costs[j] * x[j] for j in D) >= -w, name='absval_neg')
        m.Minimize(w)
    else:
        raise ValueError('Invalid optimization type')

    # subject to: each census tract appears in exactly one district
    for i in range(n_blocks):    
        m.Add(sum(x[j] * block_district_matrix[i, j] for j in D) == 1)

    # subject to: k total districts
    m.Add(sum(x[j] for j in D) == k)

    return m,x


def efficiency_gap_coefficients(district_df, state_vote_share):
    """

    Args:
        district_df: (pd.DataFrame) selected district statistics
            (requires "mean", "std_dev", "DoF")
        state_vote_share: (float) average state vote share across historical elections.

    Returns: (np.array) of efficiency gap cost coefficients

    """
    mean = district_df['mean'].values
    std_dev = district_df['std_dev'].values
    DoF = district_df['DoF'].values
    expected_seats = 1 - t.cdf(.5, DoF, mean, std_dev)
    # https://www.brennancenter.org/sites/default/files/legal-work/How_the_Efficiency_Gap_Standard_Works.pdf
    # Efficiency Gap = (Seat Margin – 50%) – 2 (Vote Margin – 50%)
    return (expected_seats - .5) - 2 * (state_vote_share - .5)


def make_root_partition_to_leaf_map(leaf_nodes, internal_nodes):
    """
    Shard the sample tree leaf nodes by root partition.

    Args:
        leaf_nodes: (SHPNode list) with node capacity equal to 1 (has no child nodes).
        internal_nodes: (SHPNode list) with node capacity >1 (has child nodes).

    Returns: (dict) {root partition index: array of leaf node indices}

    """
    def add_children(node, root_partition_id):
        if node['n_districts'] > 1:
            for partition in node['children_ids']:
                for child in partition:
                    add_children(node_dict[child], root_partition_id)
        else:
            node_to_root_partition[id_to_ix[node['id']]] = root_partition_id

    # Create mapping from leaf ix to root partition ix
    node_to_root_partition = {}
    node_dict = {n['id']: n for n in internal_nodes + leaf_nodes}
    id_to_ix = {n['id']: ix for ix, n in enumerate(leaf_nodes)}
    root = internal_nodes[0]
    for ix, root_partition in enumerate(root['children_ids']):
        for child in root_partition:
            add_children(node_dict[child], ix)

    # Create inverse mapping
    partition_map = {}
    for node_ix, partition_ix in node_to_root_partition.items():
        try:
            partition_map[partition_ix].append(node_ix)
        except KeyError:
            partition_map[partition_ix] = [node_ix]
    partition_map = {ix: np.array(leaf_list) for ix, leaf_list in partition_map.items()}

    return partition_map
