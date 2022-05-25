import requests


result = requests.get("http://127.0.0.1:3000/api/vlpandipr/data")
result = requests.delete("http://127.0.0.1:3000/api/vlpandipr/vlp")
result = requests.post("http://127.0.0.1:3000/api/vlpandipr/vlp", json={"q_liq": [0,10,20], "p_wf": [85,95,100]})
print(result.json())