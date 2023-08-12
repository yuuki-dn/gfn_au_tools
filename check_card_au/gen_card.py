import requests
import json
def check_bin(bin):
    print("Checking bin: " + bin)
    url = "https://bin-ip-checker.p.rapidapi.com/"

    querystring = {"bin":f"{bin}"}

    payload = { "bin": f"{bin}" }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "799cbbb1cdmsha27e8fe9f88bc6ep14e5b8jsn3563e9ad0b3a",
        "X-RapidAPI-Host": "bin-ip-checker.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers, params=querystring).json()
    if response["BIN"]["valid"] == True:
        print(f"{bin} is valid")
        return True
    else:
        print(f"{bin} is invalid")
        return False

with open("bin", encoding="utf-8") as f:
    lines = f.readlines()
    list_bin = []
    for line in lines:
        if check_bin(line.strip()):
            list_bin.append(line.strip())

with open("bin2","w") as f:
    f.write("\n".join(list_bin))