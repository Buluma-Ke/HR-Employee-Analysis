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


        self.page_frame = customtkinter.CTkFrame(self)
        self.page_frame.pack(side=customtkinter.RIGHT, fill=customtkinter.BOTH, expand=True)


        self.menu_bar_frame = customtkinter.CTkFrame(self)
        self.menu_bar_frame.pack(side=customtkinter.LEFT, fill=customtkinter.Y, pady=4, padx=3)
        self.menu_bar_frame.pack_propagate(flag=True)
        #self.menu_bar_frame.pack_configure(width=45)



        gen_data_button = customtkinter.CTkButton(master=self.menu_bar_frame,command=lambda: self.show_frame(self.gen_data_pg), text= "General Data", fg_color="gray1")
        gen_data_button.pack(padx=4, pady=10)

        Emp_data_button = customtkinter.CTkButton(master=self.menu_bar_frame,command=lambda: self.show_frame(self.Emp_data_pg), text= "Employee Survey", fg_color="gray5")
        Emp_data_button.pack(padx=4, pady=20)

        Mngr_data_button = customtkinter.CTkButton(master=self.menu_bar_frame, command=lambda: self.show_frame(self.Mngr_data_pg), text= "Manager Survey", fg_color="gray10")
        Mngr_data_button.pack(padx=4, pady=20)

        Dem_button = customtkinter.CTkButton(master=self.menu_bar_frame, command=lambda: self.show_frame(self.Dem_data_pg), text= "Demographic Insights", fg_color="gray15")
        Dem_button.pack(padx=4, pady=20)

        Comp_button = customtkinter.CTkButton(master=self.menu_bar_frame,command= lambda: self.show_frame(self.Comp_data_pg), text= "Compensaion Analysis", fg_color="gray20")
        Comp_button.pack(padx=4, pady=20)

        Perf_button = customtkinter.CTkButton(master=self.menu_bar_frame,command= lambda: self.show_frame(self.Perf_data_pg), text= "Performance Metrics", fg_color="gray23")
        Perf_button.pack(padx=4, pady=20)

        Jobsat_button = customtkinter.CTkButton(master=self.menu_bar_frame, command= lambda: self.show_frame(self.Jobsat_data_pg), text= "Job Satisfaction", fg_color="gray25")
        Jobsat_button.pack(padx=4, pady=20)

        Att_button = customtkinter.CTkButton(master=self.menu_bar_frame, command= lambda: self.show_frame(self.Att_data_pg), text= "Attrition Analysis", fg_color="gray30")
        Att_button.pack(padx=4, pady=20)

        # Initially show the general data page
        self.show_frame(self.gen_data_pg)

    def show_frame(self, frame_func):
        # Clear current frame
        for widget in self.page_frame.winfo_children():
            widget.destroy()
        # Call the frame function to create the new frame
        frame_func()


    def gen_data_pg(self):
        gen_data_frm = customtkinter.CTkFrame(self.page_frame)

        # gd =customtkinter.CTkLabel(gen_data_frm, text="general data")
        # gd.pack(padx=100, pady=200)

        # gen_data_frm.pack(fill=customtkinter.BOTH, expand=True)
        
        

    def Emp_data_pg(self):
        Emp_data_frm = customtkinter.CTkFrame(self.page_frame)

        gd =customtkinter.CTkLabel(Emp_data_frm, text="Employee data")
        gd.pack(padx=100, pady=200)

        Emp_data_frm.pack(fill=customtkinter.BOTH, expand=True)


    def Mngr_data_pg(self):
        # Emp_data_frm = customtkinter.CTkFrame(self.page_frame)

        # gd =customtkinter.CTkLabel(Emp_data_frm, text="Manager Data")
        # gd.pack(padx=100, pady=200)

        # Emp_data_frm.pack(fill=customtkinter.BOTH, expand=True)

        self.table_frame = customtkinter.CTkFrame(self.page_frame)
        self.table_frame.pack(fill=customtkinter.BOTH, expand=True)


    def Dem_data_pg(self):
        Emp_data_frm = customtkinter.CTkFrame(self.page_frame)

        gd =customtkinter.CTkLabel(Emp_data_frm, text="Demographic Data")
        gd.pack(padx=100, pady=200)

        Emp_data_frm.pack(fill=customtkinter.BOTH, expand=True)


    def Comp_data_pg(self):
        Emp_data_frm = customtkinter.CTkFrame(self.page_frame)

        gd =customtkinter.CTkLabel(Emp_data_frm, text="Compensation Data")
        gd.pack(padx=100, pady=200)

        Emp_data_frm.pack(fill=customtkinter.BOTH, expand=True)


    def Perf_data_pg(self):
        Emp_data_frm = customtkinter.CTkFrame(self.page_frame)

        gd =customtkinter.CTkLabel(Emp_data_frm, text="Performance Metrics")
        gd.pack(padx=100, pady=200)

        Emp_data_frm.pack(fill=customtkinter.BOTH, expand=True)


    def Jobsat_data_pg(self):
        Emp_data_frm = customtkinter.CTkFrame(self.page_frame)

        gd =customtkinter.CTkLabel(Emp_data_frm, text="Job satisfaction Data")
        gd.pack(padx=100, pady=200)

        Emp_data_frm.pack(fill=customtkinter.BOTH, expand=True)


    def Att_data_pg(self):
        Emp_data_frm = customtkinter.CTkFrame(self.page_frame)

        gd =customtkinter.CTkLabel(Emp_data_frm, text="Attrition Data")
        gd.pack(padx=100, pady=200)

        Emp_data_frm.pack(fill=customtkinter.BOTH, expand=True)


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