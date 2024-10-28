from tkinter import *
import customtkinter
from tkinter import messagebox
# import PIL
# from PIL import Image
#import CustomTkinterMessagebox as CTkMessagebox

from sqlalchemy import create_engine
from sqlalchemy import URL
from sqlalchemy import exc



customtkinter.set_appearance_mode("system")  # default
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"



class Toplevel(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Welcome!")
        self.geometry("600x400")

class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.title("LOGIN")
        self.geometry("600x400")

        self.inputpassword = customtkinter.CTkEntry(master=self, placeholder_text= 'Enter password',
                                        width=240, height=25, border_width=1,corner_radius=5, show="*")
        self.inputpassword.pack(padx=20, pady=10)

        self.cnnctbutton = customtkinter.CTkButton(master=self, text="Connect", command=self.Connect_db, fg_color="blue")
        self.cnnctbutton.pack(padx=20, pady=10)


    def Connect_db(self):

        password = self.inputpassword.get()

        try:
            url_object = URL.create(
                                "mysql+mysqlconnector",
                                username ="debian-sys-maint",
                                password = password,
                                host =  "localhost",
                                database = "hremployeedb"
                                )
            
            engine = create_engine(url_object)
            engine.connect()
            print("Connection succesful")
            messagebox.showinfo(message="Connection succesful")
            self.new_window()
        except exc.SQLAlchemyError :
            print("Connection failed")
            messagebox.showerror(message="Connection failed")

    def new_window(self):
            self.ui_window = Toplevel(self)
            self.withdraw()

 

if __name__ == "__main__":
    app = App()
    app.mainloop()