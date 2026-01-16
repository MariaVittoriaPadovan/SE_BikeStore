from UI.view import View
from model.model import Model
import flet as ft
import datetime

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model


    def set_dates(self):
        first, last = self._model.get_date_range()

        self._view.dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view.dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp2.current_date = datetime.date(last.year, last.month, last.day)


    def populate_dd_category(self):
        categories = self._model.get_categories()

        # popolo dropdown di categorie
        for c in categories:
            self._view.dd_category.options.append(ft.dropdown.Option(key=c.category_name, data=c))

        self._view.update()

    def choice_category(self, e): # e è l'evento
        # e.control è il DropDown
        selected_key= e.control.value #salvo la chiave dell'opzione scelta

        for option in e.control.options: #ciclo su tutte le opzioni del DropDown
            if option.key == selected_key: #quando trovo la chiave dell'opzione selezionata
                self.dd_category_value = option.data #salvo il valore reale associato all'opzione del dd
                break

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """
        # TODO
        self._model.build_graph(self.dd_category_value, self._view.dp1.value, self._view.dp2.value)

        n_nodes, n_edges = self._model.get_graph_details()

        self._view.txt_risultato.controls.clear()
        self._view.txt_risultato.controls.append(ft.Text("Date selezionate:"))
        self._view.txt_risultato.controls.append(ft.Text(f"Start date: {self._view.dp1.value.date()}"))
        self._view.txt_risultato.controls.append(ft.Text(f"End date: {self._view.dp2.value.date()}"))
        self._view.txt_risultato.controls.append(ft.Text("Grafo correttamente creato:"))
        self._view.txt_risultato.controls.append(ft.Text(f"Numero di nodi: {n_nodes}"))
        self._view.txt_risultato.controls.append(ft.Text(f"Numero di archi: {n_edges}"))

        self._populate_dd_products()
        self._view.update()

    def _populate_dd_products(self):
        all_nodes= self._model.get_all_nodes()

        self._view.dd_prodotto_iniziale.options= [ft.dropdown.Option(key=c.product_name, data=c) for c in all_nodes]
        self._view.dd_prodotto_finale.options = [ft.dropdown.Option(key=c.product_name, data=c) for c in all_nodes]

        self._view.update()

    def choice_prod_start(self, e):
        selected_key= e.control.value
        for option in e.control.options:
            if option.key == selected_key:
                self.dd_prod_start_value = option.data
                break

    def choice_prod_end(self, e):
        selected_key = e.control.value
        for option in e.control.options:
            if option.key == selected_key:
                self.dd_prod_end_value = option.data
                break

    def handle_best_prodotti(self, e):
        """ Handler per gestire la ricerca dei prodotti migliori """
        # TODO
        best_prodotti= self._model.get_best_prodotti()

        self._view.txt_risultato.controls.append(ft.Text(f"\n I cinque prodotti più venduti sono:"))
        for p in best_prodotti:
            self._view.txt_risultato.controls.append(ft.Text(f"{p[0].product_name} with score {p[1]}"))

        self._view.update()

    def handle_cerca_cammino(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO
