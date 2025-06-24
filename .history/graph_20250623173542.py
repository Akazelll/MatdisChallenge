from collections import namedtuple

# Mendefinisikan struktur dasar untuk Graf
# Versi update dari namedtuple untuk mendukung graf berarah
Graph = namedtuple("Graph", ["nodes", "edges", "is_directed"])

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

def adjacency_matrix(graph):
    """
    Mengembalikan representasi matriks ketetanggaan (adjacency matrix) dari sebuah graf.
    
    Bentuknya adalah list of lists, di mana adj[i][j] menunjukkan jumlah
    sisi antara simpul i dan simpul j.
    """
    # Mengasumsikan simpul adalah integer dari 0 hingga jumlah simpul - 1
    num_nodes = len(graph.nodes)
    adj = [[0] * num_nodes for _ in range(num_nodes)]
    
    for edge in graph.edges:
        node1, node2 = edge[0], edge[1]
        adj[node1][node2] += 1
        adj[node2][node1] += 1 # Baris ini dihapus/diubah untuk graf berarah
        
    return adj

