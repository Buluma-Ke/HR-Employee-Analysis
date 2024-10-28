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

        # def gen_data_pg():
        #     gen_data_frm = customtkinter.CTkFrame(self.page_frame)

        #     gd =customtkinter.CTkLabel(gen_data_frm, text="general data")
        #     gd.place(X=100, Y=200)

        #     gen_data_frm.pack(fill=customtkinter.BOTH, expand=True)


        # self.page_frame = customtkinter.CTkFrame(self)
        # self.page_frame.pack(side=customtkinter.RIGHT, fill=customtkinter.BOTH, expand=True)
        # gen_data_pg()

        self.menu_bar_frame = customtkinter.CTkFrame(self)
        self.menu_bar_frame.pack(side=customtkinter.LEFT, fill=customtkinter.Y, pady=4, padx=3)
        self.menu_bar_frame.pack_propagate(flag=True)
        #self.menu_bar_frame.pack_configure(width=45)

        gen_data_button = customtkinter.CTkButton(master=self.menu_bar_frame, text= "General Data", fg_color="gray1")
        gen_data_button.pack(padx=4, pady=10)

        Emp_data_button = customtkinter.CTkButton(master=self.menu_bar_frame, text= "Employee Survey", fg_color="gray5")
        Emp_data_button.pack(padx=4, pady=20)

        Mngr_data_button = customtkinter.CTkButton(master=self.menu_bar_frame, text= "Manager Survey", fg_color="gray10")
        Mngr_data_button.pack(padx=4, pady=20)

        Dem_button = customtkinter.CTkButton(master=self.menu_bar_frame, text= "Demographic Insights", fg_color="gray15")
        Dem_button.pack(padx=4, pady=20)

        Comp_button = customtkinter.CTkButton(master=self.menu_bar_frame, text= "Compensaion Analysis", fg_color="gray20")
        Comp_button.pack(padx=4, pady=20)

        Perf_button = customtkinter.CTkButton(master=self.menu_bar_frame, text= "Performance Metrics", fg_color="gray23")
        Perf_button.pack(padx=4, pady=20)

        Jobsat_button = customtkinter.CTkButton(master=self.menu_bar_frame, text= "Job Satisfaction", fg_color="gray25")
        Jobsat_button.pack(padx=4, pady=20)

        Att_button = customtkinter.CTkButton(master=self.menu_bar_frame, text= "Attrition Analysis", fg_color="gray30")
        Att_button.pack(padx=4, pady=20)


class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.title("LOGIN")
        self.geometry("600x400")

        #yuX1MEubEur4Gw4O
        self.inputpassword = customtkinter.CTkEntry(master=self, placeholder_text= 'Enter password',
                                        width=240, height=25, border_width=1,corner_radius=5, show="*")
        self.inputpassword.pack(padx=20, pady=10)

        self.cnnctbutton = customtkinter.CTkButton(master=self, text="Connect", command=self.Connect_db, fg_color="slate blue")
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