from collections import namedtuple

# Mendefinisikan struktur dasar untuk Graf
Graph = namedtuple("Graph", ["nodes", "edges"])

def adjacency_dict(graph):
    """
    Mengembalikan representasi daftar ketetanggaan (adjacency list) dari sebuah graf.
    
    Bentuknya adalah sebuah dictionary di mana keys adalah simpul (node) dan 
    values adalah himpunan (set) dari simpul-simpul yang bertetangga.
    """
    adj = {node: set() for node in graph.nodes}
    for edge in graph.edges:
        node1, node2 = edge[0], edge[1]
        adj[node1].add(node2)
        adj[node2].add(node1) # Baris ini dihapus/diubah untuk graf berarah
    return adj

