import tkinter as tk
import customtkinter
from tkinter import messagebox
from tkinter import ttk
# import PIL
# from PIL import Image
from sqlalchemy import create_engine, URL, exc, Table, MetaData, text
from sqlalchemy.orm import sessionmaker

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



customtkinter.set_appearance_mode("system")  # default
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"



class Toplevel(customtkinter.CTkToplevel):
    def __init__(self, engine, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Welcome!")
        self.geometry("600x400")
        
        self.engine = engine

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

        self.gen_data_frm = customtkinter.CTkFrame(self.page_frame)
        self.gen_data_frm.pack(fill=customtkinter.BOTH, expand=True)
        
        tree = ttk.Treeview(self.gen_data_frm)

        # Query the database using the engine
        try:
            with self.engine.connect() as connection:
                table = connection.execute(text("SELECT * "
                                               "FROM employeedata;"))
                
                #define number of columns
                columns = ['Age', 'Attrition', 'BusinessTravel', 'Department', 'DistanceFromHome',
                            'Education', 'EducationField', 'EmployeeCount', 'EmployeeID', 'Gender',
                            'JobLevel', 'JobRole', 'MaritalStatus', 'MonthlyIncome',
                            'NumCompaniesWorked', 'Over18', 'PercentSalaryHike', 'StandardHours',
                            'StockOptionLevel', 'TotalWorkingYears', 'TrainingTimesLastYear',
                            'YearsAtCompany', 'YearsSinceLastPromotion', 'YearsWithCurrManager']
                
                tree["columns"] = columns
                tree["show"] = "headings"
                
                # assign widh min width and anchor to the respective columns
                for column in columns:
                    tree.heading(column, text=column, anchor=tk.CENTER)
                    tree.column(column, width=50, anchor=tk.CENTER)


                for row in table:
                    tree.insert('', 'end', values = [str(value) for value in row])

            tree.pack(fill=customtkinter.BOTH, expand=True)

            ##Treeview Customisation (theme colors are selected)
            bg_color = self._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"])
            text_color = self._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkLabel"]["text_color"])
            selected_color = self._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkButton"]["fg_color"])

            treestyle = ttk.Style()
            treestyle.theme_use('default')
            treestyle.configure("Treeview", background=bg_color, foreground=text_color, fieldbackground=bg_color, borderwidth=0)
            treestyle.map('Treeview', background=[('selected', bg_color)], foreground=[('selected', selected_color)])
            self.bind("<<TreeviewSelect>>", lambda event: self.focus_set())

                # Optional: Add a scrollbar for the Treeview
            yscrollbar = ttk.Scrollbar(self.gen_data_frm, orient="vertical", command=tree.yview)
            tree.configure(yscroll=yscrollbar.set)
            yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # x axis scroll bar
            # xscrollbar = ttk.Scrollbar(self.gen_data_frm, orient="horizontal", command=tree.xview)
            # tree.configure(xscroll=xscrollbar.set)
            # xscrollbar.pack(side=tk.BOTTOM, fill=tk.x)


    # Pack the Treeview again after adding the scrollbar
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        except exc.SQLAlchemyError as e:
            print(e)
            messagebox.showerror("Error", f"Database query failed: {str(e)}")

    def Emp_data_pg(self):
        self.Emp_data_frm = customtkinter.CTkFrame(self.page_frame)
        self.Emp_data_frm.pack(fill=customtkinter.BOTH, expand=True)
        
        tree = ttk.Treeview(self.Emp_data_frm)

        # Query the database using the engine
        try:
            with self.engine.connect() as connection:
                table = connection.execute(text("SELECT * "
                                               "FROM employee_survey;"))
                
                #define number of columns
                columns = ['EmployeeID', 'EnvironmentSatisfaction', 'JobSatisfaction',
                           'WorkLifeBalance']
                
                tree["columns"] = columns
                tree["show"] = "headings"
                
                # assign widh min width and anchor to the respective columns
                for column in columns:
                    tree.heading(column, text=column, anchor=tk.CENTER)
                    tree.column(column, anchor=tk.CENTER)


                for row in table:
                    tree.insert('', 'end', values = [str(value) for value in row])

            tree.pack(side=tk.LEFT, expand=False)

                # Optional: Add a scrollbar for the Treeview
            yscrollbar = ttk.Scrollbar(self.Emp_data_frm, orient="vertical", command=tree.yview)
            tree.configure(yscroll=yscrollbar.set)
            yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)


    # Pack the Treeview again after adding the scrollbar
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        except exc.SQLAlchemyError as e:
            print(e)
            messagebox.showerror("Error", f"Database query failed: {str(e)}")


    def Mngr_data_pg(self):
        self.Mngr_data_frm = customtkinter.CTkFrame(self.page_frame)
        self.Mngr_data_frm.pack(fill=customtkinter.BOTH, expand=True)
        
        tree = ttk.Treeview(self.Mngr_data_frm)

        # Query the database using the engine
        try:
            with self.engine.connect() as connection:
                table = connection.execute(text("SELECT * "
                                               "FROM manager_survey;"))
                
                #define columns
                columns = ['EmployeeID', 'JobInvolvement', 'PerformanceRating']
                tree["columns"] = columns
                tree["show"] = "headings"
                
                # assign width and anchor to the respective columns
                for column in columns:
                    tree.heading(column, text=column, anchor=tk.CENTER)
                    tree.column(column, width=50, anchor=tk.CENTER)


                for row in table:
                    tree.insert('', 'end', values = [str(value) for value in row])

            tree.pack(fill=customtkinter.BOTH, expand=False)

                # Optional: Add a scrollbar for the Treeview
            yscrollbar = ttk.Scrollbar(self.Mngr_data_frm, orient="vertical", command=tree.yview)
            tree.configure(yscroll=yscrollbar.set)
            yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)


    # Pack the Treeview again after adding the scrollbar
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        except exc.SQLAlchemyError as e:
            print(e)
            messagebox.showerror("Error", f"Database query failed: {str(e)}")





    def Dem_data_pg(self):
        print("Initializing Dem_data_pg function...")
        
        self.Dem_data_frm = customtkinter.CTkFrame(self.page_frame)
        self.Dem_data_frm.pack(fill=customtkinter.BOTH, expand=True)  # Ensure the frame is packed
        print("Dem_data_frm frame packed.")

        # Fetch gender distribution data
        try:
            #print("Connecting to the database to fetch gender distribution data...")
            with self.engine.connect() as connection:
                query = text("SELECT Department, Gender, COUNT(*) numofemployees "
                            "FROM employeedata " 
                            "GROUP BY Department, Gender "
                            "ORDER BY numofemployees;")
                gender_dist_dept = connection.execute(query)
                gender_dist_dept = pd.DataFrame(gender_dist_dept.fetchall(), columns=gender_dist_dept.keys())
                #print("Data fetched successfully.")
                #print(gender_dist_dept.head())  # Print the first few rows of the DataFrame
        except exc.SQLAlchemyError as e:
            #print(f"Database query error: {e}")
            messagebox.showerror("Error", f"Database query failed: {str(e)}")
            return  # Exit the function if there's an error

        # Create a bar plot using Matplotlib
        #print("Creating a bar plot...")
        fig1, ax1 = plt.subplots()

        # Pivot the DataFrame for plotting
        pivot_df = gender_dist_dept.pivot(index='Department', columns='Gender', values='numofemployees').fillna(0)
        #print("Pivot DataFrame created:")
        #print(pivot_df)  # Print to check the DataFrame

        try:
            pivot_df.plot(kind='bar', ax=ax1, color=['#1f77b4', '#ff7f0e'], edgecolor='black')

            # Set title and labels
            ax1.set_title("Gender Distribution per Department")
            ax1.set_xlabel("Department")
            ax1.set_ylabel("Number of Employees")
            ax1.legend(title='Gender')
            #print("Plot created successfully.")
        except Exception as e:
            print(f"Plotting error: {e}")

        # Create and pack the canvas
        upper_frame = customtkinter.CTkFrame(self.Dem_data_frm, bg_color="red")
        upper_frame.pack(fill='both', expand=True)
        print("Upper frame packed.")

        canvas1 = FigureCanvasTkAgg(fig1, upper_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)
        print("Canvas added to the upper frame.")

                # Fetch gender distribution data
        try:
            print("Connecting to the database to fetch gender distribution per education field...")
            with self.engine.connect() as connection:
                query2 = text("SELECT EducationField,Gender, COUNT(*) numofemployees "
                            "FROM employeedata " 
                            "GROUP BY EducationField, Gender "
                            "ORDER BY numofemployees;")
                gender_dist_edfield = connection.execute(query2)
                gender_dist_edfield = pd.DataFrame(gender_dist_edfield.fetchall(), columns=gender_dist_edfield.keys())
                print("Data fetched successfully.")
                print(gender_dist_edfield.head())  # Print the first few rows of the DataFrame
        except exc.SQLAlchemyError as e:
            print(f"Database query error: {e}")
            messagebox.showerror("Error", f"Database query failed: {str(e)}")
            return  # Exit the function if there's an error

        # Create a bar plot using Matplotlib
        print("Creating a bar plot...")
        fig2, ax2 = plt.subplots()

        # Pivot the DataFrame for plotting
        pivot_df2 = gender_dist_edfield.pivot(index='EducationField', columns='Gender', values='numofemployees').fillna(0)
        print("Pivot DataFrame created:")
        print(pivot_df2)  # Print to check the DataFrame

        try:
            pivot_df2.plot(kind='bar', ax=ax1, color=['#1f77b4', '#ff7f0e'], edgecolor='black')

            # Set title and labels
            ax2.set_title("Gender Distribution per EducationField")
            ax2.set_xlabel("Education Field")
            ax2.set_ylabel("Number of Employees")
            #ax2.legend(title='Gender')
            print("Plot created successfully.")
        except Exception as e:
            print(f"Plotting error: {e}")

        # Create and pack the canvas
        # upper_frame = customtkinter.CTkFrame(self.Dem_data_frm, bg_color="red")
        # upper_frame.pack(fill='both', expand=True)
        #print("Upper frame packed.")

        canvas2 = FigureCanvasTkAgg(fig2, upper_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side="right", fill="both", expand=True)
        print("Canvas added to the upper frame.")





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
            
            
            print("Connection succesful")
            messagebox.showinfo(message="Connection succesful")
            self.new_window(engine)
        except exc.SQLAlchemyError :
            print("Connection failed")
            messagebox.showerror(message="Connection failed")

    def new_window(self, engine):
            self.ui_window = Toplevel(engine, self)
            self.withdraw()

 

if __name__ == "__main__":
    app = App()
    app.mainloop()