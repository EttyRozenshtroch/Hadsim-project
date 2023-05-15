import pyodbc as pyodbc
from flask import Flask, Response, request ,make_response, jsonify
import json

conn_str = "DRIVER={SQL Server};SERVER=DESKTOP-HI24610\SQLEXPRESS;DATABASE=HealthClinicDB;"
app = Flask(__name__)

select_all_query="SELECT *FROM Employees JOIN CoronaDetails ON CoronaDetails.IDNumber = Employees.IDNumber JOIN People_Vaccinations ON People_Vaccinations.EmployeeID = Employees.IDNumber JOIN Vaccines ON Vaccines.VaccineID = People_Vaccinations.VaccinationID;"
select_employys_query="SELECT *FROM Employees"
select_employys_by_id_query="SELECT * FROM Employees WHERE IDNumber = ?"
select_corona_detals_by_id="SELECT *FROM Employees JOIN CoronaDetails ON CoronaDetails.IDNumber = Employees.IDNumber JOIN People_Vaccinations ON People_Vaccinations.EmployeeID = Employees.IDNumber JOIN Vaccines ON Vaccines.VaccineID = People_Vaccinations.VaccinationID WHERE  CoronaDetails.IDNumber=?"
def fetch_data_from_sql(query):    #שליפת נתונים מSQL
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    try:
        cursor.execute(query)   # הרצת השאילתה
        columns = [column[0] for column in cursor.description]  # הגדרת העמודות
        rows_list = []
        for row in cursor.fetchall():
            row_dict = dict(zip(columns, row))
            rows_list.append(row_dict)
    except:
        return False
    finally:
        cursor.close()
        conn.close()
    print(rows_list)
    return rows_list
#
def fetch_column_from_sql(query,ID):
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    try:
        cursor.execute(query,ID)
        row_data=cursor.fetchone()
        columns = [column[0] for column in cursor.description]
        row_dict = dict(zip(columns, row_data))
        json_data = json.dumps(row_dict)
        return json_data
    except:
        return False
    finally:
        cursor.close()
        conn.close()


@app.route('/Employees', methods=['GET']) #קבלת כל הנתונים מSQL
def get_employees():
    data=fetch_data_from_sql(select_employys_query)
    rows_list = []
    for row in data:
        rows_list.append(dict(row))
    response = make_response(jsonify(rows_list))
    response.status_code = 200
    return response
@app.route('/Employees', methods=['POST'])# הכנסת נתונים לבנ"א
def insert_employee_into_DB():
    person = request.get_json()
    query=f"INSERT INTO[dbo].[Employees] VALUES('{person[0]}', '{person[1]}', '{person[2]}', '{person[3]}', '{person[4]}', {person[5]}, '{person[6]}', '{person[7]}', '{person[8]}')"
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    response=make_response()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
        conn.commit()
        response.status_code = 200
    except:
        response.status_code=500
    finally:
        cursor.close()
        conn.close()
        return response

@app.route('/Employees/<emp_id>', methods=['GET'])# שליפת נתונים לאדם ע"פ ת"ז
def get_employees_by_ID(emp_id):
    query="SELECT * FROM Employees WHERE IDNumber = ?"
    data=fetch_column_from_sql(query,emp_id)
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

@app.route('/Employees/CoronaDetales', methods=['GET'])# שליפת טבלת האנשים עם החיסונים שלהם
def get_employees_and_corona_details():
    data=fetch_data_from_sql(select_all_query)
    rows_list = []
    for row in data:
        rows_list.append(dict(row))
    response = make_response(jsonify(rows_list))
    response.status_code = 200
    return response


@app.route('/Employees/<emp_id>/CoronaDetales', methods=['GET']) #קבלת נתוני קורונה לאדם ע"פ ת"ז
def get_corona_detales_by_id(emp_id):
    query=f"SELECT *FROM Employees JOIN CoronaDetails ON CoronaDetails.IDNumber = Employees.IDNumber JOIN People_Vaccinations ON People_Vaccinations.EmployeeID = Employees.IDNumber JOIN Vaccines ON Vaccines.VaccineID = People_Vaccinations.VaccinationID WHERE  CoronaDetails.IDNumber={emp_id}"
    conn=pyodbc.connect(conn_str)
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            columns = [column[0] for column in cursor.description]
            rows_list = []
            data=cursor.fetchall()
            print(data)
            for row in data:
                row_dict = dict(zip(columns, row))
                rows_list.append(row_dict)
                print(row_dict)
        response = make_response(jsonify(rows_list),200)
    except:
        response=make_response()
        response.status_code(500)
    finally:
        cursor.close()
        conn.close()
        return response

@app.route('/Employees/<emp_id>/CoronaDetales/addVaccina', methods=['POST'])  #הוספת חיסון לעובד
def add_vaccina_to_employee(emp_id):
    vaccina_code= request.args.get('vaccina_code')
    vaccina_date= request.args.get('vaccina_date')
    query=f"SELECT COUNT(VaccinationID) FROM dbo.People_Vaccinations WHERE EmployeeID = '{emp_id}';"
    insert_query = f"Insert into People_Vaccinations VALUES('{emp_id}',{vaccina_code},{vaccina_date})"
    conn = pyodbc.connect(conn_str)
    response = make_response()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            result=cursor.fetchone()
            number_of_rows=int(result[0])
    except:
        print('error')
        response.status_code(500)
    finally:
        cursor.close()
        conn.close()

    if number_of_rows >=4:
        response.status_code (500)
        return response
    else:
        try:
            conn = pyodbc.connect(conn_str)
            with conn.cursor() as cursor:
                cursor.execute(insert_query)
            conn.commit()
            response.status_code ( 200)
        except:
            response.status_code  (500)
        finally:
            cursor.close()
            conn.close()
            return response

@app.route('/Employees/<emp_id>/CoronaDetales/add_positive_result', methods=['POST'])  #הוספת תאריך מחלה לאדם
def add_positive_result(emp_id):
    date_positive_result = request.args.get('date')
    insert_query=f"Insert into CoronaDetails (IDNumber,DataPositiveResult) VALUES('{emp_id}','{date_positive_result}')"
    conn = pyodbc.connect(conn_str)
    response = make_response()
    try:
        conn = pyodbc.connect(conn_str)
        with conn.cursor() as cursor:
            cursor.execute(insert_query)
        conn.commit()
        response.status_code ( 200)
    except:
        response.status_code  (500)
    finally:
        cursor.close()
        conn.close()
        return response



port_number=5000
app.run(port=port_number)
