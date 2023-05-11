import pyodbc as pyodbc
from flask import Flask, Response, request ,make_response, jsonify
conn_str = "DRIVER={SQL Server};SERVER=DESKTOP-HI24610\SQLEXPRESS;DATABASE=HealthClinicDB;"
app = Flask(__name__)

select_all_query="SELECT *FROM Employees JOIN CoronaDetails ON CoronaDetails.IDNumber = Employees.IDNumber JOIN People_Vaccinations ON People_Vaccinations.EmployeeID = Employees.IDNumber JOIN Vaccines ON Vaccines.VaccineID = People_Vaccinations.VaccinationID;"
select_employys_query="SELECT *FROM Employees"

def fetch_data_from_sql(query): #שליפת נתונים מSQL
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
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
        cursor.execute(query, ID)
        results = cursor.fetchall()
        aaaa=[]
        for row in results:
            ########
            print(row)
        cursor.execute(query)

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
@app.route('/Employees', methods=['POST'])
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
        conn.close()
        return response

@app.route('/Employees/123456789', methods=['GET'])
def get_employees_by_ID():
    # query=f"select * from Employees WHERE IDNumber =123456789"
    # print(f{employy_id})
    query="SELECT * FROM Employees WHERE IDNumber = ?"
    id="123456789"
    data=fetch_column_from_sql(query,id)
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

@app.route('/Employees/CoronaDetales', methods=['GET'])
def get_employees_and_corona_details():
    data=fetch_data_from_sql(select_all_query)
    rows_list = []
    for row in data:
        rows_list.append(dict(row))
    response = make_response(jsonify(rows_list))
    response.status_code = 200
    return response


def insert_data_into_database(data):
    conn = pyodbc.connect(conn_str)
    # יצירת מופע של סוגר קורא
    cursor = conn.cursor()
    try:
        with conn.cursor() as cursor:
            # הכנת השאילתה עם הנתונים המתקבלים
            sql = "INSERT INTO table_name (column1, column2) VALUES (?, ?)"
            cursor.execute(sql, (data['column1'], data['column2']))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

@app.route('/data',methods=['post'])
def insert_handler():
    data = request.get_json()
    print(data)
    success = insert_data_into_database(data)
    if success:
        return 'הנתונים הוזנו בהצלחה לבסיס הנתונים'
    else:
        return 'שגיאה בהכנסת הנתונים לבסיס הנתונים'


port_number=5000
app.run(port=port_number)