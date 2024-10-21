SELECT * FROM employeedata;
-- DROP TABLE employeedata;
ALTER TABLE employeedata
DROP COLUMN MyUnknownColumn;

-- DROP TABLE employeedata;

SELECT COLUMN_NAME, DATA_TYPE
  FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_NAME = "employeedata";
  
SELECT DISTINCT Attrition
  FROM employeedata;
  
ALTER TABLE employeedata
  MODIFY COLUMN Attrition VARCHAR(25);
ALTER TABLE employeedata
  MODIFY COLUMN BusinessTravel VARCHAR(25);
ALTER TABLE employeedata
  MODIFY COLUMN Department VARCHAR(25);
ALTER TABLE employeedata
  MODIFY COLUMN EducationField VARCHAR(25);
ALTER TABLE employeedata
  MODIFY COLUMN Gender VARCHAR(25);
ALTER TABLE employeedata
  MODIFY COLUMN JobRole VARCHAR(25);
ALTER TABLE employeedata
  MODIFY COLUMN MaritalStatus VARCHAR(25);
ALTER TABLE employeedata
  MODIFY COLUMN Attrition VARCHAR(25);
ALTER TABLE employeedata
  MODIFY COLUMN Over18 VARCHAR(25);
ALTER TABLE employeedata
  MODIFY COLUMN NumCompaniesWorked int;
ALTER TABLE employeedata
  MODIFY COLUMN TotalWorkingYears int;
  
(SELECT * 
  FROM employeedata
 LIMIT 1 OFFSET 210)
UNION ALL
(SELECT * 
  FROM employeedata
 LIMIT 1 OFFSET 138);

UPDATE employeedata
   SET NumCompaniesWorked = NULL
 WHERE NumCompaniesWorked = ' ';

ALTER TABLE employeedata
  ADD CONSTRAINT pk_empID PRIMARY KEY (EmployeeID);

ALTER TABLE employeedata
  ADD CONSTRAINT gender_const
  CHECK (Gender = "Male" OR Gender = "Female");

ALTER TABLE employeedata
  ADD CONSTRAINT Attrition_const
  CHECK (Attrition = "Yes" OR Attrition = "No");

SELECT * 
  FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS
  WHERE TABLE_NAME = "employeedata";
  
SELECT * FROM employee_survey;

SELECT COLUMN_NAME, DATA_TYPE
  FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_NAME = "employee_survey";
  
ALTER TABLE employee_survey
  DROP COLUMN MyUnknownColumn;
ALTER TABLE employee_survey
  MODIFY COLUMN EnvironmentSatisfaction int;
ALTER TABLE employee_survey
  MODIFY COLUMN JobSatisfaction int;
ALTER TABLE employee_survey
  MODIFY COLUMN WorkLifeBalance int;
  
ALTER TABLE employee_survey
  ADD CONSTRAINT emp_surv_fk FOREIGN KEY(EmployeeID) REFERENCES employeedata(EmployeeID);

SELECT * FROM employee_survey;

/* ALTER TABLE employeedata
DROP primary key;*/

-- DROP TABLE employee_survey, employeedata, gmanager;*/