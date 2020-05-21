import requests

data = {
 "LicAge":35,
 "Gender":1,
 "MariStat":0,
 "DrivAge":25,
 "HasKmLimit":0,
 "BonusMalus":50,
 "OutUseNb":0,
 "RiskArea":0,
 "VehUsage_Private":0,
 "VehUsage_Private+trip to office":0,
 "VehUsage_Professional":0,
 "VehUsage_Professional run":0,
 "SocioCateg_CSP1":0,
 "SocioCateg_CSP2":0,
 "SocioCateg_CSP3":0,
 "SocioCateg_CSP4":2,
 "SocioCateg_CSP5":0,
 "SocioCateg_CSP6":0,
 "SocioCateg_CSP7":0,
 "DrivAgeSq":234
}


def send_json(data):
    url = 'http://127.0.0.1:5000/predict'
    headers = {'content-type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)
    return response


if __name__ == '__main__':
    response = send_json(data)
    print(response.json())
