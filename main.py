
from unicodedata import name
from services import service_sql as sql

from tkinter  import CENTER, EW, Entry, Frame, Label, LabelFrame, Tk, ttk

class Main():
    
    def __init__(self, screen) -> None:
        
        self.screen = screen
        self.screen.title('Prducts aplication')

        self.sql = sql.Service_sql()
        #Create Container
        frame = LabelFrame(self.screen, text= 'Register A New Product')
        frame.grid(row= 0 , column= 0, columnspan= 3, pady=20 )

        #Name Input
        Label(frame, text= 'Name: ').grid(row=1, column= 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column= 1)

        #Price Input
        Label(frame, text= 'Price: ').grid(row=2, column= 0)
        self.price = Entry(frame)
        self.price.grid(row=2, column= 1)

        #Button Add Product
        ttk.Button(frame, text = 'Save Product', command= self.sql.add_product(self.name.get(), self.price.get()) ).grid(row=3, columnspan= 2, sticky= EW)

        #Table Products
        self.table = ttk.Treeview(height=10, columns= 2)
        self.table.grid(row= 4, column= 0, columnspan=2)
        #--HEADINGS
        self.table.heading('#0', text= 'Name', anchor= CENTER)
        self.table.heading('#1', text= 'Price', anchor= CENTER)
        
        self.get_listProducts()

    def get_listProducts(self):
        #cleaning table
        list_products = self.table.get_children()
        for product in list_products:
            self.table.delete(product)

        #insert data from table
        insert_products = self.sql.get_product()
        for row in insert_products:
            self.table.insert('', 0, text= row[1], values=row[2])   

    def add_product():
        pass  
            

if __name__ == "__main__":
    screen = Tk()
    app    = Main(screen)
    screen.mainloop()