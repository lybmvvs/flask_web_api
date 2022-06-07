import requests


result = requests.get("http://127.0.0.1:3000/api/vlpandipr/ipr")
result = requests.get("http://127.0.0.1:3000/api/vlpandipr/data")
#result = requests.put("http://127.0.0.1:3000/api/vlpandipr/ipr", json={"q_liq": [0,5,15], "p_wf": [90,80,70]})

print(result.json())