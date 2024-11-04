 **EMPLOYEE**  **DATA**  **ANALYIS**

The dataset contains three tables;
    General data - gives us important individual employee details eg, age, employee id, Attrition, deparment etc
    employee survey - a survey was done among the employees in it we get usefull insights such as -environment satisfaction
                                                                                                - Job satisfaction
                                                                                                - Worklife balance
    Manager Survey data - The same survey was done among the managers highlighting each employees Job environment, rating and perfomance rating

From this we can get a complete breakdown of this; workplace, painting a Human Resorce picture of the typicall employee and why They might decide to get attrited.

**WHAT'S**  **THIS**  **ABOUT?**

I used Jupyter notebook to clean and do Extensive Data analysis on the three datasets, This was the tool of choice for its flexibility when handling data related tasks, Allowing me to get a deep dive undersanding of what we are working with. I loaded the data into a mysql database, which comes with all the perks of a relational database i.e easy querying of data allowing me to get accses and look at the data in a whole new dimension.

The findings of my Analysis are all presented in a graphical user interface, made  from python's customtkinter, This i chose because of python's ability to intergrate with other language ; mysql allowing me to query data directly from the mysql database. This findings can be easly accesed by the Human resource manager with the input of the database password, The ui displays the three datasets, and dashboards highlighting important aspects of the work environment, which will come in handy when making employee based decisions.

The biggest headache to any data based project is missing values, I avoided deleting any values, which would mean deleting employees, which wouldn't make sense, I logically filled in the ones I could, However of 4410 entries, around 20 rows with missing values wouldn't make a difference to my findings.

In the future i want to intergrate a machine learning algorithm that can better predict employee attrition, preventiong the loss of much needed talent within the organisation.
 