from collections import namedtuple
import pprint

Graph = namedtuple("Graph", ["nodes", "edges", "is_directed"])


def adjacency_dict(graph: Graph) -> dict:
    """
    Membuat representasi daftar ketetanggaan (adjacency list) dari sebuah graf.

    Args:
        graph: Objek Graph yang berisi nodes, edges, dan is_directed.

    Returns:
        Sebuah dictionary di mana setiap kunci adalah simpul (node) dan nilainya 
        adalah sebuah set berisi simpul-simpul yang bertetangga dengannya.
    """
    # Inisialisasi dictionary dengan semua simpul sebagai kunci dan set kosong sebagai nilai.
    adj = {node: set() for node in graph.nodes}
    
    for edge in graph.edges:
        node1, node2 = edge[0], edge[1]
        
        # Menambahkan hubungan dari node1 ke node2
        adj[node1].add(node2)
        
        # Jika graf tidak berarah, tambahkan juga hubungan sebaliknya (dari node2 ke node1)
        if not graph.is_directed:
            adj[node2].add(node1)
            
    return adj


def adjacency_matrix(graph: Graph) -> list[list[int]]:
    """
    Membuat representasi matriks ketetanggaan (adjacency matrix) dari sebuah graf.

    PENTING: Fungsi ini mengasumsikan bahwa simpul (nodes) adalah integer
             yang berurutan dari 0 hingga (jumlah simpul - 1).

    Args:
        graph: Objek Graph yang berisi nodes, edges, dan is_directed.

    Returns:
        Sebuah list of lists (matriks) di mana adj[i][j] menunjukkan jumlah
        sisi yang menghubungkan simpul i dan simpul j.
    """
    num_nodes = len(graph.nodes)
    
    # Inisialisasi matriks N x N dengan nilai nol, di mana N adalah jumlah simpul.
    adj = [[0] * num_nodes for _ in range(num_nodes)]
    
    for edge in graph.edges:
        node1, node2 = edge[0], edge[1]
        
        # Menambahkan penanda adanya sisi dari node1 ke node2
        adj[node1][node2] += 1
        
        # Jika graf tidak berarah, tambahkan juga penanda untuk arah sebaliknya.
        if not graph.is_directed:
            adj[node2][node1] += 1
            
    return adj

# --- Contoh Penggunaan ---
if __name__ == "__main__":
    # Inisialisasi pretty printer untuk output yang lebih baik
    pp = pprint.PrettyPrinter(indent=2)

    print("===========================================")
    print("      CONTOH 1: GRAF TIDAK BERARAH         ")
    print("===========================================")
    
    # Definisikan simpul-simpul dan sisi-sisi untuk graf tidak berarah
    # Simpul direpresentasikan sebagai integer agar kompatibel dengan adjacency_matrix
    nodes_undirected = range(4) # Simpul 0, 1, 2, 3
    edges_undirected = [
        (0, 1), (0, 2),
        (1, 2), (1, 3),
        (2, 3)
    ]
    
    # Buat objek graf tidak berarah
    graph1 = Graph(nodes=nodes_undirected, edges=edges_undirected, is_directed=False)
    
    print("Graf Tidak Berarah:")
    print(f"  Simpul (Nodes): {list(graph1.nodes)}")
    print(f"  Sisi (Edges): {graph1.edges}\n")
    
    # Hasilkan dan cetak daftar ketetanggaan
    adj_list_1 = adjacency_dict(graph1)
    print("--> Representasi Daftar Ketetanggaan (Adjacency List):")
    pp.pprint(adj_list_1)
    
    print("\n" + "-"*43 + "\n")
    
    # Hasilkan dan cetak matriks ketetanggaan
    adj_mat_1 = adjacency_matrix(graph1)
    print("--> Representasi Matriks Ketetanggaan (Adjacency Matrix):")
    pp.pprint(adj_mat_1)
    
    print("\n" * 2)

    print("===========================================")
    print("        CONTOH 2: GRAF BERARAH             ")
    print("===========================================")
    
    # Definisikan simpul-simpul dan sisi-sisi untuk graf berarah
    nodes_directed = range(4) # Simpul 0, 1, 2, 3
    edges_directed = [
        (0, 1), (1, 2), # 0 -> 1 -> 2
        (2, 0),         # 2 -> 0 (membentuk siklus)
        (3, 0), (3, 1)  # 3 -> 0 dan 3 -> 1
    ]

    # Buat objek graf berarah
    graph2 = Graph(nodes=nodes_directed, edges=edges_directed, is_directed=True)
    
    print("Graf Berarah:")
    print(f"  Simpul (Nodes): {list(graph2.nodes)}")
    print(f"  Sisi (Edges): {graph2.edges}\n")

    # Hasilkan dan cetak daftar ketetanggaan
    adj_list_2 = adjacency_dict(graph2)
    print("--> Representasi Daftar Ketetanggaan (Adjacency List):")
    pp.pprint(adj_list_2)
    
    print("\n" + "-"*43 + "\n")

    # Hasilkan dan cetak matriks ketetanggaan
    adj_mat_2 = adjacency_matrix(graph2)
    print("--> Representasi Matriks Ketetanggaan (Adjacency Matrix):")
    pp.pprint(adj_mat_2)