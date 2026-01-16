import copy

import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):

        self.G = nx.DiGraph()
        self._products = []
        self.id_map= {}

        self.best_path= []
        self.best_score = 0


    def get_date_range(self):
        return DAO.get_date_range()


    def get_categories(self):
        return DAO.get_all_categories()

    def build_graph(self, category, date1, date2):
        self.G.clear()

        # creo i nodi (prodotti per categoria)
        self._products = DAO.get_all_products_by_category(category)
        for p in self._products:
            self.id_map[p.id] = p
        self.G.add_nodes_from(self._products)

        # creo gli archi
        all_edges= DAO.get_edges(category, date1, date2, self.id_map)
        for e in all_edges:
            self.G.add_edge(e[0], e[1], weight=e[2])

    def get_graph_details(self):
        return self.G.number_of_nodes(), self.G.number_of_edges()

    def get_best_prodotti(self):
        best_prodotti= []
        for n in self.G.nodes:
            score= 0
            for e_out in self.G.out_edges(n, data=True):
                score += e_out[2]['weight']
            for e_in in self.G.in_edges(n, data=True):
                score -= e_in[2]['weight']

            best_prodotti.append((n, score))

        best_prodotti.sort(reverse=True, key=lambda x: x[1])
        return best_prodotti[0:5] #voglio solo i primi 5

    def get_all_nodes(self):
        nodes= list(self.G.nodes())
        nodes.sort(key=lambda x: x.product_name)
        return nodes


    def get_best_path(self, lung, start, end):
        self.best_path= []
        self.best_score = 0
        parziale= [start]
        self._ricorsione(parziale, lung, start, end)
        return self.best_path, self.best_score

    def _ricorsione(self, parziale, lung, start, end):
        #condizione di terminazione
        if len(parziale) == lung:
            if parziale[-1] == end and self._get_score(parziale) > self.best_score:
                self.best_score= self._get_score(parziale)
                self.best_path= copy.deepcopy(parziale)
            return

        #ciclo di ricorsione
        for n in self.G.successors(parziale[-1]): #per tutti i nodi raggiungibili dal mio ultimo nodo
            #self.G.successors(n) è un metodo di NetworkX per grafi diretti, restituisce tutti i nodi raggiungibili con un arco uscente dal nodo n
            if n not in parziale: #ogni nodo deve comparire al massimo una volta
                parziale.append(n)
                self._ricorsione(parziale, lung, start, end)
                parziale.pop()

    def _get_score(self, parziale): #calcolo il peso totale del cammino
        score = 0
        for i in range(1, len(parziale)): #scorre gli archi
            score += self.G[parziale[i-1]][parziale[i]]['weight']
            '''
            parziale[i-1] nodo di partenza
            parziale[i] nodo di arrivo
            'weight' peso dell'arco tra questi due nodi
            '''
        return score

