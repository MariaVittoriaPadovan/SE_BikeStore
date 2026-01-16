import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        self.lista_categorie= []
        self.lista_prodotti_per_categoria= []

        self.G = nx.Graph()
        self._nodes = []
        self._edges = []

        self.load_categorie()

    def get_date_range(self):
        return DAO.get_date_range()

    def load_categorie(self):
        self.lista_categorie = DAO.get_categorie()

    def build_graph(self, category_name):
        self.G.clear()

        self._nodes = []
        self._edges = []

        # creo i nodi (prodotti per categoria)
        self.lista_prodotti_per_categoria = DAO.get_nodi_per_categoria(category_name)
        for p in self.lista_prodotti_per_categoria:
            self._nodes.append(p)
        self.G.add_nodes_from(self._nodes)

        # creo gli archi
        tmp_edges = DAO.get_all_weighted_neigh(year, shape)  # ottengo tutti gli archi
        self._edges.clear()
        for e in tmp_edges:
            self._edges.append((self.id_map[e[0]], self.id_map[e[1]], e[2]))
            '''
            self.id_map[e[0]] = oggetto stato1 (dove e[0]= row['st1'] è l'id dello stato1)
            self.id_map[e[1]] = oggetto stato2 (dove e[1]= row['st2'] è l'id dello stato2) 
            e[2] = N (è il peso di ogni arco)
            '''

        self.G.add_weighted_edges_from(self._edges)  # creo gli archi dandogli già il peso