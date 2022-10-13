
import logging
from services import service_sql as sql
from tkinter  import CENTER, EW, Entry, Frame, Label, LabelFrame, StringVar, Tk, Toplevel, ttk

logging.basicConfig(
	level		= logging.INFO,
	format		= "%(asctime)s [%(levelname)s]	%(module)s:%(lineno)d:	%(message)s" ,
	datefmt		= '%Y-%m-%d %H:%M:%S'
)

class Main():

    def __init__(self, screen) -> None:
        logging.info("PROCESS: __init__APP")
        self.screen = screen
        self.screen.title('Products aplication')

        #Create Container
        frame = LabelFrame(self.screen, text= 'Register A New Product')
        frame.grid(row= 0 , column= 0, columnspan= 3, pady=20 )

        #Name Input
        Label(frame, text= 'Name: ').grid(row=1, column= 0)
        self.name = Entry(frame)
        self.name.grid(row=1, column= 1)
        self.name.focus()

        #Price Input
        Label(frame, text= 'Price: ').grid(row=2, column= 0)
        self.price = Entry(frame)
        self.price.grid(row=2, column= 1)

        #Output Alert
        self.message = Label(text= '' , fg='red')
        self.message.grid(row=3, column= 0 ,columnspan= 2 , sticky= EW)

        #Button Add Product
        ttk.Button(frame, text = 'Save Product', command= lambda: self.add_product(self.name.get(),self.price.get())).grid(row=3, columnspan= 2, sticky= EW)

        #Table Products
        self.table = ttk.Treeview(height=10, columns= ('#0, #1'))
        self.table.grid(row= 4, column= 0, columnspan=2)
        #--HEADINGS
        self.table.heading('#0', text= 'ID', anchor=CENTER)
        self.table.heading('#1', text= 'Name', anchor= CENTER)
        self.table.heading('#2', text= 'Price', anchor= CENTER)

        self.service = sql.service_sql()
        self.get_listProducts()

        #Button Delete Product
        ttk.Button(text = 'Delete Product', command= lambda: self.delete_product()).grid(row=5, column= 0, sticky= EW)

        #Button Update Product
        ttk.Button(text = 'Update Product', command= lambda: self.edit_screen()).grid(row=5, column= 1, sticky= EW)


    def get_listProducts(self):

        logging.info("PROCESS: __Get list products__")

        #CLEANING TABLE
        table_product = self.table.get_children()
        for product in table_product:
            self.table.delete(product)

        #FILLING TABLE
        get_list = self.service.get_product()
        for product in get_list:
            self.table.insert('',0, text= product[0], values= (product[1],product[2]))

    def add_product(self, name, price):

        logging.info("PROCESS: __Add_product__")
        add_product          = self.service.add_product(name, price)

        if add_product:
            self.message['text'] = 'Product added successfully'
            self.message['fg']   = 'green'
        else:
            self.message['text'] = 'Product not added, please try again'
            self.message['fg']   = 'red'

        self.get_listProducts()

    def delete_product(self):

        logging.info("PROCESS: __Delete_product__")

        try:
            id_product      = self.table.item(self.table.selection())
            delete_product  = self.service.delete_product(id_product['text'])

            #ALERT MESSAGE
            if delete_product:
                logging.warning(f"DELETE PRODUCT: ID_PRODUCT --> {id_product['text']}" )
                self.message['text'] = 'Product Deleted Successfully'
                self.message['fg']   = 'green'
            else:
                self.message['text'] = 'Product not deleted, please try again'

        except IndexError as e: self.message['text'] = 'select product for delete'

        self.get_listProducts()

    def  update_product(self, name_product, price_product, id_product):
        try:
            update_product = self.service.update_product(name_product, price_product, id_product)

            if update_product:
                self.message['text'] = 'Product updated successfully'
                self.message['fg']   = 'green'
                self.edit_screen.destroy()
            else:
                self.message['text'] = 'Product not updated, please try again'
                self.message['fg']   = 'red'

            self.get_listProducts()

        except IndexError as e: logging.error(f'Product update failed:{e}')

    def edit_screen(self):

        #INIT SCREEN EDIT
        self.edit_screen        =  Toplevel()
        self.edit_screen.geometry("200x200")
        self.edit_screen.title("Edit Product")

        #OLD_DATA
        product = self.table.item(self.table.selection())
        id_product = product["text"]
        name       = product["values"][0]
        price      = product["values"][1]

        #Create Container
        frame_edit = LabelFrame(self.edit_screen, text= 'Update Product')
        frame_edit.grid(row= 0 , column= 0, columnspan= 3, pady=20 )

        #Name Input
        Label(frame_edit, text= 'Name: ').grid(row=1, column= 0)
        old_name = Entry(frame_edit, textvariable= StringVar(frame_edit, value= name))
        old_name.grid(row=1, column= 1)

        #Price Input
        Label(frame_edit, text= 'Price: ').grid(row=2, column= 0)
        old_price = Entry(frame_edit, textvariable= StringVar(frame_edit, value= price))
        old_price.grid(row=2, column= 1)

        #Button Add Product
        ttk.Button(frame_edit, text = 'Update Product', command= lambda: self.update_product(old_name.get(),old_price.get(), id_product)).grid(row=3, columnspan= 2, sticky= EW)


if __name__ == "__main__":
    screen = Tk()
    app    = Main(screen)
    screen.mainloop()