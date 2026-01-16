from database.DB_connect import DBConnect
from model.category import Category
from model.product import Product

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
    def get_all_categories():
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("Connection failed")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """
                SELECT *
                FROM category
                """

        try:
            cursor.execute(query)
            for row in cursor:
                result.append(Category(**row))

        except Exception as e:
            print("Errore durante la query category")
            result = None
        finally:  # fa quello che scrivo sia che vado nel try sia che vado nell'except
            cursor.close()
            cnx.close()

        return result  # lista di oggetti categorie

    @staticmethod
    def get_all_products_by_category(cat):
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("Connection failed")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """
                SELECT *
                FROM product
                WHERE category_id = %s
                """

        try:
            cursor.execute(query, (cat.id,))
            for row in cursor:
                result.append(Product(**row))

        except Exception as e:
            print("Errore durante la query product")
            result = None
        finally:  # fa quello che scrivo sia che vado nel try sia che vado nell'except
            cursor.close()
            cnx.close()

        return result  # lista di oggetti prodotto di una determinata categoria passata come parametro

    @staticmethod
    def get_edges(c, d1, d2, id_map): #c= categoria, d1= data inizio, d2= data fine
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("Connection failed")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """
                SELECT t1.id AS n1, t2.id AS n2, t1.num+t2.num AS peso
                FROM (SELECT p.id, count(*) AS num
                      FROM product p, order_item oi, `order` o
                      WHERE p.id = oi.product_id AND oi.order_id = o.id
                            AND o.order_date BETWEEN %s AND %s
                            AND p.category_id = %s
                      GROUP BY (p.id)
                      ORDER BY p.id) t1,
                     (SELECT p.id, count(*) AS num
                      FROM product p, order_item oi, `order` o
                      WHERE p.id = oi.product_id AND oi.order_id = o.id
                            AND o.order_date BETWEEN %s AND %s
                            AND p.category_id = %s
                      GROUP BY (p.id)
                      ORDER BY p.id) t2
                WHERE t1.num >= t2.num
                      AND t1.id <> t2.id
                ORDER BY peso DESC, n1 ASC, n2 ASC
                """

        try:
            cursor.execute(query, (d1, d2, c.id, d1, d2, c.id, ))
            for row in cursor:
                result.append((id_map[row['n1']], id_map[row['n2']], row['peso']))

        except Exception as e:
            print("Errore durante la query edges")
            result = None
        finally:  # fa quello che scrivo sia che vado nel try sia che vado nell'except
            cursor.close()
            cnx.close()

        return result

