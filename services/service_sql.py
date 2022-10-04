import sqlite3

class Service_sql:
    db_name = 'database.db'
    query = ''  
    
    def _init_db(self, query, parameters = {} ):
        with sqlite3.connect(self.db_name) as conn:
            result = conn.execute(query, parameters)
        return result
    
    def get_product(self):
        query ='SELECT * FROM product ORDER BY name_product DESC'
        db_rows = self._init_db(query)
        list_product = []

        for row in db_rows:
            list_product.append(row)
        
        return list_product
        

    def checker(self, name, price):
        return len(name) != 0 and len(price) !=0
            
    def add_product(self, name, price):
        
        if self.checker(name,price):
            query = ''
            print(name)
            print(price)
        else:
            print("Validar Informacion ingresada")
        
if __name__ == "__main__":
    sql = Service_sql()
    sql.get_product() 