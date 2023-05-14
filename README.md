# Hadsim-project
The system is based on the following script,
It must be run before running the program

CREATE DATABASE HealthClinicDB
USE HealthClinicDB

CREATE TABLE Employees (
  FirstName VARCHAR(50) NOT NULL,
  LastName VARCHAR(50) NOT NULL,
  IDNumber VARCHAR(9) PRIMARY KEY CHECK (IDNumber LIKE '%[0-9]%' AND LEN(IDNumber) = 9),
  CityOfResidence VARCHAR(50) NOT NULL,
  Street VARCHAR (50) NOT NULL,
  BuildingNumber INT NOT NULL CHECK(BuildingNumber>=0),
  DateOfBirth DATE CHECK (DateOfBirth >= '1900-01-01' AND DateOfBirth <= GETDATE()) NOT NULL,
  Phone VARCHAR(10) CHECK (Phone LIKE '%[0-9]%'AND LEN(Phone)=9),
  MobilePhone VARCHAR(10) CHECK (MobilePhone LIKE '%[0-9]%'AND LEN(MobilePhone)=10) NOT NULL
);
GO
CREATE TABLE CoronaDetails(
IDNumber VARCHAR(9) CHECK (IDNumber LIKE '%[0-9]%' AND LEN(IDNumber) = 9) UNIQUE NOT NULL,
DataPositiveResult DATE CHECK(DataPositiveResult<=GETDATE() AND DataPositiveResult>='2019-10-17'),
FOREIGN KEY (IDNumber) REFERENCES Employees (IDNumber),
DateOfRecovery DATE CHECK (DateOfRecovery <= GETDATE())
);
GO
ALTER TABLE CoronaDetails
ADD CONSTRAINT CheckDateOfRecovery
CHECK (DateOfRecovery>DATEADD(DD,10, DataPositiveResult));

GO
CREATE TABLE Vaccines (
    VaccineID INT PRIMARY KEY,
    VaccineManufacturer VARCHAR(50)
);
GO

CREATE TABLE People_Vaccinations (
    EmployeeID VARCHAR(9)  CHECK (EmployeeID LIKE '%[0-9]%' AND LEN(EmployeeID) = 9) NOT NULL,
    VaccinationID INT NOT NULL,
	DateOfReceivingTheVaccine DATE CHECK (DateOfReceivingTheVaccine>'2020-12-9'AND DateOfReceivingTheVaccine<GETDATE()) NOT NULL
    FOREIGN KEY (EmployeeID) REFERENCES Employees (IDNumber),
    FOREIGN KEY (VaccinationID) REFERENCES Vaccines (VaccineID)
);
GO 


INSERT INTO [dbo].[Vaccines] VALUES(111,'Pfizer');
INSERT INTO [dbo].[Vaccines] VALUES(222,'Moderna');
INSERT INTO [dbo].[Vaccines] VALUES(333,'AstraZeneca');

INSERT INTO [dbo].[Employees] VALUES ('Shimon','Levi','123456789','jerusalem','malachi',8,'2000-10-10','025797878','0502502323')

Insert into [dbo].[People_Vaccinations] VALUES(123456789,111,'2021-01-10')
Insert into [dbo].[People_Vaccinations] VALUES(123456789,111,'2021-05-10')

Insert into [dbo].[CoronaDetails](IDNumber,DataPositiveResult) VALUES('123456789','2020-10-1')



איפיון UI שהוצע
המערכת אינה מיועדת להכניס לבידוד, היא אמורה לשמור נתונים
אם דרישת המערכת השתנתה 
חסרים כמה דברים:
1.אין למשתמש פרטי אפשרות להתממשק למערכת איכון טלפוני.
2. הבדיקה תכניס סתם אנשים לבידוד, משום שהמפות מזהות כתובת ולא מזהות דירה בתוך בניין, וגם איכון טלפוני לא יוכל לבדוק האם שהו באותו חדר או שזה לדוגמא שתי דירות סמוכות.
3. האם אנשים שגרים באותו בית ייכנסו לבידוד למרות שאין להם טלפון (לדוגמא ילדים קטנים)?

במידה והדרישות יתקייימו ויפותח הפיצר,
הייתי בודקת בצד הלקוח והשרת
שולחת תאריך מהעתיד, או תאריך לפני פרוץ המגפה
מנסה לשלוח מיקומים מחו"ל, או מיקומים שאין שם אנשים כמו לב ים, מקומות שוממים או שאין אליהם כניסה(כמו שטחי מוקשים) וכד'
