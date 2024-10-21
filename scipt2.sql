ALTER TABLE employee_survey_data
ADD FOREIGN KEY employee_fk(EmployeeID) REFERENCES employee_data(EmployeeID);

ALTER TABLE manager_survey_data
ADD FOREIGN KEY employee_fk2(EmployeeID) REFERENCES employee_data(EmployeeID);

SELECT * FROM employee_data;

DROP TABLE employee_survey_data;
DROP TABLE manager_survey_data;
DROP TABLE employee_data;
