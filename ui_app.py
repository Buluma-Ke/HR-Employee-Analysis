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
        self.title("HR Employees Analysis!")
        self.geometry("600x400")
        
        self.engine = engine

        self.page_frame = customtkinter.CTkFrame(self)
        self.page_frame.pack(side=customtkinter.RIGHT, fill=customtkinter.BOTH, expand=True)


        self.menu_bar_frame = customtkinter.CTkFrame(self)
        self.menu_bar_frame.pack(side=customtkinter.LEFT, fill=customtkinter.Y, pady=4, padx=3)
        self.menu_bar_frame.pack_propagate(flag=True)

        self.buttons = []

        # Define original colors for buttons
        self.original_colors = {
            "General Data": "gray1",
            "Employee Survey": "gray5",
            "Manager Survey": "gray10",
            "Demographic Insights": "gray15",
            "Compensation Analysis": "gray20",
            "Attrition Analysis 1": "gray23",
            "Attrition Analysis 2": "gray25",
            "Attrition Analysis 3": "gray30"
        }

        # Create buttons
        for text, color in self.original_colors.items():
            self.create_button(text, color)

        # Initially show the general data page
        self.show_frame(self.general_data_pg)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # Handles window closing

    def create_button(self, text, color):
        button = customtkinter.CTkButton(master=self.menu_bar_frame,
                                           command=lambda: self.on_button_click(button, text),
                                           text=text, fg_color=color)
        button.pack(padx=4, pady=10)
        self.buttons.append(button)

    def on_button_click(self, button, button_text):
        # Reset all button colors to original
        for btn in self.buttons:
            btn.configure(fg_color=self.original_colors[btn.cget("text")])  # Reset to original color

        # Change the clicked button's color to indicate selection
        button.configure(fg_color="darkslateblue")  
        # Show the corresponding frame
        self.show_frame(getattr(self, f"{button_text.replace(' ', '_').lower()}_pg"))

    def show_frame(self, frame_func):
        # Clear current frame
        for widget in self.page_frame.winfo_children():
            widget.destroy()
        
        frame_func()


    def general_data_pg(self): 

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

            # Add a scrollbar for the Treeview
            yscrollbar = ttk.Scrollbar(self.gen_data_frm, orient="vertical", command=tree.yview)
            tree.configure(yscroll=yscrollbar.set)
            yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)


            # Pack the Treeview  after adding the scrollbar
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        except exc.SQLAlchemyError as e:
            print(e)
            messagebox.showerror("Error", f"Database query failed: {str(e)}")

    def employee_survey_pg(self):
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

            # Add a scrollbar for the Treeview
            yscrollbar = ttk.Scrollbar(self.Emp_data_frm, orient="vertical", command=tree.yview)
            tree.configure(yscroll=yscrollbar.set)
            yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        except exc.SQLAlchemyError as e:
            print(e)
            messagebox.showerror("Error", f"Database query failed: {str(e)}")


    def manager_survey_pg(self):
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

            # Add a scrollbar for the Treeview
            yscrollbar = ttk.Scrollbar(self.Mngr_data_frm, orient="vertical", command=tree.yview)
            tree.configure(yscroll=yscrollbar.set)
            yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        except exc.SQLAlchemyError as e:
            print(e)
            messagebox.showerror("Error", f"Database query failed: {str(e)}")



    def demographic_insights_pg(self):
        
        self.Att3_data_frm = customtkinter.CTkFrame(self.page_frame)
        self.Att3_data_frm.pack(fill=customtkinter.BOTH, expand=True)  # Ensure the frame is packed

        upper_frame = customtkinter.CTkFrame(self.Att3_data_frm)
        upper_frame.pack(fill='both', expand=True)

        Lower_frame = customtkinter.CTkFrame(self.Att3_data_frm)
        Lower_frame.pack(fill='both', expand=True)

        # Fetch gender distribution data
        def depertment():
            try:
                with self.engine.connect() as connection:
                    query = text("SELECT Department, Gender, COUNT(*) numofemployees "
                                "FROM employeedata " 
                                "GROUP BY Department, Gender "
                                "ORDER BY numofemployees;")
                    gender_dist_dept = connection.execute(query)
                    gender_dist_dept = pd.DataFrame(gender_dist_dept.fetchall(), columns=gender_dist_dept.keys())

            except exc.SQLAlchemyError as e:
                messagebox.showerror("Error", f"Database query failed: {str(e)}")
                return  # Exit the function if there's an error

            # Create a bar plot using Matplotlib
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

                for spine in ax.spines.values(): # remove the frames
                    spine.set_visible(False)

                ax.set_xlabel("")
                ax.legend(title='Gender')
                
            except Exception as e:
                print(f"Plotting error: {e}")


            canvas = FigureCanvasTkAgg(fig, upper_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True)
        
        depertment()

                # Fetch gender distribution data
        def education_field():
            try:
                with self.engine.connect() as connection:

                    query = text("SELECT EducationField,Gender, COUNT(*) numofemployees "
                                "FROM employeedata " 
                                "GROUP BY EducationField, Gender "
                                "ORDER BY numofemployees;")
                    
                    gender_dist_edfield = connection.execute(query)
                    gender_dist_edfield = pd.DataFrame(gender_dist_edfield.fetchall(), columns=gender_dist_edfield.keys())

            except exc.SQLAlchemyError as e:
                print(f"Database query error: {e}")
                messagebox.showerror("Error", f"Database query failed: {str(e)}")
                return  # Exit the function if there's an error

            # Create a bar plot using Matplotlib
            fig, ax = plt.subplots()

            # Pivot the DataFrame for plotting
            pivot_df = gender_dist_edfield.pivot(index='EducationField', columns='Gender', values='numofemployees').fillna(0)

            try:
                pivot_df.plot(kind='bar', ax=ax, color=['slateblue', 'darkslateblue'], edgecolor='black', legend=False)

                # Set title and labels
                ax.set_title("Gender Distribution per EducationField", fontsize=8)
                ax.tick_params(axis='x', rotation=0)
                ax.tick_params(axis='x', labelsize=6)
                ax.tick_params(axis='y', labelsize=6)

                for spine in ax.spines.values(): # remove the frames
                    spine.set_visible(False)

                ax.set_xlabel("")

            except Exception as e:
                print(f"Plotting error: {e}")


            canvas = FigureCanvasTkAgg(fig, upper_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="right", fill="both", expand=True)

        education_field()


        def Job_Level():
            try:
                with self.engine.connect() as connection:

                    query = text("SELECT JobLevel,Gender, COUNT(*) numofemployees "
                                    "FROM employeedata "
                                    "GROUP BY JobLevel, Gender "
                                    "ORDER BY JobLevel, Gender, numofemployees;")
                    
                    gender_dist_Joblevel = connection.execute(query)
                    gender_dist_Joblevel = pd.DataFrame(gender_dist_Joblevel.fetchall(), columns=gender_dist_Joblevel.keys())

            except exc.SQLAlchemyError as e:
                print(f"Database query error: {e}")
                messagebox.showerror("Error", f"Database query failed: {str(e)}")
                return  # Exit the function if there's an error

            # Create a bar plot using Matplotlib
            fig, ax = plt.subplots(figsize=(2, 2))

            # Pivot the DataFrame for plotting
            pivot_df = gender_dist_Joblevel.pivot(index='JobLevel', columns='Gender', values='numofemployees').fillna(0)

            try:
                pivot_df.plot(kind='bar', ax=ax, color=['slateblue', 'darkslateblue'], edgecolor='black', legend=False)

                # Set title and labels
                ax.set_title("Gender Distribution per Job Level", fontsize=8)
                ax.tick_params(axis='x', rotation=0)
                ax.tick_params(axis='x', labelsize=6)
                ax.tick_params(axis='y', labelsize=6)

                for spine in ax.spines.values():  # remove the frames
                    spine.set_visible(False)

                ax.set_xlabel("")

            except Exception as e:
                print(f"Plotting error: {e}")

            canvas = FigureCanvasTkAgg(fig, Lower_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="right", fill="both", expand=True)

        Job_Level()


        def Job_Role():
            try:
                with self.engine.connect() as connection:

                    query = text("SELECT JobRole,Gender, COUNT(*) numofemployees "
                                    "FROM employeedata "
                                    "GROUP BY JobRole, Gender "
                                    "ORDER BY numofemployees;")
                    
                    gender_dist_JobRole = connection.execute(query)
                    gender_dist_JobRole = pd.DataFrame(gender_dist_JobRole.fetchall(), columns=gender_dist_JobRole.keys())

            except exc.SQLAlchemyError as e:
                print(f"Database query error: {e}")
                messagebox.showerror("Error", f"Database query failed: {str(e)}")
                return  # Exit the function if there's an error

            # Create a bar plot using Matplotlib
            fig, ax = plt.subplots(figsize=(10, 7))

            # Pivot the DataFrame for plotting
            pivot_df = gender_dist_JobRole.pivot(index='JobRole', columns='Gender', values='numofemployees').fillna(0)

            try:
                pivot_df.plot(kind='bar', ax=ax, color=['slateblue', 'darkslateblue'], edgecolor='black', legend=False)

                # Set title and labels
                ax.set_title("Gender Distribution per Job Role", fontsize=8)
                ax.tick_params(axis='x', rotation=0)
                ax.tick_params(axis='x', labelsize=6)
                ax.tick_params(axis='y', labelsize=6)

                for spine in ax.spines.values(): # remove the frames
                    spine.set_visible(False)

                ax.set_xlabel("")

            except Exception as e:
                print(f"Plotting error: {e}")

            canvas = FigureCanvasTkAgg(fig, Lower_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="right", fill="both", expand=True)

        Job_Role()


    def compensation_analysis_pg(self):
        self.Att3_data_frm = customtkinter.CTkFrame(self.page_frame)
        self.Att3_data_frm.pack(fill=customtkinter.BOTH, expand=True)

        upper_frame = customtkinter.CTkFrame(self.Att3_data_frm)
        upper_frame.pack(fill='both', expand=True)

        Lower_frame = customtkinter.CTkFrame(self.Att3_data_frm)
        Lower_frame.pack(fill='both', expand=True)


        def depertment():
            try:
                with self.engine.connect() as connection:

                    query = text("SELECT Department, AVG(MonthlyIncome) AvgMonthlyincome "
                                    "FROM employeedata "
                                    "GROUP BY Department "
                                    "ORDER BY AvgMonthlyincome;")
                    
                    Avg_dep_sal = connection.execute(query)
                    Avg_dep_sal = pd.DataFrame(Avg_dep_sal.fetchall(), columns=Avg_dep_sal.keys())

            except exc.SQLAlchemyError as e:
                messagebox.showerror("Error", f"Database query failed: {str(e)}")
                return  # Exit the function if there's an error
            
            Avg_dep_sal['AvgMonthlyincome'] = pd.to_numeric(Avg_dep_sal['AvgMonthlyincome'], errors='coerce')

            fig, ax = plt.subplots()
    
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

            except Exception as e:
                print(f"Plotting error: {e}")

            canvas = FigureCanvasTkAgg(fig, upper_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True)
        
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

            except exc.SQLAlchemyError as e:
                messagebox.showerror("Error", f"Database query failed: {str(e)}")
                return  # Exit the function if there's an error
            
            Avg_edfield_sal['AvgMonthlyincome'] = pd.to_numeric(Avg_edfield_sal['AvgMonthlyincome'], errors='coerce')

            fig, ax = plt.subplots()

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

            except Exception as e:
                print(f"Plotting error: {e}")


            canvas = FigureCanvasTkAgg(fig, upper_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True)

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

            except exc.SQLAlchemyError as e:
                messagebox.showerror("Error", f"Database query failed: {str(e)}")
                return  # Exit the function if there's an error
            
            Avg_joblevel_sal['AvgMonthlyincome'] = pd.to_numeric(Avg_joblevel_sal['AvgMonthlyincome'], errors='coerce')

            fig, ax = plt.subplots(figsize=(3, 3))

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

            except Exception as e:
                print(f"Plotting error: {e}")


            canvas = FigureCanvasTkAgg(fig, Lower_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True)
        

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

            except exc.SQLAlchemyError as e:
                messagebox.showerror("Error", f"Database query failed: {str(e)}")
                return  # Exit the function if there's an error
            
            Avg_joblRole_sal['AvgMonthlyincome'] = pd.to_numeric(Avg_joblRole_sal['AvgMonthlyincome'], errors='coerce')

            fig, ax = plt.subplots(figsize=(10, 7))


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

            except Exception as e:
                print(f"Plotting error: {e}")


            canvas = FigureCanvasTkAgg(fig, Lower_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True)

        Job_Role()
        Job_level()


    def attrition_analysis_1_pg(self):
        self.Att3_data_frm = customtkinter.CTkFrame(self.page_frame)
        self.Att3_data_frm.pack(fill=customtkinter.BOTH, expand=True)


        upper_frame = customtkinter.CTkFrame(self.Att3_data_frm)
        upper_frame.pack(fill='both', expand=True)

        Lower_frame = customtkinter.CTkFrame(self.Att3_data_frm)
        Lower_frame.pack(fill='both', expand=True)


        def Attrition_by_wkngyrs():
            try:
                with self.engine.connect() as connection:

                    query = text("SELECT a.TotalWorkingYears, COUNT(*) numofemployees "
                                "FROM (SELECT TotalWorkingYears FROM employeedata WHERE Attrition = 'Yes') a "
                                "GROUP BY TotalWorkingYears "
                                "ORDER BY TotalWorkingYears;")
                    
                    Att_by_wrkngyrs = connection.execute(query)
                    Att_by_wrkngyrs = pd.DataFrame(Att_by_wrkngyrs.fetchall(), columns=Att_by_wrkngyrs.keys())

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

            except Exception as e:
                print(f"Plotting error: {e}")


            canvas = FigureCanvasTkAgg(fig, upper_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True)

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
                
            except Exception as e:
                print(f"Plotting error: {e}")


            canvas = FigureCanvasTkAgg(fig, Lower_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True)

        Attrition_by_yrsatcomp()



    def attrition_analysis_2_pg(self):
        self.Att2_data_frm = customtkinter.CTkFrame(self.page_frame)
        self.Att2_data_frm.pack(fill=customtkinter.BOTH, expand=True)

        upper_frame = customtkinter.CTkFrame(self.Att2_data_frm)
        upper_frame.pack(fill='both', expand=True)

        Lower_frame = customtkinter.CTkFrame(self.Att2_data_frm)
        Lower_frame.pack(fill='both', expand=True)

        def Attrition_by_yrswthcurrmngr():
            try:
                with self.engine.connect() as connection:

                    query = text("SELECT a.YearsWithCurrManager, COUNT(*) numofemployees "
                                "FROM (SELECT YearsWithCurrManager FROM employeedata WHERE Attrition = 'Yes') a "
                                "GROUP BY YearsWithCurrManager "
                                "ORDER BY YearsWithCurrManager;")
                    
                    Att_by_yrswthcurrmngr = connection.execute(query)
                    Att_by_yrswthcurrmngr = pd.DataFrame(Att_by_yrswthcurrmngr.fetchall(), columns=Att_by_yrswthcurrmngr.keys())

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

            except Exception as e:
                print(f"Plotting error: {e}")


            canvas = FigureCanvasTkAgg(fig, upper_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True)

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

            except Exception as e:
                print(f"Plotting error: {e}")


            canvas = FigureCanvasTkAgg(fig, Lower_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True)

        Attrition_by_yrspromo()


    def attrition_analysis_3_pg(self):
        self.Att3_data_frm = customtkinter.CTkFrame(self.page_frame)
        self.Att3_data_frm.pack(fill=customtkinter.BOTH, expand=True)


        upper_frame = customtkinter.CTkFrame(self.Att3_data_frm)
        upper_frame.pack(fill='both', expand=True)

        lower_frame = customtkinter.CTkFrame(self.Att3_data_frm)
        lower_frame.pack(fill='both', expand=True)

        def Attrition_by_Educationfield():
            try:
                with self.engine.connect() as connection:

                    query = text("SELECT a.EducationField, COUNT(*) numofemployees "
                                "FROM (SELECT EducationField FROM employeedata WHERE Attrition = 'Yes') a " 
                                "GROUP BY EducationField ORDER BY numofemployees ASC;")
                    
                    Att_by_educationfield = connection.execute(query)
                    Att_by_educationfield = pd.DataFrame(Att_by_educationfield.fetchall(), columns=Att_by_educationfield.keys())

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

            except Exception as e:
                print(f"Plotting error: {e}")


            canvas = FigureCanvasTkAgg(fig, upper_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True)


        Attrition_by_Educationfield()


        def Attrition_by_joblevel():
            try:
                with self.engine.connect() as connection:

                    query = text("SELECT a.JobLevel, COUNT(*) numofemployees "
                                "FROM (SELECT JobLevel FROM employeedata WHERE Attrition = 'Yes') a GROUP BY JobLevel "
                                "ORDER BY JobLevel ASC;")
                    
                    Att_by_joblevel = connection.execute(query)
                    Att_by_joblevel = pd.DataFrame(Att_by_joblevel.fetchall(), columns=Att_by_joblevel.keys())

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

            except Exception as e:
                print(f"Plotting error: {e}")


            canvas = FigureCanvasTkAgg(fig, upper_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True)

        Attrition_by_joblevel()

        def Attrition_by_jobRole():
            try:
                with self.engine.connect() as connection:

                    query = text("SELECT a.JobRole, COUNT(*) numofemployees FROM (SELECT JobRole "
                                "FROM employeedata WHERE Attrition = 'Yes') a "
                                "GROUP BY JobRole ORDER BY numofemployees;")
                    
                    Att_by_jobrole = connection.execute(query)
                    Att_by_jobrole = pd.DataFrame(Att_by_jobrole.fetchall(), columns=Att_by_jobrole.keys())

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
        
            except Exception as e:
                print(f"Plotting error: {e}")


            canvas = FigureCanvasTkAgg(fig, lower_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True)

        Attrition_by_jobRole()


        def Attrition_by_dep():
            try:
                with self.engine.connect() as connection:

                    query = text("SELECT a.Department, COUNT(*) as numofemployees "
                                "FROM (SELECT Department FROM employeedata WHERE Attrition = 'Yes') a "
                                "GROUP BY Department ORDER BY numofemployees;")
                    
                    Att_by_dep = connection.execute(query)
                    Att_by_dep = pd.DataFrame(Att_by_dep.fetchall(), columns=Att_by_dep.keys())

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
              
            except Exception as e:
                print(f"Plotting error: {e}")


            canvas = FigureCanvasTkAgg(fig, lower_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True)


        Attrition_by_dep()

    def on_closing(self):
    #a confirmation dialog before closing
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()  # This will close the Toplevel window
            self.master.destroy()



class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.title("LOGIN")
        self.geometry("600x400")


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