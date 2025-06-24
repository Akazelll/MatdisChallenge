from collections import namedtuple
import pprint

Graph = namedtuple("Graph", ["nodes", "edges", "is_directed"])


def adjacency_dict(graph: Graph) -> dict:
    adj = {node: set() for node in graph.nodes}
    
    for edge in graph.edges:
        node1, node2 = edge[0], edge[1]
        
        adj[node1].add(node2)
        
        if not graph.is_directed:
            adj[node2].add(node1)
            
    return adj


def adjacency_matrix(graph: Graph) -> list[list[int]]:
    num_nodes = len(graph.nodes)
    
    adj = [[0] * num_nodes for _ in range(num_nodes)]
    
    for edge in graph.edges:
        node1, node2 = edge[0], edge[1]
        
        adj[node1][node2] += 1
        
        if not graph.is_directed:
            adj[node2][node1] += 1
            
    return adj

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=2)

    print("===========================================")
    print("      CONTOH 1: GRAF TIDAK BERARAH         ")
    print("===========================================")
    
    nodes_undirected = range(4)
    edges_undirected = [
        (0, 1), (0, 2),
        (1, 2), (1, 3),
        (2, 3)
    ]

    graph1 = Graph(nodes=nodes_undirected, edges=edges_undirected, is_directed=False)
    
    print("Graf Tidak Berarah:")
    print(f"  Simpul (Nodes): {list(graph1.nodes)}")
    print(f"  Sisi (Edges): {graph1.edges}\n")
   
    adj_list_1 = adjacency_dict(graph1)
    print("--> Representasi Daftar Ketetanggaan (Adjacency List):")
    pp.pprint(adj_list_1)
    
    print("\n" + "-"*43 + "\n")
    
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