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

        Att1_button = customtkinter.CTkButton(master=self.menu_bar_frame,command= lambda: self.show_frame(self.AAt1_data_pg), text= "Attrition Analysis 1", fg_color="gray23")
        Att1_button.pack(padx=4, pady=20)

        Att2_button = customtkinter.CTkButton(master=self.menu_bar_frame, command= lambda: self.show_frame(self.Att2_data_pg), text= "Attrition Analysis 2", fg_color="gray25")
        Att2_button.pack(padx=4, pady=20)

        Att3_button = customtkinter.CTkButton(master=self.menu_bar_frame, command= lambda: self.show_frame(self.Att3_data_pg), text= "Attrition Analysis 3", fg_color="gray30")
        Att3_button.pack(padx=4, pady=20)
        

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
        
        self.Att3_data_frm = customtkinter.CTkFrame(self.page_frame)
        self.Att3_data_frm.pack(fill=customtkinter.BOTH, expand=True)  # Ensure the frame is packed
        print("Dem_data_frm frame packed.")

        upper_frame = customtkinter.CTkFrame(self.Att3_data_frm)
        upper_frame.pack(fill='both', expand=True)
        print("Upper frame packed.")

        Lower_frame = customtkinter.CTkFrame(self.Att3_data_frm)
        Lower_frame.pack(fill='both', expand=True)
        print("Lower frame packed.")

        # Fetch gender distribution data
        def depertment():
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
            fig, ax = plt.subplots(figsize=(2, 2))
            # Pivot the DataFrame for plotting
            pivot_df = gender_dist_dept.pivot(index='Department', columns='Gender', values='numofemployees').fillna(0)


            try:
                pivot_df.plot(kind='bar', ax=ax, color=['slateblue', 'darkslateblue'], edgecolor='black')

                # Set title and labels
                ax.set_title("Gender Distribution per Department", fontsize=8)
                ax.tick_params(axis='x', rotation=0)
                ax.tick_params(axis='x', labelsize=6)
                ax.tick_params(axis='y', labelsize=6)
                for spine in ax.spines.values():
                    spine.set_visible(False)
                ax.set_xlabel("")
                # ax.set_ylabel("Number of Employees")
                ax.legend(title='Gender')
                
                #print("Plot created successfully.")
            except Exception as e:
                print(f"Plotting error: {e}")


            canvas = FigureCanvasTkAgg(fig, upper_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True)
            print("Canvas added to the upper frame.")
        
        depertment()

                # Fetch gender distribution data
        def education_field():
            try:
                print("Connecting to the database to fetch gender distribution per education field...")
                with self.engine.connect() as connection:
                    query = text("SELECT EducationField,Gender, COUNT(*) numofemployees "
                                "FROM employeedata " 
                                "GROUP BY EducationField, Gender "
                                "ORDER BY numofemployees;")
                    gender_dist_edfield = connection.execute(query)
                    gender_dist_edfield = pd.DataFrame(gender_dist_edfield.fetchall(), columns=gender_dist_edfield.keys())
                    print("Data fetched successfully.")
                    print(gender_dist_edfield.head())  # Print the first few rows of the DataFrame
            except exc.SQLAlchemyError as e:
                print(f"Database query error: {e}")
                messagebox.showerror("Error", f"Database query failed: {str(e)}")
                return  # Exit the function if there's an error

            # Create a bar plot using Matplotlib
            print("Creating a bar plot...")
            fig, ax = plt.subplots()

            # Pivot the DataFrame for plotting
            pivot_df = gender_dist_edfield.pivot(index='EducationField', columns='Gender', values='numofemployees').fillna(0)
            print("Pivot DataFrame created:")
            print(pivot_df)  # Print to check the DataFrame

            try:
                pivot_df.plot(kind='bar', ax=ax, color=['slateblue', 'darkslateblue'], edgecolor='black', legend=False)

                # Set title and labels
                ax.set_title("Gender Distribution per EducationField", fontsize=8)
                ax.tick_params(axis='x', rotation=0)
                ax.tick_params(axis='x', labelsize=6)
                ax.tick_params(axis='y', labelsize=6)
                for spine in ax.spines.values():
                    spine.set_visible(False)
                ax.set_xlabel("")
                # ax.set_ylabel("Number of Employees")
                #ax2.legend(title='Gender')
                print("Plot created successfully.")
            except Exception as e:
                print(f"Plotting error: {e}")


            canvas = FigureCanvasTkAgg(fig, upper_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="right", fill="both", expand=True)
            print("Canvas added to the upper frame.")

        education_field()


        def Job_Level():
            try:
                print("Connecting to the database to fetch gender distribution per Job level...")
                with self.engine.connect() as connection:
                    query = text("SELECT JobLevel,Gender, COUNT(*) numofemployees "
                                    "FROM employeedata "
                                    "GROUP BY JobLevel, Gender "
                                    "ORDER BY JobLevel, Gender, numofemployees;")
                    gender_dist_Joblevel = connection.execute(query)
                    gender_dist_Joblevel = pd.DataFrame(gender_dist_Joblevel.fetchall(), columns=gender_dist_Joblevel.keys())
                    print("Data fetched successfully.")
                    print(gender_dist_Joblevel.head())  # Print the first few rows of the DataFrame
            except exc.SQLAlchemyError as e:
                print(f"Database query error: {e}")
                messagebox.showerror("Error", f"Database query failed: {str(e)}")
                return  # Exit the function if there's an error

            # Create a bar plot using Matplotlib
            print("Creating a bar plot...")
            fig, ax = plt.subplots(figsize=(2, 2))

            # Pivot the DataFrame for plotting
            pivot_df = gender_dist_Joblevel.pivot(index='JobLevel', columns='Gender', values='numofemployees').fillna(0)
            print("Pivot DataFrame created:")
            print(pivot_df)  # Print to check the DataFrame

            try:
                pivot_df.plot(kind='bar', ax=ax, color=['slateblue', 'darkslateblue'], edgecolor='black', legend=False)

                # Set title and labels
                ax.set_title("Gender Distribution per Job Level", fontsize=8)
                ax.tick_params(axis='x', rotation=0)
                ax.tick_params(axis='x', labelsize=6)
                ax.tick_params(axis='y', labelsize=6)
                for spine in ax.spines.values():
                    spine.set_visible(False)
                ax.set_xlabel("")
                #ax.set_ylabel("Number of Employees")
                #ax2.legend(title='Gender')
                print("Plot created successfully.")
            except Exception as e:
                print(f"Plotting error: {e}")

            canvas = FigureCanvasTkAgg(fig, Lower_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="right", fill="both", expand=True)
            print("Canvas added to the Lower frame.")

        Job_Level()


        def Job_Role():
            try:
                print("Connecting to the database to fetch gender distribution per Job Role...")
                with self.engine.connect() as connection:
                    query = text("SELECT JobRole,Gender, COUNT(*) numofemployees "
                                    "FROM employeedata "
                                    "GROUP BY JobRole, Gender "
                                    "ORDER BY numofemployees;")
                    gender_dist_JobRole = connection.execute(query)
                    gender_dist_JobRole = pd.DataFrame(gender_dist_JobRole.fetchall(), columns=gender_dist_JobRole.keys())
                    print("Data fetched successfully.")
                    print(gender_dist_JobRole.head())  # Print the first few rows of the DataFrame
            except exc.SQLAlchemyError as e:
                print(f"Database query error: {e}")
                messagebox.showerror("Error", f"Database query failed: {str(e)}")
                return  # Exit the function if there's an error

            # Create a bar plot using Matplotlib
            print("Creating a bar plot...")
            fig, ax = plt.subplots(figsize=(10, 7))

            # Pivot the DataFrame for plotting
            pivot_df = gender_dist_JobRole.pivot(index='JobRole', columns='Gender', values='numofemployees').fillna(0)
            print("Pivot DataFrame created:")           # Pivot the DataFrame for plotting
            #pivot_df = Avg_dep_sal.pivot(index='Department', values='AvgMonthlyincome').fillna(0)

            print(pivot_df)  # Print to check the DataFrame

            try:
                pivot_df.plot(kind='bar', ax=ax, color=['slateblue', 'darkslateblue'], edgecolor='black', legend=False)

                # Set title and labels
                ax.set_title("Gender Distribution per Job Role", fontsize=8)
                ax.tick_params(axis='x', rotation=0)
                ax.tick_params(axis='x', labelsize=6)
                ax.tick_params(axis='y', labelsize=6)
                for spine in ax.spines.values():
                    spine.set_visible(False)
                ax.set_xlabel("")
                #ax.set_ylabel("Number of Employees")
                #ax2.legend(title='Gender')
                print("Plot created successfully.")
            except Exception as e:
                print(f"Plotting error: {e}")

            canvas = FigureCanvasTkAgg(fig, Lower_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="right", fill="both", expand=True)
            print("Canvas added to the Lower frame.")

        Job_Role()






    def Comp_data_pg(self):
        self.Att3_data_frm = customtkinter.CTkFrame(self.page_frame)
        self.Att3_data_frm.pack(fill=customtkinter.BOTH, expand=True)

        upper_frame = customtkinter.CTkFrame(self.Att3_data_frm)
        upper_frame.pack(fill='both', expand=True)
        print("Upper frame packed.")

        Lower_frame = customtkinter.CTkFrame(self.Att3_data_frm)
        Lower_frame.pack(fill='both', expand=True)
        print("Lower frame packed.")

        def depertment():
            try:
                with self.engine.connect() as connection:
                    query = text("SELECT Department, AVG(MonthlyIncome) AvgMonthlyincome "
                                    "FROM employeedata "
                                    "GROUP BY Department "
                                    "ORDER BY AvgMonthlyincome;")
                    Avg_dep_sal = connection.execute(query)
                    Avg_dep_sal = pd.DataFrame(Avg_dep_sal.fetchall(), columns=Avg_dep_sal.keys())
                    print(Avg_dep_sal.head())

            except exc.SQLAlchemyError as e:
                messagebox.showerror("Error", f"Database query failed: {str(e)}")
                return  # Exit the function if there's an error
            
            Avg_dep_sal['AvgMonthlyincome'] = pd.to_numeric(Avg_dep_sal['AvgMonthlyincome'], errors='coerce')

            fig, ax = plt.subplots()
            # Pivot the DataFrame for plotting
            #pivot_df = Avg_dep_sal.pivot(index='Department', values='AvgMonthlyincome').fillna(0)


            try:
                Avg_dep_sal.plot(ax=ax, kind='bar',x="Department", y="AvgMonthlyincome", color=['slateblue'], edgecolor='black', legend=False)

                # Set title and labels
                ax.set_title("Average monthly income by Department", fontsize=8)
                ax.tick_params(axis='x', rotation=0)
                ax.tick_params(axis='x', labelsize=6)
                ax.tick_params(axis='y', labelsize=6)
                for spine in ax.spines.values():
                    spine.set_visible(False)
                ax.set_xlabel("")
                # ax.set_ylabel("Number of Employees")
                
                #print("Plot created successfully.")
            except Exception as e:
                print(f"Plotting error: {e}")


            canvas = FigureCanvasTkAgg(fig, upper_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True)
            print("Canvas added to the upper frame.")
        
        depertment()


        def Education_field():
            try:
                with self.engine.connect() as connection:
                    query = text("SELECT EducationField, AVG(MonthlyIncome) AvgMonthlyincome "
                                    "FROM employeedata "
                                    "GROUP BY EducationField "
                                    "ORDER BY AvgMonthlyincome;")
                    Avg_edfield_sal = connection.execute(query)
                    Avg_edfield_sal = pd.DataFrame(Avg_edfield_sal.fetchall(), columns=Avg_edfield_sal.keys())
                    print(Avg_edfield_sal.head())

            except exc.SQLAlchemyError as e:
                messagebox.showerror("Error", f"Database query failed: {str(e)}")
                return  # Exit the function if there's an error
            
            Avg_edfield_sal['AvgMonthlyincome'] = pd.to_numeric(Avg_edfield_sal['AvgMonthlyincome'], errors='coerce')

            fig, ax = plt.subplots()
            # Pivot the DataFrame for plotting
            #pivot_df = Avg_dep_sal.pivot(index='Department', values='AvgMonthlyincome').fillna(0)


            try:
                Avg_edfield_sal.plot(ax=ax, kind='bar',x="EducationField", y="AvgMonthlyincome", color=['slateblue'], edgecolor='black', legend=False)

                # Set title and labels
                ax.set_title("Average monthly income by Education Field", fontsize=8)
                ax.tick_params(axis='x', rotation=0)
                ax.tick_params(axis='x', labelsize=6)
                ax.tick_params(axis='y', labelsize=6)
                for spine in ax.spines.values():
                    spine.set_visible(False)
                ax.set_xlabel("")
                # ax.set_ylabel("Number of Employees")
                
                #print("Plot created successfully.")
            except Exception as e:
                print(f"Plotting error: {e}")


            canvas = FigureCanvasTkAgg(fig, upper_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True)
            print("Canvas added to the upper frame.")

        Education_field()


        def Job_level():
            try:
                with self.engine.connect() as connection:
                    query = text("SELECT JobLevel, AVG(MonthlyIncome) AvgMonthlyincome "
                                    "FROM employeedata "
                                    "GROUP BY JobLevel "
                                    "ORDER BY JobLevel;")
                    Avg_joblevel_sal = connection.execute(query)
                    Avg_joblevel_sal = pd.DataFrame(Avg_joblevel_sal.fetchall(), columns=Avg_joblevel_sal.keys())
                    print(Avg_joblevel_sal.head())

            except exc.SQLAlchemyError as e:
                messagebox.showerror("Error", f"Database query failed: {str(e)}")
                return  # Exit the function if there's an error
            
            Avg_joblevel_sal['AvgMonthlyincome'] = pd.to_numeric(Avg_joblevel_sal['AvgMonthlyincome'], errors='coerce')

            fig, ax = plt.subplots(figsize=(3, 3))
            # Pivot the DataFrame for plotting
            #pivot_df = Avg_dep_sal.pivot(index='Department', values='AvgMonthlyincome').fillna(0)


            try:
                Avg_joblevel_sal.plot(ax=ax, kind='bar',x="JobLevel", y="AvgMonthlyincome", color=['slateblue'], edgecolor='black', legend=False)

                # Set title and labels
                ax.set_title("Average monthly income by Job Level", fontsize=8)
                ax.tick_params(axis='x', rotation=0)
                ax.tick_params(axis='x', labelsize=6)
                ax.tick_params(axis='y', labelsize=6)
                for spine in ax.spines.values():
                    spine.set_visible(False)
                ax.set_xlabel("")
                # ax.set_ylabel("Number of Employees")
                
                #print("Plot created successfully.")
            except Exception as e:
                print(f"Plotting error: {e}")


            canvas = FigureCanvasTkAgg(fig, Lower_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True)
            print("Canvas added to the upper frame.")

        #Job_level()


        def Job_Role():
            try:
                with self.engine.connect() as connection:
                    query = text("SELECT JobRole, AVG(MonthlyIncome) AvgMonthlyincome "
                                    "FROM employeedata "
                                    "GROUP BY JobRole "
                                    "ORDER BY AvgMonthlyincome;")
                    Avg_joblRole_sal = connection.execute(query)
                    Avg_joblRole_sal = pd.DataFrame(Avg_joblRole_sal.fetchall(), columns=Avg_joblRole_sal.keys())
                    print(Avg_joblRole_sal.head())

            except exc.SQLAlchemyError as e:
                messagebox.showerror("Error", f"Database query failed: {str(e)}")
                return  # Exit the function if there's an error
            
            Avg_joblRole_sal['AvgMonthlyincome'] = pd.to_numeric(Avg_joblRole_sal['AvgMonthlyincome'], errors='coerce')

            fig, ax = plt.subplots(figsize=(10, 7))
            # Pivot the DataFrame for plotting
            #pivot_df = Avg_dep_sal.pivot(index='Department', values='AvgMonthlyincome').fillna(0)


            try:
                Avg_joblRole_sal.plot(ax=ax, kind='bar',x="JobRole", y="AvgMonthlyincome", color=['darkslateblue'], edgecolor='black', legend=False)

                # Set title and labels
                ax.set_title("Average monthly income by Job Role", fontsize=8)
                ax.tick_params(axis='x', rotation=0)
                ax.tick_params(axis='x', labelsize=6)
                ax.tick_params(axis='y', labelsize=6)
                for spine in ax.spines.values():
                    spine.set_visible(False)
                ax.set_xlabel("")
                # ax.set_ylabel("Number of Employees")
                
                #print("Plot created successfully.")
            except Exception as e:
                print(f"Plotting error: {e}")


            canvas = FigureCanvasTkAgg(fig, Lower_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True)
            print("Canvas added to the upper frame.")

        Job_Role()
        Job_level()


    def AAt1_data_pg(self):
        self.Att3_data_frm = customtkinter.CTkFrame(self.page_frame)
        self.Att3_data_frm.pack(fill=customtkinter.BOTH, expand=True)


        upper_frame = customtkinter.CTkFrame(self.Att3_data_frm)
        upper_frame.pack(fill='both', expand=True)
        print("Upper frame packed.")

        Lower_frame = customtkinter.CTkFrame(self.Att3_data_frm)
        Lower_frame.pack(fill='both', expand=True)
        print("Lower frame packed.")


        def Attrition_by_wkngyrs():
            try:
                with self.engine.connect() as connection:
                    query = text("SELECT a.TotalWorkingYears, COUNT(*) numofemployees "
                                "FROM (SELECT TotalWorkingYears FROM employeedata WHERE Attrition = 'Yes') a "
                                "GROUP BY TotalWorkingYears "
                                "ORDER BY TotalWorkingYears;")
                    Att_by_wrkngyrs = connection.execute(query)
                    Att_by_wrkngyrs = pd.DataFrame(Att_by_wrkngyrs.fetchall(), columns=Att_by_wrkngyrs.keys())
                    print(Att_by_wrkngyrs.head())

            except exc.SQLAlchemyError as e:
                messagebox.showerror("Error", f"Database query failed: {str(e)}")
                return  # Exit the function if there's an error
            
            Att_by_wrkngyrs['numofenployees'] = pd.to_numeric(Att_by_wrkngyrs['numofemployees'], errors='coerce')

            fig, ax = plt.subplots()

            try:
                Att_by_wrkngyrs.plot(ax=ax, kind='bar',x="TotalWorkingYears", y="numofemployees", color=['darkslateblue'], edgecolor='black', legend=False)

                # Set title and labels
                ax.set_title("Attrition by total working years", fontsize=10)
                ax.tick_params(axis='x', rotation=0)
                ax.tick_params(axis='x', labelsize=6)
                ax.tick_params(axis='y', labelsize=6)
                for spine in ax.spines.values():
                    spine.set_visible(False)
                ax.set_xlabel("")
                # ax.set_ylabel("Number of Employees")
                
                #print("Plot created successfully.")
            except Exception as e:
                print(f"Plotting error: {e}")


            canvas = FigureCanvasTkAgg(fig, upper_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True)
            print("Canvas added to the upper frame.")

        Attrition_by_wkngyrs()


        def Attrition_by_yrsatcomp():
            try:
                with self.engine.connect() as connection:
                    query = text("SELECT a.YearsAtCompany, COUNT(*) numofemployees "
                                "FROM (SELECT YearsAtCompany FROM employeedata WHERE Attrition = 'Yes') a "
                                "GROUP BY YearsAtCompany "
                                "ORDER BY YearsAtCompany;")
                    Att_by_yrsatcomp = connection.execute(query)
                    Att_by_yrsatcomp = pd.DataFrame(Att_by_yrsatcomp.fetchall(), columns=Att_by_yrsatcomp.keys())
                    print(Att_by_yrsatcomp.head())

            except exc.SQLAlchemyError as e:
                messagebox.showerror("Error", f"Database query failed: {str(e)}")
                return  # Exit the function if there's an error
            
            Att_by_yrsatcomp['numofenployees'] = pd.to_numeric(Att_by_yrsatcomp['numofemployees'], errors='coerce')

            fig, ax = plt.subplots()

            try:
                Att_by_yrsatcomp.plot(ax=ax, kind='bar',x="YearsAtCompany", y="numofemployees", color=['darkslateblue'], edgecolor='black', legend=False)

                # Set title and labels
                ax.set_title("Attrition by total years at company", fontsize=10)
                ax.tick_params(axis='x', rotation=0)
                ax.tick_params(axis='x', labelsize=6)
                ax.tick_params(axis='y', labelsize=6)
                for spine in ax.spines.values():
                    spine.set_visible(False)
                ax.set_xlabel("")
                # ax.set_ylabel("Number of Employees")
                
                #print("Plot created successfully.")
            except Exception as e:
                print(f"Plotting error: {e}")


            canvas = FigureCanvasTkAgg(fig, Lower_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True)
            print("Canvas added to the upper frame.")

        Attrition_by_yrsatcomp()



    def Att2_data_pg(self):
        self.Att2_data_frm = customtkinter.CTkFrame(self.page_frame)
        self.Att2_data_frm.pack(fill=customtkinter.BOTH, expand=True)

        upper_frame = customtkinter.CTkFrame(self.Att2_data_frm)
        upper_frame.pack(fill='both', expand=True)
        print("Upper frame packed.")

        Lower_frame = customtkinter.CTkFrame(self.Att2_data_frm)
        Lower_frame.pack(fill='both', expand=True)
        print("Lower frame packed.")

        def Attrition_by_yrswthcurrmngr():
            try:
                with self.engine.connect() as connection:
                    query = text("SELECT a.YearsWithCurrManager, COUNT(*) numofemployees "
                                "FROM (SELECT YearsWithCurrManager FROM employeedata WHERE Attrition = 'Yes') a "
                                "GROUP BY YearsWithCurrManager "
                                "ORDER BY YearsWithCurrManager;")
                    Att_by_yrswthcurrmngr = connection.execute(query)
                    Att_by_yrswthcurrmngr = pd.DataFrame(Att_by_yrswthcurrmngr.fetchall(), columns=Att_by_yrswthcurrmngr.keys())
                    print(Att_by_yrswthcurrmngr.head())

            except exc.SQLAlchemyError as e:
                messagebox.showerror("Error", f"Database query failed: {str(e)}")
                return  # Exit the function if there's an error
            
            Att_by_yrswthcurrmngr['numofenployees'] = pd.to_numeric(Att_by_yrswthcurrmngr['numofemployees'], errors='coerce')

            fig, ax = plt.subplots()

            try:
                Att_by_yrswthcurrmngr.plot(ax=ax, kind='bar',x="YearsWithCurrManager", y="numofemployees", color=['darkslateblue'], edgecolor='black', legend=False)

                # Set title and labels
                ax.set_title("Attrition by total years with current manager", fontsize=10)
                ax.tick_params(axis='x', rotation=0)
                ax.tick_params(axis='x', labelsize=6)
                ax.tick_params(axis='y', labelsize=6)
                for spine in ax.spines.values():
                    spine.set_visible(False)
                ax.set_xlabel("")
                # ax.set_ylabel("Number of Employees")
                
                #print("Plot created successfully.")
            except Exception as e:
                print(f"Plotting error: {e}")


            canvas = FigureCanvasTkAgg(fig, upper_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True)
            print("Canvas added to the upper frame.")

        Attrition_by_yrswthcurrmngr()


        def Attrition_by_yrspromo():
            try:
                with self.engine.connect() as connection:
                    query = text("SELECT a.YearsSinceLastPromotion, COUNT(*) numofemployees "
                                "FROM (SELECT YearsSinceLastPromotion FROM employeedata WHERE Attrition = 'Yes') a "
                                "GROUP BY YearsSinceLastPromotion "
                                "ORDER BY YearsSinceLastPromotion;")
                    Att_by_yrspromo = connection.execute(query)
                    Att_by_yrspromo = pd.DataFrame(Att_by_yrspromo.fetchall(), columns=Att_by_yrspromo.keys())
                    print(Att_by_yrspromo.head())

            except exc.SQLAlchemyError as e:
                messagebox.showerror("Error", f"Database query failed: {str(e)}")
                return  # Exit the function if there's an error
            
            Att_by_yrspromo['numofenployees'] = pd.to_numeric(Att_by_yrspromo['numofemployees'], errors='coerce')

            fig, ax = plt.subplots()

            try:
                Att_by_yrspromo.plot(ax=ax, kind='bar',x="YearsSinceLastPromotion", y="numofemployees", color=['darkslateblue'], edgecolor='black', legend=False)

                # Set title and labels
                ax.set_title("Attrition by total years since last promotion", fontsize=10)
                ax.tick_params(axis='x', rotation=0)
                ax.tick_params(axis='x', labelsize=6)
                ax.tick_params(axis='y', labelsize=6)
                for spine in ax.spines.values():
                    spine.set_visible(False)
                ax.set_xlabel("")
                # ax.set_ylabel("Number of Employees")
                
                #print("Plot created successfully.")
            except Exception as e:
                print(f"Plotting error: {e}")


            canvas = FigureCanvasTkAgg(fig, Lower_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True)
            print("Canvas added to the upper frame.")

        Attrition_by_yrspromo()


    def Att3_data_pg(self):
        self.Att3_data_frm = customtkinter.CTkFrame(self.page_frame)
        self.Att3_data_frm.pack(fill=customtkinter.BOTH, expand=True)


        upper_frame = customtkinter.CTkFrame(self.Att3_data_frm)
        upper_frame.pack(fill='both', expand=True)
        print("Upper frame packed.")

        lower_frame = customtkinter.CTkFrame(self.Att3_data_frm)
        lower_frame.pack(fill='both', expand=True)
        print("Lower frame packed.")

        def Attrition_by_Educationfield():
            try:
                with self.engine.connect() as connection:
                    query = text("SELECT a.EducationField, COUNT(*) numofemployees "
                                "FROM (SELECT EducationField FROM employeedata WHERE Attrition = 'Yes') a " 
                                "GROUP BY EducationField ORDER BY numofemployees ASC;")
                    Att_by_educationfield = connection.execute(query)
                    Att_by_educationfield = pd.DataFrame(Att_by_educationfield.fetchall(), columns=Att_by_educationfield.keys())
                    print(Att_by_educationfield.head())

            except exc.SQLAlchemyError as e:
                messagebox.showerror("Error", f"Database query failed: {str(e)}")
                return  # Exit the function if there's an error
            
            Att_by_educationfield['numofenployees'] = pd.to_numeric(Att_by_educationfield['numofemployees'], errors='coerce')

            fig, ax = plt.subplots()

            try:
                Att_by_educationfield.plot(ax=ax, kind='bar',x="EducationField", y="numofemployees", color=['darkslateblue'], edgecolor='black', legend=False)

                # Set title and labels
                ax.set_title("Attrition by Education Field", fontsize=10)
                ax.tick_params(axis='x', rotation=0)
                ax.tick_params(axis='x', labelsize=6)
                ax.tick_params(axis='y', labelsize=6)
                for spine in ax.spines.values():
                    spine.set_visible(False)
                ax.set_xlabel("")
                # ax.set_ylabel("Number of Employees")
                
                #print("Plot created successfully.")
            except Exception as e:
                print(f"Plotting error: {e}")


            canvas = FigureCanvasTkAgg(fig, upper_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True)
            print("Canvas added to the upper frame.")

        Attrition_by_Educationfield()


        def Attrition_by_joblevel():
            try:
                with self.engine.connect() as connection:
                    query = text("SELECT a.JobLevel, COUNT(*) numofemployees "
                                "FROM (SELECT JobLevel FROM employeedata WHERE Attrition = 'Yes') a GROUP BY JobLevel "
                                "ORDER BY JobLevel ASC;")
                    Att_by_joblevel = connection.execute(query)
                    Att_by_joblevel = pd.DataFrame(Att_by_joblevel.fetchall(), columns=Att_by_joblevel.keys())
                    print(Att_by_joblevel.head())

            except exc.SQLAlchemyError as e:
                messagebox.showerror("Error", f"Database query failed: {str(e)}")
                return  # Exit the function if there's an error
            
            Att_by_joblevel['numofenployees'] = pd.to_numeric(Att_by_joblevel['numofemployees'], errors='coerce')

            fig, ax = plt.subplots()

            try:
                Att_by_joblevel.plot(ax=ax, kind='bar',x="JobLevel", y="numofemployees", color=['darkslateblue'], edgecolor='black', legend=False)

                # Set title and labels
                ax.set_title("Attrition by Job Level", fontsize=10)
                ax.tick_params(axis='x', rotation=0)
                ax.tick_params(axis='x', labelsize=6)
                ax.tick_params(axis='y', labelsize=6)
                for spine in ax.spines.values():
                    spine.set_visible(False)
                ax.set_xlabel("")
                # ax.set_ylabel("Number of Employees")
                
                #print("Plot created successfully.")
            except Exception as e:
                print(f"Plotting error: {e}")


            canvas = FigureCanvasTkAgg(fig, upper_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True)
            print("Canvas added to the upper frame.")

        Attrition_by_joblevel()

        def Attrition_by_jobRole():
            try:
                with self.engine.connect() as connection:
                    query = text("SELECT a.JobRole, COUNT(*) numofemployees FROM (SELECT JobRole "
                                "FROM employeedata WHERE Attrition = 'Yes') a "
                                "GROUP BY JobRole ORDER BY numofemployees;")
                    Att_by_jobrole = connection.execute(query)
                    Att_by_jobrole = pd.DataFrame(Att_by_jobrole.fetchall(), columns=Att_by_jobrole.keys())
                    print(Att_by_jobrole.head())

            except exc.SQLAlchemyError as e:
                messagebox.showerror("Error", f"Database query failed: {str(e)}")
                return  # Exit the function if there's an error
            
            Att_by_jobrole['numofenployees'] = pd.to_numeric(Att_by_jobrole['numofemployees'], errors='coerce')

            fig, ax = plt.subplots(figsize=(10, 7))

            try:
                Att_by_jobrole.plot(ax=ax, kind='bar',x="JobRole", y="numofemployees", color=['darkslateblue'], edgecolor='black', legend=False)

                # Set title and labels
                ax.set_title("Attrition by Job Role", fontsize=10)
                ax.tick_params(axis='x', rotation=0)
                ax.tick_params(axis='x', labelsize=6)
                ax.tick_params(axis='y', labelsize=6)
                for spine in ax.spines.values():
                    spine.set_visible(False)
                ax.set_xlabel("")
                # ax.set_ylabel("Number of Employees")
                
                #print("Plot created successfully.")
            except Exception as e:
                print(f"Plotting error: {e}")


            canvas = FigureCanvasTkAgg(fig, lower_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True)
            print("Canvas added to the upper frame.")

        Attrition_by_jobRole()


        def Attrition_by_dep():
            try:
                with self.engine.connect() as connection:
                    query = text("SELECT a.Department, COUNT(*) as numofemployees "
                                "FROM (SELECT Department FROM employeedata WHERE Attrition = 'Yes') a "
                                "GROUP BY Department ORDER BY numofemployees;")
                    Att_by_dep = connection.execute(query)
                    Att_by_dep = pd.DataFrame(Att_by_dep.fetchall(), columns=Att_by_dep.keys())
                    print(Att_by_dep.head())

            except exc.SQLAlchemyError as e:
                messagebox.showerror("Error", f"Database query failed: {str(e)}")
                return  # Exit the function if there's an error
            
            Att_by_dep['numofenployees'] = pd.to_numeric(Att_by_dep['numofemployees'], errors='coerce')

            fig, ax = plt.subplots(figsize=(2, 2))

            try:
                Att_by_dep.plot(ax=ax, kind='bar',x="Department", y="numofemployees", color=['darkslateblue'], edgecolor='black', legend=False)

                # Set title and labels
                ax.set_title("Attrition by Department", fontsize=10)
                ax.tick_params(axis='x', rotation=0)
                ax.tick_params(axis='x', labelsize=6)
                ax.tick_params(axis='y', labelsize=6)
                for spine in ax.spines.values():
                    spine.set_visible(False)
                ax.set_xlabel("")
                # ax.set_ylabel("Number of Employees")
                
                #print("Plot created successfully.")
            except Exception as e:
                print(f"Plotting error: {e}")


            canvas = FigureCanvasTkAgg(fig, lower_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True)
            print("Canvas added to the upper frame.")


        Attrition_by_dep()



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