import requests
import time
# params
status_nr = "Job is NOT ready"
status_r = " Job is ready"
error = "No job linked to this token"

url = "https://playground.learnqa.ru/ajax/api/longtime_job"
"""
W/o token: {"token":"gM1oTOxoTMxACNx0iMw0yMyAjM","seconds":15}
"""
# 1
create_task = requests.get(url).json()
print(create_task)
# 2
task = requests.get(url, params={"token": create_task["token"]}).json()
req_status = task["status"]
print(f"Status for task is expected: {req_status == status_nr}")
# 3
time.sleep(create_task["seconds"])
# 4 делал бы один запрос c token ПОСЛЕ того, как задача готова, убеждался
# в правильности поля status и наличии поля result
task_done = requests.get(url, params={"token": create_task["token"]}).json()
print(f"Status for task is expected: "
      f"{'YES' if req_status == status_r else f'NO, Actual status: {req_status}, Expected status: {status_r}'}")
print(f"Task contains field 'result': {task_done.get('result') is not None}")
