#DEVELOPER: Diego Puentes
#DESCRIPTION:    This code is used  to generate the consult from the database 

from itertools import product
import logging
from math import prod
import sqlite3
from typing import List

class service_sql:
    db_name = 'database.db'
    query   = ''

    def  __init__(self):
        pass

    #INIT AND CONNECT TO DB 'database.db'
    def _init_db(self, query, parameters = ()):

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    #GET LIST PRODUCTS
    def get_product(self):

        query          = 'SELECT * FROM product ORDER BY name DESC'
        db_getProducts = self._init_db(query)
        db_list        = []

        for product in db_getProducts:
            db_list.append(product)
        return db_list

    #CHECK INPUT EMPTY
    def checker(self, name, price): return len(name) != 0 and len(price) !=0

    #ADD PRODUCT TO DB
    def add_product(self, name_product, price_product):
        try:
            if self.checker(name_product, price_product):
                query         = 'INSERT INTO product VALUES (NULL, ?, ?)'
                parameters    = (name_product,price_product)
                db_addProduct = self._init_db(query,parameters)
                logging.info("PRODUCT ADDED")
                return True
            else:
                logging.info("VALIDATE INFO")
                return False

        except Exception as e: logging.error("ADDED ERROR: {e}")

    #DELETE PRODUCT FROM DB
    def delete_product(self, id_product):
        try:
            query            = 'DELETE FROM product WHERE id_product = ?'
            db_deleteProduct =  self._init_db(query,(id_product, ))
            logging.info("PRODUCT DELETED")
            return True
        except Exception as e:
            logging.info(f"DELETE  ERROR: {e}")
            return False

    #UPDATE PRODUCT TO DB
    def update_product(self,name_product,price_product,id_product):
        try:
            if self.checker(name_product, price_product):
                query             = 'UPDATE product SET name = ?, price = ? WHERE id_product = ?'
                parameters        = (name_product,int(price_product),id_product)
                db_updateProduct  = self._init_db(query,parameters)
                return True
            else:
                logging.error(f"INSERT CORRECT VALUES")
                return False
        except Exception as e:
            logging.error(f"UPDATE ERROR: {e}")
            return False
