import requests

url = "https://playground.learnqa.ru/api/long_redirect"
resp = requests.get(url)
last_resp = resp.history[-1]
print(f"Кол-во редиректов от изначальной точки назначения до итоговой: "
      f"{len(resp.history)}")
print(f"URL итоговый: {last_resp.url}")
