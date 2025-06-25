import networkx as nx
import matplotlib.pyplot as plt
import random

def validate_degrees(degrees, num_nodes, allow_loops=False):
    """
    Validasi derajat simpul.
    - Jumlah total derajat harus genap.
    - Derajat simpul tidak boleh lebih besar dari jumlah simpul lain (kecuali loop diizinkan).
    """
    if sum(degrees) % 2 != 0:
        print("Jumlah total derajat harus genap. Silakan periksa kembali input Anda.")
        return False
    if not allow_loops and any(degree > num_nodes - 1 for degree in degrees):
        print("Derajat simpul tidak boleh lebih besar dari jumlah simpul lain tanpa loop. Silakan periksa kembali input Anda.")
        return False
    return True

def create_graph():
    print("Selamat datang di aplikasi pembuatan graf!")

    # Input jumlah simpul
    num_nodes = int(input("Masukkan jumlah total simpul: "))
    
    # Input derajat masing-masing simpul
    while True:
        degrees = []
        for i in range(num_nodes):
            degree = int(input(f"Masukkan derajat untuk simpul {i + 1}: "))
            degrees.append(degree)
        
        # Validasi derajat
        print("Apakah Anda ingin menggunakan syarat tertentu (loop/sisi ganda)? (y/n)")
        use_constraints = input().strip().lower()
        allow_loops = False
        if use_constraints == 'y':
            allow_loops = True

        if validate_degrees(degrees, num_nodes, allow_loops=allow_loops):
            break

    multi_edges = 0
    loops = 0
    if use_constraints == 'y':
        # Input jumlah sisi ganda
        multi_edges = int(input("Masukkan jumlah sisi ganda yang diinginkan: "))
        # Input jumlah loop
        loops = int(input("Masukkan jumlah loop yang diinginkan: "))

    # Buat graf
    G = nx.MultiGraph() if multi_edges > 0 or loops > 0 else nx.Graph()
    G.add_nodes_from(range(1, num_nodes + 1))

    # Tambahkan sisi sesuai derajat
    remaining_degrees = degrees[:]
    while sum(remaining_degrees) > 0:
        available_nodes = [i for i, degree in enumerate(remaining_degrees, start=1) if degree > 0]
        if len(available_nodes) < 2 and loops == 0:
            print("Tidak dapat membentuk graf sesuai derajat yang diberikan.")
            return

        node1 = random.choice(available_nodes)
        node2 = random.choice(available_nodes) if loops > 0 else random.choice([n for n in available_nodes if n != node1])
        
        G.add_edge(node1, node2)
        remaining_degrees[node1 - 1] -= 1
        remaining_degrees[node2 - 1] -= 1

    # Tambahkan sisi ganda jika diminta
    for _ in range(multi_edges):
        G.add_edge(1, 2)

    # Tambahkan loop jika diminta
    for _ in range(loops):
        G.add_edge(1, 1)

    # Visualisasi graf
    plt.figure(figsize=(8, 6))
    nx.draw(G, with_labels=True, node_color='skyblue', node_size=700, font_weight='bold')
    plt.title("Visualisasi Graf")
    plt.show()

if __name__ == "__main__":
    create_graph()
