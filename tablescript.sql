-- ceate database hremployeedb
create table employee_data
(
Age int,
Attrition varchar(25),
BusinessTravel varchar(25),
Department varchar(25),
DistanceFromHome int,
Education int,
EducationField varchar(25),
EmployeeCount int,
EmployeeID int primary key not null,
Gender varchar(25),
JobLevel int,
JobRole varchar(25),
MaritalStatus varchar(25),
MonthlyIncome int,
NumCompaniesWorked decimal(2, 1),
Over18 varchar(25),
PercentSalaryHike int,
StandardHours int,
StockOptionLevel int,
TotalWorkingYears decimal(2, 1),
TrainingTimesLastYear int,
YearsAtCompany int,
YearsSinceLastPromotion int,
YearsWithCurrManager int
);



create table employee_survey_data
(
EmployeeID int not null,
EnvironmentSatisfaction decimal(2, 1),
JobSatisfaction	decimal(2, 1),
WorkLifeBalance decimal(2, 1)
);

create table manager_survey_data
(
EmployeeID int not null,
JobInvolvement int,
PerformanceRating int
);