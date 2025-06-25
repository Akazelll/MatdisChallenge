import networkx as nx
import matplotlib.pyplot as plt

def create_graph():
    print("Selamat datang di aplikasi pembuatan graf!")

    # Input jumlah simpul
    num_nodes = int(input("Masukkan jumlah total simpul: "))
    
    # Input derajat masing-masing simpul
    degrees = []
    for i in range(num_nodes):
        degree = int(input(f"Masukkan derajat untuk simpul {i + 1}: "))
        degrees.append(degree)

    print("Apakah Anda ingin menggunakan syarat tertentu? (y/n)")
    use_constraints = input().strip().lower()

    loops = 0
    multi_edges = 0
    if use_constraints == 'y':
        # Input jumlah sisi ganda
        multi_edges = int(input("Masukkan jumlah sisi ganda yang diinginkan: "))

        # Input jumlah loop
        loops = int(input("Masukkan jumlah loop yang diinginkan: "))

    # Buat graf
    G = nx.MultiGraph() if multi_edges > 0 or loops > 0 else nx.Graph()
    G.add_nodes_from(range(1, num_nodes + 1))

    # Tambahkan sisi sesuai derajat
    edges_added = 0
    for node, degree in enumerate(degrees, start=1):
        while degree > 0:
            target = (node if loops > 0 else (node + 1) % num_nodes) + 1
            G.add_edge(node, target)
            degree -= 1
            edges_added += 1

    # Tambahkan sisi ganda jika diminta
    for _ in range(multi_edges):
        G.add_edge(1, 2)

    # Visualisasi graf
    plt.figure(figsize=(8, 6))
    nx.draw(G, with_labels=True, node_color='skyblue', node_size=700, font_weight='bold')
    plt.title("Visualisasi Graf")
    plt.show()

if __name__ == "__main__":
    create_graph()
