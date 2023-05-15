import requests
person=['ari','segal','987654321','jerusalem','yafo',26,'1990-1-21','025326569','0533323698']


def get_data_from_server():
    url = 'http://127.0.0.1:5000/Employees/123456789/CoronaDetales'  # ה-URL של השרת שברצונך לשלוח לו את הבקשה
    response = requests.get(url)
    if response.status_code == 200:  # בדיקת קוד המצב של התגובה - 200 משמעו שהבקשה בוצעה בהצלחה
        data = response.json()  # קריאת הנתונים מתוך התגובה
        return data
    else:
        print(f"Request failed with status code: {response.status_code}")

def put_into():
    # url = "http://127.0.0.1:5000/Employees/123456789/CoronaDetales/addVaccina?vaccina_code=222&vaccina_date='2021-12-30'"
    url = "http://127.0.0.1:5000/Employees/987654321/CoronaDetales/add_positive_result?date=2022-01-01"
    # data={'first_name': 'first_name_1', 'last_name': 'last_name_1', 'customerID': 1111, 'city': 'city_1', 'street': 'street_1', 'house_number': 1, 'phone': '11', 'mobile_phone': '1111'}
    # response = requests.post(url, json=person,headers = {'Content-Type': 'application/json'})
    response = requests.post(url)
    return response

# קריאה לפונקצית עדכון והדפסת סטטוס הצלחה/כישלון
try_put=put_into()
print(try_put)

# קריאה לפונקציה והדפסת הנתונים שהתקבלו
# data = get_data_from_server()
# print(data)