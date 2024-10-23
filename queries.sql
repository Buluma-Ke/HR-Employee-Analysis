-- Attrition analysis
SELECT Age, JobLevel, JobRole, Department, DistanceFromHome, 
       Gender, NumCompaniesWorked, PercentSalaryHike
  FROM employeedata
 WHERE Attrition = "Yes";
 
SELECT a.Department, COUNT(*)
  FROM (SELECT Department
		  FROM employeedata
		 WHERE Attrition = "Yes") a
 GROUP BY Department;
 
SELECT a.JobLevel, COUNT(*) numofemployees
  FROM (SELECT JobLevel
		  FROM employeedata
		 WHERE Attrition = 'Yes') a
  GROUP BY JobLevel
  ORDER BY JobLevel ASC;
  
  SELECT a.JobRole, COUNT(*) numofemployees
  FROM (SELECT JobRole
		  FROM employeedata
		 WHERE Attrition = 'Yes') a
  GROUP BY JobRole
  ORDER BY numofemployees DESC;
  
SELECT a.DistanceFromHome, COUNT(*) numofemployees
  FROM (SELECT DistanceFromHome
		  FROM employeedata
		 WHERE Attrition = 'Yes') a
 GROUP BY DistanceFromHome
 ORDER BY numofemployees DESC;


SELECT a.Age, COUNT(*) numofemployees
  FROM (SELECT Age
		  FROM employeedata
		 WHERE Attrition = 'Yes') a
 GROUP BY Age
 ORDER BY Age;
 

-- education field
SELECT a.EducationField, COUNT(*) numofemployees
  FROM (SELECT EducationField
		  FROM employeedata
		 WHERE Attrition = 'Yes') a
 GROUP BY EducationField
 ORDER BY numofemployees DESC;
 
 -- education level
 SELECT a.Education, COUNT(*) numofemployees
  FROM (SELECT Education
		  FROM employeedata
		 WHERE Attrition = 'Yes') a
 GROUP BY Education
 ORDER BY Education;
 
 -- Years since last promotion
SELECT a.YearsSinceLastPromotion, COUNT(*) numofemployees
  FROM (SELECT YearsSinceLastPromotion
		  FROM employeedata
		 WHERE Attrition = 'Yes') a
 GROUP BY YearsSinceLastPromotion
 ORDER BY YearsSinceLastPromotion;
 
 -- Years at company
SELECT a.YearsAtCompany, COUNT(*) numofemployees
  FROM (SELECT YearsAtCompany
		  FROM employeedata
		 WHERE Attrition = 'Yes') a
 GROUP BY YearsAtCompany
 ORDER BY numofemployees DESC;
 

-- Years with current manager
SELECT a.YearsWithCurrManager, COUNT(*) numofemployees
  FROM (SELECT YearsWithCurrManager
		  FROM employeedata
		 WHERE Attrition = 'Yes') a
 GROUP BY YearsWithCurrManager
 ORDER BY YearsWithCurrManager;
 
-- Total working years
SELECT a.TotalWorkingYears, COUNT(*) numofemployees
  FROM (SELECT TotalWorkingYears
		  FROM employeedata
		 WHERE Attrition = 'Yes') a
 GROUP BY TotalWorkingYears
 ORDER BY TotalWorkingYears;
 
 -- Gender
 SELECT a.Gender, COUNT(*) numofemployees
  FROM (SELECT Gender
		  FROM employeedata
		 WHERE Attrition = 'Yes') a
 GROUP BY Gender
 ORDER BY numofemployees;
 
 -- Demographic ensights
 
 SELECT Department, EducationField, JobRole, JobLevel, Gender
   FROM employeedata;
 
-- employee count by department
SELECT Department,Gender, COUNT(*) numofemployees
  FROM employeedata
 GROUP BY Department, Gender
 ORDER BY numofemployees;
 
 -- employee count by education field
SELECT EducationField,Gender, COUNT(*) numofemployees
  FROM employeedata
 GROUP BY EducationField, Gender
 ORDER BY numofemployees;
 
 -- employee count by Job Role
 SELECT JobRole,Gender, COUNT(*) numofemployees
  FROM employeedata
 GROUP BY JobRole, Gender
 ORDER BY numofemployees;
   
 -- employee count by Job Level
 SELECT JobLevel,Gender, COUNT(*) numofemployees
  FROM employeedata
 GROUP BY JobLevel, Gender
 ORDER BY JobLevel, Gender, numofemployees;
 
 -- Compensation Analysis
 SELECT Department, AVG(MonthlyIncome) AvgMonthlyincome
   FROM employeedata
  GROUP BY Department
  ORDER BY AvgMonthlyincome;
  
-- Avarage salary per department
 SELECT Department, AVG(MonthlyIncome) avg_monthly_income
   FROM employeedata
  GROUP BY Department
  ORDER BY avg_monthly_income DESC;
  
-- Average Monthly income by Education field
SELECT EducationField, AVG(MonthlyIncome) avg_monthly_income
  FROM employeedata
 GROUP BY EducationField
 ORDER BY avg_monthly_income DESC;
 
 -- Average Monthly income by Job role
SELECT JobRole, AVG(MonthlyIncome) avg_monthly_income
  FROM employeedata
 GROUP BY JobRole
 ORDER BY avg_monthly_income;
 
-- Average Monthly income by Job Level
SELECT JobLevel, AVG(MonthlyIncome) avg_monthly_income
  FROM employeedata
 GROUP BY JobLevel
 ORDER BY JobLevel;
 
 -- Salary hikes by Years at company
 SELECT YearsAtCompany, PercentSalaryHike
   FROM employeedata
  ORDER BY YearsAtCompany;

SELECT * from employeedata;

SELECT ed.PercentSalaryHike, ed.StandardHours, ed.TotalWorkingYears, 
       ed.YearsAtCompany, ed.YearsSinceLastPromotion, ed.YearsWithCurrManager, 
       ms.PerformanceRating
  FROM employeedata ed
 INNER JOIN manager_survey ms
    ON ed.EmployeeID = ms.EmployeeID;

-- Job satisfaction analysis

SELECT ed.PercentSalaryHike, ed.TotalWorkingYears,
       ed.YearsAtCompany, ed.YearsSinceLastPromotion, ed.YearsWithCurrManager, 
       es.WorkLifeBalance, es.JobSatisfaction
  FROM employeedata ed
 INNER JOIN employee_survey es
    ON ed.EmployeeID = es.EmployeeID;
    
-- among attritous employees
SELECT ed.PercentSalaryHike, ed.TotalWorkingYears,
       ed.YearsAtCompany, ed.YearsSinceLastPromotion, ed.YearsWithCurrManager, 
       es.WorkLifeBalance, es.JobSatisfaction
  FROM employeedata ed
 INNER JOIN employee_survey es
    ON ed.EmployeeID = es.EmployeeID
 WHERE ed.Attrition = 'Yes';

