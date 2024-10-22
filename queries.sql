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
  
  SELECT ed.YearsWithCurrManager, AVG(es.JobSatisfaction) avgjobsatisfaction
    FROM employeedata ed
   INNER JOIN employee_survey es
   GROUP BY ed.YearsWithCurrManager
   ORDER BY avgjobsatisfaction;
   
-- Attrition analysis
SELECT * FROM employeedata
 WHERE Attrition = "Yes";
   