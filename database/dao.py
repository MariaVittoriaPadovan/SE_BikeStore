from database.DB_connect import DBConnect

class DAO:
    @staticmethod
    def get_date_range():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT order_date
                    FROM `order` 
                    ORDER BY order_date """
        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last


    @staticmethod
    def get_categorie():
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("Connection failed")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """
                SELECT DISTINCT category_name
                FROM category
                """

        try:
            cursor.execute(query)
            for row in cursor:
                result.append(row['category_name'])

        except Exception as e:
            print("Errore durante la query state")
            result = None
        finally:  # fa quello che scrivo sia che vado nel try sia che vado nell'except
            cursor.close()
            cnx.close()

        return result  # lista di categorie

    @staticmethod
    def get_nodi_per_categoria(category_name):
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("Connection failed")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """
                SELECT id
                FROM category
                WHERE category_name = %s
                """

        try:
            cursor.execute(query, (category_name,))
            for row in cursor:
                result.append(row['id'])

        except Exception as e:
            print("Errore durante la query state")
            result = None
        finally:  # fa quello che scrivo sia che vado nel try sia che vado nell'except
            cursor.close()
            cnx.close()

        return result  # lista id prodotti di una determinata categoria passata come parametro

    @staticmethod
    def prodotti_connessi(data_inizio, data_fine):
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("Connection failed")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """
                SELECT o1.product_id AS p1, o2.product_id AS p2
                FROM order_item o1, order_item o2, order o
                WHERE o1.product_id <> o2.product_id 
                      AND COUNT(o1.product_id) > 0 AND COUNT(o2.product_id) > 0
                      AND o.id = o1.order_id AND o.id = o2.order_id
                      AND o.order_date BETWEEN %s AND %s
                """

        try:
            cursor.execute(query, (data_inizio, data_fine, ))
            for row in cursor:
                result.append(row['id'])

        except Exception as e:
            print("Errore durante la query state")
            result = None
        finally:  # fa quello che scrivo sia che vado nel try sia che vado nell'except
            cursor.close()
            cnx.close()

        return result

