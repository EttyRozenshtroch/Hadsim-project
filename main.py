import json
import pyodbc as pyodbc
from flask import Flask, Response, request ,make_response, jsonify

print("hi");
conn_str = "DRIVER={SQL Server};SERVER=DESKTOP-HI24610\SQLEXPRESS;DATABASE=CustomersDB;"
# with pyodbc.connect(conn_str) as connection:
#     with open("customers_data.json") as file:
#         customers_data = json.load(file)
#     cursor = connection.cursor()  # הגדרת הסמן

    # for i in poke_data:
    #     query = f"insert into customers_tbl values('{i['first_name']}','{i['last_name']}',{i['customerID']},'{i['city']}','{i['street']}',{i['house_number']},'{i['phone']}','{i['mobile_phone']}')"
    #     cursor.execute(query)
    # select_query="select * from customers_tbl"
    # cursor.execute(select_query)
    # row = cursor.fetchone()
    # print(row)
    # table=cursor.fetchall();
    # print(table)




app = Flask(__name__)

#post request



@app.route('/')
def get_func():
        # data = cursor.fetchall()
        # print(table)
        # data = {'name': 'John Doe', 'age': 30, 'city': 'New York'}
        print(data)
        rows_list = []
        for row in data:
            rows_list.append(dict(row))
        response = make_response(jsonify(rows_list))
        response.status_code = 200
        return response
def fetch_data_from_sql():
    # # התחברות למסד הנתונים
    # # יצירת מופע של סוגר קורא
    # cursor = conn_str.cursor()
    # query="select * from customers_tbl"
    # # ביצוע השאילתה
    # cursor.execute(query)
    #
    # # קבלת שמות העמודות
    # columns = [column[0] for column in cursor.description]
    #
    # # יצירת רשימה לאחסון התוצאות
    # rows_list = []
    #
    # # קריאת השורות ויצירת מילון עבור כל שורה
    # for row in cursor.fetchall():
    #     row_dict = dict(zip(columns, row))
    #     rows_list.append(row_dict)
    #
    # # סגירת החיבור למסד הנתונים
    # cursor.close()
    # conn_str.close()
    #
    # # החזרת התוצאות
    # return rows_list
    conn = pyodbc.connect(conn_str)

    # יצירת מופע של סוגר קורא
    cursor = conn.cursor()

    # ביצוע השאילתה
    cursor.execute('SELECT * FROM customers_tbl')

    # קבלת שמות העמודות
    columns = [column[0] for column in cursor.description]

    # יצירת רשימה לאחסון התוצאות
    rows_list = []

    # קריאת השורות ויצירת מילון עבור כל שורה
    for row in cursor.fetchall():
        row_dict = dict(zip(columns, row))
        rows_list.append(row_dict)

    # סגירת החיבור למסד הנתונים
    cursor.close()
    conn.close()
    print(rows_list)
    # החזרת התוצאות
    return rows_list

def fetch_data():
    # קוד לשליפת הנתונים ממסד הנתונים
    with pyodbc.connect(conn_str) as connection:
        cursor = connection.cursor()  # הגדרת הסמן
        select_query = "select * from customers_tbl"
        cursor.execute(select_query)
        rows = cursor.fetchall()
        return rows

@app.route('/data', methods=['GET'])
def get_data():
    # שליפת הנתונים

    # data = fetch_data()
    data=fetch_data_from_sql()
    # המרת הנתונים לרשימת מילונים
    rows_list = []
    for row in data:
        rows_list.append(dict(row))

    # בניית התגובה
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


port_number=3000
if __name__ == "__main__":
    app.run(port=port_number)