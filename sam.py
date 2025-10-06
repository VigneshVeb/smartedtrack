import requests
import json
data=[
    {
        "student_id": 2,
        "date": "2025-10-01",
        "status": "present"
    },
    {
        "student_id": 3,
        "date": "2025-10-01",
        "status": "present"
    }

]
url="http://127.0.0.1:8000/students/mark-attendance/"
json_data=json.dumps(data)
response=requests.post(url,data=json_data,headers={"Content-Type":"application/json"},cookies={"sessionid":"your_session_id_here","csrftoken":"your_csrf_token_here"})

print(response.status_code)